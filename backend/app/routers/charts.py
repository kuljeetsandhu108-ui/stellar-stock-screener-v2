from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from ..services import gemini_service, yahoo_service, binance_service, technical_service, quant_engine
from ..services.system_watchdog import auto_heal
import asyncio
import pandas as pd

router = APIRouter()

ERROR_TICKET = """TREND: Data Unavailable
PATTERNS: Insufficient historical data to calculate structure.
MOMENTUM: N/A
LEVELS: Key Support at 0.00, Key Resistance at 0.00.
VOLUME: N/A
INDICATORS: RSI (50.0) indicates Neutral.
CONCLUSION: Market data temporarily unavailable for this asset.
ACTION: WAIT
ENTRY_ZONE: 0.00
STOP_LOSS: 0.00
TARGET_1: 0.00
TARGET_2: 0.00
RISK_REWARD: N/A
CONFIDENCE: Low (Missing Data)
RATIONALE: Please upload a clearer chart screenshot."""

@router.post("/analyze")
async def analyze_chart_image(chart_image: UploadFile = File(...), analysis_type: str = Form("stock")):
    if not chart_image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid file.")

    image_bytes = await chart_image.read()
    
    # 1. AI OCR: Read Ticker and Timeframe ONLY (Zero Hallucination)
    context_str = await asyncio.to_thread(gemini_service.identify_chart_context_from_image, image_bytes)
    parts = context_str.split(',')
    raw_symbol = parts[0] if len(parts) > 0 else "NOT_FOUND"
    timeframe = parts[1].strip().upper() if len(parts) > 1 else "1D"
    if timeframe in ["1M", "1MIN", "3M", "3MIN"]:
        timeframe = "5M"
    if timeframe not in ["5M", "15M", "30M", "1H", "4H", "1D", "1W", "1MO"]:
        timeframe = "1D"

    if not raw_symbol or "NOT_FOUND" in raw_symbol:
        return {"identified_symbol": "NOT_FOUND", "analysis_data": "Could not identify symbol text.", "technical_data": {}}

    is_crypto = binance_service.is_crypto_symbol(raw_symbol)
    
    if is_crypto:
        final_symbol = binance_service.format_symbol_for_binance(raw_symbol)
        chart_list = await asyncio.to_thread(binance_service.get_crypto_klines, final_symbol, timeframe)
        quote = await asyncio.to_thread(binance_service.get_crypto_price, final_symbol)
    else:
        final_symbol = yahoo_service.format_symbol_for_yahoo(raw_symbol)
        chart_list = await asyncio.to_thread(yahoo_service.get_historical_data, final_symbol, timeframe)
        quote = await asyncio.to_thread(yahoo_service.get_live_price, final_symbol)

    # 2. Stitch Live Price for 100% Accuracy
    current_price = quote.get("price") if quote else None
    if chart_list and current_price:
        chart_list[-1]["close"] = current_price
        if current_price > chart_list[-1]["high"]:
            chart_list[-1]["high"] = current_price
        if current_price < chart_list[-1]["low"]:
            chart_list[-1]["low"] = current_price

    # 3. Calculate Deterministic Mathematical Quant Report
    if not chart_list or len(chart_list) < 20:
        analysis_report = ERROR_TICKET
    else:
        df = pd.DataFrame(chart_list)
        technicals = technical_service.calculate_technical_indicators(df)
        pivots = technical_service.calculate_pivot_points(df)
        mas = technical_service.calculate_moving_averages(df)
        analysis_report = quant_engine.generate_algorithmic_report(final_symbol, timeframe, technicals, pivots, mas)

    return {
        "identified_symbol": final_symbol,
        "analysis_data": analysis_report,
        "technical_data": {}
    }

@router.post("/analyze-pure")
async def analyze_pure_chart(chart_image: UploadFile = File(...)):
    if not chart_image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid file type.")
    image_bytes = await chart_image.read()
    analysis_report = await asyncio.to_thread(gemini_service.analyze_pure_vision, image_bytes)
    return {"analysis": analysis_report}
