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

# The timeframes we want "Hard Numbers" for to verify the AI's visual hunch
TIMEFRAMES_TO_ANALYZE = ["5M", "1H", "4H", "1D"]

# ==========================================
# 2. HELPER: SYMBOL RESOLUTION
# ==========================================

async def resolve_symbol_with_eodhd(ai_text: str, context_type: str):
    """
    Intelligently maps AI text (e.g., "Reliance", "Nifty", "BTC") 
    to a valid EODHD Ticker (e.g., "RELIANCE.NSE", "NSEI.INDX", "BTC-USD.CC").
    """
    symbol = ai_text.strip().upper()
    
    # --- A. INDICES (Hardcoded for stability) ---
    if context_type == 'index' or '^' in symbol or 'NIFTY' in symbol or 'SENSEX' in symbol:
        if "BANK" in symbol: return "NSEBANK.INDX"
        if "NIFTY" in symbol: return "NSEI.INDX"
        if "SENSEX" in symbol: return "BSESN.INDX"
        if "SPX" in symbol or "S&P" in symbol: return "GSPC.INDX"
        if "NDX" in symbol or "NASDAQ" in symbol: return "NDX.INDX"
        if "DOW" in symbol or "DJI" in symbol: return "DJI.INDX"
        if "VIX" in symbol: return "INDIAVIX.INDX"

    # --- B. CRYPTO ---
    if "BTC" in symbol: return "BTC-USD.CC"
    if "ETH" in symbol: return "ETH-USD.CC"

    # --- C. STOCKS (Smart Suffixing) ---
    # If the AI gave us a specific exchange suffix, adapt it to EODHD
    if ".NS" in symbol: return symbol.replace(".NS", ".NSE")
    if ".BO" in symbol: return symbol.replace(".BO", ".BSE")
    
    # If no suffix, we need to guess based on context or check existence.
    # We prioritize NSE (India) as per your requirement.
    candidates = [f"{symbol}.NSE", f"{symbol}.US"]
    
    for cand in candidates:
        try:
            # Quick check: Get live price to see if symbol exists
            # We use asyncio.to_thread to not block the event loop
            check = await asyncio.to_thread(eodhd_service.get_live_price, cand)
            if check and check.get('price'):
                return cand
        except:
            continue
            
    # Default fallback
    return f"{symbol}.US"

# ==========================================
# 3. ENDPOINT: ANALYZE
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
    5. Synthesis
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
    # This generates the text report (Buy/Sell, Stop Loss, etc.)
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
            # This uses the 'technical_service' we just updated
            technicals = await asyncio.to_thread(technical_service.calculate_extended_technicals, df)
            
            return tf, technicals
        except Exception as e:
            print(f"Error analyzing {tf} for {final_symbol}: {e}")
            return tf, None

    # Run all data fetches in parallel
    data_tasks = [fetch_and_calc(tf) for tf in TIMEFRAMES_TO_ANALYZE]
    
    # Execute Vision + Data simultaneously
    # This ensures the user waits the minimum amount of time
    results = await asyncio.gather(vision_task, *data_tasks)

    # Unpack Results
    analysis_text = results[0] # The text report from Gemini
    tech_results = results[1:] # The list of (tf, data) tuples from EODHD

    # Structure Technical Data for Frontend
    technical_data = {tf: data for tf, data in tech_results if data is not None}

    # --- Step 4: Final Response ---
    return {
        "identified_symbol": final_symbol,
        "analysis_data": analysis_text,
        "technical_data": technical_data # The frontend uses this to show "Hard Numbers" sidebar
    }