import asyncio
import json
import os
import threading
import logging
from typing import List, Dict
from fastapi import WebSocket
import yfinance as yf 
from ..services import eodhd_service, fmp_service
from ..services.redis_service import redis_client

# --- LOGGING SETUP ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("StreamHub")

# ==========================================
# 1. ASSET CONFIGURATION
# ==========================================

FYERS_MAP = {
    "NSEI.INDX": "NSE:NIFTY50-INDEX", "NSEBANK.INDX": "NSE:NIFTYBANK-INDEX",
    "BSESN.INDX": "BSE:SENSEX-INDEX", "INDIAVIX.INDX": "NSE:INDIAVIX-INDEX",
    "RELIANCE.NSE": "NSE:RELIANCE-EQ", "HDFCBANK.NSE": "NSE:HDFCBANK-EQ",
    "TCS.NSE": "NSE:TCS-EQ", "INFY.NSE": "NSE:INFY-EQ",
    "SBIN.NSE": "NSE:SBIN-EQ", "ICICIBANK.NSE": "NSE:ICICIBANK-EQ"
}

FMP_ASSETS = [
    "BTC-USD.CC", "ETH-USD.CC", "SOL-USD.CC", "XRP-USD.CC", "DOGE-USD.CC",
    "ADA-USD.CC", "MATIC-USD.CC", "DOT-USD.CC", "LTC-USD.CC", "BNB-USD.CC"
]

YAHOO_MAP = {
    "CL=F": "USO.US", "GC=F": "XAU-USD.CC", "SI=F": "XAG-USD.CC",
    "NG=F": "UNG.US", "HG=F": "HGUSD", "BZ=F": "UKOIL"
}

# ==========================================
# 2. THE PRODUCER
# ==========================================
class StreamProducer:
    def __init__(self):
        self.is_running = False
        self.is_master = False
        self.fyers_thread = None
        
    async def start(self):
        if self.is_running: return
        self.is_running = True
        logger.info("🚀 STREAM PRODUCER STARTING...")

        asyncio.create_task(self._manage_master_status())
        asyncio.create_task(self._poll_fmp_assets())   
        asyncio.create_task(self._poll_eodhd_assets()) 
        asyncio.create_task(self._poll_yahoo_assets())

    async def _manage_master_status(self):
        LOCK_KEY = "stream_master_lock"
        LOCK_TTL = 15 
        
        while self.is_running:
            try:
                is_leader = await redis_client.acquire_lock(LOCK_KEY, ttl=LOCK_TTL)
                if is_leader:
                    if not self.is_master:
                        logger.info("👑 I am now the DATA MASTER. Starting Fyers...")
                        self.is_master = True
                        self._start_fyers_thread()
                    else:
                        await redis_client.extend_lock(LOCK_KEY, ttl=LOCK_TTL)
                else:
                    if self.is_master:
                        self.is_master = False
            except Exception as e:
                logger.error(f"Leader Election Error: {e}")
            
            await asyncio.sleep(5)

    def _start_fyers_thread(self):
        if self.fyers_thread and self.fyers_thread.is_alive():
            return
        self.fyers_thread = threading.Thread(target=self._run_fyers_engine, daemon=True)
        self.fyers_thread.start()

    def _run_fyers_engine(self):
        """LANE 1: Fyers WebSocket (Debug Mode)"""
        
        # 1. Clean Inputs
        raw_token = os.getenv("FYERS_ACCESS_TOKEN", "").strip().replace('"', '').replace("'", "")
        raw_client_id = os.getenv("FYERS_CLIENT_ID", "").strip().replace('"', '').replace("'", "")
        
        if not raw_token or not raw_client_id: 
            logger.warning("⚠️ Fyers Config Missing.")
            return

        # 2. Extract Token (Handle "AppID:Token" case)
        final_token = raw_token
        if ":" in raw_token:
            parts = raw_token.split(":")
            if len(parts) > 1 and len(parts[1]) > 50:
                final_token = parts[1]
                logger.info("🔧 Extracted Token from 'AppID:Token' format")

        # 3. Ensure AppID has suffix (Common Mistake Fix)
        # Most Fyers App IDs are "XV12345-100". If user put "XV12345", we fix it.
        final_client_id = raw_client_id
        if not final_client_id.endswith("-100") and len(final_client_id) < 15:
             # Heuristic: If it looks like a base ID, try appending -100
             # Only apply if it doesn't look like a different type of ID
             logger.info(f"🔧 AppID '{final_client_id}' might be missing '-100'. Attempting as-is first.")
        
        # 4. Construct Auth String
        auth_string = f"{final_client_id}:{final_token}"
        
        # --- DEBUG LOGS (COMPARE THESE WITH YOUR LOCAL ENV) ---
        logger.info(f"🔍 FYERS DEBUG INFO:")
        logger.info(f"   -> App ID (Used): {final_client_id}")
        logger.info(f"   -> Token Start:   {final_token[:6]}...")
        logger.info(f"   -> Token End:     ...{final_token[-6:]}")
        logger.info(f"   -> Token Length:  {len(final_token)}")
        # -----------------------------------------------------

        try:
            from fyers_apiv3.FyersWebsocket import data_ws
            
            def on_message(msg):
                if not self.is_master: return
                if isinstance(msg, dict) and 'symbol' in msg and 'ltp' in msg:
                    fyers_sym = msg['symbol']
                    internal_sym = next((k for k, v in FYERS_MAP.items() if v == fyers_sym), None)
                    if not internal_sym and fyers_sym.startswith("NSE:") and "-EQ" in fyers_sym:
                        internal_sym = fyers_sym.replace("NSE:", "").replace("-EQ", "") + ".NSE"
                    if internal_sym:
                        payload = {"price": msg.get('ltp'), "change": msg.get('ch', 0), "percent_change": msg.get('chp', 0), "timestamp": msg.get('exch_feed_time')}
                        asyncio.run(redis_client.publish_update(internal_sym, payload))
            
            def on_error(err):
                logger.error(f"❌ Fyers Error: {err}")
                # AUTO-HEAL: If token expired (-99), generate a new one immediately
                if isinstance(err, dict) and err.get('code') in [-99, -300]:
                    logger.info("♻️ Generating Fresh Token...")
                    from ..utils import auth_helper
                    new_token = auth_helper.get_fresh_fyers_token()
                    if new_token:
                        os.environ["FYERS_ACCESS_TOKEN"] = new_token
                        # Recursively restart with new token
                        self._run_fyers_engine()

            def on_open():
                logger.info("✅ Fyers WebSocket Connected! Subscribing...")
                fyers.subscribe(symbols=list(FYERS_MAP.values()), data_type="SymbolUpdate")

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
        yahoo_symbols = list(YAHOO_MAP.keys())
        while self.is_running:
            if not self.is_master: 
                await asyncio.sleep(3)
                continue
            try:
                tickers_str = " ".join(yahoo_symbols)
                data = await asyncio.to_thread(lambda: yf.Tickers(tickers_str))
                for y_sym in yahoo_symbols:
                    try:
                        info = data.tickers[y_sym].fast_info
                        price = info.last_price
                        prev = info.previous_close
                        if price and prev:
                            await redis_client.publish_update(YAHOO_MAP[y_sym], {
                                "price": price, "change": price - prev, "percent_change": ((price - prev) / prev) * 100, "timestamp": int(asyncio.get_event_loop().time())
                            })
                    except: continue
            except: pass
            await asyncio.sleep(3)

    async def _poll_fmp_assets(self):
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
                                "price": item.get('price'), "change": item.get('change'), "percent_change": item.get('changesPercentage'), "timestamp": item.get('timestamp')
                            })
            except: pass
            await asyncio.sleep(1) 

    async def _poll_eodhd_assets(self):
        while self.is_running:
            if not self.is_master: 
                await asyncio.sleep(1.5)
                continue
            try:
                active_list = await redis_client.get_active_symbols()
                targets = [s for s in active_list if s not in FMP_ASSETS and s not in FYERS_MAP and s not in YAHOO_MAP.values()]
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
                                        "price": item.get('close'), "change": item.get('change'), "percent_change": item.get('change_p'), "timestamp": item.get('timestamp')
                                    })
            except: pass
            await asyncio.sleep(1.5) 

# ==========================================
# 3. THE CONSUMER
# ==========================================
class StreamConsumer:
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
            if websocket in self.active_sockets[symbol]: self.active_sockets[symbol].remove(websocket)
            if not self.active_sockets[symbol]: del self.active_sockets[symbol]

    async def _listen_to_bus(self):
        self.is_listening = True
        subscriber = redis_client.get_subscriber()
        if hasattr(subscriber, "subscribe"): await subscriber.subscribe("market_feed")
        logger.info("🎧 Worker listening to Data Bus")
        
        try:
            async for message in subscriber.listen():
                if message["type"] == "message":
                    try:
                        payload = json.loads(message["data"])
                        symbol = payload["symbol"]
                        data = payload["data"]
                        if symbol in self.active_sockets: await self._broadcast_to_list(symbol, data)
                        is_banner = (symbol in FMP_ASSETS or symbol in FYERS_MAP or symbol in YAHOO_MAP.values())
                        if is_banner and "MARKET_OVERVIEW" in self.active_sockets:
                            await self._broadcast_to_list("MARKET_OVERVIEW", {**data, "symbol": symbol})
                    except: pass
        except:
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

producer = StreamProducer()
consumer = StreamConsumer()