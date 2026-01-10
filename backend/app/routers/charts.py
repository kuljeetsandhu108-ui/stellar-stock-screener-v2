from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from ..services import gemini_service, eodhd_service, technical_service
import asyncio
import pandas as pd
import json

router = APIRouter()

# ==========================================
# 1. CONFIGURATION
# ==========================================
# We fetch hard data for these timeframes to verify the AI's visual analysis
TIMEFRAMES_TO_ANALYZE = ["5M", "1H", "4H", "1D"]

# ==========================================
# 2. HELPER: SMART SYMBOL RESOLUTION
# ==========================================

async def resolve_symbol_with_eodhd(ai_text: str, context_type: str):
    """
    Maps AI text to a valid EODHD Ticker. 
    PRIORITY: Indices -> Crypto -> NSE (India) -> US.
    High-End Logic to handle variations like 'Nifty', 'BTCUSDT', 'Reliance'.
    """
    symbol = ai_text.strip().upper()
    clean_sym = symbol.replace("/", "").replace("-", "").replace(" ", "")
    
    # --- 1. Handle INDICES (Hardcoded for stability) ---
    # AI often just says "Nifty" or "BankNifty", we map to EODHD Index tickers
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
    crypto_map = {
        "BTC": "BTC-USD.CC", "BITCOIN": "BTC-USD.CC",
        "ETH": "ETH-USD.CC", "ETHEREUM": "ETH-USD.CC",
        "SOL": "SOL-USD.CC", "SOLANA": "SOL-USD.CC",
        "XRP": "XRP-USD.CC",
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

    # Check for direct matches or common variations (e.g., BTCUSDT, ETH/USD)
    for key, ticker in crypto_map.items():
        # Match 'BTC', 'BTCUSD', 'BTCUSDT'
        if clean_sym == key or clean_sym == f"{key}USD" or clean_sym == f"{key}USDT":
            return ticker

    # --- 3. Handle STOCKS (Explicit Suffixes) ---
    # If AI read the suffix from the image, convert to EODHD format
    if ".NS" in symbol: return symbol.replace(".NS", ".NSE")
    if ".BO" in symbol: return symbol.replace(".BO", ".BSE")
    if ".US" in symbol: return symbol 
    if "." in symbol: return symbol # Trust other existing suffixes

    # --- 4. Suffix Discovery (The Robust Fallback) ---
    # If symbol is "KOTAKBANK" or "AAPL", check India first, then US.
    candidates = [f"{symbol}.NSE", f"{symbol}.US"]
    
    for cand in candidates:
        try:
            # Short timeout check to see if symbol exists on EODHD
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
    analysis_type: str = Form("stock")
):
    """
    1. AI identifies symbol (Stock, Index, or Crypto).
    2. Backend resolves to valid EODHD ticker.
    3. Backend fetches multi-timeframe data & math.
    4. AI analyzes visuals.
    5. Returns normalized symbol to Frontend.
    """
    if not chart_image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload an image.")

    image_bytes = await chart_image.read()

    # --- Step 1: AI Vision (Identify Ticker) ---
    raw_symbol = await asyncio.to_thread(gemini_service.identify_ticker_from_image, image_bytes)

    if not raw_symbol or raw_symbol == "NOT_FOUND":
        return {
            "identified_symbol": "NOT_FOUND", 
            "analysis_data": "Could not identify symbol from image. Please ensure the ticker name is visible.", 
            "technical_data": None
        }
    
    # --- Step 2: Resolve & Normalize Symbol (Crypto Aware) ---
    final_symbol = await resolve_symbol_with_eodhd(raw_symbol, analysis_type)
    
    # --- Step 3: Parallel Execution (Visuals + Data) ---
    
    # Task A: AI Visual Strategy
    vision_task = asyncio.to_thread(gemini_service.analyze_chart_technicals_from_image, image_bytes)

    # Task B: Mathematical Data Verification (Multi-Timeframe)
    async def fetch_and_calc(tf):
        try:
            raw_data = await asyncio.to_thread(eodhd_service.get_historical_data, final_symbol, range_type=tf)
            
            # Validate data
            if not raw_data or len(raw_data) < 20: return tf, None
            
            # Math
            df = pd.DataFrame(raw_data)
            technicals = await asyncio.to_thread(technical_service.calculate_extended_technicals, df)
            
            return tf, technicals
        except: return tf, None

    # Run everything concurrently
    data_tasks = [fetch_and_calc(tf) for tf in TIMEFRAMES_TO_ANALYZE]
    results = await asyncio.gather(vision_task, *data_tasks)

    # Unpack
    analysis_text = results[0]
    tech_results = results[1:]
    technical_data = {tf: data for tf, data in tech_results if data is not None}

    # --- Step 4: Final Response Formatting ---
    # Convert EODHD format back to Frontend format for routing
    frontend_symbol = final_symbol
    
    # India Mapping
    if final_symbol.endswith(".NSE"):
        frontend_symbol = final_symbol.replace(".NSE", ".NS")
    elif final_symbol.endswith(".BSE"):
        frontend_symbol = final_symbol.replace(".BSE", ".BO")
    
    # Crypto Mapping (Keep as is, Frontend chart handles it if symbol is passed correctly)
    # The CustomChart component and Header will adapt based on the symbol string.

    return {
        "identified_symbol": frontend_symbol,
        "analysis_data": analysis_text,
        "technical_data": technical_data
    }