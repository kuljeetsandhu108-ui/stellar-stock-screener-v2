import asyncio
import json
from fastapi import WebSocket
from ..services import eodhd_service

class StreamHub:
    def __init__(self):
        # Stores active connections: { "RELIANCE.NS": [socket1, socket2], "BTC-USD.CC": [socket3] }
        # The key is the symbol the FRONTEND requested.
        self.active_connections: dict[str, list[WebSocket]] = {}
        self.is_running = False

    async def connect(self, websocket: WebSocket, symbol: str):
        """
        Connects a user (Frontend Chart/Header) to a specific Symbol Channel.
        """
        await websocket.accept()
        # Normalize symbol key (Upper case)
        symbol = symbol.upper().strip()
        
        if symbol not in self.active_connections:
            self.active_connections[symbol] = []
        self.active_connections[symbol].append(websocket)
        # print(f"User connected to channel: {symbol}")

    def disconnect(self, websocket: WebSocket, symbol: str):
        """
        Removes a user when they close the tab or navigate away.
        """
        symbol = symbol.upper().strip()
        if symbol in self.active_connections:
            if websocket in self.active_connections[symbol]:
                self.active_connections[symbol].remove(websocket)
            # If channel is empty, delete it to save memory & API calls
            if not self.active_connections[symbol]:
                del self.active_connections[symbol]

    async def broadcast(self, symbol: str, data: dict):
        """
        The PUSH Mechanism. Sends data to all users on a specific channel.
        """
        if symbol in self.active_connections:
            message = json.dumps(data)
            # Send to everyone watching this symbol simultaneously
            # We iterate a copy of the list to allow safe removal during iteration if needed
            for connection in self.active_connections[symbol][:]:
                try:
                    await connection.send_text(message)
                except:
                    # If socket is dead (client closed without telling us), clean it up
                    self.disconnect(connection, symbol)

    async def start_stream_engine(self):
        """
        The High-Performance Engine. 
        Fetches data from EODHD in bulk and pumps it into the correct channels.
        Optimized for Mixed Assets (Stocks + Crypto + Indices).
        """
        self.is_running = True
        print("🚀 Stream Hub Engine Started (Ultra-Low Latency Mode)")
        
        while self.is_running:
            try:
                # 1. Get all symbols currently being watched
                active_symbols = list(self.active_connections.keys())
                
                if not active_symbols:
                    await asyncio.sleep(1) # Sleep if no one is online
                    continue

                # 2. Bulk Fetch from EODHD (1 Request for ALL users)
                # Chunking prevents URL overflow, but we keep chunks large (30) for efficiency
                chunk_size = 30 
                for i in range(0, len(active_symbols), chunk_size):
                    chunk = active_symbols[i:i + chunk_size]
                    
                    # Fetch live data using our high-speed service
                    data_list = await asyncio.to_thread(eodhd_service.get_real_time_bulk, chunk)
                    
                    if not data_list: continue

                    # 3. Distribute Data to Channels (The Router Logic)
                    for item in data_list:
                        code = item.get('code') # API returns this (e.g. "NSEI", "BTC-USD", "AAPL")
                        if not code: continue
                        
                        # --- SMART MATCHING LOGIC (CRITICAL FOR CRYPTO/INDICES) ---
                        # Problem: API returns "BTC-USD", but our key is "BTC-USD.CC"
                        # Problem: API returns "NSEI", but our key is "NSEI.INDX"
                        
                        target_symbol = None
                        
                        # A. Direct Match (Best Case)
                        if code in self.active_connections:
                            target_symbol = code
                        
                        # B. Suffix/Code Match (The Fix)
                        # We look through the chunk to find who asked for this code
                        if not target_symbol:
                            for watched in chunk:
                                # Check if the API code matches the start of the Watched Symbol
                                # e.g. "BTC-USD" matches start of "BTC-USD.CC"
                                # e.g. "NSEI" matches start of "NSEI.INDX"
                                if watched.startswith(code) or code in watched: 
                                    target_symbol = watched
                                    break
                        
                        if target_symbol:
                            payload = {
                                "price": item.get('close'),
                                "change": item.get('change'),
                                "percent_change": item.get('change_p'),
                                "timestamp": item.get('timestamp'),
                                "volume": item.get('volume')
                            }
                            # PUSH to all users watching this specific symbol
                            await self.broadcast(target_symbol, payload)
            
            except Exception as e:
                print(f"Stream Hub Error: {e}")
            
            # 4. Ultra-Fast Heartbeat (1s)
            # This makes Crypto tickers feel extremely "Live"
            await asyncio.sleep(1)

# Singleton Instance
# This object is imported by other files, ensuring only ONE engine runs.
hub = StreamHub()