import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from ..services.stream_hub import consumer, producer
from ..services.yahoo_service import format_symbol_for_yahoo
from ..services.binance_service import is_crypto_symbol, format_symbol_for_binance
from ..services import redis_service

router = APIRouter()

@router.websocket("/live/{symbol}")
async def websocket_endpoint(websocket: WebSocket, symbol: str):
    """
    High-Performance Redis Pub/Sub WebSocket Gateway.
    """
    is_crypto = is_crypto_symbol(symbol)
    clean_symbol = format_symbol_for_binance(symbol) if is_crypto else format_symbol_for_yahoo(symbol)
    
    await consumer.connect(websocket, clean_symbol)
    
    try:
        while True:
            data = await websocket.receive_text()
            # Refresh Heartbeat so Redis keeps fetching this symbol
            if data == "ping" and clean_symbol:
                await redis_service.redis_client.add_active_symbol(clean_symbol)
    except WebSocketDisconnect:
        consumer.disconnect(websocket, clean_symbol)
    except Exception:
        consumer.disconnect(websocket, clean_symbol)

@router.on_event("startup")
async def startup_event():
    print("✅ API Server Starting...")
    print("🚀 Initializing Stream Producer (Yahoo Batch + Binance WS)...")
    asyncio.create_task(producer.start())
