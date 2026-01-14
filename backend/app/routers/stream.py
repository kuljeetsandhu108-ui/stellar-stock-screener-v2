import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
# Import the Singleton Hub Instance (The Brain)
from ..services.stream_hub import hub
# Import EODHD Service for Symbol Normalization
from ..services import eodhd_service

router = APIRouter()

# ==========================================
# 1. WEBSOCKET ENDPOINT (Gateway)
# ==========================================

@router.websocket("/live/{symbol}")
async def websocket_endpoint(websocket: WebSocket, symbol: str):
    """
    High-Performance WebSocket Gateway.
    
    1. Accepts connection from Frontend.
    2. Normalizes the Symbol (e.g. "btc-usd" -> "BTC-USD.CC").
    3. Registers the user with the Stream Hub.
    4. Keeps the pipe open for Real-Time Pushes.
    """
    
    # 1. Normalize Symbol
    # This is critical. It ensures that "RELIANCE.NS" and "reliance.ns" 
    # and "BTC-USD" map to the exact keys used by the Stream Hub.
    clean_symbol = eodhd_service.format_symbol_for_eodhd(symbol)
    
    # 2. Connect to Hub
    # The Hub handles the accept() and storage logic
    await hub.connect(websocket, clean_symbol)
    
    try:
        while True:
            # 3. Keep Alive Loop
            # We wait for messages from the client (like pings) to keep the socket open.
            # If the client closes the tab, this line throws WebSocketDisconnect.
            await websocket.receive_text()
            
    except WebSocketDisconnect:
        # 4. Graceful Disconnect
        # Remove user from the broadcast list to save memory
        hub.disconnect(websocket, clean_symbol)
        
    except Exception as e:
        # Catch-all for network interruptions or unexpected socket closures
        # print(f"Socket Error: {e}")
        hub.disconnect(websocket, clean_symbol)

# ==========================================
# 2. LIFECYCLE EVENTS (The Engine Starter)
# ==========================================

@router.on_event("startup")
async def startup_event():
    """
    SERVER BOOT TRIGGER.
    This starts the 'Stream Engine' background task as soon as the server launches.
    It runs forever in the background, fetching data from EODHD and pushing it to connected users.
    """
    # Create a non-blocking background task for the Stream Hub
    asyncio.create_task(hub.start_stream_engine())