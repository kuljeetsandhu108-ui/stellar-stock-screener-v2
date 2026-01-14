import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
# Import the Singleton Hub Instance
# This ensures all users connect to the SAME data stream engine
from ..services.stream_hub import hub

router = APIRouter()

# ==========================================
# 1. WEBSOCKET ENDPOINT
# ==========================================

@router.websocket("/live/{symbol}")
async def websocket_endpoint(websocket: WebSocket, symbol: str):
    """
    High-Performance WebSocket Gateway.
    
    1. Accepts connection from Frontend.
    2. Registers the user with the Stream Hub for the specific symbol.
    3. Keeps the connection open until the user leaves.
    4. Automatically cleans up on disconnect.
    """
    
    # 1. Connect
    # The Hub handles the accept() and storage logic
    await hub.connect(websocket, symbol)
    
    try:
        while True:
            # 2. Keep Alive Loop
            # We wait for messages from the client to keep the socket open.
            # If the client closes the tab, this line throws WebSocketDisconnect.
            # We don't expect data FROM the client, but we must listen to keep the pipe open.
            await websocket.receive_text()
            
    except WebSocketDisconnect:
        # 3. Graceful Disconnect
        # Remove user from the broadcast list to save memory
        hub.disconnect(websocket, symbol)
        
    except Exception as e:
        # Catch-all for network interruptions
        # print(f"Socket Error: {e}")
        hub.disconnect(websocket, symbol)

# ==========================================
# 2. LIFECYCLE EVENTS
# ==========================================

@router.on_event("startup")
async def startup_event():
    """
    SERVER BOOT TRIGGER.
    This starts the 'Stream Engine' background task as soon as the server launches.
    It runs forever in the background, fetching data and pushing it to connected users.
    """
    # Create a non-blocking background task
    asyncio.create_task(hub.start_stream_engine())