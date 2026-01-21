import asyncio
import json
import os
import threading
import logging
from typing import List, Dict
from fastapi import WebSocket
# NEW IMPORT: Yahoo Finance for Commodities
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
FYERS_MAP = {
    "NSEI.INDX": "NSE:NIFTY50-INDEX",
    "NSEBANK.INDX": "NSE:NIFTYBANK-INDEX",
    "BSESN.INDX": "BSE:SENSEX-INDEX",
    "INDIAVIX.INDX": "NSE:INDIAVIX-INDEX",
    "RELIANCE.NSE": "NSE:RELIANCE-EQ",
    "HDFCBANK.NSE": "NSE:HDFCBANK-EQ",
    "TCS.NSE": "NSE:TCS-EQ",
    "INFY.NSE": "NSE:INFY-EQ",
    "SBIN.NSE": "NSE:SBIN-EQ",
    "ICICIBANK.NSE": "NSE:ICICIBANK-EQ"
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
# 2. THE PRODUCER (Data Fetcher)
# ==========================================
class StreamProducer:
    """
    Runs in the background. 
    Fetches data from APIs (Fyers/FMP/EODHD/Yahoo) and Pushes to Redis/Memory.
    It DOES NOT handle user connections directly.
    """
    def __init__(self):
        self.is_running = False
        
    async def start(self):
        """Boot up the engines."""
        if self.is_running: return
        self.is_running = True
        logger.info("🚀 STREAM PRODUCER STARTING...")

        # 1. Fyers (Threaded because SDK is blocking)
        threading.Thread(target=self._run_fyers_engine, daemon=True).start()

        # 2. Polling Engines (Async with thread offloading)
        asyncio.create_task(self._poll_fmp_assets())   
        asyncio.create_task(self._poll_eodhd_assets()) 
        asyncio.create_task(self._poll_yahoo_assets())

    def _run_fyers_engine(self):
        """LANE 1: Fyers WebSocket"""
        token = os.getenv("FYERS_ACCESS_TOKEN")
        client_id = os.getenv("FYERS_CLIENT_ID")
        
        if not token or not client_id: 
            return # Silent fail if not configured

        try:
            from fyers_apiv3.FyersWebsocket import data_ws
            def on_message(msg):
                if isinstance(msg, dict) and 'symbol' in msg and 'ltp' in msg:
                    fyers_sym = msg['symbol']
                    internal_sym = next((k for k, v in FYERS_MAP.items() if v == fyers_sym), None)
                    
                    if not internal_sym:
                        if fyers_sym.startswith("NSE:") and "-EQ" in fyers_sym:
                            internal_sym = fyers_sym.replace("NSE:", "").replace("-EQ", "") + ".NSE"

                    if internal_sym:
                        payload = {
                            "price": msg.get('ltp'),
                            "change": msg.get('ch', 0),
                            "percent_change": msg.get('chp', 0),
                            "timestamp": msg.get('exch_feed_time')
                        }
                        # Fire & Forget
                        asyncio.run(redis_client.publish_update(internal_sym, payload))

            def on_open():
                # Subscribe
                symbols = list(FYERS_MAP.values())
                fyers.subscribe(symbols=symbols, data_type="SymbolUpdate")

            fyers = data_ws.FyersDataSocket(
                access_token=f"{client_id}:{token}", log_path="", litemode=True, 
                write_to_file=False, reconnect=True, on_connect=on_open, on_message=on_message
            )
            fyers.connect()
        except Exception: 
            pass # Keep main thread alive

    async def _poll_yahoo_assets(self):
        """
        LANE 4: Fetches Commodities from Yahoo Finance.
        Uses asyncio.to_thread to prevent blocking the main loop.
        """
        yahoo_symbols = list(YAHOO_MAP.keys()) # ['CL=F', 'GC=F', ...]
        
        while self.is_running:
            try:
                # 1. Bulk Fetch (Efficient) in a separate thread
                tickers_str = " ".join(yahoo_symbols)
                
                # Fetching...
                data = await asyncio.to_thread(lambda: yf.Tickers(tickers_str))
                
                # 2. Parse and Push
                for y_sym in yahoo_symbols:
                    try:
                        ticker_obj = data.tickers[y_sym]
                        # fast_info is instantaneous
                        info = ticker_obj.fast_info
                        
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

            except Exception as e:
                # logger.error(f"Yahoo Poll Error: {e}")
                pass
            
            # Sleep 3 seconds (Safe zone)
            await asyncio.sleep(3)

    async def _poll_fmp_assets(self):
        """LANE 2: FMP Crypto (1s)"""
        while self.is_running:
            try:
                # Offload network request to thread
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
            
            await asyncio.sleep(1) 

    async def _poll_eodhd_assets(self):
        """LANE 3: Stocks (1.5s) - On Demand Only"""
        while self.is_running:
            try:
                active_list = await redis_client.get_active_symbols()
                # Exclude things handled by Yahoo, Fyers, or FMP
                targets = [
                    s for s in active_list 
                    if s not in FMP_ASSETS and s not in FYERS_MAP and s not in YAHOO_MAP.values()
                ]

                if targets:
                    # Chunking
                    for i in range(0, len(targets), 50):
                        chunk = targets[i:i+50]
                        # Offload network request
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
            
            await asyncio.sleep(1.5) 

# ==========================================
# 3. THE CONSUMER (Socket Manager)
# ==========================================
class StreamConsumer:
    """
    Runs on EVERY Worker.
    Listens to Redis/Memory -> Forwards to User.
    """
    def __init__(self):
        self.active_sockets: Dict[str, List[WebSocket]] = {}
        self.is_listening = False

    async def connect(self, websocket: WebSocket, symbol: str):
        await websocket.accept()
        if symbol not in self.active_sockets: self.active_sockets[symbol] = []
        self.active_sockets[symbol].append(websocket)
        await redis_client.add_active_symbol(symbol)
        
        if not self.is_listening:
            asyncio.create_task(self._listen_to_bus())

    def disconnect(self, websocket: WebSocket, symbol: str):
        if symbol in self.active_sockets:
            if websocket in self.active_sockets[symbol]:
                self.active_sockets[symbol].remove(websocket)
            if not self.active_sockets[symbol]: del self.active_sockets[symbol]

    async def _listen_to_bus(self):
        """
        The Infinite Loop: Data Bus -> WebSocket
        """
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
                        
                        # 1. Direct Delivery
                        if symbol in self.active_sockets:
                            await self._broadcast_to_list(symbol, data)
                        
                        # 2. Banner Delivery (Indices/Crypto/Commodities)
                        is_banner_asset = (
                            symbol in FMP_ASSETS or 
                            symbol in FYERS_MAP or 
                            symbol in YAHOO_MAP.values()
                        )
                        
                        if is_banner_asset and "MARKET_OVERVIEW" in self.active_sockets:
                            banner_data = {**data, "symbol": symbol}
                            await self._broadcast_to_list("MARKET_OVERVIEW", banner_data)
                            
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