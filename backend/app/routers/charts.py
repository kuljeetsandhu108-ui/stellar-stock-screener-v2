from fastapi import APIRouter, UploadFile, File, HTTPException, Form
# Import all services
from ..services import gemini_service, eodhd_service, technical_service, fmp_service
import asyncio
import pandas as pd
import json
from urllib.parse import unquote

router = APIRouter()

# Timeframes to fetch for "Deep Dive" analysis
TIMEFRAMES_TO_ANALYZE = ["5M", "1H", "4H", "1D"]

# ==========================================
# 1. SMART SYMBOL RESOLVER
# ==========================================

async def resolve_symbol_smart(ai_text: str, context_type: str):
    """
    Routes the AI-identified ticker to the Best Data Provider.
    Returns: (resolved_ticker, source_api)
    """
    symbol = ai_text.strip().upper()
    
    # Clean up common artifacts
    # Remove USD, USDT to isolate the coin symbol (e.g. BTCUSD -> BTC)
    clean_sym = symbol.replace("/", "").replace("-", "").replace(" ", "").replace("USDT", "").replace("USD", "").replace("=F", "")
    
    # --- A. COMMODITIES (Prioritize FMP) ---
    fmp_commodities = {
        "GOLD": "XAUUSD", "XAU": "XAUUSD", "XAUUSD": "XAUUSD", "GC": "XAUUSD",
        "SILVER": "XAGUSD", "XAG": "XAGUSD", "SI": "XAGUSD",
        "CRUDE": "CLUSD", "CRUDEOIL": "CLUSD", "OIL": "CLUSD", "WTI": "CLUSD", "USOIL": "CLUSD", "CL": "CLUSD",
        "BRENT": "UKOIL", "BRENTOIL": "UKOIL", "UKOIL": "UKOIL",
        "NATURALGAS": "NGUSD", "GAS": "NGUSD", "NATGAS": "NGUSD", "NG": "NGUSD", "UNG": "NGUSD",
        "COPPER": "HGUSD", "HG": "HGUSD",
        "PLATINUM": "PLUSD", "PALLADIUM": "PAUSD"
    }
    
    if clean_sym in fmp_commodities: return fmp_commodities[clean_sym], "FMP"
    if symbol in fmp_commodities: return fmp_commodities[symbol], "FMP"

    # --- B. CRYPTO (CRITICAL FIX) ---
    # We must return the Internal Format (BTC-USD.CC) so stocks.py recognizes it correctly
    crypto_shorts = ["BTC", "ETH", "SOL", "XRP", "DOGE", "ADA", "BNB", "MATIC", "AVAX", "LTC", "DOT", "SHIB"]
    
    if clean_sym in crypto_shorts:
        return f"{clean_sym}-USD.CC", "FMP"
        
    if "BTC" in symbol or "ETH" in symbol or "SOL" in symbol:
        # Fallback if cleaning missed it
        return f"{clean_sym}-USD.CC", "FMP"

    # --- C. INDICES (Prioritize EODHD) ---
    if context_type == 'index' or '^' in symbol or 'NIFTY' in symbol or 'SENSEX' in symbol or 'SPX' in symbol:
        if "BANK" in symbol: return "NSEBANK.INDX", "EODHD"
        if "NIFTY" in symbol: return "NSEI.INDX", "EODHD"
        if "SENSEX" in symbol: return "BSESN.INDX", "EODHD"
        if "SPX" in symbol or "S&P" in symbol: return "GSPC.INDX", "EODHD"
        if "NDX" in symbol or "NASDAQ" in symbol: return "NDX.INDX", "EODHD"
        if "DOW" in symbol or "DJI" in symbol: return "DJI.INDX", "EODHD"
        if "VIX" in symbol: return "INDIAVIX.INDX", "EODHD"
        if "DAX" in symbol: return "GDAXI.INDX", "EODHD"
        if "NIKKEI" in symbol: return "N225.INDX", "EODHD"

    # --- D. STOCKS (EODHD) ---
    if ".NS" in symbol: return symbol.replace(".NS", ".NSE"), "EODHD"
    if ".BO" in symbol: return symbol.replace(".BO", ".BSE"), "EODHD"
    if ".US" in symbol: return symbol, "EODHD"

    # Suffix Discovery Fallback
    candidates = [f"{symbol}.NSE", f"{symbol}.US"]
    for cand in candidates:
        try:
            check = await asyncio.to_thread(eodhd_service.get_live_price, cand)
            if check and 'price' in check and check['price'] > 0:
                return cand, "EODHD"
        except: continue
            
    return f"{symbol}.NSE", "EODHD"

# ==========================================
# 2. ENDPOINT: ANALYZE CHART
# ==========================================

@router.post("/analyze")
async def analyze_chart_image(
    chart_image: UploadFile = File(...),
    analysis_type: str = Form("stock")
):
    """
    Master AI Chart Analyst.
    1. AI Vision (Identify Ticker).
    2. Hybrid Resolution (Route to FMP or EODHD).
    3. Parallel Data Fetch (Vision + Math).
    4. Technical Calculation (Pandas).
    5. Synthesis & Response.
    """
    if not chart_image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload an image.")

    image_bytes = await chart_image.read()

    # --- Step 1: AI Vision (Identify Ticker) ---
    # We ask Gemini to just tell us WHAT is in the image first.
    raw_symbol = await asyncio.to_thread(gemini_service.identify_ticker_from_image, image_bytes)

    if not raw_symbol or raw_symbol == "NOT_FOUND":
        return {
            "identified_symbol": "NOT_FOUND", 
            "analysis_data": "Could not identify symbol from image. Please ensure the ticker name is visible.", 
            "technical_data": None
        }
    
    # --- Step 2: Resolve & Normalize (Hybrid Engine) ---
    final_symbol, data_source = await resolve_symbol_smart(raw_symbol, analysis_type)
    print(f"Chart Upload: AI detected '{raw_symbol}' -> Resolved to '{final_symbol}' via {data_source}")

    # --- Step 3: Parallel Execution ---
    
    # Task A: AI Visual Strategy (Generates the text report)
    vision_task = asyncio.to_thread(gemini_service.analyze_chart_technicals_from_image, image_bytes)

    # Task B: Fetch Data for Multiple Timeframes (Math Engine)
    async def fetch_and_calc(tf):
        try:
            raw_data = []
            
            # --- HYBRID FETCHING LOGIC ---
            if data_source == "FMP":
                # Try Commodity First
                raw_data = await asyncio.to_thread(fmp_service.get_commodity_history, final_symbol, range_type=tf)
                # If Empty, Try Crypto
                if not raw_data:
                    raw_data = await asyncio.to_thread(fmp_service.get_crypto_history, final_symbol, range_type=tf)
            else:
                # Fetch Stocks/Indices from EODHD
                raw_data = await asyncio.to_thread(eodhd_service.get_historical_data, final_symbol, range_type=tf)
            
            # Validation
            if not raw_data or len(raw_data) < 20: 
                return tf, None
            
            # Convert to Pandas for Math
            df = pd.DataFrame(raw_data)
            
            # Calculate Indicators
            technicals = await asyncio.to_thread(technical_service.calculate_extended_technicals, df)
            
            return tf, technicals
        except Exception as e:
            print(f"Error analyzing {tf} for {final_symbol}: {e}")
            return tf, None

    # Run all data tasks in parallel
    data_tasks = [fetch_and_calc(tf) for tf in TIMEFRAMES_TO_ANALYZE]
    
    # Execute Vision + Data simultaneously
    results = await asyncio.gather(vision_task, *data_tasks)

    # Unpack Results
    analysis_text = results[0] # The text report from Gemini
    tech_results = results[1:] # The list of (tf, data) tuples

    # Structure Technical Data for Frontend
    technical_data = {tf: data for tf, data in tech_results if data is not None}

    # --- Step 4: Final Response Formatting ---
    frontend_symbol = final_symbol
    
    # Convert EODHD format back to Frontend format if it's a Stock
    if final_symbol.endswith(".NSE"): 
        frontend_symbol = final_symbol.replace(".NSE", ".NS")
    elif final_symbol.endswith(".BSE"): 
        frontend_symbol = final_symbol.replace(".BSE", ".BO")
    
    return {
        "identified_symbol": frontend_symbol,
        "analysis_data": analysis_text,
        "technical_data": technical_data
    }