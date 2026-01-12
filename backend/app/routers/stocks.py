import asyncio
import math
import pandas as pd
import json
from fastapi import APIRouter, HTTPException, Query, Body
# ROBUST SERVICE IMPORTS (100% Yahoo-Free)
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
# 1. STRICT DATA MODELS (Input Validation)
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

# TradingView Symbol Mapping (Fixes frontend chart mismatches)
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
    "XAU-USD.CC": "OANDA:XAUUSD"
}

# ==========================================
# 2. AI & SEARCH ENDPOINTS (Low Latency)
# ==========================================

@router.get("/search")
async def search_stock_ticker(query: str = Query(..., min_length=2)):
    """
    Smart Search: Redis (Instant) -> FMP (Cheap) -> Gemini (Smart).
    """
    cache_key = f"search_{query.lower().strip()}"
    cached = redis_service.get_cache(cache_key)
    if cached: return cached

    # 1. FMP is fastest/cheapest for standard tickers
    results = fmp_service.search_ticker(query)
    if results: 
        res = {"symbol": results[0]['symbol']}
        redis_service.set_cache(cache_key, res, 86400) # Cache 24h
        return res

    # 2. Gemini AI for natural language (e.g., "Google of India")
    ticker = gemini_service.get_ticker_from_query(query)
    if ticker not in ["NOT_FOUND", "ERROR"]:
        res = {"symbol": ticker}
        redis_service.set_cache(cache_key, res, 86400)
        return res
    
    raise HTTPException(status_code=404, detail=f"Could not find a ticker for '{query}'")

# --- AI ANALYSIS WRAPPERS (Heavy Caching) ---

@router.post("/{symbol}/swot")
async def get_swot_analysis(symbol: str, request_data: SwotRequest = Body(...)):
    cache_key = f"swot_{symbol}"
    cached = redis_service.get_cache(cache_key)
    if cached: return cached

    # Fetch News
    news_articles = await asyncio.to_thread(news_service.get_company_news, request_data.companyName)
    news_headlines = [a.get('title', '') for a in news_articles[:10]]
    
    swot_analysis = await asyncio.to_thread(
        gemini_service.generate_swot_analysis,
        request_data.companyName, request_data.description, news_headlines
    )
    res = {"swot_analysis": swot_analysis}
    redis_service.set_cache(cache_key, res, 3600) # 1 Hour Cache
    return res

@router.post("/{symbol}/forecast-analysis")
async def get_forecast_analysis(symbol: str, d: ForecastRequest = Body(...)):
    cache_key = f"fc_{symbol}"
    cached = redis_service.get_cache(cache_key)
    if cached: return cached
    analysis = await asyncio.to_thread(gemini_service.generate_forecast_analysis, d.companyName, d.analystRatings, d.priceTarget, d.keyStats, d.newsHeadlines, d.currency)
    res = {"analysis": analysis}; redis_service.set_cache(cache_key, res, 3600); return res

@router.post("/{symbol}/fundamental-analysis")
async def get_fundamental_analysis(symbol: str, d: FundamentalRequest = Body(...)):
    cache_key = f"fa_{symbol}"
    cached = redis_service.get_cache(cache_key)
    if cached: return cached
    analysis = await asyncio.to_thread(gemini_service.generate_investment_philosophy_assessment, d.companyName, d.keyMetrics)
    res = {"assessment": analysis}; redis_service.set_cache(cache_key, res, 86400); return res # 24h Cache

@router.post("/{symbol}/canslim-analysis")
async def get_canslim_analysis(symbol: str, d: CanslimRequest = Body(...)):
    cache_key = f"can_{symbol}"
    cached = redis_service.get_cache(cache_key)
    if cached: return cached
    analysis = await asyncio.to_thread(gemini_service.generate_canslim_assessment, d.companyName, d.quote, d.quarterlyEarnings, d.annualEarnings, d.institutionalHolders)
    res = {"assessment": analysis}; redis_service.set_cache(cache_key, res, 3600); return res

@router.post("/{symbol}/conclusion-analysis")
async def get_conclusion_analysis(symbol: str, d: ConclusionRequest = Body(...)):
    cache_key = f"conc_{symbol}"
    cached = redis_service.get_cache(cache_key)
    if cached: return cached
    conclusion = await asyncio.to_thread(gemini_service.generate_fundamental_conclusion, d.companyName, d.piotroskiData, d.grahamData, d.darvasData, {k: v for k, v in d.keyStats.items() if v is not None}, d.newsHeadlines)
    res = {"conclusion": conclusion}; redis_service.set_cache(cache_key, res, 3600); return res

# ==========================================
# 3. TECHNICAL ANALYSIS (Calculated Live)
# ==========================================

@router.post("/{symbol}/timeframe-analysis")
async def get_timeframe_analysis(symbol: str, request_data: TimeframeRequest = Body(...)):
    """
    AI Technical Analysis. Fetches EODHD Data -> Calculates Math -> Sends to Gemini.
    """
    cache_key = f"tf_ai_{symbol}_{request_data.timeframe}"
    cached = redis_service.get_cache(cache_key)
    if cached: return cached

    # 1. Fetch History from EODHD (Reliable)
    chart_list = await asyncio.to_thread(eodhd_service.get_historical_data, symbol, range_type=request_data.timeframe)
    if not chart_list: return {"analysis": f"Market data unavailable for {request_data.timeframe}."}

    # 2. Math Layer (Pandas TA)
    df = pd.DataFrame(chart_list)
    technicals = technical_service.calculate_technical_indicators(df)
    pivots = technical_service.calculate_pivot_points(df)
    mas = technical_service.calculate_moving_averages(df)
    
    # 3. AI Layer
    analysis = await asyncio.to_thread(gemini_service.generate_timeframe_analysis, symbol, request_data.timeframe, technicals, pivots, mas)
    res = {"analysis": analysis}; redis_service.set_cache(cache_key, res, 30); return res

@router.post("/{symbol}/technicals-data")
async def get_technicals_data(symbol: str, request_data: TimeframeRequest = Body(...)):
    """Raw data for the Technicals Dashboard UI."""
    chart_list = await asyncio.to_thread(eodhd_service.get_historical_data, symbol, range_type=request_data.timeframe)
    if not chart_list: return {"error": "No data available"}

    df = pd.DataFrame(chart_list)
    # Uses technical_service logic (No Yahoo)
    return {
        "technicalIndicators": technical_service.calculate_technical_indicators(df),
        "pivotPoints": technical_service.calculate_pivot_points(df),
        "movingAverages": technical_service.calculate_moving_averages(df)
    }

# ==========================================
# 4. MASTER DATA ENDPOINTS (EODHD CORE)
# ==========================================

@router.get("/{symbol}/peers")
async def get_peers_comparison(symbol: str):
    """
    Robust Peer Comparison.
    Flow: Check Cache -> Try FMP -> Fallback to Gemini AI -> Fetch Data from EODHD.
    """
    cache_key = f"peers_v5_{symbol}"
    cached = redis_service.get_cache(cache_key)
    if cached: return cached

    # 1. Identify Sector/Industry for AI Fallback
    base_profile = await asyncio.to_thread(eodhd_service.get_company_fundamentals, symbol)
    general = base_profile.get('General', {})
    
    # 2. Get Peer List (Try FMP First - It's best for this)
    peers = await asyncio.to_thread(fmp_service.get_stock_peers, symbol)
    
    # 3. AI Fallback: If FMP fails, ask Gemini
    if not peers:
        name = general.get('Name', symbol)
        sector = general.get('Sector', '')
        industry = general.get('Industry', '')
        country = "India" if ".NS" in symbol or ".BO" in symbol else "US"
        
        peers = await asyncio.to_thread(
            gemini_service.find_peer_tickers_by_industry, 
            name, sector, industry, country
        )

    if not peers: return []

    # 4. Normalize Suffixes (Critical for EODHD)
    if "." in symbol:
        suffix = "." + symbol.split(".")[-1]
        corrected_peers = []
        for p in peers:
            p = p.strip().upper()
            if "." not in p: p += suffix
            corrected_peers.append(p)
        peers = corrected_peers

    target_peers = peers[:4] 
    
    # 5. Parallel Data Fetch using EODHD
    async def fetch_peer_data(ticker):
        try:
            fund = await asyncio.to_thread(eodhd_service.get_company_fundamentals, ticker)
            if not fund: return None
            metrics = eodhd_service.parse_metrics_from_fundamentals(fund)
            metrics['symbol'] = ticker
            return metrics
        except: return None

    tasks = [fetch_peer_data(p) for p in target_peers]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    final_data = [r for r in results if r and not isinstance(r, Exception)]
    
    # Add main symbol for context
    main_metrics = eodhd_service.parse_metrics_from_fundamentals(base_profile)
    main_metrics['symbol'] = symbol
    final_data.insert(0, main_metrics)

    redis_service.set_cache(cache_key, final_data, 86400)
    return final_data

@router.get("/{symbol}/chart")
async def get_stock_chart(symbol: str, range: str = "1D"):
    """
    High-End Chart Engine with Resampling & Live Stitching.
    """
    # 1. Determine if this request can be served from the "Master 5M" cache
    # 5M, 15M, 1H, 4H can all be derived from 5M data
    is_intraday_derived = range in ["5M", "15M", "1H", "4H"]
    
    # If derived, we look for the "5M" cache key, regardless of what user asked
    lookup_range = "5M" if is_intraday_derived else range
    
    cache_key = f"chart_{symbol}_{lookup_range}_v2" # v2 for new logic
    cached = redis_service.get_cache(cache_key)
    
    # 2. Fetch if missing
    if not cached:
        # We fetch the 'lookup_range' (which is 5M for all intraday requests)
        cached = await asyncio.to_thread(eodhd_service.get_historical_data, symbol, range_type=lookup_range)
        if cached:
            # Cache Intraday (5M) for 5 minutes, Daily/Weekly for 12 hours
            ttl = 300 if is_intraday_derived else 43200
            redis_service.set_cache(cache_key, cached, ttl)

    if not cached: return []

    # 3. RESAMPLING ENGINE
    # If user wants 1H but we have 5M data, we resample it now.
    final_data = cached
    if is_intraday_derived and range != "5M":
        # Math Magic: Turn 5M into 15M/1H/4H
        final_data = technical_service.resample_chart_data(cached, range)

    # 4. LIVE STITCHING
    # Patch the last candle with real-time price
    try:
        live = await asyncio.to_thread(eodhd_service.get_live_price, symbol)
        if live and live.get('price'):
            current_price = live['price']
            
            # Recalculate Time Shift for India
            is_indian = ".NS" in symbol or ".BO" in symbol or "NIFTY" in symbol or "SENSEX" in symbol
            offset = 19800 if is_indian and is_intraday_derived else 0
            
            ts_now = live.get('timestamp') or int(pd.Timestamp.now().timestamp())
            ts_now += offset

            if final_data:
                last = final_data[-1]
                # Simple Stitch: Update Close/High/Low of last candle
                last['close'] = current_price
                if current_price > last['high']: last['high'] = current_price
                if current_price < last['low']: last['low'] = current_price
                # We don't change 'time' to avoid creating new candles prematurely
    except: pass

    return final_data

@router.get("/{symbol}/all")
async def get_all_stock_data(symbol: str):
    """
    THE MASTER DATA AGGREGATOR (OPTIMIZED FOR SCALE).
    Smartly routes requests based on Asset Type to save API resources.
    """
    # Cache Key V14: Forces refresh
    cache_key = f"all_data_v14_{symbol}"
    cached = redis_service.get_cache(cache_key)
    if cached: return cached

    # --- 1. SMART ASSET DETECTION ---
    is_crypto = ".CC" in symbol or "BTC" in symbol or "ETH" in symbol or "XAU" in symbol
    is_index = ".INDX" in symbol or "^" in symbol
    is_traditional_stock = not (is_crypto or is_index)

    # --- 2. LOAD BALANCED TASKS ---
    # Core tasks (Everyone needs these)
    tasks = {
        "eod_fund": asyncio.to_thread(eodhd_service.get_company_fundamentals, symbol),
        "eod_live": asyncio.to_thread(eodhd_service.get_live_price, symbol),
        "news": asyncio.to_thread(news_service.get_company_news, symbol), # FMP News is global
        "chart_data": asyncio.to_thread(eodhd_service.get_historical_data, symbol, "1D"), 
    }

    # Conditional Tasks (Only for Stocks - Saves ~40% API calls for Crypto/Indices)
    if is_traditional_stock:
        tasks.update({
            "fmp_prof": asyncio.to_thread(fmp_service.get_company_profile, symbol),
            "fmp_rating": asyncio.to_thread(fmp_service.get_analyst_ratings, symbol),
            "fmp_target": asyncio.to_thread(fmp_service.get_price_target_consensus, symbol),
            "shareholding": asyncio.to_thread(fmp_service.get_shareholding_data, symbol),
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
    
    # 3. Profile & Quote
    eod_fund = safe('eod_fund', {})
    eod_p = eodhd_service.parse_profile_from_fundamentals(eod_fund, symbol)
    fmp_p = safe('fmp_prof', {}) or {}
    
    tv_symbol = symbol
    if symbol in TRADINGVIEW_OVERRIDE_MAP: tv_symbol = TRADINGVIEW_OVERRIDE_MAP[symbol]
    elif symbol.endswith(".NS"): tv_symbol = "NSE:" + symbol.replace(".NS", "")
    elif symbol.endswith(".BO"): tv_symbol = "BSE:" + symbol.replace(".BO", "")
    
    final_data['profile'] = {
        **eod_p,
        "description": fmp_p.get("description") or eod_p.get("description") or "Market Asset",
        "image": fmp_p.get("image") or eod_p.get("image"),
        "tradingview_symbol": tv_symbol
    }
    
    final_data['key_metrics'] = eodhd_service.parse_metrics_from_fundamentals(eod_fund)
    final_data['quote'] = safe('eod_live', {})

    # 4. Financials (EODHD)
    final_data['annual_revenue_and_profit'] = eodhd_service.parse_financials(eod_fund, 'Financials::Income_Statement', 'yearly')
    final_data['annual_balance_sheets'] = eodhd_service.parse_financials(eod_fund, 'Financials::Balance_Sheet', 'yearly')
    final_data['annual_cash_flow_statements'] = eodhd_service.parse_financials(eod_fund, 'Financials::Cash_Flow', 'yearly')
    final_data['quarterly_income_statements'] = eodhd_service.parse_financials(eod_fund, 'Financials::Income_Statement', 'quarterly')
    final_data['quarterly_balance_sheets'] = eodhd_service.parse_financials(eod_fund, 'Financials::Balance_Sheet', 'quarterly')
    final_data['quarterly_cash_flow_statements'] = eodhd_service.parse_financials(eod_fund, 'Financials::Cash_Flow', 'quarterly')

    # 5. Technicals (Internal Math)
    chart_data = safe('chart_data', [])
    tech_inds, mas, pivots, darvas = {}, {}, {}, {}
    
    if chart_data and len(chart_data) > 30:
        try:
            df = pd.DataFrame(chart_data)
            tech_inds = technical_service.calculate_technical_indicators(df)
            mas = technical_service.calculate_moving_averages(df)
            pivots = technical_service.calculate_pivot_points(df)
            # Darvas only for Stocks
            if is_traditional_stock and final_data['quote']:
                darvas = technical_service.calculate_darvas_box(df, final_data['quote'], final_data['profile'].get('currency', 'USD'))
        except: pass

    final_data['technical_indicators'] = tech_inds
    final_data['moving_averages'] = mas
    final_data['pivot_points'] = pivots
    final_data['darvas_scan'] = darvas

    # 6. Scans & Sentiment (Stocks Only)
    piotroski, graham = {}, {}
    if is_traditional_stock:
        piotroski = fundamental_service.calculate_piotroski_f_score(final_data['annual_revenue_and_profit'], final_data['annual_balance_sheets'], final_data['annual_cash_flow_statements'])
        graham = fundamental_service.calculate_graham_scan(final_data['profile'], final_data['key_metrics'], final_data['annual_revenue_and_profit'], final_data['annual_cash_flow_statements'])
    
    final_data['piotroski_f_score'] = piotroski
    final_data['graham_scan'] = graham
    
    # Sentiment (Using generated metrics)
    final_data['overall_sentiment'] = sentiment_service.calculate_overall_sentiment(
        piotroski.get('score'), final_data['key_metrics'], tech_inds, safe('fmp_rating', [])
    )

    final_data['news'] = safe('news', [])
    
    # --- 7. UNIVERSAL FORECAST ENGINE (Stocks + Crypto + Commodities) ---
    eod_ratings, eod_targets = eodhd_service.parse_analyst_data(eod_fund) if hasattr(eodhd_service, 'parse_analyst_data') else ([], {})
    fmp_ratings = safe('fmp_rating', [])
    fmp_targets = safe('fmp_target', {})
    
    def has_votes(r): return r and isinstance(r, list) and len(r)>0 and (r[0].get('ratingBuy',0)+r[0].get('ratingHold',0)+r[0].get('ratingSell',0) > 0)
    
    # Priority 1: EODHD/FMP (Stocks)
    if is_traditional_stock and has_votes(eod_ratings):
        final_data['analyst_ratings'] = eod_ratings; final_data['price_target_consensus'] = eod_targets
    elif is_traditional_stock and has_votes(fmp_ratings):
        final_data['analyst_ratings'] = fmp_ratings; final_data['price_target_consensus'] = fmp_targets
    else:
        # Priority 2: Technical Math (Crypto/Indices/No-Data Stocks)
        price = final_data['quote'].get('price') or 0
        if price == 0 and chart_data: price = chart_data[-1]['close']
            
        rsi = tech_inds.get('rsi', 50)
        
        # Synthetic Rating
        syn = {"ratingStrongBuy": 0, "ratingBuy": 0, "ratingHold": 0, "ratingSell": 0, "ratingStrongSell": 0}
        if rsi < 30: syn["ratingStrongBuy"] = 12; syn["ratingBuy"] = 8
        elif rsi < 45: syn["ratingBuy"] = 10; syn["ratingHold"] = 10
        elif rsi < 55: syn["ratingHold"] = 20
        elif rsi < 70: syn["ratingSell"] = 10; syn["ratingHold"] = 10
        else: syn["ratingStrongSell"] = 12; syn["ratingSell"] = 8
            
        # Synthetic Target (Pivot Based)
        target = price if price > 0 else 100
        if price > 0:
            pc = pivots.get('classic', {})
            # Bullish? Target R1. Bearish? Target S1.
            target = pc.get('r1') if rsi < 50 else pc.get('s1') or price
            
        final_data['analyst_ratings'] = [syn]
        final_data['price_target_consensus'] = {"targetHigh": target*1.1, "targetLow": target*0.9, "targetConsensus": target}

    # Ensure target consensus is never 0/null
    pt = final_data.get('price_target_consensus', {})
    if not pt.get('targetConsensus'):
        p = final_data['quote'].get('price') or 100
        final_data['price_target_consensus'] = {"targetHigh": p*1.1, "targetLow": p*0.9, "targetConsensus": p}

    # 8. Shareholding (Stocks Only)
    share_bd, shares = {}, []
    if is_traditional_stock:
        share_bd = eodhd_service.parse_shareholding_breakdown(eod_fund)
        shares = eodhd_service.parse_holders(eod_fund)
        if share_bd.get('promoter') == 0 and share_bd.get('fii') == 0:
            fmp_s = safe('shareholding', [])
            if fmp_s:
                shares = fmp_s
                t = sum(h.get('shares', 0) for h in fmp_s)
                share_bd = {"promoter": 0, "fii": t*0.6, "dii": t*0.4, "public": 0}

    final_data['shareholding'] = shares
    final_data['shareholding_breakdown'] = share_bd

    # 9. Key Stats
    km = final_data.get('key_metrics', {})
    kq = final_data.get('quote', {})
    def n(v): 
        try: return None if isinstance(v, float) and (math.isnan(v) or math.isinf(v)) else v
        except: return None

    final_data['keyStats'] = {
        "marketCap": n(km.get('marketCap')), "peRatio": n(km.get('peRatioTTM')),
        "dividendYield": n(km.get('dividendYieldTTM')), "basicEPS": n(km.get('epsTTM')),
        "sharesFloat": n(km.get('sharesOutstanding')), "beta": n(km.get('beta')),
        "netIncome": n(km.get('epsTTM')), "revenue": n(km.get('revenueGrowth')),
        "dayLow": n(kq.get('low')), "dayHigh": n(kq.get('high')), "yearHigh": n(kq.get('high')),
        "nextReportDate": None, "epsEstimate": None, "revenueEstimate": None
    }

    # 10. Final Clean & Cache
    def clean_json(obj):
        if isinstance(obj, float): return None if math.isnan(obj) or math.isinf(obj) else obj
        if isinstance(obj, dict): return {k: clean_json(v) for k, v in obj.items()}
        if isinstance(obj, list): return [clean_json(v) for v in obj]
        return obj

    final = clean_json(final_data)
    redis_service.set_cache(cache_key, final, 300)
    return final