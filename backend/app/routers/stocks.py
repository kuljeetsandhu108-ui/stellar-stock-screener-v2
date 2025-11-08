import asyncio
from fastapi import APIRouter, HTTPException, Query, Body
from ..services import fmp_service, yahoo_service, news_service, gemini_service

# --- NEW: A data model for our new endpoint ---
from pydantic import BaseModel

class SwotRequest(BaseModel):
    companyName: str
    description: str

router = APIRouter()

@router.get("/search")
async def search_stock_ticker(query: str = Query(..., min_length=2)):
    ticker = gemini_service.get_ticker_from_query(query)
    if ticker in ["NOT_FOUND", "ERROR"]:
        raise HTTPException(status_code=404, detail=f"Could not find a ticker for '{query}'")
    return {"symbol": ticker}

@router.post("/{symbol}/swot")
async def get_swot_analysis(symbol: str, request_data: SwotRequest):
    """
    This endpoint is dedicated to generating the SWOT analysis.
    It receives the company name and description from the frontend.
    """
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


@router.get("/{symbol}/all")
async def get_all_stock_data(symbol: str):
    """
    The main '/all' endpoint is now faster because it no longer waits for the AI.
    """
    tasks = {
        "profile": asyncio.to_thread(fmp_service.get_company_profile, symbol),
        "quote": asyncio.to_thread(fmp_service.get_quote, symbol),
        "shareholding": asyncio.to_thread(fmp_service.get_shareholding_data, symbol),
        "analyst_ratings": asyncio.to_thread(fmp_service.get_analyst_ratings, symbol),
        "annual_revenue_and_profit": asyncio.to_thread(fmp_service.get_financial_statements, symbol, "income-statement", "annual", 5),
        "fmp_technicals": asyncio.to_thread(fmp_service.get_technical_indicators, symbol),
        "news": asyncio.to_thread(news_service.get_company_news, symbol),
    }
    results = await asyncio.gather(*tasks.values(), return_exceptions=True)
    
    # --- THIS IS THE CORRECTED LINE ---
    # We must zip the results with the original 'tasks' dictionary keys.
    data = dict(zip(tasks.keys(), results))

    # Fallback and error handling logic remains the same...
    fmp_technicals = data.get("fmp_technicals")
    if not fmp_technicals or isinstance(fmp_technicals, Exception) or not fmp_technicals.get('rsi'):
        hist_df = await asyncio.to_thread(yahoo_service.get_historical_data, symbol, "1y")
        calculated_technicals = await asyncio.to_thread(yahoo_service.calculate_technical_indicators, hist_df)
        data['technical_indicators'] = calculated_technicals
    else:
        data['technical_indicators'] = fmp_technicals
    data.pop("fmp_technicals", None)
    
    for key, value in data.items():
        if isinstance(value, Exception):
            print(f"Error fetching '{key}' for {symbol}: {value}")
            data[key] = {} if isinstance(data[key], dict) else []

    data['profile'] = data['profile'][0] if isinstance(data['profile'], list) and data['profile'] else data.get('profile', {})
    data['quote'] = data['quote'][0] if isinstance(data['quote'], list) and data['quote'] else data.get('quote', {})
    
    return data