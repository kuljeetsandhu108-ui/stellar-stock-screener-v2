from fastapi import APIRouter, UploadFile, File, HTTPException, Form
# Import all high-performance services
from ..services import gemini_service, eodhd_service, technical_service, fmp_service
import asyncio
import pandas as pd
import json

router = APIRouter()

# ==========================================
# 1. CONFIGURATION
# ==========================================
# Timeframes for Mathematical Verification
TIMEFRAMES_TO_ANALYZE = ["5M", "1H", "4H", "1D"]

# ==========================================
# 2. HELPER: UNIVERSAL SYMBOL RESOLVER
# ==========================================

async def resolve_symbol_with_eodhd(ai_text: str, context_type: str):
    """
    Intelligently maps AI text (e.g., "Gold", "Reliance", "BTC", "Shiba") 
    to the most liquid EODHD Ticker available.
    
    PRIORITY: 
    1. Indices (Hardcoded)
    2. Major Commodities (Hardcoded)
    3. Major Crypto (Hardcoded)
    4. Dynamic FMP Search (For niche assets)
    5. NSE Stocks (India Priority)
    6. US Stocks
    """
    symbol = ai_text.strip().upper()
    # Clean up common artifacts: "Crude Oil" -> "CRUDEOIL", "BTC/USD" -> "BTCUSD"
    clean_sym = symbol.replace("/", "").replace("-", "").replace(" ", "").replace("USDT", "").replace("USD", "").replace("=F", "")
    
    # --- 1. Handle INDICES (Macro View) ---
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

    # --- 2. Handle COMMODITIES (Liquid ETFs/Spot) ---
    commodity_map = {
        "GOLD": "XAU-USD.CC", "XAU": "XAU-USD.CC", "XAUUSD": "XAU-USD.CC", "GC": "XAU-USD.CC",
        "SILVER": "XAG-USD.CC", "XAG": "XAG-USD.CC", "XAGUSD": "XAG-USD.CC", "SI": "XAG-USD.CC",
        "CRUDE": "USO.US", "CRUDEOIL": "USO.US", "OIL": "USO.US", "WTI": "USO.US", "USOIL": "USO.US",
        "BRENT": "BNO.US", "BRENTOIL": "BNO.US", "UKOIL": "BNO.US",
        "NATURALGAS": "UNG.US", "GAS": "UNG.US", "NATGAS": "UNG.US", "NG": "UNG.US",
        "COPPER": "CPER.US", "HG": "CPER.US"
    }
    
    if clean_sym in commodity_map: return commodity_map[clean_sym]
    if symbol in commodity_map: return commodity_map[symbol]
    for key, ticker in commodity_map.items():
        if key == clean_sym: return ticker

    # --- 3. Handle MAJOR CRYPTO (Hardcoded for Speed) ---
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
    
    if clean_sym in crypto_map: return crypto_map[clean_sym]
    if symbol in crypto_map: return crypto_map[symbol]

    # --- 4. DYNAMIC SEARCH (FMP FALLBACK) ---
    # If it's a niche crypto or commodity not in our list (e.g. "Cotton", "Fetch.ai")
    if context_type == 'crypto' or len(symbol) > 4:
        try:
            # Ask FMP what this symbol is
            search_res = await asyncio.to_thread(fmp_service.search_ticker, clean_sym, limit=1)
            if search_res:
                found = search_res[0]
                ticker = found.get('symbol', '')
                
                # Conversion Logic: FMP -> EODHD
                # FMP Crypto: "BTCUSD" -> EODHD: "BTC-USD.CC"
                if "USD" in ticker and "-" not in ticker and (context_type == 'crypto' or "COIN" in found.get('name', '').upper()):
                    return f"{ticker.replace('USD', '-USD')}.CC"
                
                # FMP Default: If no suffix, assume US
                if "." not in ticker:
                    return f"{ticker}.US"
                    
                return ticker # Return as is if it has suffix
        except: pass

    # --- 5. Handle STOCKS (Explicit Suffixes) ---
    if ".NS" in symbol: return symbol.replace(".NS", ".NSE")
    if ".BO" in symbol: return symbol.replace(".BO", ".BSE")
    if ".US" in symbol: return symbol 

    # --- 6. Stock Discovery (Priority: India -> US) ---
    candidates = [f"{symbol}.NSE", f"{symbol}.US"]
    
    for cand in candidates:
        try:
            # Fast check: Does this symbol exist?
            check = await asyncio.to_thread(eodhd_service.get_live_price, cand)
            if check and 'price' in check:
                return cand
        except:
            continue
            
    # 7. Final Fallback (Assume India)
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
    Master AI Chart Analyst.
    1. AI Vision (Identify)
    2. Asset Resolution (Map to EODHD)
    3. Parallel Data Fetch (Vision + Math)
    4. Response
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
    
    # --- Step 2: Normalize Symbol (Multi-Asset Engine) ---
    final_symbol = await resolve_symbol_with_eodhd(raw_symbol, analysis_type)
    print(f"Chart Upload: AI detected '{raw_symbol}' -> Resolved to '{final_symbol}'")

    # --- Step 3: Parallel Execution ---
    
    # Task A: AI Visual Strategy
    vision_task = asyncio.to_thread(gemini_service.analyze_chart_technicals_from_image, image_bytes)

    # Task B: Fetch Data for Multiple Timeframes (Math Engine)
    async def fetch_and_calc(tf):
        try:
            # 1. Fetch from EODHD (Uses our optimized service)
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

    # Run all data tasks in parallel
    data_tasks = [fetch_and_calc(tf) for tf in TIMEFRAMES_TO_ANALYZE]
    
    # Execute Vision + Data simultaneously
    results = await asyncio.gather(vision_task, *data_tasks)

    # Unpack Results
    analysis_text = results[0] # The text report from Gemini
    tech_results = results[1:] # The list of (tf, data) tuples

    # Structure Technical Data for Frontend Sidebar
    technical_data = {tf: data for tf, data in tech_results if data is not None}

    # --- Step 4: Final Response Formatting ---
    frontend_symbol = final_symbol
    
    # Convert back for frontend routing
    if final_symbol.endswith(".NSE"): 
        frontend_symbol = final_symbol.replace(".NSE", ".NS")
    elif final_symbol.endswith(".BSE"): 
        frontend_symbol = final_symbol.replace(".BSE", ".BO")
    
    return {
        "identified_symbol": frontend_symbol,
        "analysis_data": analysis_text,
        "technical_data": technical_data
    }