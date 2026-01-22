import asyncio
import json
import os
import threading
import logging
from typing import List, Dict
from fastapi import WebSocket
# YFINANCE IMPORT (Lane 4)
import yfinance as yf 
from ..services import eodhd_service, fmp_service
from ..services.redis_service import redis_client

# --- LOGGING SETUP ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("StreamHub")

# ==========================================
# 1. ASSET CONFIGURATION (The Speed Lanes)
# ==========================================

# LANE 1: FYERS (Tick-by-Tick) - Indices & Major India Stocks
# Internal ID -> Fyers Symbol
FYERS_MAP = {
    "NSEI.INDX": "NSE:NIFTY50-INDEX",
    "NSEBANK.INDX": "NSE:NIFTYBANK-INDEX",
    "BSESN.INDX": "BSE:SENSEX-INDEX",
    "INDIAVIX.INDX": "NSE:INDIAVIX-INDEX",
    "RELIANCE.NSE": "NSE:RELIANCE-EQ",
    "HDFCBANK.NSE": "NSE:HDFCBANK-EQ",
    "ICICIBANK.NSE": "NSE:ICICIBANK-EQ",
    "INFY.NSE": "NSE:INFY-EQ",
    "TCS.NSE": "NSE:TCS-EQ",
    "SBIN.NSE": "NSE:SBIN-EQ"
}

# LANE 2: FMP (High Frequency 1s) - Crypto
FMP_ASSETS = [
    "BTC-USD.CC", "ETH-USD.CC", "SOL-USD.CC", "XRP-USD.CC", "DOGE-USD.CC",
    "ADA-USD.CC", "MATIC-USD.CC", "DOT-USD.CC", "LTC-USD.CC", "BNB-USD.CC"
]

# LANE 4: YAHOO (Commodities - 3s Interval)
# We map Yahoo Tickers -> Internal IDs (EODHD compatible format for frontend)
YAHOO_MAP = {
    "CL=F": "USO.US",      # Crude Oil (WTI)
    "GC=F": "XAU-USD.CC",  # Gold
    "SI=F": "XAG-USD.CC",  # Silver
    "NG=F": "UNG.US",      # Natural Gas
    "HG=F": "HGUSD",       # Copper (Internal ID)
    "BZ=F": "UKOIL"        # Brent Crude
}

# ==========================================
# 2. THE PRODUCER (Data Fetcher with Leader Election)
# ==========================================
class StreamProducer:
    """
    Runs in the background. 
    Implements 'Leader Election' so only ONE worker fetches data.
    """
    def __init__(self):
        self.is_running = False
        self.is_master = False # Am I the leader?
        self.fyers_thread = None
        
    async def start(self):
        """Boot up the engines."""
        if self.is_running: return
        self.is_running = True
        logger.info("🚀 STREAM PRODUCER STARTING...")

        # 1. Start the Leader Election Loop (The Brain)
        asyncio.create_task(self._manage_master_status())

        # 2. Start Data Loops (They will only fetch if self.is_master is True)
        asyncio.create_task(self._poll_fmp_assets())   
        asyncio.create_task(self._poll_eodhd_assets()) 
        asyncio.create_task(self._poll_yahoo_assets())

    async def _manage_master_status(self):
        """
        Periodically tries to acquire the 'master_lock' in Redis.
        If successful, this worker becomes the Data Fetcher.
        """
        LOCK_KEY = "stream_master_lock"
        LOCK_TTL = 15 # Seconds
        
        while self.is_running:
            try:
                # Try to grab lock for 15 seconds
                is_leader = await redis_client.acquire_lock(LOCK_KEY, ttl=LOCK_TTL)
                
                if is_leader:
                    # I won the election, or I already own it and extended it
                    if not self.is_master:
                        logger.info("👑 I am now the DATA MASTER. Starting Fyers...")
                        self.is_master = True
                        self._start_fyers_thread()
                    else:
                        # I am already master, just extend the lock
                        await redis_client.extend_lock(LOCK_KEY, ttl=LOCK_TTL)
                else:
                    # I am not the leader
                    if self.is_master:
                        logger.warning("👑 Lost Master status. Stopping fetches.")
                        self.is_master = False
            
            except Exception as e:
                logger.error(f"Leader Election Error: {e}")
            
            # Check again in 5 seconds (well within the 15s TTL)
            await asyncio.sleep(5)

    def _start_fyers_thread(self):
        if self.fyers_thread and self.fyers_thread.is_alive():
            return
        self.fyers_thread = threading.Thread(target=self._run_fyers_engine, daemon=True)
        self.fyers_thread.start()

    def _run_fyers_engine(self):
        """LANE 1: Fyers WebSocket (Runs in Thread)"""
        
        # --- CRITICAL FIX: SANITIZE INPUTS ---
        # Strip spaces, newlines, and quotes that might be pasted in Railway variables
        token_raw = os.getenv("FYERS_ACCESS_TOKEN", "")
        client_id_raw = os.getenv("FYERS_CLIENT_ID", "")
        
        # 1. Basic Cleaning
        token = token_raw.strip().replace('"', '').replace("'", "")
        client_id = client_id_raw.strip().replace('"', '').replace("'", "")
        
        if not token or not client_id: 
            logger.warning("⚠️ Fyers Config Missing.")
            return

        # 2. Smart Fix: If user pasted "AppID:Token", strip the AppID part
        # Fyers SDK expects us to combine them manually.
        final_token = token
        if ":" in token:
            parts = token.split(":")
            # If the first part looks like the App ID, take the second part
            if len(parts) > 1 and len(parts[0]) > 5: 
                final_token = parts[1]
                logger.info("🔧 Auto-Fixed Token format (Removed duplicate AppID prefix)")

        # 3. Construct Auth String
        auth_string = f"{client_id}:{final_token}"

        # Debug Log (Masked)
        safe_id = f"{client_id[:4]}***{client_id[-3:]}" if len(client_id) > 5 else "INVALID"
        logger.info(f"🧐 Fyers Connecting -> AppID: '{safe_id}'")

        try:
            from fyers_apiv3.FyersWebsocket import data_ws
            
            def on_message(msg):
                # Critical: Stop publishing if we lost master status
                if not self.is_master: return

                if isinstance(msg, dict) and 'symbol' in msg and 'ltp' in msg:
                    fyers_sym = msg['symbol']
                    internal_sym = next((k for k, v in FYERS_MAP.items() if v == fyers_sym), None)
                    
                    if not internal_sym:
                        # Fallback for generic NSE stocks
                        if fyers_sym.startswith("NSE:") and "-EQ" in fyers_sym:
                            internal_sym = fyers_sym.replace("NSE:", "").replace("-EQ", "") + ".NSE"

                    if internal_sym:
                        payload = {
                            "price": msg.get('ltp'),
                            "change": msg.get('ch', 0),
                            "percent_change": msg.get('chp', 0),
                            "timestamp": msg.get('exch_feed_time')
                        }
                        # Push to Redis
                        asyncio.run(redis_client.publish_update(internal_sym, payload))

            def on_open():
                logger.info("✅ Fyers WebSocket Connected Successfully!")
                # Subscribe to VIP list
                symbols = list(FYERS_MAP.values())
                fyers.subscribe(symbols=symbols, data_type="SymbolUpdate")

            def on_error(err):
                logger.error(f"❌ Fyers Error: {err}")

            fyers = data_ws.FyersDataSocket(
                access_token=auth_string, 
                log_path="", 
                litemode=True, 
                write_to_file=False, 
                reconnect=True, 
                on_connect=on_open, 
                on_message=on_message,
                on_error=on_error
            )
            fyers.connect()

        except Exception as e: 
            logger.error(f"Fyers Crash: {e}")

    async def _poll_yahoo_assets(self):
        """LANE 4: Yahoo Finance (Master Only)"""
        yahoo_symbols = list(YAHOO_MAP.keys())
        
        while self.is_running:
            # Gating: Only fetch if Master
            if not self.is_master:
                await asyncio.sleep(3)
                continue

            try:
                tickers_str = " ".join(yahoo_symbols)
                # Offload blocking IO to thread
                data = await asyncio.to_thread(lambda: yf.Tickers(tickers_str))
                
                for y_sym in yahoo_symbols:
                    try:
                        info = data.tickers[y_sym].fast_info
                        price = info.last_price
                        prev = info.previous_close
                        
                        if price and prev:
                            change = price - prev
                            pct = (change / prev) * 100
                            
                            target_sym = YAHOO_MAP[y_sym]
                            
                            await redis_client.publish_update(target_sym, {
                                "price": price,
                                "change": change,
                                "percent_change": pct,
                                "timestamp": int(asyncio.get_event_loop().time())
                            })
                    except: continue

            except Exception: pass
            await asyncio.sleep(3) # 3s Interval for Commodities

    async def _poll_fmp_assets(self):
        """LANE 2: FMP Crypto (Master Only)"""
        while self.is_running:
            if not self.is_master:
                await asyncio.sleep(1)
                continue

            try:
                data = await asyncio.to_thread(fmp_service.get_crypto_real_time_bulk, FMP_ASSETS)
                if data:
                    for item in data:
                        fmp_sym = item.get('symbol')
                        internal_sym = next((s for s in FMP_ASSETS if fmp_sym in s.replace("-","").replace(".CC","").replace(".US","")), None)
                        if internal_sym:
                            await redis_client.publish_update(internal_sym, {
                                "price": item.get('price'),
                                "change": item.get('change'),
                                "percent_change": item.get('changesPercentage'),
                                "timestamp": item.get('timestamp')
                            })
            except: pass
            await asyncio.sleep(1) # 1s Interval for Crypto

    async def _poll_eodhd_assets(self):
        """LANE 3: Stocks (Master Only)"""
        while self.is_running:
            if not self.is_master:
                await asyncio.sleep(1.5)
                continue

            try:
                active_list = await redis_client.get_active_symbols()
                # Exclude VIP assets handled by other lanes
                targets = [
                    s for s in active_list 
                    if s not in FMP_ASSETS and s not in FYERS_MAP and s not in YAHOO_MAP.values()
                ]

                if targets:
                    for i in range(0, len(targets), 50):
                        chunk = targets[i:i+50]
                        data = await asyncio.to_thread(eodhd_service.get_real_time_bulk, chunk)
                        if data:
                            for item in data:
                                code = item.get('code')
                                target_sym = next((t for t in chunk if code in t), None)
                                if target_sym:
                                    await redis_client.publish_update(target_sym, {
                                        "price": item.get('close'),
                                        "change": item.get('change'),
                                        "percent_change": item.get('change_p'),
                                        "timestamp": item.get('timestamp')
                                    })
            except: pass
            await asyncio.sleep(1.5) # 1.5s Interval for Stocks

# ==========================================
# 3. THE CONSUMER (Socket Manager)
# ==========================================
class StreamConsumer:
    """
    Runs on EVERY Worker.
    Listens to Redis -> Forwards to User.
    """
    def __init__(self):
        self.active_sockets: Dict[str, List[WebSocket]] = {}
        self.is_listening = False

    async def connect(self, websocket: WebSocket, symbol: str):
        await websocket.accept()
        if symbol not in self.active_sockets: self.active_sockets[symbol] = []
        self.active_sockets[symbol].append(websocket)
        await redis_client.add_active_symbol(symbol)
        if not self.is_listening: asyncio.create_task(self._listen_to_bus())

    def disconnect(self, websocket: WebSocket, symbol: str):
        if symbol in self.active_sockets:
            if websocket in self.active_sockets[symbol]:
                self.active_sockets[symbol].remove(websocket)
            if not self.active_sockets[symbol]: del self.active_sockets[symbol]

    async def _listen_to_bus(self):
        self.is_listening = True
        subscriber = redis_client.get_subscriber()
        
        # Subscribe if real Redis
        if hasattr(subscriber, "subscribe"): 
            await subscriber.subscribe("market_feed")
        
        logger.info("🎧 Worker listening to Data Bus")
        
        try:
            async for message in subscriber.listen():
                if message["type"] == "message":
                    try:
                        payload = json.loads(message["data"])
                        symbol = payload["symbol"]
                        data = payload["data"]
                        
                        # 1. Direct Stock/Crypto Update
                        if symbol in self.active_sockets:
                            await self._broadcast_to_list(symbol, data)
                        
                        # 2. Homepage Banner Update
                        is_banner_asset = (
                            symbol in FMP_ASSETS or 
                            symbol in FYERS_MAP or 
                            symbol in YAHOO_MAP.values()
                        )
                        
                        if is_banner_asset and "MARKET_OVERVIEW" in self.active_sockets:
                            await self._broadcast_to_list("MARKET_OVERVIEW", {**data, "symbol": symbol})
                            
                    except: pass
        except Exception as e:
            logger.error(f"Bus Listener Died: {e}")
            self.is_listening = False
            await asyncio.sleep(5)
            asyncio.create_task(self._listen_to_bus())

    async def _broadcast_to_list(self, key: str, data: dict):
        if key not in self.active_sockets: return
        msg = json.dumps(data)
        dead = []
        for ws in self.active_sockets[key]:
            try: await ws.send_text(msg)
            except: dead.append(ws)
        for ws in dead: self.disconnect(ws, key)

# Create Singletons
producer = StreamProducer()
consumer = StreamConsumer()