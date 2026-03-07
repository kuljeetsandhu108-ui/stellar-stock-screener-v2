from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from ..services import gemini_service, eodhd_service, technical_service, fmp_service, quant_engine, redis_service
import asyncio
import pandas as pd

router = APIRouter()

async def resolve_symbol_smart(raw_text: str):
    """
    Takes raw text from AI (e.g. 'RELIANCE') and maps it to the correct API symbol.
    """
    s = raw_text.strip().upper()
    
    # 1. Clean up
    s = s.replace("USDT", "").replace("USD", "").replace("/", "").replace("-", "")
    
    # 2. Known Indices (Hardcoded for stability)
    indices = {
        "NIFTY": "NSEI.INDX", "NIFTY50": "NSEI.INDX", "BANKNIFTY": "NSEBANK.INDX", 
        "SENSEX": "BSESN.INDX", "SPX": "GSPC.INDX", "NDX": "NDX.INDX", 
        "DOW": "DJI.INDX", "VIX": "INDIAVIX.INDX"
    }
    for k, v in indices.items():
        if k in s: return v, "EODHD"

    # 3. Crypto & Commodities (FMP)
    commodities = {"GOLD": "XAUUSD", "SILVER": "XAGUSD", "CRUDE": "CLUSD", "OIL": "CLUSD"}
    if s in commodities: return commodities[s], "FMP"
    
    crypto = ["BTC", "ETH", "SOL", "XRP", "DOGE", "BNB"]
    if s in crypto: return f"{s}-USD.CC", "FMP"

    # 4. Stocks (Default to Indian NSE if no suffix found)
    # This fixes the "Stocks not working" issue.
    if "." not in s:
        return f"{s}.NSE", "EODHD"
        
    # Handle existing suffixes
    if ".NS" in s: return s.replace(".NS", ".NSE"), "EODHD"
    if ".BO" in s: return s.replace(".BO", ".BSE"), "EODHD"
    
    return s, "EODHD"

@router.post("/analyze")
async def analyze_chart_image(chart_image: UploadFile = File(...), analysis_type: str = Form("stock")):
    if not chart_image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid file.")

    image_bytes = await chart_image.read()

    # STEP 1: AI READS THE NAME (Fast)
    raw_symbol = await asyncio.to_thread(gemini_service.identify_ticker_from_image, image_bytes)
    
    if not raw_symbol or "NOT_FOUND" in raw_symbol:
        return {"identified_symbol": "NOT_FOUND", "analysis_data": "Could not identify symbol text."}

    # STEP 2: PYTHON MAPS THE NAME
    final_symbol, data_source = await resolve_symbol_smart(raw_symbol)
    print(f"🔍 AI saw '{raw_symbol}' -> Mapped to '{final_symbol}'")

    # STEP 3: FETCH MASTER DATA (5-Min Candles)
    # We grab 5-min data because we can mathematically build ALL other timeframes from it.
    cache_key = f"chart_base_v16_{final_symbol}_5M"
    chart_data = await redis_service.redis_client.get_cache(cache_key)
    
    if not chart_data:
        if data_source == "FMP":
            chart_data = await asyncio.to_thread(fmp_service.get_commodity_history, final_symbol, "5M")
            if not chart_data: chart_data = await asyncio.to_thread(fmp_service.get_crypto_history, final_symbol, "5M")
        else:
            chart_data = await asyncio.to_thread(eodhd_service.get_historical_data, final_symbol, "5M")
        
        if chart_data: await redis_service.redis_client.set_cache(cache_key, chart_data, 300)

    if not chart_data or len(chart_data) < 50:
        return {"identified_symbol": raw_symbol, "analysis_data": "Insufficient market data."}

    # STEP 4: MATHEMATICAL RESAMPLING & ANALYSIS
    # We convert the 5m data into Daily data instantly for the report
    daily_data = technical_service.resample_chart_data(chart_data, "1D")
    df = pd.DataFrame(daily_data)
    
    technicals = technical_service.calculate_technical_indicators(df)
    pivots = technical_service.calculate_pivot_points(df)
    mas = technical_service.calculate_moving_averages(df)

    # STEP 5: GENERATE QUANT REPORT
    report = quant_engine.generate_algorithmic_report(raw_symbol, "Daily", technicals, pivots, mas)

    frontend_sym = final_symbol.replace(".NSE", ".NS").replace(".BSE", ".BO")
    
    return {
        "identified_symbol": frontend_sym,
        "analysis_data": report,
        "technical_data": {} 
    }

@router.post("/analyze-pure")
async def analyze_pure_chart(chart_image: UploadFile = File(...)):
    # Legacy endpoint
    return {"analysis": "Please use the main upload feature."}
