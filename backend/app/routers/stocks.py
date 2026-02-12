import asyncio
import math
import pandas as pd
import json
from urllib.parse import unquote
from fastapi import APIRouter, HTTPException, Query, Body
# ROBUST SERVICE IMPORTS
from ..services import (
    fmp_service, 
    eodhd_service, 
    news_service, 
    gemini_service, 
    fundamental_service, 
    technical_service, 
    sentiment_service, 
    redis_service
)
from pydantic import BaseModel
from typing import List, Dict, Any

router = APIRouter()

# ==========================================
# 1. STRICT DATA MODELS
# ==========================================

class SwotRequest(BaseModel):
    companyName: str
    description: str

class ForecastRequest(BaseModel):
    companyName: str
    analystRatings: List[Dict[str, Any]]
    priceTarget: Dict[str, Any]
    keyStats: Dict[str, Any]
    newsHeadlines: List[str]
    currency: str = "USD"

class FundamentalRequest(BaseModel):
    companyName: str
    keyMetrics: Dict[str, Any]

class CanslimRequest(BaseModel):
    companyName: str
    quote: Dict[str, Any]
    quarterlyEarnings: List[Dict[str, Any]]
    annualEarnings: List[Dict[str, Any]]
    institutionalHolders: int

class ConclusionRequest(BaseModel):
    companyName: str
    piotroskiData: Dict[str, Any]
    grahamData: Dict[str, Any]
    darvasData: Dict[str, Any]
    canslimAssessment: str
    philosophyAssessment: str
    keyStats: Dict[str, Any]
    newsHeadlines: List[str]

class TimeframeRequest(BaseModel):
    timeframe: str

# TradingView Symbol Mapping
TRADINGVIEW_OVERRIDE_MAP = {
    "TATAPOWER.NS": "NSE:TATAPOWER",
    "RELIANCE.NS": "NSE:RELIANCE",
    "BAJFINANCE.NS": "NSE:BAJFINANCE",
    "HDFCBANK.NS": "NSE:HDFCBANK",
    "SBIN.NS": "NSE:SBIN",
    "INFY.NS": "NSE:INFY",
    "TCS.NS": "NSE:TCS",
    "BTC-USD": "BINANCE:BTCUSD",
    "ETH-USD": "BINANCE:ETHUSD",
    "XAU-USD.CC": "OANDA:XAUUSD",
    "USO.US": "TVC:USOIL"
}

# ==========================================
# 2. INTELLIGENT ASSET RECOGNITION
# ==========================================

def identify_asset_class(symbol: str):
    """
    Maps ANY ticker format (Yahoo, TradingView, Colloquial) to our Internal Data Sources.
    Returns: (Source_System, Clean_Ticker)
    """
    s = unquote(symbol).upper().strip()
    
    # --- A. COMMODITIES (Yahoo/TV -> FMP) ---
    if s in ["CL=F", "CL%3DF", "USOIL", "WTI", "CRUDE", "CRUDEOIL", "OIL", "CLUSD"]: return "FMP", "CLUSD"
    if s in ["BZ=F", "BRENT", "UKOIL", "BRENTOIL"]: return "FMP", "UKOIL"
    if s in ["GC=F", "GOLD", "XAU", "XAUUSD"]: return "FMP", "XAUUSD"
    if s in ["SI=F", "SILVER", "XAG", "XAGUSD"]: return "FMP", "XAGUSD"
    if s in ["NG=F", "GAS", "NATGAS", "NGUSD", "UNG", "UNG.US"]: return "FMP", "NGUSD"
    if s in ["HG=F", "COPPER", "HGUSD"]: return "FMP", "HGUSD"
    if s in ["PL=F", "PLATINUM", "PLUSD"]: return "FMP", "PLUSD"

    # --- B. CRYPTO (Coinbase/Yahoo -> FMP) ---
    if ".CC" in s or s in ["BTC", "ETH", "SOL", "XRP", "DOGE", "ADA", "MATIC", "DOT", "LTC"]:
        clean = s.replace("-USD.CC", "USD").replace(".CC", "")
        if not clean.endswith("USD"): clean += "USD"
        return "FMP", clean

    # --- C. STOCKS / INDICES (Default -> EODHD) ---
    return "EODHD", s

# ==========================================
# 3. AI & SEARCH ENDPOINTS
# ==========================================

@router.get("/autocomplete")
async def get_stock_autocomplete(query: str = Query(..., min_length=1)):
    """High-Speed Autocomplete Engine."""
    cache_key = f"autocomplete_v3_{query.lower().strip()}"
    cached = await redis_service.redis_client.get_cache(cache_key)
    if cached: return cached

    results = await asyncio.to_thread(fmp_service.search_ticker, query, limit=25)
    if not results: return []

    nse_stocks, bse_stocks, us_stocks, others = [], [], [], []
    for stock in results:
        sym = stock.get('symbol', '').upper()
        exch = stock.get('exchangeShortName', '').upper()
        
        is_nse = sym.endswith('.NS') or exch == 'NSE'
        is_bse = sym.endswith('.BO') or exch == 'BSE'
        is_us = not (is_nse or is_bse) and ('.' not in sym) 

        if is_nse: nse_stocks.append(stock)
        elif is_bse: bse_stocks.append(stock)
        elif is_us: us_stocks.append(stock)
        else: others.append(stock)

    final_list = (nse_stocks + bse_stocks + us_stocks + others)[:10]
    await redis_service.redis_client.set_cache(cache_key, final_list, 86400)
    return final_list

@router.get("/search")
async def search_stock_ticker(query: str = Query(..., min_length=2)):
    cache_key = f"search_v4_{query.lower().strip()}"
    cached = await redis_service.redis_client.get_cache(cache_key)
    if cached: return cached
    
    source, ticker = identify_asset_class(query)
    if source == "FMP" and ticker in ["XAUUSD", "XAGUSD", "CLUSD", "NGUSD", "UKOIL"]:
        return {"symbol": ticker} 

    results = fmp_service.search_ticker(query)
    if results: 
        res = {"symbol": results[0]['symbol']}
        await redis_service.redis_client.set_cache(cache_key, res, 86400) 
        return res

    ticker = gemini_service.get_ticker_from_query(query)
    if ticker not in ["NOT_FOUND", "ERROR"]:
        res = {"symbol": ticker}
        await redis_service.redis_client.set_cache(cache_key, res, 86400)
        return res
    raise HTTPException(status_code=404, detail="Ticker not found")

# --- AI ANALYSIS WRAPPERS ---

@router.post("/{symbol}/swot")
async def get_swot_analysis(symbol: str, request_data: SwotRequest = Body(...)):
    cache_key = f"swot_v2_{symbol}"
    cached = await redis_service.redis_client.get_cache(cache_key)
    if cached: return cached
    news_articles = await asyncio.to_thread(news_service.get_company_news, request_data.companyName)
    news_headlines = [a.get('title', '') for a in news_articles[:10]]
    swot_analysis = await asyncio.to_thread(gemini_service.generate_swot_analysis, request_data.companyName, request_data.description, news_headlines)
    res = {"swot_analysis": swot_analysis}
    await redis_service.redis_client.set_cache(cache_key, res, 3600)
    return res

@router.post("/{symbol}/forecast-analysis")
async def get_forecast_analysis(symbol: str, d: ForecastRequest = Body(...)):
    cache_key = f"fc_v2_{symbol}"
    cached = await redis_service.redis_client.get_cache(cache_key)
    if cached: return cached
    analysis = await asyncio.to_thread(gemini_service.generate_forecast_analysis, d.companyName, d.analystRatings, d.priceTarget, d.keyStats, d.newsHeadlines, d.currency)
    res = {"analysis": analysis}; await redis_service.redis_client.set_cache(cache_key, res, 3600); return res

@router.post("/{symbol}/fundamental-analysis")
async def get_fundamental_analysis(symbol: str, d: FundamentalRequest = Body(...)):
    cache_key = f"fa_v2_{symbol}"
    cached = await redis_service.redis_client.get_cache(cache_key)
    if cached: return cached
    analysis = await asyncio.to_thread(gemini_service.generate_investment_philosophy_assessment, d.companyName, d.keyMetrics)
    res = {"assessment": analysis}; await redis_service.redis_client.set_cache(cache_key, res, 86400); return res

@router.post("/{symbol}/canslim-analysis")
async def get_canslim_analysis(symbol: str, d: CanslimRequest = Body(...)):
    cache_key = f"can_v2_{symbol}"
    cached = await redis_service.redis_client.get_cache(cache_key)
    if cached: return cached
    analysis = await asyncio.to_thread(gemini_service.generate_canslim_assessment, d.companyName, d.quote, d.quarterlyEarnings, d.annualEarnings, d.institutionalHolders)
    res = {"assessment": analysis}; await redis_service.redis_client.set_cache(cache_key, res, 3600); return res

@router.post("/{symbol}/conclusion-analysis")
async def get_conclusion_analysis(symbol: str, d: ConclusionRequest = Body(...)):
    cache_key = f"conc_v2_{symbol}"
    cached = await redis_service.redis_client.get_cache(cache_key)
    if cached: return cached
    conclusion = await asyncio.to_thread(gemini_service.generate_fundamental_conclusion, d.companyName, d.piotroskiData, d.grahamData, d.darvasData, {k: v for k, v in d.keyStats.items() if v is not None}, d.newsHeadlines)
    res = {"conclusion": conclusion}; await redis_service.redis_client.set_cache(cache_key, res, 3600); return res

# ==========================================
# 4. TECHNICAL ANALYSIS & CHART ENGINE
# ==========================================

@router.post("/{symbol}/timeframe-analysis")
async def get_timeframe_analysis(symbol: str, request_data: TimeframeRequest = Body(...)):
    """
    AI Chart Analysis with Mathematical Resampling.
    Fetches 5M data ONCE, then computes 15M/1H/4H locally for the AI.
    """
    source, ticker = identify_asset_class(symbol)
    
    # 1. Determine "Master" Timeframe
    # If user wants Intraday (15M, 1H, 4H), we fetch 5M Base Data
    is_intraday_request = request_data.timeframe.upper() in ["5M", "15M", "30M", "1H", "4H"]
    lookup_range = "5M" if is_intraday_request else request_data.timeframe

    # 2. Check Cache for the MASTER Data (e.g., 5M)
    # Note: Cache key matches get_stock_chart so they share the data pool
    cache_key = f"chart_base_v16_{symbol}_{lookup_range}" 
    chart_list = await redis_service.redis_client.get_cache(cache_key)
    
    # 3. If Cache Miss, Fetch from API
    if not chart_list:
        if source == "FMP":
            chart_list = await asyncio.to_thread(fmp_service.get_commodity_history, ticker, range_type=lookup_range)
            if not chart_list: chart_list = await asyncio.to_thread(fmp_service.get_crypto_history, ticker, range_type=lookup_range)
        else:
            chart_list = await asyncio.to_thread(eodhd_service.get_historical_data, ticker, range_type=lookup_range)
        
        # Save Master Data
        if chart_list:
            await redis_service.redis_client.set_cache(cache_key, chart_list, 300)

    if not chart_list: return {"analysis": f"Market data unavailable for {request_data.timeframe}."}
    
    # 4. MATHEMATICAL RESAMPLING (The Optimization)
    # If we have 5M data but the AI needs 1H, we compute it here.
    if is_intraday_request and request_data.timeframe.upper() != "5M":
         chart_list = technical_service.resample_chart_data(chart_list, request_data.timeframe)

    # 5. Calculate Indicators on the RESAMPLED data
    df = pd.DataFrame(chart_list)
    technicals = technical_service.calculate_technical_indicators(df)
    pivots = technical_service.calculate_pivot_points(df)
    mas = technical_service.calculate_moving_averages(df)
    
    # 6. AI Insight
    analysis = await asyncio.to_thread(gemini_service.generate_timeframe_analysis, symbol, request_data.timeframe, technicals, pivots, mas)
    
    return {"analysis": analysis}


@router.post("/{symbol}/technicals-data")
async def get_technicals_data(symbol: str, request_data: TimeframeRequest = Body(...)):
    """
    Returns Raw Technical Data using Math Resampling.
    Used for the Gauge and Table UI.
    """
    source, ticker = identify_asset_class(symbol)
    
    is_intraday_request = request_data.timeframe.upper() in ["5M", "15M", "30M", "1H", "4H"]
    lookup_range = "5M" if is_intraday_request else request_data.timeframe
    
    # Check Cache for Master Data
    cache_key = f"chart_base_v16_{symbol}_{lookup_range}"
    chart_list = await redis_service.redis_client.get_cache(cache_key)

    if not chart_list:
        if source == "FMP":
            chart_list = await asyncio.to_thread(fmp_service.get_commodity_history, ticker, range_type=lookup_range)
            if not chart_list: chart_list = await asyncio.to_thread(fmp_service.get_crypto_history, ticker, request_data.timeframe)
        else:
            chart_list = await asyncio.to_thread(eodhd_service.get_historical_data, ticker, range_type=lookup_range)
        
        if chart_list:
             await redis_service.redis_client.set_cache(cache_key, chart_list, 300)

    if not chart_list: return {"error": "No data available"}
    
    # Math Resampling
    if is_intraday_request and request_data.timeframe.upper() != "5M":
         chart_list = technical_service.resample_chart_data(chart_list, request_data.timeframe)

    df = pd.DataFrame(chart_list)
    return {
        "technicalIndicators": technical_service.calculate_technical_indicators(df),
        "pivotPoints": technical_service.calculate_pivot_points(df),
        "movingAverages": technical_service.calculate_moving_averages(df)
    }

# ==========================================
# 5. MASTER DATA ENDPOINTS (ROBUST)
# ==========================================

@router.get("/{symbol}/peers")
async def get_peers_comparison(symbol: str):
    """
    High-Performance Peers Engine.
    Uses FMP Bulk Fetch to get metrics for all peers in 1 API Call.
    """
    cache_key = f"peers_v8_{symbol}"
    cached = await redis_service.redis_client.get_cache(cache_key)
    if cached: return cached
    
    # 1. Get Peer Tickers
    peers = await asyncio.to_thread(fmp_service.get_stock_peers, symbol)
    
    # AI Fallback if API returns nothing
    if not peers:
        # We try to guess the sector/industry from the symbol string or defaults
        # For simplicity in this fast endpoint, we might skip AI here to keep it fast, 
        # or use a very small fallback list if it's a known big stock.
        pass

    # 2. Normalize Tickers
    # If main symbol is RELIANCE.NS, ensure peers are also .NS
    clean_peers = []
    suffix = ""
    if ".NS" in symbol: suffix = ".NS"
    elif ".BO" in symbol: suffix = ".BO"
    
    # Add Main Symbol to the list (so it appears in comparison)
    all_symbols = [symbol]
    
    for p in peers:
        p_clean = p.strip().upper()
        # If peer doesn't have suffix but main does, add it
        if suffix and "." not in p_clean:
            p_clean += suffix
        all_symbols.append(p_clean)

    # Limit to main + 4 peers to save bandwidth
    target_symbols = all_symbols[:5]

    # 3. BULK FETCH (The Speed Fix)
    # We ask FMP for metrics of ALL stocks in ONE call
    raw_metrics = await asyncio.to_thread(fmp_service.get_peers_with_metrics, target_symbols)
    
    if not raw_metrics:
        return []

    # 4. Format Data for Frontend
    final_data = []
    for item in raw_metrics:
        final_data.append({
            "symbol": item.get('symbol'),
            "marketCap": item.get('marketCapTTM'),
            "peRatioTTM": item.get('peRatioTTM'),
            "revenueGrowth": item.get('revenueGrowthTTM'),
            "grossMargins": item.get('grossProfitMarginTTM')
        })

    # Cache result
    await redis_service.redis_client.set_cache(cache_key, final_data, 86400)
    return final_data

@router.get("/{symbol}/chart")
async def get_stock_chart(symbol: str, range: str = "1D"):
    source, fmp_ticker = identify_asset_class(symbol)
    
    # Timeframe logic
    is_intraday_derived = range in ["5M", "15M", "30M", "1H", "4H"]
    lookup_range = "5M" if is_intraday_derived else range
    
    cache_key = f"chart_base_v16_{symbol}_{lookup_range}"
    ttl = 300 if is_intraday_derived else 43200
    
    chart_data = await redis_service.redis_client.get_cache(cache_key)
    if not chart_data:
        if source == "FMP":
            chart_data = await asyncio.to_thread(fmp_service.get_commodity_history, fmp_ticker, range_type=lookup_range)
            if not chart_data:
                 chart_data = await asyncio.to_thread(fmp_service.get_crypto_history, fmp_ticker, range_type=lookup_range)
            if not chart_data:
                chart_data = await asyncio.to_thread(eodhd_service.get_historical_data, symbol, range_type=lookup_range)
        else:
            chart_data = await asyncio.to_thread(eodhd_service.get_historical_data, symbol, range_type=lookup_range)
        if chart_data:
            await redis_service.redis_client.set_cache(cache_key, chart_data, ttl)
    
    if not chart_data: return []
    final_data = chart_data
    
    # Resample for Display
    if is_intraday_derived and range != "5M":
        resampled = technical_service.resample_chart_data(chart_data, range)
        if resampled: final_data = resampled

    # Live Price Stitching
    try:
        current_price = 0
        if source == "FMP":
            q = await asyncio.to_thread(fmp_service.get_quote, fmp_ticker)
            current_price = q.get('price')
        else:
            q = await asyncio.to_thread(eodhd_service.get_live_price, symbol)
            current_price = q.get('price')
        if current_price and final_data:
            last = final_data[-1]
            last['close'] = current_price
            if current_price > last['high']: last['high'] = current_price
            if current_price < last['low']: last['low'] = current_price
    except Exception: pass 

    return final_data

@router.get("/{symbol}/all")
async def get_all_stock_data(symbol: str):
    cache_key = f"all_data_v27_{symbol}"
    cached = await redis_service.redis_client.get_cache(cache_key)
    if cached: return cached

    source, fmp_ticker = identify_asset_class(symbol)
    tasks = { "news": asyncio.to_thread(news_service.get_company_news, symbol) }

    if source == "FMP":
        tasks.update({
            "fmp_quote": asyncio.to_thread(fmp_service.get_quote, fmp_ticker),
            "chart_data": asyncio.to_thread(fmp_service.get_commodity_history, fmp_ticker, "1D") 
        })
    else:
        tasks.update({
            "eod_fund": asyncio.to_thread(eodhd_service.get_company_fundamentals, symbol),
            "eod_live": asyncio.to_thread(eodhd_service.get_live_price, symbol),
            "fmp_prof": asyncio.to_thread(fmp_service.get_company_profile, symbol),
            "fmp_rating": asyncio.to_thread(fmp_service.get_analyst_ratings, symbol),
            "fmp_target": asyncio.to_thread(fmp_service.get_price_target_consensus, symbol),
            "shareholding": asyncio.to_thread(fmp_service.get_shareholding_data, symbol),
            "chart_data": asyncio.to_thread(eodhd_service.get_historical_data, symbol, "1D")
        })

    try:
        results = await asyncio.gather(*tasks.values(), return_exceptions=True)
        raw = dict(zip(tasks.keys(), results))
    except: raw = {}

    def safe(k, d=None):
        val = raw.get(k)
        if isinstance(val, Exception) or val is None: return d
        return val

    final_data = {}

    if source == "FMP":
        q = safe('fmp_quote', {})
        if not q: q = await asyncio.to_thread(eodhd_service.get_live_price, symbol)

        final_data['profile'] = {
            "companyName": q.get('name') or symbol, 
            "symbol": symbol, "description": f"Real-Time Market Data for {symbol}.",
            "image": "", "currency": "USD", "sector": "Commodity/Crypto",
            "tradingview_symbol": TRADINGVIEW_OVERRIDE_MAP.get(symbol, symbol)
        }
        final_data['quote'] = q
        
        chart_data = safe('chart_data', [])
        if not chart_data:
             chart_data = await asyncio.to_thread(fmp_service.get_crypto_history, fmp_ticker, "1D")
        if not chart_data:
             chart_data = await asyncio.to_thread(eodhd_service.get_historical_data, symbol, "1D")

        # --- SAFE INITIALIZATION ---
        final_data['key_metrics'] = {} 
        final_data['annual_revenue_and_profit'] = []
        final_data['annual_balance_sheets'] = []
        final_data['annual_cash_flow_statements'] = []
        final_data['quarterly_income_statements'] = []
        final_data['quarterly_balance_sheets'] = []
        final_data['quarterly_cash_flow_statements'] = []
        final_data['shareholding'] = []
        final_data['shareholding_breakdown'] = {}
        eod_ratings, eod_targets, fmp_ratings, fmp_targets = [], {}, [], {}
        
    else:
        # STOCK LOGIC
        eod_fund = safe('eod_fund', {})
        eod_p = eodhd_service.parse_profile_from_fundamentals(eod_fund, symbol)
        fmp_p = safe('fmp_prof', {}) or {}
        tv_symbol = symbol
        if symbol in TRADINGVIEW_OVERRIDE_MAP: tv_symbol = TRADINGVIEW_OVERRIDE_MAP[symbol]
        elif symbol.endswith(".NS"): tv_symbol = "NSE:" + symbol.replace(".NS", "")
        
        final_data['profile'] = {**eod_p, "description": fmp_p.get("description") or eod_p.get("description"), "image": fmp_p.get("image") or eod_p.get("image"), "tradingview_symbol": tv_symbol}
        final_data['key_metrics'] = eodhd_service.parse_metrics_from_fundamentals(eod_fund)
        final_data['quote'] = safe('eod_live', {})
        final_data['annual_revenue_and_profit'] = eodhd_service.parse_financials(eod_fund, 'Financials::Income_Statement', 'yearly')
        final_data['annual_balance_sheets'] = eodhd_service.parse_financials(eod_fund, 'Financials::Balance_Sheet', 'yearly')
        final_data['annual_cash_flow_statements'] = eodhd_service.parse_financials(eod_fund, 'Financials::Cash_Flow', 'yearly')
        final_data['quarterly_income_statements'] = eodhd_service.parse_financials(eod_fund, 'Financials::Income_Statement', 'quarterly')
        final_data['quarterly_balance_sheets'] = eodhd_service.parse_financials(eod_fund, 'Financials::Balance_Sheet', 'quarterly')
        final_data['quarterly_cash_flow_statements'] = eodhd_service.parse_financials(eod_fund, 'Financials::Cash_Flow', 'quarterly')
        chart_data = safe('chart_data', [])
        share_bd = eodhd_service.parse_shareholding_breakdown(eod_fund)
        shares = eodhd_service.parse_holders(eod_fund)
        if share_bd.get('promoter') == 0:
            fmp_s = safe('shareholding', [])
            if fmp_s:
                t = sum(h.get('shares', 0) for h in fmp_s)
                share_bd = {"promoter": 0, "fii": t*0.6, "dii": t*0.4, "public": 0}
                shares = fmp_s
        final_data['shareholding'] = shares
        final_data['shareholding_breakdown'] = share_bd
        eod_ratings, eod_targets = eodhd_service.parse_analyst_data(eod_fund) if hasattr(eodhd_service, 'parse_analyst_data') else ([], {})
        fmp_ratings, fmp_targets = safe('fmp_rating', []), safe('fmp_target', {})

    tech_inds, mas, pivots, darvas = {}, {}, {}, {}
    if chart_data and len(chart_data) > 20:
        try:
            df = pd.DataFrame(chart_data)
            tech_inds = technical_service.calculate_technical_indicators(df)
            mas = technical_service.calculate_moving_averages(df)
            pivots = technical_service.calculate_pivot_points(df)
            if source != "FMP" and final_data['quote']:
                darvas = technical_service.calculate_darvas_box(df, final_data['quote'], final_data['profile'].get('currency', 'USD'))
        except: pass

    final_data['technical_indicators'] = tech_inds
    final_data['moving_averages'] = mas
    final_data['pivot_points'] = pivots
    final_data['darvas_scan'] = darvas

    piotroski, graham = {}, {}
    if source != "FMP":
        piotroski = fundamental_service.calculate_piotroski_f_score(final_data['annual_revenue_and_profit'], final_data['annual_balance_sheets'], final_data['annual_cash_flow_statements'])
        graham = fundamental_service.calculate_graham_scan(final_data['profile'], final_data.get('key_metrics', {}), final_data['annual_revenue_and_profit'], final_data['annual_cash_flow_statements'])
    
    final_data['piotroski_f_score'] = piotroski
    final_data['graham_scan'] = graham
    
    # SAFE CALL
    final_data['overall_sentiment'] = sentiment_service.calculate_overall_sentiment(
        piotroski.get('score'), 
        final_data.get('key_metrics', {}), 
        tech_inds, 
        safe('fmp_rating', [])
    )
    final_data['news'] = safe('news', [])

    def has_votes(r): return r and isinstance(r, list) and len(r)>0 and (r[0].get('ratingBuy',0)+r[0].get('ratingHold',0)+r[0].get('ratingSell',0) > 0)
    
    if source != "FMP" and has_votes(eod_ratings):
        final_data['analyst_ratings'] = eod_ratings; final_data['price_target_consensus'] = eod_targets
    elif source != "FMP" and has_votes(fmp_ratings):
        final_data['analyst_ratings'] = fmp_ratings; final_data['price_target_consensus'] = fmp_targets
    else:
        price = final_data['quote'].get('price') or 0
        if price == 0 and chart_data: price = chart_data[-1]['close']
        rsi = tech_inds.get('rsi', 50)
        syn = {"ratingStrongBuy": 0, "ratingBuy": 0, "ratingHold": 0, "ratingSell": 0, "ratingStrongSell": 0}
        if rsi < 30: syn["ratingStrongBuy"] = 12; syn["ratingBuy"] = 8
        elif rsi < 45: syn["ratingBuy"] = 10; syn["ratingHold"] = 10
        elif rsi < 55: syn["ratingHold"] = 20
        elif rsi < 70: syn["ratingSell"] = 10; syn["ratingHold"] = 10
        else: syn["ratingStrongSell"] = 12; syn["ratingSell"] = 8
        target = price if price > 0 else 100
        if price > 0:
            pc = pivots.get('classic', {})
            target = pc.get('r1') if rsi < 50 else pc.get('s1') or price
        final_data['analyst_ratings'] = [syn]
        final_data['price_target_consensus'] = {"targetHigh": target*1.1, "targetLow": target*0.9, "targetConsensus": target}

    pt = final_data.get('price_target_consensus', {})
    if not pt.get('targetConsensus'):
        p = final_data['quote'].get('price') or 100
        final_data['price_target_consensus'] = {"targetHigh": p*1.1, "targetLow": p*0.9, "targetConsensus": p}

    km = final_data.get('key_metrics', {})
    kq = final_data.get('quote', {})
    def n(v): return None if isinstance(v, float) and (math.isnan(v) or math.isinf(v)) else v

    final_data['keyStats'] = {
        "marketCap": n(km.get('marketCap')), "peRatio": n(km.get('peRatioTTM')), 
        "dividendYield": n(km.get('dividendYieldTTM')), "basicEPS": n(km.get('epsTTM')),
        "sharesFloat": n(km.get('sharesOutstanding')), "beta": n(km.get('beta')),
        "netIncome": n(km.get('epsTTM')), "revenue": n(km.get('revenueGrowth')),
        "dayLow": n(kq.get('dayLow') or kq.get('low')), 
        "dayHigh": n(kq.get('dayHigh') or kq.get('high')), 
        "yearHigh": n(kq.get('yearHigh') or kq.get('high')),
        "nextReportDate": None, "epsEstimate": None, "revenueEstimate": None
    }

    def clean_json(obj):
        if isinstance(obj, float): return None if math.isnan(obj) or math.isinf(obj) else obj
        if isinstance(obj, dict): return {k: clean_json(v) for k, v in obj.items()}
        if isinstance(obj, list): return [clean_json(v) for v in obj]
        return obj

    final = clean_json(final_data)
    await redis_service.redis_client.set_cache(cache_key, final, 300)
    return final


# ==========================================
# 5. THE "OMNI-ANALYST" ENGINE (ALL TIMEFRAMES AT ONCE)
# ==========================================

@router.post("/{symbol}/all-timeframe-analysis")
async def get_all_timeframe_analysis(symbol: str):
    """
    Generates AI Analysis for 5M, 15M, 1H, 4H, and 1D in a SINGLE request.
    Uses Mathematical Resampling to avoid extra API calls.
    """
    cache_key = f"omni_analysis_v1_{symbol}"
    cached = await redis_service.redis_client.get_cache(cache_key)
    if cached: return cached

    # 1. Identify Asset
    source, ticker = identify_asset_class(symbol)
    
    # 2. Fetch MASTER Data (5 Minute)
    # We use 5M because we can build 15M, 1H, 4H, 1D from it mathematically.
    if source == "FMP":
        chart_data = await asyncio.to_thread(fmp_service.get_commodity_history, ticker, range_type="5M")
        if not chart_data: chart_data = await asyncio.to_thread(fmp_service.get_crypto_history, ticker, range_type="5M")
    else:
        chart_data = await asyncio.to_thread(eodhd_service.get_historical_data, ticker, range_type="5M")

    if not chart_data or len(chart_data) < 50:
        return {"error": "Insufficient market data for analysis."}

    # 3. Define Targets
    timeframes = ["15M", "1H", "4H", "1D"]
    tasks = []

    # Helper function to process one timeframe
    async def process_timeframe(tf):
        try:
            # A. Resample (Math)
            # If tf is 5M, use original. Else resample.
            data = chart_data if tf == "5M" else technical_service.resample_chart_data(chart_data, tf)
            
            # B. Calculate Technicals (Math)
            df = pd.DataFrame(data)
            techs = technical_service.calculate_technical_indicators(df)
            pivots = technical_service.calculate_pivot_points(df)
            mas = technical_service.calculate_moving_averages(df)
            
            # C. Generate AI Insight
            analysis = await asyncio.to_thread(
                gemini_service.generate_timeframe_analysis, 
                symbol, tf, techs, pivots, mas
            )
            return tf.lower(), analysis # Return key like "1h"
        except:
            return tf.lower(), "Analysis unavailable."

    # 4. Execute Parallel Processing
    # We run 5 AI Models simultaneously. This takes ~3 seconds total instead of 15s.
    results = await asyncio.gather(
        process_timeframe("5M"),
        process_timeframe("15M"),
        process_timeframe("1H"),
        process_timeframe("4H"),
        process_timeframe("1D")
    )

    # 5. Construct Final Response
    response_map = {k: v for k, v in results}
    
    # Cache the heavy result
    await redis_service.redis_client.set_cache(cache_key, response_map, 300) # 5 min cache
    
    return response_map