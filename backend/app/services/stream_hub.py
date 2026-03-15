import asyncio
import json
import os
import logging
from typing import List, Dict
from fastapi import WebSocket
import yfinance as yf 
from ..services import eodhd_service, fmp_service
from ..services.redis_service import redis_client

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("StreamHub")

# Fyers completely removed for stability
FYERS_MAP = {}
FMP_ASSETS =["BTC-USD.CC", "ETH-USD.CC", "SOL-USD.CC", "XRP-USD.CC", "DOGE-USD.CC", "ADA-USD.CC", "MATIC-USD.CC", "DOT-USD.CC", "LTC-USD.CC", "BNB-USD.CC"]
YAHOO_MAP = {"CL=F": "USO.US", "GC=F": "XAU-USD.CC", "SI=F": "XAG-USD.CC", "NG=F": "UNG.US", "HG=F": "HGUSD", "BZ=F": "UKOIL"}

class StreamProducer:
    def __init__(self):
        self.is_running = False
        self.is_master = False
        
    async def start(self):
        if self.is_running: return
        self.is_running = True
        logger.info("ðŸš€ STREAM PRODUCER STARTING...")

        asyncio.create_task(self._manage_master_status())
        asyncio.create_task(self._poll_bullish_screener())
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
                        logger.info("ðŸ‘‘ I am now the DATA MASTER. Running pure API feeds...")
                        self.is_master = True
                    else:
                        await redis_client.extend_lock(LOCK_KEY, ttl=LOCK_TTL)
                else:
                    if self.is_master:
                        self.is_master = False
            except Exception as e:
                pass
            await asyncio.sleep(5)

    async def _poll_bullish_screener(self):
        from .chartink_engine import SCREENERS, fetch_screener
        while self.is_running:
            if not self.is_master:
                await asyncio.sleep(10)
                continue
            try:
                for key in SCREENERS.keys():
                    data = await asyncio.to_thread(fetch_screener, key)
                    if data and len(data) > 0:
                        await redis_client.set_cache(f"live_screener_{key}", data, 86400)
                        logger.info(f"✅ Auto-Scraped {len(data)} stocks for {key}")
            except Exception as e:
                pass
            await asyncio.sleep(120)

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
                targets =[s for s in active_list if s not in FMP_ASSETS and s not in YAHOO_MAP.values()]
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
        
        try:
            async for message in subscriber.listen():
                if message["type"] == "message":
                    try:
                        payload = json.loads(message["data"])
                        symbol = payload["symbol"]
                        data = payload["data"]
                        if symbol in self.active_sockets: await self._broadcast_to_list(symbol, data)
                        is_banner = (symbol in FMP_ASSETS or symbol in YAHOO_MAP.values())
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
        dead =[]
        for ws in self.active_sockets[key]:
            try: await ws.send_text(msg)
            except: dead.append(ws)
        for ws in dead: self.disconnect(ws, key)

producer = StreamProducer()
consumer = StreamConsumer()

