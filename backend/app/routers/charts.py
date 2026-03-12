from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from ..services import gemini_service, eodhd_service, technical_service, fmp_service, quant_engine, redis_service
import asyncio
import pandas as pd

router = APIRouter()

ERROR_TICKET = '''TREND: Data Unavailable
PATTERNS: Insufficient historical data to calculate structure.
MOMENTUM: N/A
LEVELS: Key Support at 0.00, Key Resistance at 0.00.
VOLUME: N/A
INDICATORS: RSI (50.0) indicates Neutral.
CONCLUSION: API Data Limit reached for this specific asset.
ACTION: WAIT
ENTRY_ZONE: 0.00
STOP_LOSS: 0.00
TARGET_1: 0.00
TARGET_2: 0.00
RISK_REWARD: N/A
CONFIDENCE: Low (Missing Data)
RATIONALE: The data provider does not supply enough candles for this asset.'''

async def resolve_symbol_smart(ai_text: str):
    s = ai_text.strip().upper()
    crypto_map = {"BITCOIN": "BTC", "ETHEREUM": "ETH", "SOLANA": "SOL", "RIPPLE": "XRP", "DOGECOIN": "DOGE"}
    for name, short in crypto_map.items():
        if name in s: s = s.replace(name, short)
    
    clean_sym = s.replace("/", "").replace("-", "").replace(" ", "").replace("USDT", "").replace("USD", "")
    
    indices = {"NIFTY": "NSEI.INDX", "BANK": "NSEBANK.INDX", "SENSEX": "BSESN.INDX", "SPX": "GSPC.INDX", "NDX": "NDX.INDX", "DOW": "DJI.INDX"}
    for k, v in indices.items():
        if k in s: return v, "EODHD"

    # 💥 STRICT GLOBAL COMMODITIES MAP (FMP)
    commodities = {
        "GOLD": "XAUUSD", "XAU": "XAUUSD", "XAUUSD": "XAUUSD", "GC=F": "XAUUSD",
        "SILVER": "XAGUSD", "XAG": "XAGUSD", "XAGUSD": "XAGUSD", "SI=F": "XAGUSD",
        "CRUDE": "CLUSD", "OIL": "CLUSD", "WTI": "CLUSD", "CLUSD": "CLUSD", "CL=F": "CLUSD",
        "BRENT": "UKOIL", "UKOIL": "UKOIL",
        "NATURALGAS": "NGUSD", "NGUSD": "NGUSD", "NG=F": "NGUSD"
    }
    if clean_sym in commodities: return commodities[clean_sym], "FMP"
    if s in commodities: return commodities[s], "FMP"
    
    # 💥 CRYPTO ROUTING (EODHD)
    crypto_list =["BTC", "ETH", "SOL", "XRP", "DOGE", "BNB", "MATIC", "ADA", "AVAX", "DOT", "LTC", "SHIB"]
    if clean_sym in crypto_list: return f"{clean_sym}-USD.CC", "EODHD"
    for c in crypto_list:
        if c in s: return f"{c}-USD.CC", "EODHD"

    # 💥 INDIAN STOCKS FALLBACK
    if "." not in s: return f"{s}.NSE", "EODHD"
    if ".NS" in s: return s.replace(".NS", ".NSE"), "EODHD"
    if ".BO" in s: return s.replace(".BO", ".BSE"), "EODHD"
    return s, "EODHD"    

@router.post("/analyze")
async def analyze_chart_image(chart_image: UploadFile = File(...), analysis_type: str = Form("stock")):
    if not chart_image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid file.")

    image_bytes = await chart_image.read()
    
    # 1. AI Tasks (Run concurrently for speed)
    ticker_task = asyncio.to_thread(gemini_service.identify_ticker_from_image, image_bytes)
    analysis_task = asyncio.to_thread(gemini_service.analyze_chart_technicals_from_image, image_bytes)
    
    raw_symbol, analysis_report = await asyncio.gather(ticker_task, analysis_task)
    
    if not raw_symbol or "NOT_FOUND" in raw_symbol:
        return {"identified_symbol": "NOT_FOUND", "analysis_data": "Could not identify symbol text.", "technical_data": {}}

    final_symbol, data_source = await resolve_symbol_smart(raw_symbol)

    # 2. Background Data Warmup (Silently fetches data for timeframe tabs so they load instantly later)
    async def warm_cache():
        try:
            cache_key_5m = f"chart_base_v16_{final_symbol}_5M"
            chart_data = await redis_service.redis_client.get_cache(cache_key_5m)
            if not chart_data:
                if data_source == "FMP":
                    chart_data = await asyncio.to_thread(fmp_service.get_commodity_history, final_symbol, "5M")
                    if not chart_data: chart_data = await asyncio.to_thread(fmp_service.get_crypto_history, final_symbol, "5M")
                else:
                    chart_data = await asyncio.to_thread(eodhd_service.get_historical_data, final_symbol, "5M")
                if chart_data: await redis_service.redis_client.set_cache(cache_key_5m, chart_data, 300)
        except: pass
        
    asyncio.create_task(warm_cache())

    # 3. Format Symbol for Frontend
    frontend_sym = final_symbol
    if frontend_sym.endswith(".NSE"): frontend_sym = frontend_sym.replace(".NSE", ".NS")
    elif frontend_sym.endswith(".BSE"): frontend_sym = frontend_sym.replace(".BSE", ".BO")
    
    # The Original Image Tab gets the Pure AI Vision Analysis!
    return {
        "identified_symbol": frontend_sym,
        "analysis_data": analysis_report,
        "technical_data": {} 
    }

@router.post("/analyze-pure")
async def analyze_pure_chart(chart_image: UploadFile = File(...)):
    return {"analysis": "Please use the main upload feature."}
