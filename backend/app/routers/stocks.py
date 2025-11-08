import asyncio
from fastapi import APIRouter, HTTPException, Query
from ..services import fmp_service, yahoo_service, news_service, gemini_service

# The APIRouter will be used to group all stock-related endpoints
router = APIRouter()

@router.get("/search")
async def search_stock_ticker(query: str = Query(..., min_length=2, description="User's search query for a company")):
    """
    Takes a natural language query from the user and uses the Gemini AI service
    to find the corresponding stock ticker.
    """
    if not query:
        raise HTTPException(status_code=400, detail="Query parameter cannot be empty.")
    
    ticker = gemini_service.get_ticker_from_query(query)
    
    if ticker == "NOT_FOUND" or ticker == "ERROR":
        raise HTTPException(status_code=404, detail=f"Could not find a ticker for the query: '{query}'")
        
    return {"symbol": ticker}


@router.get("/{symbol}/history")
async def get_stock_history(symbol: str, period: str = "5y", interval: str = "1d"):
    """
    Provides historical price data for a given stock symbol,
    fetched from the Yahoo Finance service. Primarily used for charting.
    """
    historical_data = yahoo_service.get_historical_data(symbol, period, interval)
    if not historical_data:
        raise HTTPException(status_code=404, detail=f"Historical data not found for symbol {symbol}")
    return historical_data


@router.get("/{symbol}/all")
async def get_all_stock_data(symbol: str):
    """
    This is the primary data endpoint. It aggregates all necessary data for the
    stock detail page from various services in a single, efficient API call
    using concurrent requests.
    """
    # Create a list of asynchronous tasks to be executed concurrently
    tasks = {
        "profile": asyncio.to_thread(fmp_service.get_company_profile, symbol),
        "quote": asyncio.to_thread(fmp_service.get_quote, symbol),
        "key_metrics": asyncio.to_thread(fmp_service.get_key_metrics, symbol),
        "annual_revenue_and_profit": asyncio.to_thread(fmp_service.get_financial_statements, symbol, "income-statement", "annual", 5),
        "shareholding": asyncio.to_thread(fmp_service.get_shareholding_data, symbol),
        "analyst_ratings": asyncio.to_thread(fmp_service.get_analyst_ratings, symbol),
    }

    # Execute all tasks in parallel and wait for them to complete
    results = await asyncio.gather(*tasks.values(), return_exceptions=True)
    
    # Map results back to their keys
    data = dict(zip(tasks.keys(), results))

    # Error handling: Check if any of the tasks failed
    for key, value in data.items():
        if isinstance(value, Exception):
            print(f"Error fetching '{key}' for {symbol}: {value}")
            # Replace the exception with a more friendly error message or empty dict/list
            data[key] = {"error": f"Failed to fetch {key} data."}

    # Some data is nested inside a list, so we extract the first element if it exists
    data['profile'] = data['profile'][0] if data['profile'] and isinstance(data['profile'], list) else data['profile']
    data['quote'] = data['quote'][0] if data['quote'] and isinstance(data['quote'], list) else data['quote']
    
    # --- Secondary data fetching that depends on the first batch ---
    company_name = data.get("profile", {}).get("companyName", symbol)
    description = data.get("profile", {}).get("description", "")
    
    # Fetch news using the determined company name
    news_articles = await asyncio.to_thread(news_service.get_company_news, company_name)
    data['news'] = news_articles
    
    # Generate AI SWOT analysis using company info and news headlines
    news_headlines = [article.get('title', '') for article in news_articles[:10]] # Use top 10 headlines
    swot_analysis = await asyncio.to_thread(gemini_service.generate_swot_analysis, company_name, description, news_headlines)
    data['swot_analysis'] = swot_analysis
    
    return data