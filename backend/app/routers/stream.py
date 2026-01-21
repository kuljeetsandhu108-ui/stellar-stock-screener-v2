import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
# Import the new architecture
from ..services.stream_hub import consumer, producer
from ..services import eodhd_service, redis_service

router = APIRouter()

# ==========================================
# 1. WEBSOCKET ENDPOINT (The Gateway)
# ==========================================

@router.websocket("/live/{symbol}")
async def websocket_endpoint(websocket: WebSocket, symbol: str):
    """
    Handles the connection between User and Server.
    """
    
    # 1. Normalize Symbol
    # Frontend sends "RELIANCE.NS", EODHD wants "RELIANCE.NSE"
    # Frontend sends "BTC-USD", FMP wants "BTCUSD" (handled internally), EODHD wants "BTC-USD.CC"
    clean_symbol = eodhd_service.format_symbol_for_eodhd(symbol)
    
    # 2. Connect to the Consumer (The Socket Manager)
    await consumer.connect(websocket, clean_symbol)
    
    try:
        while True:
            # 3. Heartbeat & Keep-Alive
            # We wait for messages from the client.
            # Ideally, the frontend should send a "ping" every few seconds.
            # Even if it doesn't, this await keeps the connection open.
            data = await websocket.receive_text()
            
            # 4. Refresh Interest
            # Every time we hear from the user, we tell Redis:
            # "User is still watching this symbol. Reset the 10-second expiry timer."
            if clean_symbol:
                await redis_service.redis_client.add_active_symbol(clean_symbol)
            
    except WebSocketDisconnect:
        # User closed the tab
        consumer.disconnect(websocket, clean_symbol)
        
    except Exception as e:
        # Unexpected network error
        # print(f"WS Error: {e}")
        consumer.disconnect(websocket, clean_symbol)

# ==========================================
# 2. LIFECYCLE (Engine Starter)
# ==========================================

@router.on_event("startup")
async def startup_event():
    """
    When the server boots up, start the Data Fetching Engine (Producer).
    This runs in the background forever.
    """
    asyncio.create_task(producer.start())