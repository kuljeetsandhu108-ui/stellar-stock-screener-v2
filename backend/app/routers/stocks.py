import asyncio
import math
import pandas as pd
import json
from fastapi import APIRouter, HTTPException, Query, Body
from ..services import fmp_service, eodhd_service, news_service, gemini_service, fundamental_service, technical_service, sentiment_service, redis_service, yahoo_service
from pydantic import BaseModel
from typing import List, Dict, Any

router = APIRouter()

# ==========================================
# 1. DATA MODELS
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
}

# ==========================================
# 2. ENDPOINTS
# ==========================================

@router.get("/search")
async def search_stock_ticker(query: str = Query(..., min_length=2)):
    cache_key = f"search_{query.lower().strip()}"
    cached = redis_service.get_cache(cache_key)
    if cached: return cached

    results = fmp_service.search_ticker(query)
    if results: 
        res = {"symbol": results[0]['symbol']}
        redis_service.set_cache(cache_key, res, 86400)
        return res

    ticker = gemini_service.get_ticker_from_query(query)
    if ticker not in ["NOT_FOUND", "ERROR"]:
        res = {"symbol": ticker}
        redis_service.set_cache(cache_key, res, 86400)
        return res
    
    raise HTTPException(status_code=404, detail=f"Could not find a ticker for '{query}'")

@router.post("/{symbol}/swot")
async def get_swot_analysis(symbol: str, request_data: SwotRequest = Body(...)):
    cache_key = f"swot_{symbol}"
    cached = redis_service.get_cache(cache_key)
    if cached: return cached

    news_articles = await asyncio.to_thread(news_service.get_company_news, request_data.companyName)
    news_headlines = [a.get('title', '') for a in news_articles[:10]]
    
    swot_analysis = await asyncio.to_thread(
        gemini_service.generate_swot_analysis,
        request_data.companyName, request_data.description, news_headlines
    )
    res = {"swot_analysis": swot_analysis}
    redis_service.set_cache(cache_key, res, 3600)
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
    res = {"assessment": analysis}; redis_service.set_cache(cache_key, res, 86400); return res

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

@router.post("/{symbol}/timeframe-analysis")
async def get_timeframe_analysis(symbol: str, request_data: TimeframeRequest = Body(...)):
    cache_key = f"tf_ai_{symbol}_{request_data.timeframe}"
    cached = redis_service.get_cache(cache_key)
    if cached: return cached

    chart_list = await asyncio.to_thread(eodhd_service.get_historical_data, symbol, range_type=request_data.timeframe)
    if not chart_list: return {"analysis": "Market data unavailable."}

    df = pd.DataFrame(chart_list)
    technicals = technical_service.calculate_technical_indicators(df)
    pivots = technical_service.calculate_pivot_points(df)
    mas = technical_service.calculate_moving_averages(df)
    
    analysis = await asyncio.to_thread(gemini_service.generate_timeframe_analysis, symbol, request_data.timeframe, technicals, pivots, mas)
    res = {"analysis": analysis}; redis_service.set_cache(cache_key, res, 30); return res

@router.post("/{symbol}/technicals-data")
async def get_technicals_data(symbol: str, request_data: TimeframeRequest = Body(...)):
    chart_list = await asyncio.to_thread(eodhd_service.get_historical_data, symbol, range_type=request_data.timeframe)
    if not chart_list: return {"error": "No data available"}
    df = pd.DataFrame(chart_list)
    return {
        "technicalIndicators": technical_service.calculate_technical_indicators(df),
        "pivotPoints": technical_service.calculate_pivot_points(df),
        "movingAverages": technical_service.calculate_moving_averages(df)
    }

# ==========================================
# 3. MASTER ENDPOINTS
# ==========================================

@router.get("/{symbol}/peers")
async def get_peers_comparison(symbol: str):
    """
    Robust Peer Comparison.
    Flow: Check Cache -> Try FMP -> Fallback to Gemini AI -> Fetch Data from EODHD.
    """
    cache_key = f"peers_v2_{symbol}"
    cached = redis_service.get_cache(cache_key)
    if cached: return cached

    # 1. Identify Sector/Industry for AI Fallback
    # We fetch basic profile first to help the AI if needed
    base_profile = await asyncio.to_thread(eodhd_service.get_company_fundamentals, symbol)
    general = base_profile.get('General', {})
    
    # 2. Get Peer List (Try FMP First)
    peers = await asyncio.to_thread(fmp_service.get_stock_peers, symbol)
    
    # 3. AI Fallback: If FMP fails, ask Gemini
    if not peers:
        # Construct context for AI
        name = general.get('Name', symbol)
        sector = general.get('Sector', '')
        industry = general.get('Industry', '')
        country = "India" if ".NS" in symbol or ".BO" in symbol else "US"
        
        # Ask Gemini
        peers = await asyncio.to_thread(
            gemini_service.find_peer_tickers_by_industry, 
            name, sector, industry, country
        )

    if not peers: return [] # Give up if both fail

    # 4. Normalize Suffixes (Critical for EODHD)
    # If the main symbol is RELIANCE.NS, peers must also have .NS
    if "." in symbol:
        suffix = "." + symbol.split(".")[-1]
        corrected_peers = []
        for p in peers:
            p = p.strip().upper()
            # If peer has no suffix, add one. If it has a different one, keep it.
            if "." not in p:
                p = p + suffix
            corrected_peers.append(p)
        peers = corrected_peers

    # Limit to top 4 peers + original logic not needed as we map individually
    target_peers = peers[:4] 
    
    # 5. Parallel Data Fetch using EODHD (Reliable)
    async def fetch_peer_data(ticker):
        try:
            # Fetch fundamentals
            fund = await asyncio.to_thread(eodhd_service.get_company_fundamentals, ticker)
            if not fund: return None
            
            # Parse using our existing EODHD helper
            metrics = eodhd_service.parse_metrics_from_fundamentals(fund)
            
            # Add symbol for the frontend table
            metrics['symbol'] = ticker
            return metrics
        except: return None

    # Run all fetches at once
    tasks = [fetch_peer_data(p) for p in target_peers]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Filter out failures
    final_data = [r for r in results if r and not isinstance(r, Exception)]
    
    # Add the main symbol to the comparison for context
    main_metrics = eodhd_service.parse_metrics_from_fundamentals(base_profile)
    main_metrics['symbol'] = symbol
    final_data.insert(0, main_metrics)

    redis_service.set_cache(cache_key, final_data, 86400)
    return final_data

@router.get("/{symbol}/chart")
async def get_stock_chart(symbol: str, range: str = "1D"):
    cache_key = f"chart_{symbol}_{range}"
    cached = redis_service.get_cache(cache_key)
    if cached: return cached

    data = await asyncio.to_thread(eodhd_service.get_historical_data, symbol, range_type=range)
    if data: 
        ttl = 60 if range in ["1D", "5M", "15M"] else 3600
        redis_service.set_cache(cache_key, data, ttl)
    return data or []

@router.get("/{symbol}/all")
async def get_all_stock_data(symbol: str):
    cache_key = f"all_data_v3_{symbol}"
    cached = redis_service.get_cache(cache_key)
    if cached: return cached

    tasks = {
        "eod_fund": asyncio.to_thread(eodhd_service.get_company_fundamentals, symbol),
        "eod_live": asyncio.to_thread(eodhd_service.get_live_price, symbol),
        "fmp_prof": asyncio.to_thread(fmp_service.get_company_profile, symbol),
        "fmp_rating": asyncio.to_thread(fmp_service.get_analyst_ratings, symbol),
        "fmp_target": asyncio.to_thread(fmp_service.get_price_target_consensus, symbol),
        "news": asyncio.to_thread(news_service.get_company_news, symbol),
        "shareholding": asyncio.to_thread(fmp_service.get_shareholding_data, symbol),
        "chart": asyncio.to_thread(eodhd_service.get_historical_data, symbol, "1D")
    }

    try:
        results = await asyncio.gather(*tasks.values(), return_exceptions=True)
        raw = dict(zip(tasks.keys(), results))
    except: raw = {}

    def safe(k, d=None):
        val = raw.get(k)
        if isinstance(val, Exception) or val is None: return d
        return val

    final_data = {}
    
    # 1. Profile
    eod_fund = safe('eod_fund', {})
    eod_p = eodhd_service.parse_profile_from_fundamentals(eod_fund, symbol)
    fmp_p = safe('fmp_prof', {}) or {}
    
    final_data['profile'] = {
        **eod_p,
        "description": fmp_p.get("description") or eod_p.get("description"),
        "image": fmp_p.get("image") or eod_p.get("image"),
        "tradingview_symbol": "NSE:" + symbol.replace(".NS", "") if ".NS" in symbol else symbol
    }
    
    final_data['quote'] = safe('eod_live', {})
    final_data['key_metrics'] = eodhd_service.parse_metrics_from_fundamentals(eod_fund)

    # 2. Financials
    final_data['annual_revenue_and_profit'] = eodhd_service.parse_financials(eod_fund, 'Financials::Income_Statement', 'yearly')
    final_data['annual_balance_sheets'] = eodhd_service.parse_financials(eod_fund, 'Financials::Balance_Sheet', 'yearly')
    final_data['annual_cash_flow_statements'] = eodhd_service.parse_financials(eod_fund, 'Financials::Cash_Flow', 'yearly')
    
    final_data['quarterly_income_statements'] = eodhd_service.parse_financials(eod_fund, 'Financials::Income_Statement', 'quarterly')
    final_data['quarterly_balance_sheets'] = eodhd_service.parse_financials(eod_fund, 'Financials::Balance_Sheet', 'quarterly')
    final_data['quarterly_cash_flow_statements'] = eodhd_service.parse_financials(eod_fund, 'Financials::Cash_Flow', 'quarterly')

    # 3. Technicals
    chart_data = safe('chart', [])
    tech_inds, mas, pivots, darvas = {}, {}, {}, {}
    
    if chart_data and len(chart_data) > 0:
        try:
            df = pd.DataFrame(chart_data)
            tech_inds = technical_service.calculate_technical_indicators(df)
            mas = technical_service.calculate_moving_averages(df)
            pivots = technical_service.calculate_pivot_points(df)
            if final_data['quote']:
                darvas = technical_service.calculate_darvas_box(df, final_data['quote'], final_data['profile'].get('currency', 'USD'))
        except: pass

    final_data['technical_indicators'] = tech_inds
    final_data['moving_averages'] = mas
    final_data['pivot_points'] = pivots
    final_data['darvas_scan'] = darvas

    # 4. Scans & Sentiment
    # ... inside get_all_stock_data ...

    # 4. Scans & Sentiment
    piotroski = fundamental_service.calculate_piotroski_f_score(
        final_data['annual_revenue_and_profit'], 
        final_data['annual_balance_sheets'], 
        final_data['annual_cash_flow_statements']
    )
    
    # UPDATED CALL: Passing Cash Flow Data
    graham = fundamental_service.calculate_graham_scan(
        final_data['profile'], 
        final_data['key_metrics'], 
        final_data['annual_revenue_and_profit'],
        final_data['annual_cash_flow_statements'] # <--- Added this
    )
    
    final_data['piotroski_f_score'] = piotroski
    final_data['graham_scan'] = graham
    
    final_data['overall_sentiment'] = sentiment_service.calculate_overall_sentiment(
        piotroski_score=piotroski.get('score'),
        key_metrics=final_data['key_metrics'],
        technicals=tech_inds,
        analyst_ratings=safe('fmp_rating', [])
    )

    # 5. EXTRAS & INTELLIGENT FORECAST
    final_data['news'] = safe('news', [])
    
    # Try EODHD Analyst Data (Parsed here or in service)
    # Using the new helper we defined
    eod_ratings, eod_targets = eodhd_service.parse_analyst_data(eod_fund) if hasattr(eodhd_service, 'parse_analyst_data') else ([], {})
    
    fmp_ratings = safe('fmp_rating', [])
    fmp_targets = safe('fmp_target', {})
    
    # Logic: EODHD > FMP > Algorithmic Fallback
    if eod_ratings and (eod_ratings[0].get('ratingBuy') or eod_ratings[0].get('ratingHold')):
        final_data['analyst_ratings'] = eod_ratings
        final_data['price_target_consensus'] = eod_targets
    elif fmp_ratings and (fmp_ratings[0].get('ratingBuy') or fmp_ratings[0].get('ratingHold')):
        final_data['analyst_ratings'] = fmp_ratings
        final_data['price_target_consensus'] = fmp_targets
    else:
        # --- ALGORITHMIC FORECAST (The Fix) ---
        price = final_data['quote'].get('price') or 0
        rsi = tech_inds.get('rsi', 50)
        
        # Synthetic Rating
        syn_rating = {
            "ratingStrongBuy": 1 if rsi < 30 else 0,
            "ratingBuy": 1 if 30 <= rsi < 45 else 0,
            "ratingHold": 1 if 45 <= rsi <= 55 else 0,
            "ratingSell": 1 if 55 < rsi <= 70 else 0,
            "ratingStrongSell": 1 if rsi > 70 else 0
        }
        # Synthetic Target (Using Pivots)
        pivots_classic = pivots.get('classic', {})
        if pivots_classic and price > 0:
            target = pivots_classic.get('r1') if rsi < 50 else pivots_classic.get('s1')
        else:
            target = price # Neutral
            
        final_data['analyst_ratings'] = [syn_rating]
        final_data['price_target_consensus'] = {
            "targetHigh": price * 1.1, "targetLow": price * 0.9, "targetConsensus": target
        }

    # --- Shareholding Logic (Fixed) ---
    # 1. Try parsing EODHD Fundamentals first (Most accurate for % breakdown)
    share_breakdown = eodhd_service.parse_shareholding_breakdown(eod_fund)
    
    # 2. Get Holders List (Used to validate if data exists)
    shares = eodhd_service.parse_holders(eod_fund)
    
    # 3. Fallback: If EODHD has 0% insiders/institutions, try FMP
    if share_breakdown.get('promoter') == 0 and share_breakdown.get('fii') == 0:
        fmp_shares = safe('shareholding', [])
        if fmp_shares:
            shares = fmp_shares
            total = sum(h.get('shares', 0) for h in fmp_shares)
            # Rough Estimate for FMP
            share_breakdown = {"promoter": 0, "fii": total * 0.6, "dii": total * 0.4, "public": 0}

    final_data['shareholding'] = shares
    final_data['shareholding_breakdown'] = share_breakdown

    # 6. Final Clean
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

    def clean_json(obj):
        if isinstance(obj, float): return None if math.isnan(obj) or math.isinf(obj) else obj
        if isinstance(obj, dict): return {k: clean_json(v) for k, v in obj.items()}
        if isinstance(obj, list): return [clean_json(v) for v in obj]
        return obj

    final = clean_json(final_data)
    redis_service.set_cache(cache_key, final, 300)
    return final