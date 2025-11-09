import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure the Gemini API with your key from the .env file
try:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY not found in .env file.")
    genai.configure(api_key=GEMINI_API_KEY)
except ValueError as e:
    print(f"Error: {e}")
    # Handle the error appropriately, maybe exit or use a fallback
    # For now, we'll just print it.


def get_ticker_from_query(query: str):
    """
    Uses the Gemini model to intelligently find a stock ticker symbol from a natural language query.
    For example, "what's the stock for the company that makes iPhones" -> "AAPL".
    """
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    # This is a carefully crafted prompt to ensure the model returns ONLY the ticker.
    prompt = f"""
    Analyze the following user query to identify the company and its official stock ticker symbol.
    
    Query: "{query}"

    Return ONLY the stock ticker symbol. For example, if the company is Apple, return "AAPL". 
    If it's Reliance Industries in India, return "RELIANCE.NS". 
    If you cannot determine a clear ticker, return "NOT_FOUND".
    """
    
    try:
        response = model.generate_content(prompt)
        # We clean the response to remove any potential markdown or extra text
        # although the prompt is designed to prevent it.
        ticker = response.text.strip().replace("`", "").upper()
        return ticker
    except Exception as e:
        print(f"An error occurred while calling the Gemini API: {e}")
        return "ERROR"

def generate_swot_analysis(company_name: str, description: str, news_headlines: list):
    """
    Generates a SWOT analysis for a given company using its description and recent news.
    """
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    # Joining news headlines into a single string for the prompt
    news_string = "\n- ".join(news_headlines)
    
    prompt = f"""
    Based on the following company information and recent news headlines, generate a SWOT analysis.
    The output should be in four distinct sections: Strengths, Weaknesses, Opportunities, and Threats.
    For each section, provide at least 3-4 concise bullet points.

    Company Name: {company_name}

    Company Description: {description}

    Recent News Headlines:
    - {news_string}

    Generate the SWOT analysis now.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"An error occurred while generating SWOT analysis: {e}")
        return "Could not generate AI-powered analysis at this time."

# (Keep the existing get_ticker_from_query and generate_swot_analysis functions)

# --- ADD THIS NEW FUNCTION AT THE END OF THE FILE ---

def generate_forecast_analysis(company_name: str, analyst_ratings: list, price_target: dict, key_stats: dict, news_headlines: list):
    """
    Generates a comprehensive summary of the analyst forecast using Gemini.
    """
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    # Format the data into a human-readable string for the AI prompt
    ratings_summary = "\n".join([f"- {r['ratingStrongBuy']} Strong Buy, {r['ratingBuy']} Buy, {r['ratingHold']} Hold" for r in analyst_ratings[:1]])
    news_string = "\n- ".join(news_headlines)
    
    prompt = f"""
    Act as a professional financial analyst. Based on the following data for {company_name}, provide a concise, insightful summary of the analyst forecast.
    The summary should be easy for a retail investor to understand.
    Structure your response in two paragraphs:
    1.  **Analyst Sentiment:** Briefly describe the overall analyst sentiment based on the ratings breakdown and consensus.
    2.  **Price Target Analysis:** Explain the 1-year price target, including the high, average, and low estimates, and what this implies for the stock's potential.

    **DATA:**
    - **Analyst Ratings Breakdown:**
    {ratings_summary}
    - **Price Target Consensus:**
    - High: ${price_target.get('targetHigh')}
    - Average: ${price_target.get('targetConsensus')}
    - Low: ${price_target.get('targetLow')}
    - **Key Financials:**
    - P/E Ratio: {key_stats.get('peRatio')}
    - EPS: {key_stats.get('basicEPS')}
    - **Recent News Headlines:**
    - {news_string}

    Generate the two-paragraph summary now.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"An error occurred while generating forecast analysis: {e}")
        return "Could not generate AI-powered forecast analysis at this time."