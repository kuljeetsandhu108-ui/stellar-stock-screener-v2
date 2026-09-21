import asyncio
import json
import os
import logging
import websockets
from typing import List, Dict
from fastapi import WebSocket

from .yahoo_service import get_real_time_bulk, format_symbol_for_yahoo
from .binance_service import is_crypto_symbol, format_symbol_for_binance
from .redis_service import redis_client

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("StreamHub")

# Standard tracked symbols on the homepage banner
STATIC_INDICES = ["^NSEI", "^NSEBANK", "^BSESN", "^INDIAVIX", "GC=F", "CL=F", "^DJI", "^GSPC", "^IXIC", "^N225", "^GDAXI", "BTCUSDT", "ETHUSDT", "SOLUSDT"]

class StreamProducer:
    def __init__(self):
        self.is_running = False
        self.is_master = False
        
    async def start(self):
        if self.is_running:
            return
        self.is_running = True
        logger.info("🚀 STREAM PRODUCER STARTING (Yahoo + Binance Engine)...")

        asyncio.create_task(self._manage_master_status())
        asyncio.create_task(self._listen_binance_websocket())
        asyncio.create_task(self._poll_yahoo_active_symbols())
        asyncio.create_task(self._poll_chartink_screeners())

    async def _manage_master_status(self):
        LOCK_KEY = "stream_master_lock"
        LOCK_TTL = 15
        while self.is_running:
            try:
                is_leader = await redis_client.acquire_lock(LOCK_KEY, ttl=LOCK_TTL)
                if is_leader:
                    if not self.is_master:
                        logger.info("👑 I am now the DATA MASTER. Running Yahoo batch poller & Binance stream...")
                        self.is_master = True
                    else:
                        await redis_client.extend_lock(LOCK_KEY, ttl=LOCK_TTL)
                else:
                    if self.is_master:
                        self.is_master = False
            except Exception:
                pass
            await asyncio.sleep(5)

    # ==========================================
    # 1. BINANCE REAL-TIME WEBSOCKET (Push-based)
    # ==========================================
    async def _listen_binance_websocket(self):
        """
        Direct connection to Binance open public mini-ticker stream.
        Pushes real-time ticks with zero rate limit and zero API costs.
        """
        uri = "wss://stream.binance.com:9443/ws/!miniTicker@arr"
        while self.is_running:
            if not self.is_master:
                await asyncio.sleep(3)
                continue
            try:
                async with websockets.connect(uri, ping_interval=20, ping_timeout=10) as ws:
                    logger.info("⚡ Live connected to Binance Public WebSocket Stream.")
                    while self.is_running and self.is_master:
                        msg = await ws.recv()
                        tickers = json.loads(msg)
                        
                        for t in tickers:
                            pair = t.get("s")
                            if pair and pair.endswith("USDT"):
                                price = float(t.get("c", 0))
                                open_p = float(t.get("o", price))
                                chg = price - open_p
                                pct = ((price - open_p) / open_p) * 100 if open_p else 0.0

                                payload = {
                                    "symbol": pair,
                                    "price": price,
                                    "change": chg,
                                    "percent_change": pct,
                                    "timestamp": int(t.get("E", 0) // 1000)
                                }
                                
                                # Broadcast directly to symbol room and Market Overview
                                await redis_client.publish_update(pair, payload)
                                if pair in STATIC_INDICES:
                                    await redis_client.publish_update("MARKET_OVERVIEW", payload)

            except Exception as e:
                logger.warning(f"⚠️ Binance WS reconnecting in 3s... ({e})")
                await asyncio.sleep(3)

    # ==========================================
    # 2. YAHOO BATCHED ON-DEMAND POLLING (1-2s Interval)
    # ==========================================
    async def _poll_yahoo_active_symbols(self):
        while self.is_running:
            if not self.is_master:
                await asyncio.sleep(2)
                continue
            try:
                active_list = await redis_client.get_active_symbols()
                indian_targets = [s for s in active_list if not is_crypto_symbol(s)]
                yahoo_static = [s for s in STATIC_INDICES if not s.endswith("USDT")]
                all_targets = list(set(yahoo_static + indian_targets))
                
                if all_targets:
                    for i in range(0, len(all_targets), 50):
                        chunk = all_targets[i:i+50]
                        data = await asyncio.to_thread(get_real_time_bulk, chunk)
                        for item in data:
                            sym = item.get("symbol")
                            if sym:
                                payload = {
                                    "symbol": sym,
                                    "price": item.get("price"),
                                    "change": item.get("change"),
                                    "percent_change": item.get("percent_change"),
                                    "volume": item.get("volume"),
                                    "timestamp": item.get("timestamp")
                                }
                                await redis_client.publish_update(sym, payload)
                                if sym in STATIC_INDICES:
                                    await redis_client.publish_update("MARKET_OVERVIEW", payload)
            except Exception as e:
                logger.error(f"⚠️ Yahoo Poller error: {e}")
                
            await asyncio.sleep(1.5)

    # ==========================================
    # 3. CHARTINK AUTO-SCREENER
    # ==========================================
    async def _poll_chartink_screeners(self):
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
            except Exception:
                pass
            await asyncio.sleep(120)

# ==========================================
# 4. WEBSOCKET BROADCAST CONSUMER
# ==========================================

class StreamConsumer:
    def __init__(self):
        self.active_sockets: Dict[str, List[WebSocket]] = {}
        self.is_listening = False

    async def connect(self, websocket: WebSocket, symbol: str):
        await websocket.accept()
        clean_sym = symbol if symbol == "MARKET_OVERVIEW" else (format_symbol_for_binance(symbol) if is_crypto_symbol(symbol) else format_symbol_for_yahoo(symbol))
        
        if clean_sym not in self.active_sockets:
            self.active_sockets[clean_sym] = []
        self.active_sockets[clean_sym].append(websocket)
        
        if clean_sym != "MARKET_OVERVIEW":
            await redis_client.add_active_symbol(clean_sym)
            
        if not self.is_listening:
            asyncio.create_task(self._listen_to_bus())

    def disconnect(self, websocket: WebSocket, symbol: str):
        clean_sym = symbol if symbol == "MARKET_OVERVIEW" else (format_symbol_for_binance(symbol) if is_crypto_symbol(symbol) else format_symbol_for_yahoo(symbol))
        if clean_sym in self.active_sockets:
            if websocket in self.active_sockets[clean_sym]:
                self.active_sockets[clean_sym].remove(websocket)
            if not self.active_sockets[clean_sym]:
                del self.active_sockets[clean_sym]

    async def _listen_to_bus(self):
        self.is_listening = True
        subscriber = redis_client.get_subscriber()
        if hasattr(subscriber, "subscribe"):
            await subscriber.subscribe("market_feed")
        
        try:
            async for message in subscriber.listen():
                if message["type"] == "message":
                    try:
                        payload = json.loads(message["data"])
                        symbol = payload.get("symbol")
                        data = payload.get("data", payload)
                        
                        # Forward to symbol subscribers
                        if symbol and symbol in self.active_sockets:
                            await self._broadcast_to_list(symbol, data)
                        
                        # Forward to Market Overview banner
                        if "MARKET_OVERVIEW" in self.active_sockets:
                            await self._broadcast_to_list("MARKET_OVERVIEW", {**data, "symbol": symbol})
                    except Exception:
                        pass
        except Exception:
            self.is_listening = False
            await asyncio.sleep(3)
            asyncio.create_task(self._listen_to_bus())

    async def _broadcast_to_list(self, key: str, data: dict):
        if key not in self.active_sockets:
            return
        msg = json.dumps(data)
        dead = []
        for ws in self.active_sockets[key]:
            try:
                await ws.send_text(msg)
            except Exception:
                dead.append(ws)
        for ws in dead:
            self.disconnect(ws, key)

producer = StreamProducer()
consumer = StreamConsumer()
