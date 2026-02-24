from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from ..services import gemini_service, eodhd_service, technical_service, fmp_service, quant_engine, redis_service
import asyncio
import pandas as pd

router = APIRouter()

async def resolve_symbol_smart(ai_text: str):
    symbol = ai_text.strip().upper()
    clean_sym = symbol.replace("/", "").replace("-", "").replace(" ", "").replace("USDT", "").replace("USD", "")
    
    # 1. Commodities
    commodities = {"GOLD": "XAUUSD", "CRUDE": "CLUSD", "OIL": "CLUSD", "SILVER": "XAGUSD"}
    if clean_sym in commodities: return commodities[clean_sym], "FMP"
    
    # 2. Crypto
    crypto = ["BTC", "ETH", "SOL", "XRP", "DOGE", "BNB", "MATIC"]
    if clean_sym in crypto or "BTC" in symbol: return f"{clean_sym}-USD.CC", "FMP"
    
    # 3. Indices
    if "NIFTY" in symbol or "NSEI" in symbol: return "NSEI.INDX", "EODHD"
    if "BANK" in symbol: return "NSEBANK.INDX", "EODHD"
    if "SENSEX" in symbol or "BSESN" in symbol: return "BSESN.INDX", "EODHD"
    
    # 4. Stocks
    if ".NS" not in symbol and ".BO" not in symbol and ".INDX" not in symbol and ".CC" not in symbol and len(symbol) < 6:
        # Check if it's an Indian stock implied
        return f"{symbol}.NSE", "EODHD"
        
    if ".NS" in symbol: return symbol.replace(".NS", ".NSE"), "EODHD"
    return symbol, "EODHD"

@router.post("/analyze")
async def analyze_chart_image(chart_image: UploadFile = File(...), analysis_type: str = Form("stock")):
    if not chart_image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid file.")

    image_bytes = await chart_image.read()

    # 1. VISION AI (Fast ID)
    raw_symbol = await asyncio.to_thread(gemini_service.identify_ticker_from_image, image_bytes)
    if not raw_symbol or "NOT_FOUND" in raw_symbol:
        return {"identified_symbol": "NOT_FOUND", "analysis_data": "Could not identify ticker."}

    final_symbol, data_source = await resolve_symbol_smart(raw_symbol)
    print(f"Analyzing: {final_symbol} via {data_source}")

    # 2. SMART DATA FETCH (CACHE FIRST)
    # We fetch 5M data because we can mathematically build 1H/4H/1D from it.
    cache_key = f"chart_base_v16_{final_symbol}_5M"
    
    # A. Check Redis
    chart_data = await redis_service.redis_client.get_cache(cache_key)
    
    # B. If Miss, Hit API
    if not chart_data:
        print("⚡ Cache Miss. Fetching API...")
        if data_source == "FMP":
            chart_data = await asyncio.to_thread(fmp_service.get_commodity_history, final_symbol, "5M")
            if not chart_data: chart_data = await asyncio.to_thread(fmp_service.get_crypto_history, final_symbol, "5M")
        else:
            chart_data = await asyncio.to_thread(eodhd_service.get_historical_data, final_symbol, "5M")
        
        # Save to Redis (5 Minutes TTL)
        if chart_data:
            await redis_service.redis_client.set_cache(cache_key, chart_data, 300)
    else:
        print("✅ Using Cached Data (0 API Cost)")

    if not chart_data or len(chart_data) < 20:
        return {"identified_symbol": raw_symbol, "analysis_data": "Insufficient market data for analysis."}

    # 3. LOCAL MATH ENGINE (No AI Latency)
    # We assume the user wants a Daily/Swing view for the main report
    # Resample 5M -> Daily for the report
    daily_data = technical_service.resample_chart_data(chart_data, "1D")
    df = pd.DataFrame(daily_data)
    
    technicals = technical_service.calculate_technical_indicators(df)
    pivots = technical_service.calculate_pivot_points(df)
    mas = technical_service.calculate_moving_averages(df)

    report = quant_engine.generate_algorithmic_report(raw_symbol, "Daily", technicals, pivots, mas)

    # 4. Return Data
    frontend_sym = final_symbol.replace(".NSE", ".NS").replace(".BSE", ".BO")
    
    return {
        "identified_symbol": frontend_sym,
        "analysis_data": report,
        "technical_data": {} # Frontend fetches specific timeframes via /technicals-data endpoint
    }

@router.post("/analyze-pure")
async def analyze_pure_chart(chart_image: UploadFile = File(...)):
    # Legacy endpoint for pure vision
    image_bytes = await chart_image.read()
    return {"analysis": "Please use the main upload feature for data-backed analysis."}
