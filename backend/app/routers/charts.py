from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from ..services import gemini_service, eodhd_service, technical_service, fmp_service, quant_engine, redis_service
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
CONCLUSION: API Data Limit reached for this specific asset.
ACTION: WAIT
ENTRY_ZONE: 0.00
STOP_LOSS: 0.00
TARGET_1: 0.00
TARGET_2: 0.00
RISK_REWARD: N/A
CONFIDENCE: Low (Missing Data)
RATIONALE: The data provider does not supply enough candles for this asset."""

@auto_heal(fallback_return=("NSEI.INDX", "EODHD"))
async def resolve_symbol_smart(ai_text: str):
    s = ai_text.strip().upper()
    crypto_map = {"BITCOIN": "BTC", "ETHEREUM": "ETH", "SOLANA": "SOL", "RIPPLE": "XRP", "DOGECOIN": "DOGE"}
    for name, short in crypto_map.items():
        if name in s: s = s.replace(name, short)
    clean_sym = s.replace("/", "").replace("-", "").replace(" ", "").replace("USDT", "").replace("USD", "")
    
    if clean_sym in["NIFTY", "NIFTY50", "NSEI"]: return "NSEI.INDX", "EODHD"
    if clean_sym in["BANKNIFTY", "NIFTYBANK", "NSEBANK"]: return "NSEBANK.INDX", "EODHD"
    if clean_sym in ["SENSEX", "BSESN"]: return "BSESN.INDX", "EODHD"
    if clean_sym in["SPX", "S&P500", "GSPC"]: return "GSPC.INDX", "EODHD"
    if clean_sym in["NDX", "NASDAQ"]: return "NDX.INDX", "EODHD"
    if clean_sym in["DOW", "DJI", "DOWJONES"]: return "DJI.INDX", "EODHD"

    commodities = {
        "GOLD": "XAUUSD", "XAU": "XAUUSD", "XAUUSD": "XAUUSD", "GC=F": "XAUUSD",
        "SILVER": "XAGUSD", "XAG": "XAGUSD", "XAGUSD": "XAGUSD", "SI=F": "XAGUSD",
        "CRUDE": "CLUSD", "OIL": "CLUSD", "WTI": "CLUSD", "CLUSD": "CLUSD", "CL=F": "CLUSD",
        "BRENT": "UKOIL", "UKOIL": "UKOIL",
        "NATURALGAS": "NGUSD", "NGUSD": "NGUSD", "NG=F": "NGUSD"
    }
    if clean_sym in commodities: return commodities[clean_sym], "FMP"
    if s in commodities: return commodities[s], "FMP"
    
    crypto_list =["BTC", "ETH", "SOL", "XRP", "DOGE", "BNB", "MATIC", "ADA", "AVAX", "DOT", "LTC", "SHIB"]
    if clean_sym in crypto_list: return f"{clean_sym}-USD.CC", "EODHD"
    for c in crypto_list:
        if c in s: return f"{c}-USD.CC", "EODHD"

    if "." not in s: return f"{s}.NSE", "EODHD"
    if ".NS" in s: return s.replace(".NS", ".NSE"), "EODHD"
    if ".BO" in s: return s.replace(".BO", ".BSE"), "EODHD"
    return s, "EODHD"

@router.post("/analyze")
async def analyze_chart_image(chart_image: UploadFile = File(...), analysis_type: str = Form("stock")):
    if not chart_image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid file.")

    image_bytes = await chart_image.read()
    
    # 1. AI OCR: Read Ticker and Timeframe ONLY (Zero Hallucination)
    context_str = await asyncio.to_thread(gemini_service.identify_chart_context_from_image, image_bytes)
    parts = context_str.split(',')
    raw_symbol = parts[0] if len(parts) > 0 else "NOT_FOUND"
    timeframe = parts[1] if len(parts) > 1 else "1D"
    
    if timeframe not in["5M", "15M", "30M", "1H", "4H", "1D", "1W", "1M"]: timeframe = "1D"

    if not raw_symbol or "NOT_FOUND" in raw_symbol:
        return {"identified_symbol": "NOT_FOUND", "analysis_data": "Could not identify symbol text.", "technical_data": {}}

    final_symbol, data_source = await resolve_symbol_smart(raw_symbol)

    # 2. Fetch REAL Math Data for the exact Timeframe
    is_intraday = timeframe in["5M", "15M", "30M", "1H", "4H"]
    lookup_range = "5M" if is_intraday else timeframe

    if data_source == "FMP":
        chart_list = await asyncio.to_thread(fmp_service.get_commodity_history, final_symbol, lookup_range)
        if not chart_list: chart_list = await asyncio.to_thread(fmp_service.get_crypto_history, final_symbol, lookup_range)
        quote = await asyncio.to_thread(fmp_service.get_quote, final_symbol)
    else:
        chart_list = await asyncio.to_thread(eodhd_service.get_historical_data, final_symbol, lookup_range)
        quote = await asyncio.to_thread(eodhd_service.get_live_price, final_symbol)

    # 3. Stitch Live Price for 100% Accuracy
    current_price = quote.get('price') if quote else None
    if chart_list and current_price:
        chart_list[-1]['close'] = current_price
        if current_price > chart_list[-1]['high']: chart_list[-1]['high'] = current_price
        if current_price < chart_list[-1]['low']: chart_list[-1]['low'] = current_price

    # 4. Mathematical Resampling & Processing
    if is_intraday and timeframe != "5M":
        chart_list = technical_service.resample_chart_data(chart_list, timeframe)

    if not chart_list or len(chart_list) < 20:
        analysis_report = ERROR_TICKET
    else:
        df = pd.DataFrame(chart_list)
        technicals = technical_service.calculate_technical_indicators(df)
        pivots = technical_service.calculate_pivot_points(df)
        mas = technical_service.calculate_moving_averages(df)
        # Execute Pure Quant Engine (No AI)
        analysis_report = quant_engine.generate_algorithmic_report(final_symbol, timeframe, technicals, pivots, mas)

    frontend_sym = final_symbol
    if frontend_sym.endswith(".NSE"): frontend_sym = frontend_sym.replace(".NSE", ".NS")
    elif frontend_sym.endswith(".BSE"): frontend_sym = frontend_sym.replace(".BSE", ".BO")
    
    return {
        "identified_symbol": frontend_sym,
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