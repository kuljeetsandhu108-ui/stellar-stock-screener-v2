import asyncio
import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from ..services import eodhd_service

router = APIRouter()

# --- CONNECTION MANAGER ---
# Keeps track of all 1000 connected users so we can push data to them.
class ConnectionManager:
    def __init__(self):
        # Dictionary to hold lists of connections per symbol
        # Format: { "RELIANCE.NS": [socket1, socket2], "BTC-USD.CC": [socket3] }
        self.active_connections: dict[str, list[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, symbol: str):
        await websocket.accept()
        if symbol not in self.active_connections:
            self.active_connections[symbol] = []
        self.active_connections[symbol].append(websocket)

    def disconnect(self, websocket: WebSocket, symbol: str):
        if symbol in self.active_connections:
            if websocket in self.active_connections[symbol]:
                self.active_connections[symbol].remove(websocket)
            if not self.active_connections[symbol]:
                del self.active_connections[symbol]

    async def broadcast(self, symbol: str, data: dict):
        if symbol in self.active_connections:
            # Convert to JSON string once
            message = json.dumps(data)
            # Send to all users watching this symbol
            for connection in self.active_connections[symbol]:
                try:
                    await connection.send_text(message)
                except:
                    # Clean up dead connections
                    self.disconnect(connection, symbol)

manager = ConnectionManager()

# --- THE ENGINE ---
# This background task fetches data and pushes it to the manager.
# In a true Enterprise setup, this would consume a Kafka/Redis stream.
# Here, we use high-speed asyncio fetching.
async def data_streamer():
    while True:
        try:
            # 1. Get list of all symbols currently being watched by users
            active_symbols = list(manager.active_connections.keys())
            
            if not active_symbols:
                await asyncio.sleep(1)
                continue

            # 2. Bulk Fetch from EODHD (Extremely Fast)
            # We fetch up to 50 symbols at a time to stay efficient
            chunk_size = 20
            for i in range(0, len(active_symbols), chunk_size):
                chunk = active_symbols[i:i + chunk_size]
                
                # Fetch Real Live Data
                data_list = await asyncio.to_thread(eodhd_service.get_real_time_bulk, chunk)
                
                # 3. Broadcast Updates
                if data_list:
                    # Map results to symbols
                    for item in data_list:
                        code = item.get('code')
                        # Find matching full symbol (e.g. NSEI for NSEI.INDX)
                        # We try to match the code back to the watched symbol
                        for watched_sym in chunk:
                            if code in watched_sym:
                                payload = {
                                    "price": item.get('close'),
                                    "change": item.get('change'),
                                    "percent_change": item.get('change_p'),
                                    "timestamp": item.get('timestamp')
                                }
                                await manager.broadcast(watched_sym, payload)
            
            # 4. Frequency (1 second for Crypto feel, 2 seconds for Stocks)
            await asyncio.sleep(2) 
            
        except Exception as e:
            print(f"Stream Error: {e}")
            await asyncio.sleep(2)

# --- WEBSOCKET ENDPOINT ---
@router.websocket("/live/{symbol}")
async def websocket_endpoint(websocket: WebSocket, symbol: str):
    await manager.connect(websocket, symbol)
    try:
        while True:
            # Keep connection alive, wait for client messages (ping/pong)
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket, symbol)

# --- STARTUP HOOK ---
# We need to start the background streamer when the app starts
import asyncio
@router.on_event("startup")
async def startup_event():
    asyncio.create_task(data_streamer())