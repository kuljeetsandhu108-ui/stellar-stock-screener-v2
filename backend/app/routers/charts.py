from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from ..services import gemini_service, eodhd_service, technical_service
import asyncio
import pandas as pd
import json

router = APIRouter()

# ==========================================
# 1. CONFIGURATION
# ==========================================
TIMEFRAMES_TO_ANALYZE = ["5M", "1H", "4H", "1D"]

# ==========================================
# 2. HELPER: SMART SYMBOL RESOLUTION
# ==========================================

async def resolve_symbol_with_eodhd(ai_text: str, context_type: str):
    """
    Maps AI text to a valid EODHD Ticker. 
    PRIORITY: Hardcoded Crypto > Indices > NSE (India) > US Stocks.
    """
    symbol = ai_text.strip().upper()
    clean_sym = symbol.replace("/", "").replace("-", "").replace(" ", "").replace("USDT", "").replace("USD", "")
    
    # --- 1. HARDCODED CRYPTO TRAP ---
    # Prevents "BTC" mapping to Grayscale ETF. Forces Crypto.
    crypto_map = {
        "BTC": "BTC-USD.CC", "BITCOIN": "BTC-USD.CC",
        "ETH": "ETH-USD.CC", "ETHEREUM": "ETH-USD.CC",
        "SOL": "SOL-USD.CC", "SOLANA": "SOL-USD.CC",
        "XRP": "XRP-USD.CC", "RIPPLE": "XRP-USD.CC",
        "DOGE": "DOGE-USD.CC",
        "ADA": "ADA-USD.CC", "CARDANO": "ADA-USD.CC",
        "BNB": "BNB-USD.CC",
        "MATIC": "MATIC-USD.CC",
        "AVAX": "AVAX-USD.CC",
        "LTC": "LTC-USD.CC",
        "DOT": "DOT-USD.CC",
        "LINK": "LINK-USD.CC",
        "SHIB": "SHIB-USD.CC",
        "PEPE": "PEPE-USD.CC"
    }
    
    # Check exact match or common variations
    if clean_sym in crypto_map: return crypto_map[clean_sym]
    if symbol in crypto_map: return crypto_map[symbol]

    # --- 2. Handle INDICES ---
    if context_type == 'index' or '^' in symbol or 'NIFTY' in symbol or 'SENSEX' in symbol:
        if "BANK" in symbol: return "NSEBANK.INDX"
        if "NIFTY" in symbol: return "NSEI.INDX"
        if "SENSEX" in symbol: return "BSESN.INDX"
        if "SPX" in symbol or "S&P" in symbol: return "GSPC.INDX"
        if "NDX" in symbol or "NASDAQ" in symbol: return "NDX.INDX"
        if "DOW" in symbol or "DJI" in symbol: return "DJI.INDX"
        if "VIX" in symbol: return "INDIAVIX.INDX"

    # --- 3. Handle STOCKS (Explicit Suffixes) ---
    if ".NS" in symbol: return symbol.replace(".NS", ".NSE")
    if ".BO" in symbol: return symbol.replace(".BO", ".BSE")
    if ".US" in symbol: return symbol 
    if "." in symbol: return symbol 

    # --- 4. Suffix Discovery (Priority: India -> US) ---
    candidates = [f"{symbol}.NSE", f"{symbol}.US"]
    
    for cand in candidates:
        try:
            # Quick check if symbol exists via price fetch
            check = await asyncio.to_thread(eodhd_service.get_live_price, cand)
            if check and 'price' in check:
                return cand
        except:
            continue
            
    # 5. Fallback Default
    return f"{symbol}.NSE"

# ==========================================
# 3. ENDPOINT: ANALYZE CHART
# ==========================================

@router.post("/analyze")
async def analyze_chart_image(
    chart_image: UploadFile = File(...),
    analysis_type: str = Form("stock")
):
    if not chart_image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid file type.")

    image_bytes = await chart_image.read()

    # --- 1. AI Vision ---
    raw_symbol = await asyncio.to_thread(gemini_service.identify_ticker_from_image, image_bytes)

    if not raw_symbol or raw_symbol == "NOT_FOUND":
        return {
            "identified_symbol": "NOT_FOUND", 
            "analysis_data": "Could not identify symbol from image.", 
            "technical_data": None
        }
    
    # --- 2. Normalize Symbol ---
    final_symbol = await resolve_symbol_with_eodhd(raw_symbol, analysis_type)
    
    # --- 3. Parallel Execution ---
    vision_task = asyncio.to_thread(gemini_service.analyze_chart_technicals_from_image, image_bytes)

    async def fetch_and_calc(tf):
        try:
            # Fetch Data from EODHD
            raw_data = await asyncio.to_thread(eodhd_service.get_historical_data, final_symbol, range_type=tf)
            
            if not raw_data or len(raw_data) < 20: 
                return tf, None
            
            # Perform Math
            df = pd.DataFrame(raw_data)
            technicals = await asyncio.to_thread(technical_service.calculate_extended_technicals, df)
            
            return tf, technicals
        except: 
            return tf, None

    data_tasks = [fetch_and_calc(tf) for tf in TIMEFRAMES_TO_ANALYZE]
    results = await asyncio.gather(vision_task, *data_tasks)

    analysis_text = results[0]
    tech_results = results[1:]
    technical_data = {tf: data for tf, data in tech_results if data is not None}

    # --- 4. Final Response Formatting ---
    frontend_symbol = final_symbol
    
    # Convert back for frontend routing if needed
    if final_symbol.endswith(".NSE"): 
        frontend_symbol = final_symbol.replace(".NSE", ".NS")
    elif final_symbol.endswith(".BSE"): 
        frontend_symbol = final_symbol.replace(".BSE", ".BO")
    
    return {
        "identified_symbol": frontend_symbol,
        "analysis_data": analysis_text,
        "technical_data": technical_data
    }