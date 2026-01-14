import asyncio
import json
from fastapi import WebSocket
from ..services import eodhd_service

class StreamHub:
    def __init__(self):
        # Stores active connections: { "RELIANCE.NS": [socket1, socket2, socket3] }
        self.active_connections: dict[str, list[WebSocket]] = {}
        self.is_running = False

    async def connect(self, websocket: WebSocket, symbol: str):
        """
        Connects a user (Frontend Chart/Header) to a specific Symbol Channel.
        """
        await websocket.accept()
        if symbol not in self.active_connections:
            self.active_connections[symbol] = []
        self.active_connections[symbol].append(websocket)
        print(f"User connected to channel: {symbol}")

    def disconnect(self, websocket: WebSocket, symbol: str):
        """
        Removes a user when they close the tab.
        """
        if symbol in self.active_connections:
            if websocket in self.active_connections[symbol]:
                self.active_connections[symbol].remove(websocket)
            # If channel is empty, delete it to save memory
            if not self.active_connections[symbol]:
                del self.active_connections[symbol]

    async def broadcast(self, symbol: str, data: dict):
        """
        The PUSH Mechanism. Sends data to all users on a channel.
        """
        if symbol in self.active_connections:
            message = json.dumps(data)
            # Send to everyone watching this symbol simultaneously
            for connection in self.active_connections[symbol]:
                try:
                    await connection.send_text(message)
                except:
                    # If socket is dead, clean it up
                    self.disconnect(connection, symbol)

    async def start_stream_engine(self):
        """
        The Engine. Fetches data from EODHD and pumps it into the Hub.
        """
        self.is_running = True
        print("🚀 Stream Hub Engine Started")
        
        while self.is_running:
            try:
                # 1. Get all symbols currently being watched
                # keys() gives us ["RELIANCE.NS", "BTC-USD.CC", etc.]
                active_symbols = list(self.active_connections.keys())
                
                if not active_symbols:
                    await asyncio.sleep(1) # Sleep if no one is online
                    continue

                # 2. Bulk Fetch from EODHD (1 Request for ALL users)
                # We split into chunks of 20 to be safe with URL lengths
                chunk_size = 20
                for i in range(0, len(active_symbols), chunk_size):
                    chunk = active_symbols[i:i + chunk_size]
                    
                    # Fetch live data
                    # This uses our existing high-speed service
                    data_list = await asyncio.to_thread(eodhd_service.get_real_time_bulk, chunk)
                    
                    if not data_list: continue

                    # 3. Distribute Data to Channels
                    for item in data_list:
                        code = item.get('code')
                        if not code: continue
                        
                        # Find the full symbol matching the code (e.g. NSEI match NSEI.INDX)
                        # This logic ensures we push to the correct channel
                        target_symbol = next((s for s in chunk if code in s), None)
                        
                        if target_symbol:
                            payload = {
                                "price": item.get('close'),
                                "change": item.get('change'),
                                "percent_change": item.get('change_p'),
                                "timestamp": item.get('timestamp'),
                                "volume": item.get('volume')
                            }
                            # PUSH!
                            await self.broadcast(target_symbol, payload)
            
            except Exception as e:
                print(f"Stream Hub Error: {e}")
            
            # 4. Heartbeat Speed (1s = Realtime feel)
            await asyncio.sleep(1)

# Singleton Instance
hub = StreamHub()