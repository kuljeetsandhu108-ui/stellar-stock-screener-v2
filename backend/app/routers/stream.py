import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
# Import the robust Stream Architecture
from ..services.stream_hub import consumer, producer
from ..services import eodhd_service, redis_service

router = APIRouter()

# ==========================================
# 1. WEBSOCKET ENDPOINT (The Gateway)
# ==========================================

@router.websocket("/live/{symbol}")
async def websocket_endpoint(websocket: WebSocket, symbol: str):
    """
    High-Performance WebSocket Gateway.
    Handles User Connections, Heartbeats, and Disconnects.
    """
    
    # 1. Normalize Symbol
    # Ensures frontend tickers map to backend data keys correctly
    # e.g. "RELIANCE.NS" -> "RELIANCE.NSE"
    # e.g. "BTC-USD" -> "BTC-USD.CC"
    clean_symbol = eodhd_service.format_symbol_for_eodhd(symbol)
    
    # 2. Connect to the Consumer (The Socket Manager)
    # This registers the user to receive updates from Redis
    await consumer.connect(websocket, clean_symbol)
    
    try:
        while True:
            # 3. Heartbeat & Keep-Alive Loop
            # We wait for messages from the client.
            # The frontend sends "ping" every 10s to keep the connection alive.
            data = await websocket.receive_text()
            
            # 4. Refresh Interest (The Credit Saver)
            # If we hear a "ping", we tell Redis to keep fetching this symbol.
            # If the user closes the tab, pings stop, and we stop fetching after 15s.
            if data == "ping" and clean_symbol:
                await redis_service.redis_client.add_active_symbol(clean_symbol)
            
    except WebSocketDisconnect:
        # Graceful Disconnect
        consumer.disconnect(websocket, clean_symbol)
        
    except Exception as e:
        # Unexpected network error (e.g., wifi drop)
        # print(f"Socket Error: {e}")
        consumer.disconnect(websocket, clean_symbol)

# ==========================================
# 2. LIFECYCLE (THE ENGINE STARTER)
# ==========================================

@router.on_event("startup")
async def startup_event():
    """
    SERVER BOOT.
    
    We start the Producer here using asyncio.
    
    CRITICAL: 
    The Producer inside 'stream_hub.py' uses REDIS LOCKS (Leader Election).
    Even if Railway starts 4 Workers, they will race to grab the lock.
    Only ONE worker will become the 'Data Master' and connect to Fyers/Yahoo.
    The other 3 will sit idle and just serve users.
    
    This prevents API Bans and ensures stability.
    """
    print("✅ API Server Starting...")
    print("🚀 Initializing Stream Producer (Leader Election Mode)...")
    
    # Run the Producer in the background without blocking the API
    asyncio.create_task(producer.start())