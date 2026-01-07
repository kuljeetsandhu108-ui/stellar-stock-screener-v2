import asyncio
import math
import time
from datetime import datetime, timedelta
import pytz 
from fastapi import APIRouter, HTTPException, Query, Body
# Import all services including the new Redis service
from ..services import fmp_service, yahoo_service, news_service, gemini_service, fundamental_service, technical_service, sentiment_service, redis_service
from pydantic import BaseModel
from typing import List, Dict, Any

# ==========================================
# 1. DATA MODELS (Strict Validation)
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
    currency: str = "USD" # Currency awareness

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

router = APIRouter()

# TradingView Symbol Mapping (Fixes chart mismatches for specific indices/stocks)
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
# 2. AI & UTILITY ENDPOINTS (With Caching)
# ==========================================

@router.get("/search")
async def search_stock_ticker(query: str = Query(..., min_length=2)):
    """
    AI-Powered Search with Redis Caching.
    """
    # 1. Check Cache
    cache_key = f"search_{query.lower().strip()}"
    cached = redis_service.get_cache(cache_key)
    if cached: return cached

    # 2. Ask AI
    ticker = gemini_service.get_ticker_from_query(query)
    
    # 3. Fallback to FMP Search if AI fails
    if ticker in ["NOT_FOUND", "ERROR"]:
        results = fmp_service.search_ticker(query)
        if results: 
            res = {"symbol": results[0]['symbol']}
            redis_service.set_cache(cache_key, res, 86400) # Cache for 24h
            return res
        raise HTTPException(status_code=404, detail=f"Could not find a ticker for '{query}'")
    
    # 4. Save to Cache
    res = {"symbol": ticker}
    redis_service.set_cache(cache_key, res, 86400)
    return res

@router.post("/{symbol}/swot")
async def get_swot_analysis(symbol: str, request_data: SwotRequest = Body(...)):
    cache_key = f"swot_{symbol}"
    cached = redis_service.get_cache(cache_key)
    if cached: return cached

    news_articles = await asyncio.to_thread(news_service.get_company_news, request_data.companyName)
    news_headlines = [article.get('title', '') for article in news_articles[:10]]
    
    swot_analysis = await asyncio.to_thread(
        gemini_service.generate_swot_analysis,
        request_data.companyName,
        request_data.description,
        news_headlines
    )
    
    res = {"swot_analysis": swot_analysis}
    redis_service.set_cache(cache_key, res, 3600) # 1 Hour
    return res

@router.post("/{symbol}/forecast-analysis")
async def get_forecast_analysis(symbol: str, request_data: ForecastRequest = Body(...)):
    cache_key = f"forecast_{symbol}"
    cached = redis_service.get_cache(cache_key)
    if cached: return cached

    analysis = await asyncio.to_thread(
        gemini_service.generate_forecast_analysis,
        request_data.companyName,
        request_data.analystRatings,
        request_data.priceTarget,
        request_data.keyStats,
        request_data.newsHeadlines,
        request_data.currency
    )
    res = {"analysis": analysis}
    redis_service.set_cache(cache_key, res, 3600)
    return res

@router.post("/{symbol}/fundamental-analysis")
async def get_fundamental_analysis(symbol: str, request_data: FundamentalRequest = Body(...)):
    cache_key = f"fund_ai_{symbol}"
    cached = redis_service.get_cache(cache_key)
    if cached: return cached

    assessment = await asyncio.to_thread(
        gemini_service.generate_investment_philosophy_assessment,
        request_data.companyName,
        request_data.keyMetrics
    )
    res = {"assessment": assessment}
    redis_service.set_cache(cache_key, res, 86400) # 24 Hours
    return res

@router.post("/{symbol}/canslim-analysis")
async def get_canslim_analysis(symbol: str, request_data: CanslimRequest = Body(...)):
    cache_key = f"canslim_{symbol}"
    cached = redis_service.get_cache(cache_key)
    if cached: return cached

    assessment = await asyncio.to_thread(
        gemini_service.generate_canslim_assessment,
        request_data.companyName,
        request_data.quote,
        request_data.quarterlyEarnings,
        request_data.annualEarnings,
        request_data.institutionalHolders
    )
    res = {"assessment": assessment}
    redis_service.set_cache(cache_key, res, 3600)
    return res

@router.post("/{symbol}/conclusion-analysis")
async def get_conclusion_analysis(symbol: str, request_data: ConclusionRequest = Body(...)):
    cache_key = f"conclusion_{symbol}"
    cached = redis_service.get_cache(cache_key)
    if cached: return cached

    conclusion = await asyncio.to_thread(
        gemini_service.generate_fundamental_conclusion,
        request_data.companyName,
        request_data.piotroskiData,
        request_data.grahamData,
        request_data.darvasData,
        {k: v for k, v in request_data.dict().get('keyStats', {}).items() if v is not None},
        request_data.newsHeadlines
    )
    res = {"conclusion": conclusion}
    redis_service.set_cache(cache_key, res, 3600)
    return res

@router.post("/{symbol}/timeframe-analysis")
async def get_timeframe_analysis(symbol: str, request_data: TimeframeRequest = Body(...)):
    """
    AI Technical Analysis on specific timeframe. 
    Short cache (30s) because price action moves fast.
    """
    cache_key = f"tf_ai_{symbol}_{request_data.timeframe}"
    cached = redis_service.get_cache(cache_key)
    if cached: return cached

    # 1. Fetch History (Yahoo is best for specific intervals like 15m)
    hist_df = await asyncio.to_thread(yahoo_service.get_historical_data, symbol, period="1mo", interval=request_data.timeframe)
    
    if hist_df is None or hist_df.empty:
        return {"analysis": f"Could not fetch market data for {request_data.timeframe} timeframe."}

    # 2. Calc Indicators
    technicals = await asyncio.to_thread(yahoo_service.calculate_technical_indicators, hist_df)
    pivots = technical_service.calculate_pivot_points(hist_df)
    mas = technical_service.calculate_moving_averages(hist_df)
    
    # 3. AI Analysis
    analysis = await asyncio.to_thread(
        gemini_service.generate_timeframe_analysis,
        symbol,
        request_data.timeframe,
        technicals,
        pivots,
        mas
    )
    
    res = {"analysis": analysis}
    redis_service.set_cache(cache_key, res, 30)
    return res

# --- NEW: RAW TECHNICAL DATA FOR UI ---
@router.post("/{symbol}/technicals-data")
async def get_technicals_data(symbol: str, request_data: TimeframeRequest = Body(...)):
    """Returns raw indicator values for UI dashboards."""
    hist_df = await asyncio.to_thread(yahoo_service.get_historical_data, symbol, period="1mo", interval=request_data.timeframe)
    if hist_df is None or hist_df.empty: return {"error": "No data available"}

    technicals = await asyncio.to_thread(yahoo_service.calculate_technical_indicators, hist_df)
    pivots = technical_service.calculate_pivot_points(hist_df)
    mas = technical_service.calculate_moving_averages(hist_df)
    
    return {"technicalIndicators": technicals, "pivotPoints": pivots, "movingAverages": mas}

# ==========================================
# 3. ROBUST DATA ENDPOINTS (Peers, Charts, Master)
# ==========================================

@router.get("/{symbol}/peers")
async def get_peers_comparison(symbol: str):
    cache_key = f"peers_{symbol}"
    cached = redis_service.get_cache(cache_key)
    if cached: return cached

    # 1. Try FMP Official Peers
    peer_tickers = await asyncio.to_thread(fmp_service.get_stock_peers, symbol)
    
    # 2. Fallback to AI
    if not peer_tickers:
        company_info = await asyncio.to_thread(yahoo_service.get_company_info, symbol)
        sector = company_info.get('sector')
        industry = company_info.get('industry')
        country = company_info.get('country')
        name = company_info.get('longName', symbol)
        
        if all([sector, industry, country]):
            peer_tickers = await asyncio.to_thread(gemini_service.find_peer_tickers_by_industry, name, sector, industry, country)

    if not peer_tickers: return []
    
    # 3. Suffix Intelligence (Fixes .NS issues)
    if "." in symbol:
        suffix = "." + symbol.split(".")[-1]
        corrected_peers = []
        for peer in peer_tickers:
            peer = peer.strip().upper()
            if "." not in peer:
                peer = peer + suffix
            corrected_peers.append(peer)
        peer_tickers = corrected_peers

    # Limit to 5
    all_symbols = [symbol] + peer_tickers[:5]
    
    # 4. Fetch Data (Bulk FMP -> Fallback Yahoo)
    fmp_peers_data = await asyncio.to_thread(fmp_service.get_peers_with_metrics, all_symbols)
    peers_map = {item['symbol']: item for item in fmp_peers_data}
    
    # Fallback to Yahoo for missing data
    tasks_to_run = []
    for peer_symbol in all_symbols:
        if peer_symbol not in peers_map or not peers_map[peer_symbol].get('peRatioTTM'):
            tasks_to_run.append((peer_symbol, asyncio.to_thread(yahoo_service.get_key_fundamentals, peer_symbol)))
            
    if tasks_to_run:
        fallback_results = await asyncio.gather(*[task for _, task in tasks_to_run], return_exceptions=True)
        for (peer_symbol, _), result in zip(tasks_to_run, fallback_results):
            if not isinstance(result, Exception) and result:
                if peer_symbol not in peers_map: peers_map[peer_symbol] = {"symbol": peer_symbol}
                peers_map[peer_symbol].update(result)
                
    res = list(peers_map.values())
    redis_service.set_cache(cache_key, res, 86400)
    return res


@router.get("/{symbol}/chart")
async def get_stock_chart(symbol: str, range: str = "1D"):
    """
    Zero-Lag Charting Engine.
    1. Checks Redis.
    2. Fetches History (FMP preferred).
    3. Stitches Live Quote (Yahoo).
    4. Updates Redis.
    """
    cache_key = f"chart_{symbol}_{range}"
    cached_data = redis_service.get_cache(cache_key)
    if cached_data: return cached_data

    # 1. Fetch History
    is_international = "." in symbol
    data = []
    
    # Weekly/Monthly -> Yahoo handles aggregation better
    if range in ["1W", "1M"]:
        data = await asyncio.to_thread(yahoo_service.get_chart_data, symbol, range_type=range.lower())
    else:
        # Intraday/Daily -> Try FMP first
        data = await asyncio.to_thread(fmp_service.get_historical_candles, symbol, timeframe=range)
        if not data:
             data = await asyncio.to_thread(yahoo_service.get_chart_data, symbol, range_type=range.lower())

    if not data: return []

    # 2. Live Stitching (Only needed for Daily/Intraday)
    # We grab a live quote to ensure the very last candle is up to the second.
    live_quote = await asyncio.to_thread(yahoo_service.get_quote, symbol)
    
    if live_quote and live_quote.get('price'):
        price = live_quote['price']
        
        # Determine Market Timezone
        tz = pytz.utc
        if symbol.endswith(".NS") or symbol.endswith(".BO"): tz = pytz.timezone('Asia/Kolkata')
        elif symbol.endswith(".L"): tz = pytz.timezone('Europe/London')
        else: tz = pytz.timezone('US/Eastern')
        
        now = datetime.now(tz)
        today_str = now.strftime('%Y-%m-%d')
        
        if len(data) > 0:
            last = data[-1]
            last_date_str = datetime.fromtimestamp(last['time'], tz=tz).strftime('%Y-%m-%d')
            
            if range == "1D":
                if last_date_str == today_str:
                    # Update existing today candle
                    last['close'] = price
                    last['high'] = max(last['high'], price)
                    last['low'] = min(last['low'], price)
                    if live_quote.get('volume'): last['volume'] = live_quote['volume']
                else:
                    # Market open, but FMP hasn't updated yet -> Append new candle
                    day_open = live_quote.get('open') or price
                    new_candle = {
                        "time": int(now.replace(hour=0,minute=0,second=0,microsecond=0).timestamp()),
                        "open": day_open,
                        "high": max(day_open, price),
                        "low": min(day_open, price),
                        "close": price,
                        "volume": live_quote.get('volume') or 0
                    }
                    data.append(new_candle)

    # 3. Save to Redis (Short TTL for live charts)
    redis_service.set_cache(cache_key, data, 15)
    return data


@router.get("/{symbol}/all")
async def get_all_stock_data(symbol: str):
    """
    The Smart Race Aggregator.
    Fetches all dashboard data in parallel.
    """
    cache_key = f"all_data_{symbol}"
    cached = redis_service.get_cache(cache_key)
    if cached: return cached

    is_international = "." in symbol
    
    # Base Tasks (FMP)
    tasks = {
        "fmp_profile": asyncio.to_thread(fmp_service.get_company_profile, symbol),
        "fmp_quote": asyncio.to_thread(fmp_service.get_quote, symbol),
        "fmp_key_metrics": asyncio.to_thread(fmp_service.get_key_metrics, symbol, "annual", 1),
        
        "fmp_inc": asyncio.to_thread(fmp_service.get_financial_statements, symbol, "income-statement", "annual", 10),
        "fmp_bal": asyncio.to_thread(fmp_service.get_financial_statements, symbol, "balance-sheet-statement", "annual", 10),
        "fmp_cf": asyncio.to_thread(fmp_service.get_financial_statements, symbol, "cash-flow-statement", "annual", 10),
        
        "fmp_q_inc": asyncio.to_thread(fmp_service.get_financial_statements, symbol, "income-statement", "quarter", 5),
        "fmp_q_bal": asyncio.to_thread(fmp_service.get_financial_statements, symbol, "balance-sheet-statement", "quarter", 5),
        "fmp_q_cf": asyncio.to_thread(fmp_service.get_financial_statements, symbol, "cash-flow-statement", "quarter", 5),
        
        "shareholding": asyncio.to_thread(fmp_service.get_shareholding_data, symbol),
        "news": asyncio.to_thread(news_service.get_company_news, symbol),
        "yf_rec": asyncio.to_thread(yahoo_service.get_analyst_recommendations, symbol),
        "yf_tar": asyncio.to_thread(yahoo_service.get_price_target_data, symbol),
        
        # Technicals Base (Daily)
        "hist_df": asyncio.to_thread(yahoo_service.get_historical_data, symbol, "260d"),
    }

    # Backup Tasks (Triggered concurrently for Intl stocks to avoid wait)
    if is_international:
        tasks.update({
            "yf_p": asyncio.to_thread(yahoo_service.get_company_profile, symbol),
            "yf_q": asyncio.to_thread(yahoo_service.get_quote, symbol),
            "yf_m": asyncio.to_thread(yahoo_service.get_key_fundamentals, symbol),
            "yf_share": asyncio.to_thread(yahoo_service.get_shareholding_summary, symbol),
            "yf_hist": asyncio.to_thread(yahoo_service.get_historical_financials, symbol),
            "yf_q_fin": asyncio.to_thread(yahoo_service.get_quarterly_financials, symbol),
        })
    else:
        # Lazy load backups for US if needed
        tasks["yf_m"] = asyncio.to_thread(yahoo_service.get_key_fundamentals, symbol)
        tasks["yf_share"] = asyncio.to_thread(yahoo_service.get_shareholding_summary, symbol)

    try:
        results = await asyncio.gather(*tasks.values(), return_exceptions=True)
        raw = dict(zip(tasks.keys(), results))
    except: raise HTTPException(status_code=500, detail="Data fetch failed.")

    # --- MERGE & FALLBACK LOGIC ---
    def safe(k, d=None):
        v = raw.get(k)
        if isinstance(v, Exception) or v is None: return d
        if isinstance(v, list) and len(v)==0: return d
        if isinstance(v, list) and isinstance(d, dict): return v[0]
        return v

    def is_valid(data):
        if not data or not isinstance(data, list) or len(data) == 0: return False
        for i in range(min(3, len(data))):
            if data[i].get('netIncome') is not None or data[i].get('revenue') is not None: return True
        return False

    final_data = {}

    # 1. Profile/Quote
    p = safe('fmp_profile')
    q = safe('fmp_quote')
    if not p or not q.get('price'):
        if not is_international:
            # Emergency Fetch if not already running
            p = await asyncio.to_thread(yahoo_service.get_company_profile, symbol)
            q = await asyncio.to_thread(yahoo_service.get_quote, symbol)
        else:
            p = safe('yf_p', {})
            q = safe('yf_q', {})

    final_data['profile'] = p or {}
    final_data['quote'] = q or {}

    # 2. Metrics
    final_data['key_metrics'] = {**safe('yf_m', {}), **safe('fmp_key_metrics', {})}

    # 3. Financials
    inc = safe('fmp_income_5y', [])
    if is_valid(inc):
        final_data['annual_revenue_and_profit'] = inc
        final_data['annual_balance_sheets'] = safe('fmp_balance_5y', [])
        final_data['annual_cash_flow_statements'] = safe('fmp_cash_flow_5y', [])
        final_data['quarterly_income_statements'] = safe('fmp_quarterly_income', [])
        final_data['quarterly_balance_sheets'] = safe('fmp_quarterly_balance', [])
        final_data['quarterly_cash_flow_statements'] = safe('fmp_quarterly_cash_flow', [])
    else:
        # Fallback to Yahoo
        if not is_international:
             yf_h = await asyncio.to_thread(yahoo_service.get_historical_financials, symbol)
             yf_q = await asyncio.to_thread(yahoo_service.get_quarterly_financials, symbol)
        else:
             yf_h = safe('yf_hist', {'income':[]})
             yf_q = safe('yf_q_fin', {'income':[]})
        
        final_data['annual_revenue_and_profit'] = yf_h.get('income', [])
        final_data['annual_balance_sheets'] = yf_h.get('balance', [])
        final_data['annual_cash_flow_statements'] = yf_h.get('cash_flow', [])
        final_data['quarterly_income_statements'] = yf_q.get('income', [])
        final_data['quarterly_balance_sheets'] = yf_q.get('balance', [])
        final_data['quarterly_cash_flow_statements'] = yf_q.get('cash_flow', [])

    # 4. Calculations
    final_data['piotroski_f_score'] = fundamental_service.calculate_piotroski_f_score(
        final_data['annual_revenue_and_profit'], 
        final_data['annual_balance_sheets'], 
        final_data['annual_cash_flow_statements']
    )
    final_data['graham_scan'] = fundamental_service.calculate_graham_scan(
        final_data['profile'], final_data['key_metrics'], final_data['annual_revenue_and_profit']
    )

    # 5. Technicals
    hist_df = raw.get('hist_df')
    if isinstance(hist_df, Exception) or hist_df is None:
        hist_df = await asyncio.to_thread(yahoo_service.get_historical_data, symbol, "260d")

    final_data['technical_indicators'] = await asyncio.to_thread(yahoo_service.calculate_technical_indicators, hist_df)
    final_data['darvas_scan'] = technical_service.calculate_darvas_box(hist_df, final_data['quote'], final_data['profile'].get('currency'))
    final_data['moving_averages'] = technical_service.calculate_moving_averages(hist_df)
    final_data['pivot_points'] = technical_service.calculate_pivot_points(hist_df)
    
    final_data['overall_sentiment'] = sentiment_service.calculate_overall_sentiment(
        piotroski_score=final_data['piotroski_f_score'].get('score'),
        key_metrics=final_data['key_metrics'],
        technicals=final_data['technical_indicators'],
        analyst_ratings=safe('yf_rec', [])
    )
    
    # 6. Shareholding
    fmp_hold = safe('shareholding', [])
    if fmp_hold:
        total_inst = sum(h.get('shares', 0) for h in fmp_hold)
        final_data['shareholding_breakdown'] = {"promoter": 0, "fii": total_inst * 0.6, "dii": total_inst * 0.4, "public": 0} 
        final_data['shareholding'] = fmp_hold
    else:
        if not is_international:
             yf_hold_sum = await asyncio.to_thread(yahoo_service.get_shareholding_summary, symbol)
        else:
             yf_hold_sum = safe('yf_share', {})
        final_data['shareholding_breakdown'] = yf_hold_sum
        final_data['shareholding'] = []

    final_data['news'] = safe('news', [])
    final_data['analyst_ratings'] = safe('yf_rec', [])
    final_data['price_target_consensus'] = safe('yf_tar', {})

    tv_symbol = symbol
    if symbol in TRADINGVIEW_OVERRIDE_MAP: tv_symbol = TRADINGVIEW_OVERRIDE_MAP[symbol]
    elif symbol.endswith(".NS"): tv_symbol = symbol.replace(".NS", "")
    elif symbol.endswith(".BO"): tv_symbol = "BSE:" + symbol.replace(".BO", "")
    final_data['profile']['tradingview_symbol'] = tv_symbol

    # 7. Sanitization
    k_met = final_data.get('key_metrics', {})
    k_prof = final_data.get('profile', {})
    k_quo = final_data.get('quote', {})
    k_est = safe('analyst_estimates', {})
    
    def sanitize(v): return None if isinstance(v, float) and (math.isnan(v) or math.isinf(v)) else v

    raw_stats = {
        "marketCap": k_prof.get('mktCap') or k_met.get('marketCap'),
        "dividendYield": k_met.get('dividendYieldTTM'),
        "peRatio": k_met.get('peRatioTTM'),
        "basicEPS": k_met.get('epsTTM'),
        "netIncome": k_met.get('netIncomePerShareTTM'),
        "revenue": k_met.get('revenuePerShareTTM'),
        "sharesFloat": k_quo.get('sharesOutstanding') or k_met.get('sharesOutstanding'),
        "beta": k_prof.get('beta') or k_met.get('beta'),
        "employees": k_prof.get('fullTimeEmployees') or k_met.get('fullTimeEmployees'),
        "nextReportDate": k_est.get('date') if isinstance(k_est, dict) else None,
        "epsEstimate": k_est.get('estimatedEpsAvg') if isinstance(k_est, dict) else None,
        "revenueEstimate": k_est.get('estimatedRevenueAvg') if isinstance(k_est, dict) else None,
    }
    
    final_data['keyStats'] = {k: sanitize(v) for k, v in raw_stats.items()}
    
    def clean_nans(obj):
        if isinstance(obj, float): return None if math.isnan(obj) or math.isinf(obj) else obj
        if isinstance(obj, dict): return {k: clean_nans(v) for k, v in obj.items()}
        if isinstance(obj, list): return [clean_nans(v) for v in obj]
        return obj

    final = clean_nans(final_data)
    
    # Save to Redis (60s cache for master data)
    redis_service.set_cache(cache_key, final, 60)
    
    return final