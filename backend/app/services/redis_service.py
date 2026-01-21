import os
import json
import asyncio
import time
import redis.asyncio as redis
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

REDIS_URL = os.getenv("REDIS_URL")

# ==========================================
# 1. IN-MEMORY ENGINE (Zero-Latency Localhost)
# ==========================================
class MemoryPubSub:
    """
    Simulates Redis Pub/Sub using Python Asyncio.
    Used when Redis is unavailable or for local testing.
    """
    def __init__(self):
        # A set of queues, one for each connected user
        self.queues = set()

    async def subscribe(self, channel):
        # In local mode, we listen to everything implicitly
        pass

    async def listen(self):
        """Yields messages to the WebSocket consumer."""
        q = asyncio.Queue()
        self.queues.add(q)
        try:
            while True:
                msg = await q.get()
                yield {"type": "message", "data": msg}
        except asyncio.CancelledError:
            self.queues.discard(q)

    async def publish(self, message):
        """Push data to all active local listeners."""
        # Loop over a copy to avoid modification errors during iteration
        for q in list(self.queues):
            try: 
                q.put_nowait(message)
            except: 
                pass

# Global Memory State
memory_bus = MemoryPubSub()
local_storage = {
    "cache": {},
    "active": set(),
    "heartbeats": {}
}

# ==========================================
# 2. ROBUST REDIS MANAGER
# ==========================================
class RedisManager:
    def __init__(self):
        self.redis = None
        self.use_redis = False
        self._checked = False

    async def _get_connection(self):
        """
        Determines whether to use Real Redis or Local Memory.
        Checks only ONCE to prevent repeated timeouts/lag.
        """
        if self._checked:
            return self.redis if self.use_redis else None

        # Logic: If no URL or it's the internal Railway URL (unreachable locally)
        if not REDIS_URL or "railway.internal" in REDIS_URL:
            print("⚡ Redis: Using Local Memory Mode (Fast)")
            self.use_redis = False
            self._checked = True
            return None

        try:
            # Strict 1-second timeout test to Fail Fast
            client = redis.from_url(REDIS_URL, decode_responses=True, socket_connect_timeout=1)
            await client.ping()
            await client.close()
            
            # If successful, establish pool
            pool = redis.ConnectionPool.from_url(REDIS_URL, decode_responses=True)
            self.redis = redis.Redis(connection_pool=pool)
            self.use_redis = True
            print("✅ Redis: Connected Successfully")
        except Exception:
            print("⚡ Redis: Unreachable. Switching to Local Memory Mode.")
            self.use_redis = False
        
        self._checked = True
        return self.redis if self.use_redis else None

    # --- WATCHLIST LOGIC ---
    async def add_active_symbol(self, symbol: str):
        r = await self._get_connection()
        if r:
            try:
                await r.sadd("active_symbols_v2", symbol)
                await r.setex(f"heartbeat:{symbol}", 15, "alive")
            except: pass
        else:
            # Local Mode
            local_storage["active"].add(symbol)
            local_storage["heartbeats"][symbol] = time.time() + 15

    async def get_active_symbols(self):
        r = await self._get_connection()
        if r:
            try:
                candidates = await r.smembers("active_symbols_v2")
                active = []
                for sym in candidates:
                    if await r.exists(f"heartbeat:{sym}"): active.append(sym)
                    else: await r.srem("active_symbols_v2", sym)
                return active
            except: return []
        else:
            # Local Mode: Check heartbeats
            now = time.time()
            alive = []
            for sym in list(local_storage["active"]):
                if sym in local_storage["heartbeats"] and now < local_storage["heartbeats"][sym]:
                    alive.append(sym)
                else:
                    local_storage["active"].discard(sym)
            return alive

    # --- PUB/SUB LOGIC ---
    async def publish_update(self, symbol: str, data: dict):
        try:
            msg = json.dumps({"symbol": symbol, "data": data}, default=str)
            r = await self._get_connection()
            if r:
                await r.publish("market_feed", msg)
            else:
                await memory_bus.publish(msg)
        except: pass

    def get_subscriber(self):
        # Note: This is synchronous, so we check the flag directly
        if self.use_redis and self.redis:
            return self.redis.pubsub()
        return memory_bus

    # --- CACHE LOGIC ---
    async def get_cache(self, key: str):
        r = await self._get_connection()
        if r:
            try:
                data = await r.get(key)
                return json.loads(data) if data else None
            except: return None
        # Local Mode: Simple Dict Get
        return local_storage["cache"].get(key)

    async def set_cache(self, key: str, data: any, ttl: int = 60):
        r = await self._get_connection()
        if r:
            try: await r.set(key, json.dumps(data, default=str), ex=ttl)
            except: pass
        else:
            # Local Mode: Simple Dict Set (No TTL for simplicity in dev)
            local_storage["cache"][key] = data

# Singleton Export
redis_client = RedisManager()