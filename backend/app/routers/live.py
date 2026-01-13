import asyncio
import json
import logging
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from ..services import eodhd_service

router = APIRouter()

# Manager to handle active connections
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

manager = ConnectionManager()

@router.websocket("/ws/{symbol}")
async def websocket_endpoint(websocket: WebSocket, symbol: str):
    await manager.connect(websocket)
    
    # Identify Asset Class
    symbol = symbol.upper()
    is_crypto = "BTC" in symbol or "ETH" in symbol or ".CC" in symbol
    is_us = ".US" in symbol and not is_crypto
    is_nse = ".NSE" in symbol or ".BO" in symbol or "NIFTY" in symbol or "SENSEX" in symbol

    # Normalization for EODHD logic
    eod_symbol = eodhd_service.format_symbol_for_eodhd(symbol)

    try:
        while True:
            # 1. FETCH DATA (Fastest Method Available)
            data = await asyncio.to_thread(eodhd_service.get_live_price, eod_symbol)
            
            if data and data.get('price'):
                # 2. CONSTRUCT PAYLOAD
                payload = {
                    "price": data.get('price'),
                    "change": data.get('change'),
                    "percent_change": data.get('changesPercentage'),
                    "volume": data.get('volume'),
                    "timestamp": data.get('timestamp')
                }
                
                # 3. PUSH TO FRONTEND
                await manager.send_personal_message(json.dumps(payload), websocket)
            
            # 4. THROTTLE (The Heartbeat)
            # For Crypto: Ultra Fast (1s)
            # For NSE/Stocks: Standard Fast (2s) - To respect API limits while feeling "Live"
            sleep_time = 1 if is_crypto else 2
            await asyncio.sleep(sleep_time)

    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        print(f"WS Error {symbol}: {e}")
        manager.disconnect(websocket)