from fastapi import APIRouter, UploadFile, File, HTTPException, Form
# Import our high-performance EODHD and Calculation services
from ..services import gemini_service, eodhd_service, technical_service
import asyncio
import pandas as pd
import json

router = APIRouter()

# ==========================================
# 1. CONFIGURATION
# ==========================================

# The timeframes we want "Hard Numbers" for to verify the AI's visual analysis
TIMEFRAMES_TO_ANALYZE = ["5M", "1H", "4H", "1D"]

# ==========================================
# 2. HELPER: SMART SYMBOL RESOLUTION
# ==========================================

async def resolve_symbol_with_eodhd(ai_text: str, context_type: str):
    """
    Intelligently maps AI text (e.g., "Reliance", "Nifty", "BTC") 
    to a valid EODHD Ticker (e.g., "RELIANCE.NSE", "NSEI.INDX", "BTC-USD.CC").
    
    PRIORITY: Indices -> Crypto -> India Stocks -> US Stocks.
    """
    symbol = ai_text.strip().upper()
    clean_sym = symbol.replace("/", "").replace("-", "").replace(" ", "")
    
    # --- 1. Handle INDICES (Hardcoded for stability) ---
    if context_type == 'index' or '^' in symbol or 'NIFTY' in symbol or 'SENSEX' in symbol or 'SPX' in symbol:
        if "BANK" in symbol: return "NSEBANK.INDX"
        if "NIFTY" in symbol: return "NSEI.INDX"
        if "SENSEX" in symbol: return "BSESN.INDX"
        if "SPX" in symbol or "S&P" in symbol: return "GSPC.INDX"
        if "NDX" in symbol or "NASDAQ" in symbol: return "NDX.INDX"
        if "DOW" in symbol or "DJI" in symbol: return "DJI.INDX"
        if "VIX" in symbol: return "INDIAVIX.INDX"
        if "DAX" in symbol: return "GDAXI.INDX"
        if "NIKKEI" in symbol: return "N225.INDX"

    # --- 2. Handle CRYPTO (Expanded High-End Support) ---
    # Smart Map for Top Coins to EODHD's .CC exchange
    # This prevents "BTC" (Bitcoin) from matching "BTC" (Grayscale Trust)
    crypto_map = {
        "BTC": "BTC-USD.CC", "BITCOIN": "BTC-USD.CC", "BTCUSD": "BTC-USD.CC",
        "ETH": "ETH-USD.CC", "ETHEREUM": "ETH-USD.CC", "ETHUSD": "ETH-USD.CC",
        "SOL": "SOL-USD.CC", "SOLANA": "SOL-USD.CC",
        "XRP": "XRP-USD.CC", "RIPPLE": "XRP-USD.CC",
        "BNB": "BNB-USD.CC",
        "DOGE": "DOGE-USD.CC",
        "ADA": "ADA-USD.CC", "CARDANO": "ADA-USD.CC",
        "AVAX": "AVAX-USD.CC",
        "MATIC": "MATIC-USD.CC",
        "LTC": "LTC-USD.CC",
        "DOT": "DOT-USD.CC",
        "LINK": "LINK-USD.CC",
        "SHIB": "SHIB-USD.CC"
    }

    # Check for direct matches or common variations
    for key, ticker in crypto_map.items():
        # Exact match
        if clean_sym == key: return ticker
        # Variation match (e.g., BTCUSDT)
        if clean_sym == f"{key}USD" or clean_sym == f"{key}USDT": return ticker

    # --- 3. Handle STOCKS (Explicit Suffixes) ---
    # If AI read the suffix from the image, convert to EODHD format
    if ".NS" in symbol: return symbol.replace(".NS", ".NSE")
    if ".BO" in symbol: return symbol.replace(".BO", ".BSE")
    if ".US" in symbol: return symbol 
    if "." in symbol: return symbol # Trust other existing suffixes

    # --- 4. Suffix Discovery (The Robust Fallback) ---
    # If no suffix, we check India first, then US.
    candidates = [f"{symbol}.NSE", f"{symbol}.US"]
    
    for cand in candidates:
        try:
            # Check if symbol exists on EODHD by getting live price
            check = await asyncio.to_thread(eodhd_service.get_live_price, cand)
            if check and 'price' in check:
                return cand
        except:
            continue
            
    # 5. FINAL SAFETY NET (Priority: India)
    return f"{symbol}.NSE"

# ==========================================
# 3. ENDPOINT: ANALYZE CHART
# ==========================================

@router.post("/analyze")
async def analyze_chart_image(
    chart_image: UploadFile = File(...),
    analysis_type: str = Form("stock") # 'stock' or 'index' passed from frontend
):
    """
    Master AI Chart Analyst.
    1. Visual Recognition (Gemini Vision)
    2. Symbol Verification (EODHD)
    3. Multi-Timeframe Data Fetch (EODHD Intraday/EOD)
    4. Technical Calculation (Pandas TA)
    5. Synthesis & Response
    """
    if not chart_image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload an image.")

    image_bytes = await chart_image.read()

    # --- Step 1: Identify Symbol (AI Vision) ---
    # We ask Gemini to look at the top-left of the chart image
    raw_symbol = await asyncio.to_thread(gemini_service.identify_ticker_from_image, image_bytes)

    if not raw_symbol or raw_symbol == "NOT_FOUND":
        return {
            "identified_symbol": "NOT_FOUND", 
            "analysis_data": "Could not identify symbol from image. Please ensure the ticker name is visible.", 
            "technical_data": None
        }
    
    # --- Step 2: Normalize Symbol for EODHD ---
    final_symbol = await resolve_symbol_with_eodhd(raw_symbol, analysis_type)
    print(f"Chart Upload: AI detected '{raw_symbol}' -> Resolved to '{final_symbol}'")

    # --- Step 3: Parallel Execution (Visual Analysis + Mathematical Data) ---
    
    # Task A: Gemini Vision Analysis (The Strategy)
    vision_task = asyncio.to_thread(gemini_service.analyze_chart_technicals_from_image, image_bytes)

    # Task B: Fetch Data for Multiple Timeframes (The Confirmation)
    async def fetch_and_calc(tf):
        try:
            # 1. Fetch from EODHD (Uses our new robust service)
            raw_data = await asyncio.to_thread(eodhd_service.get_historical_data, final_symbol, range_type=tf)
            
            # 2. Validation
            if not raw_data or len(raw_data) < 20: 
                return tf, None
            
            # 3. Convert to Pandas for Math
            df = pd.DataFrame(raw_data)
            
            # 4. Calculate Indicators (RSI, MACD, EMAs, Pivots)
            technicals = await asyncio.to_thread(technical_service.calculate_extended_technicals, df)
            
            return tf, technicals
        except Exception as e:
            print(f"Error analyzing {tf} for {final_symbol}: {e}")
            return tf, None

    # Run all data fetches in parallel
    data_tasks = [fetch_and_calc(tf) for tf in TIMEFRAMES_TO_ANALYZE]
    
    # Execute Vision + Data simultaneously
    results = await asyncio.gather(vision_task, *data_tasks)

    # Unpack Results
    analysis_text = results[0] # The text report from Gemini
    tech_results = results[1:] # The list of (tf, data) tuples from EODHD

    # Structure Technical Data for Frontend
    technical_data = {tf: data for tf, data in tech_results if data is not None}

    # --- Step 4: Final Response Formatting ---
    # Convert EODHD format back to Frontend format for seamless routing
    frontend_symbol = final_symbol
    
    # India Mapping (.NSE -> .NS)
    if final_symbol.endswith(".NSE"):
        frontend_symbol = final_symbol.replace(".NSE", ".NS")
    elif final_symbol.endswith(".BSE"):
        frontend_symbol = final_symbol.replace(".BSE", ".BO")
    
    # Crypto Mapping is handled automatically by the frontend if it receives "BTC-USD.CC"
    
    return {
        "identified_symbol": frontend_symbol,
        "analysis_data": analysis_text,
        "technical_data": technical_data 
    }