import asyncio
import math
from fastapi import APIRouter, HTTPException, Query, Body
from ..services import fmp_service, yahoo_service, news_service, gemini_service, fundamental_service, technical_service, sentiment_service
from pydantic import BaseModel
from typing import List, Dict, Any

# --- Data Models for all POST requests ---
# --- Data Models for all POST requests ---
class SwotRequest(BaseModel):
    companyName: str
    description: str

class ForecastRequest(BaseModel):
    companyName: str
    analystRatings: List[Dict[str, Any]]
    priceTarget: Dict[str, Any]
    keyStats: Dict[str, Any]
    newsHeadlines: List[str]

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
    keyStats: Dict[str, Any]
    newsHeadlines: List[str]
    # These are kept for backward compatibility if needed, but we rely on keyStats now
    canslimAssessment: str = ""
    philosophyAssessment: str = ""

router = APIRouter()

# --- TRADINGVIEW SYMBOL OVERRIDE MAP ---
TRADINGVIEW_OVERRIDE_MAP = {
    "TATAPOWER.NS": "BSE:TATAPOWER",
    "RELIANCE.NS": "BSE:RELIANCE",
    # Add more here as needed
}

# --- All lazy-loading endpoints ---
@router.get("/search")
async def search_stock_ticker(query: str = Query(..., min_length=2)):
    ticker = gemini_service.get_ticker_from_query(query)
    if ticker in ["NOT_FOUND", "ERROR"]:
        raise HTTPException(status_code=404, detail=f"Could not find a ticker for '{query}'")
    return {"symbol": ticker}

# ... (imports remain the same)

# --- NEW AUTOCOMPLETE ENDPOINT ---
@router.get("/autocomplete")
async def get_stock_suggestions(query: str = Query(..., min_length=1)):
    """
    Fast endpoint for search bar autocomplete.
    Uses FMP search API directly, not AI, for speed.
    """
    suggestions = await asyncio.to_thread(fmp_service.search_ticker, query)
    return suggestions

# ... (rest of the file remains the same)

@router.post("/{symbol}/swot")
async def get_swot_analysis(symbol: str, request_data: SwotRequest = Body(...)):
    print(f"Received SWOT request for {symbol}...")
    news_articles = await asyncio.to_thread(news_service.get_company_news, request_data.companyName)
    news_headlines = [article.get('title', '') for article in news_articles[:10]]
    swot_analysis = await asyncio.to_thread(
        gemini_service.generate_swot_analysis,
        request_data.companyName,
        request_data.description,
        news_headlines
    )
    return {"swot_analysis": swot_analysis}

@router.post("/{symbol}/forecast-analysis")
async def get_forecast_analysis(symbol: str, request_data: ForecastRequest = Body(...)):
    print(f"Received AI Forecast Analysis request for {symbol}...")
    analysis = await asyncio.to_thread(
        gemini_service.generate_forecast_analysis,
        company_name=request_data.companyName,
        analyst_ratings=request_data.analystRatings,
        price_target=request_data.priceTarget,
        key_stats=request_data.keyStats,
        news_headlines=request_data.newsHeadlines
    )
    return {"analysis": analysis}

@router.post("/{symbol}/fundamental-analysis")
async def get_fundamental_analysis(symbol: str, request_data: FundamentalRequest = Body(...)):
    print(f"Received AI Fundamental Analysis request for {symbol}...")
    assessment = await asyncio.to_thread(
        gemini_service.generate_investment_philosophy_assessment,
        company_name=request_data.companyName,
        key_metrics=request_data.keyMetrics
    )
    return {"assessment": assessment}

@router.post("/{symbol}/canslim-analysis")
async def get_canslim_analysis(symbol: str, request_data: CanslimRequest = Body(...)):
    print(f"Received AI CANSLIM Analysis request for {symbol}...")
    assessment = await asyncio.to_thread(
        gemini_service.generate_canslim_assessment,
        company_name=request_data.companyName,
        quote=request_data.quote,
        quarterly_earnings=request_data.quarterlyEarnings,
        annual_earnings=request_data.annualEarnings,
        institutional_holders=request_data.institutionalHolders
    )
    return {"assessment": assessment}

@router.post("/{symbol}/conclusion-analysis")
async def get_conclusion_analysis(symbol: str, request_data: ConclusionRequest = Body(...)):
    print(f"Received AI Conclusion Analysis request for {symbol}...")
    conclusion = await asyncio.to_thread(
        gemini_service.generate_fundamental_conclusion,
        company_name=request_data.companyName,
        piotroski_data=request_data.piotroskiData,
        graham_data=request_data.grahamData,
        darvas_data=request_data.darvasData,
        key_stats=request_data.keyStats,          # <-- Updated
        news_headlines=request_data.newsHeadlines # <-- Updated
    )
    return {"conclusion": conclusion}

@router.get("/{symbol}/peers")
async def get_peers_comparison(symbol: str):
    print(f"Received AI Peers Comparison request for {symbol}...")
    
    company_info = await asyncio.to_thread(yahoo_service.get_company_info, symbol)
    sector, industry, country, company_name = company_info.get('sector'), company_info.get('industry'), company_info.get('country'), company_info.get('longName', symbol)
    
    if not all([sector, industry, country]):
        return []

    print(f"Asking AI for peers of {company_name}...")
    peer_tickers = await asyncio.to_thread(gemini_service.find_peer_tickers_by_industry, company_name, sector, industry, country)
    
    if not peer_tickers:
        return []
    
    print(f"AI found peers: {peer_tickers}")
    all_symbols_to_fetch = [symbol] + peer_tickers
    
    # Dual-Source Peers Fetching
    fmp_peers_data = await asyncio.to_thread(fmp_service.get_peers_with_metrics, all_symbols_to_fetch)
    peers_map = {item['symbol']: item for item in fmp_peers_data}
    
    tasks_to_run = []
    for peer_symbol in all_symbols_to_fetch:
        # If FMP data is missing or incomplete (no P/E), fetch from Yahoo
        if peer_symbol not in peers_map or not peers_map[peer_symbol].get('peRatioTTM'):
            tasks_to_run.append((peer_symbol, asyncio.to_thread(yahoo_service.get_key_fundamentals, peer_symbol)))
            
    if tasks_to_run:
        fallback_results = await asyncio.gather(*[task for _, task in tasks_to_run], return_exceptions=True)
        for (peer_symbol, _), result in zip(tasks_to_run, fallback_results):
            if not isinstance(result, Exception) and result:
                if peer_symbol not in peers_map: peers_map[peer_symbol] = {"symbol": peer_symbol}
                peers_map[peer_symbol].update(result)
                
    return list(peers_map.values())


# --- THE ULTIMATE DATA FETCHING ENDPOINT ---
@router.get("/{symbol}/all")
async def get_all_stock_data(symbol: str):
    """
    This definitive endpoint fetches all required data from FMP and Yahoo Finance
    concurrently, intelligently merges it, and runs all necessary calculations.
    """
    # Step 1: Define all data fetching tasks from all sources
    tasks = {
        "fmp_profile": asyncio.to_thread(fmp_service.get_company_profile, symbol),
        "fmp_quote": asyncio.to_thread(fmp_service.get_quote, symbol),
        "fmp_key_metrics": asyncio.to_thread(fmp_service.get_key_metrics, symbol, "annual", 1),
        "fmp_income_5y": asyncio.to_thread(fmp_service.get_financial_statements, symbol, "income-statement", "annual", 5),
        "fmp_balance_5y": asyncio.to_thread(fmp_service.get_financial_statements, symbol, "balance-sheet-statement", "annual", 5),
        "fmp_cash_flow_5y": asyncio.to_thread(fmp_service.get_financial_statements, symbol, "cash-flow-statement", "annual", 5),
        
        # Fetch Quarterly data from FMP
        "fmp_quarterly_income": asyncio.to_thread(fmp_service.get_financial_statements, symbol, "income-statement", "quarter", 5),
        "fmp_quarterly_balance": asyncio.to_thread(fmp_service.get_financial_statements, symbol, "balance-sheet-statement", "quarter", 5),
        "fmp_quarterly_cash_flow": asyncio.to_thread(fmp_service.get_financial_statements, symbol, "cash-flow-statement", "quarter", 5),
        
        "shareholding": asyncio.to_thread(fmp_service.get_shareholding_data, symbol),
        "news": asyncio.to_thread(news_service.get_company_news, symbol),
        
        # Yahoo Finance Tasks
        "yf_recommendations": asyncio.to_thread(yahoo_service.get_analyst_recommendations, symbol),
        "yf_price_target": asyncio.to_thread(yahoo_service.get_price_target_data, symbol),
        "yf_historical_financials": asyncio.to_thread(yahoo_service.get_historical_financials, symbol),
        "yf_key_fundamentals": asyncio.to_thread(yahoo_service.get_key_fundamentals, symbol),
        "yf_shareholding": asyncio.to_thread(yahoo_service.get_shareholding_summary, symbol),
        # --- NEW: Yahoo Quarterly Fallback ---
        "yf_quarterly_financials": asyncio.to_thread(yahoo_service.get_quarterly_financials, symbol),
    }

    # Step 2: Run all tasks concurrently with UNBREAKABLE Error Handling
    try:
        results = await asyncio.gather(*tasks.values(), return_exceptions=True)
        raw_data = dict(zip(tasks.keys(), results))
    except Exception as e:
        print(f"CRITICAL ASYNCIO ERROR: {e}")
        raise HTTPException(status_code=500, detail="A critical error occurred while fetching data.")

    final_data = {}

    # Unbreakable Error Handling
    for key, value in raw_data.items():
        if isinstance(value, BaseException):
            print(f"HANDLED SEVERE ERROR for '{key}': {value}")
            raw_data[key] = {} if 'profile' in key or 'quote' in key or 'metrics' in key else []

    def safe_get_first(data, default={}):
        if isinstance(data, list) and len(data) > 0: return data[0]
        return default
    
    # --- HELPER: Validate Financial Data ---
    # Checks if a list of financial statements actually contains valid numbers.
    def is_data_valid(data_list):
        if not data_list or not isinstance(data_list, list) or len(data_list) == 0:
            return False
        # Check the most recent entry for a critical key
        first_item = data_list[0]
        if first_item.get('netIncome') is None and first_item.get('eps') is None:
            return False
        return True

    # --- Data Merging and Cleaning ---
    
    final_data['profile'] = safe_get_first(raw_data.get('fmp_profile'))
    final_data['quote'] = safe_get_first(raw_data.get('fmp_quote'))
    
    # Key Metrics: Intelligent Merge
    fmp_metrics = safe_get_first(raw_data.get('fmp_key_metrics'))
    yf_fundamentals = raw_data.get('yf_key_fundamentals', {})
    # Merge: start with Yahoo, overwrite with FMP if available, but Yahoo fills the gaps!
    merged_metrics = {**yf_fundamentals, **fmp_metrics}
    final_data['key_metrics'] = merged_metrics

    # Annual Financial Statements: Intelligent Merge
    fmp_income = raw_data.get('fmp_income_5y', [])
    yf_income = raw_data.get('yf_historical_financials', {}).get('income', [])
    income_statements = fmp_income if is_data_valid(fmp_income) else yf_income
    final_data['annual_revenue_and_profit'] = income_statements
    
    fmp_balance = raw_data.get('fmp_balance_5y', [])
    yf_balance = raw_data.get('yf_historical_financials', {}).get('balance', [])
    balance_sheets = fmp_balance if is_data_valid(fmp_balance) else yf_balance
    final_data['annual_balance_sheets'] = balance_sheets
    
    fmp_cash_flow = raw_data.get('fmp_cash_flow_5y', [])
    yf_cash_flow = raw_data.get('yf_historical_financials', {}).get('cash_flow', [])
    cash_flow_statements = fmp_cash_flow if is_data_valid(fmp_cash_flow) else yf_cash_flow
    final_data['annual_cash_flow_statements'] = cash_flow_statements
    
    # --- Quarterly Financial Statements: Intelligent Merge (CRITICAL FOR CANSLIM) ---
    fmp_q_income = raw_data.get('fmp_quarterly_income', [])
    yf_q_income = raw_data.get('yf_quarterly_financials', {}).get('income', [])
    
    # Only use FMP if it has VALID data, otherwise use Yahoo
    final_data['quarterly_income_statements'] = fmp_q_income if is_data_valid(fmp_q_income) else yf_q_income
    
    fmp_q_balance = raw_data.get('fmp_quarterly_balance', [])
    yf_q_balance = raw_data.get('yf_quarterly_financials', {}).get('balance', [])
    final_data['quarterly_balance_sheets'] = fmp_q_balance if is_data_valid(fmp_q_balance) else yf_q_balance
    
    fmp_q_cash = raw_data.get('fmp_quarterly_cash_flow', [])
    yf_q_cash = raw_data.get('yf_quarterly_financials', {}).get('cash_flow', [])
    final_data['quarterly_cash_flow_statements'] = fmp_q_cash if is_data_valid(fmp_q_cash) else yf_q_cash

    # --- Calculations ---
    final_data['piotroski_f_score'] = fundamental_service.calculate_piotroski_f_score(
        final_data['annual_revenue_and_profit'], 
        final_data['annual_balance_sheets'], 
        final_data['annual_cash_flow_statements']
    )
    final_data['graham_scan'] = fundamental_service.calculate_graham_scan(
        final_data['profile'], 
        final_data['key_metrics'], 
        final_data['annual_revenue_and_profit']
    )

    hist_df = await asyncio.to_thread(yahoo_service.get_historical_data, symbol, "300d")
    final_data['technical_indicators'] = await asyncio.to_thread(yahoo_service.calculate_technical_indicators, hist_df)
    final_data['darvas_scan'] = technical_service.calculate_darvas_box(hist_df, final_data['quote'], final_data['profile'].get('currency'))
    final_data['moving_averages'] = technical_service.calculate_moving_averages(hist_df)
    final_data['pivot_points'] = technical_service.calculate_pivot_points(hist_df)
    
    final_data['overall_sentiment'] = sentiment_service.calculate_overall_sentiment(
        piotroski_score=final_data['piotroski_f_score'].get('score'),
        pe_ratio=final_data['key_metrics'].get('peRatioTTM'),
        analyst_ratings=raw_data.get('yf_recommendations', []),
        rsi=final_data['technical_indicators'].get('rsi')
    )
    
    # Shareholding Merge
    yf_shareholding = raw_data.get('yf_shareholding', {})
    if yf_shareholding and yf_shareholding.get('promoter', 0) > 0:
        final_data['shareholding_breakdown'] = yf_shareholding
    else:
        fmp_shareholding = raw_data.get('shareholding', [])
        total_inst = sum(h.get('shares', 0) for h in fmp_shareholding)
        final_data['shareholding_breakdown'] = {"promoter": 0, "fii": total_inst * 0.6, "dii": total_inst * 0.4, "public": 0}
    
    final_data['shareholding'] = raw_data.get('shareholding', [])
    final_data['news'] = raw_data.get('news', [])
    final_data['analyst_ratings'] = raw_data.get('yf_recommendations', [])
    final_data['price_target_consensus'] = raw_data.get('yf_price_target', {})

    # TradingView Symbol Translation
    tv_symbol = symbol
    if symbol in TRADINGVIEW_OVERRIDE_MAP:
        tv_symbol = TRADINGVIEW_OVERRIDE_MAP[symbol]
    elif symbol.endswith(".NS"):
        tv_symbol = symbol.replace(".NS", "")
    elif symbol.endswith(".BO"):
        tv_symbol = "BSE:" + symbol.replace(".BO", "")
    final_data['profile']['tradingview_symbol'] = tv_symbol

    # Consolidate Key Stats (Prioritize Merged Metrics)
    keyStats_metrics = final_data['key_metrics']
    keyStats_profile = final_data.get('profile', {})
    keyStats_quote = final_data.get('quote', {})
    keyStats_estimates = raw_data.get('analyst_estimates', {})
    
    # --- DATA SANITIZATION FOR JSON COMPLIANCE ---
    def sanitize_float(value):
        if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
            return None
        return value

    raw_stats = {
        "marketCap": keyStats_profile.get('mktCap') or keyStats_metrics.get('marketCap'),
        "dividendYield": keyStats_metrics.get('dividendYieldTTM'),
        "peRatio": keyStats_metrics.get('peRatioTTM'),
        "basicEPS": keyStats_metrics.get('epsTTM'),
        "netIncome": keyStats_metrics.get('netIncomePerShareTTM'),
        "revenue": keyStats_metrics.get('revenuePerShareTTM'),
        "sharesFloat": keyStats_quote.get('sharesOutstanding') or keyStats_metrics.get('sharesOutstanding'),
        "beta": keyStats_profile.get('beta') or keyStats_metrics.get('beta'),
        "employees": keyStats_profile.get('fullTimeEmployees') or keyStats_metrics.get('fullTimeEmployees'),
        "nextReportDate": keyStats_estimates.get('date'),
        "epsEstimate": keyStats_estimates.get('estimatedEpsAvg'),
        "revenueEstimate": keyStats_estimates.get('estimatedRevenueAvg'),
    }
    
    final_data['keyStats'] = {k: sanitize_float(v) for k, v in raw_stats.items()}
    
    # Use the same sanitization on the ENTIRE final_data object to be safe
    def clean_nans(obj):
        if isinstance(obj, float):
            if math.isnan(obj) or math.isinf(obj): return None
            return obj
        elif isinstance(obj, dict):
            return {k: clean_nans(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [clean_nans(v) for v in obj]
        return obj

    return clean_nans(final_data)