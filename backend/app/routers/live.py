import asyncio
import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from ..services.yahoo_service import get_live_price, format_symbol_for_yahoo
from ..services.binance_service import get_crypto_price, is_crypto_symbol, format_symbol_for_binance

router = APIRouter()

@router.websocket("/ws/{symbol}")
async def websocket_endpoint(websocket: WebSocket, symbol: str):
    await websocket.accept()
    is_crypto = is_crypto_symbol(symbol)
    clean_symbol = format_symbol_for_binance(symbol) if is_crypto else format_symbol_for_yahoo(symbol)

    try:
        while True:
            if is_crypto:
                data = await asyncio.to_thread(get_crypto_price, clean_symbol)
            else:
                data = await asyncio.to_thread(get_live_price, clean_symbol)

            if data and data.get("price"):
                payload = {
                    "price": data.get("price"),
                    "change": data.get("change"),
                    "percent_change": data.get("changesPercentage") or data.get("percent_change"),
                    "volume": data.get("volume"),
                    "timestamp": data.get("timestamp")
                }
                await websocket.send_text(json.dumps(payload))

            sleep_time = 1 if is_crypto else 2
            await asyncio.sleep(sleep_time)

    except WebSocketDisconnect:
        pass
    except Exception:
        pass
