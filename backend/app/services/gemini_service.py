import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

try:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY not found in .env file.")
    genai.configure(api_key=GEMINI_API_KEY)
except ValueError as e:
    print(f"Error: {e}")


def get_ticker_from_query(query: str):
    # ... (this function is unchanged)
    model = genai.GenerativeModel('gemini-2.5-flash')
    prompt = f"""
    Analyze the following user query to identify the company and its official stock ticker symbol.
    Query: "{query}"
    Return ONLY the stock ticker symbol. For example, if the company is Apple, return "AAPL". 
    If it's Reliance Industries in India, return "RELIANCE.NS". 
    If you cannot determine a clear ticker, return "NOT_FOUND".
    """
    try:
        response = model.generate_content(prompt)
        ticker = response.text.strip().replace("`", "").upper()
        return ticker
    except Exception as e:
        print(f"An error occurred while calling the Gemini API: {e}")
        return "ERROR"

def generate_swot_analysis(company_name: str, description: str, news_headlines: list):
    # ... (this function is unchanged)
    model = genai.GenerativeModel('gemini-2.5-flash')
    news_string = "\n- ".join(news_headlines)
    prompt = f"""
    Based on the following company information and recent news headlines, generate a SWOT analysis...
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


def generate_forecast_analysis(company_name: str, analyst_ratings: list, price_target: dict, key_stats: dict, news_headlines: list):
    # ... (this function is unchanged)
    model = genai.GenerativeModel('gemini-2.5-flash')
    ratings_summary = "\n".join([f"- {r['ratingStrongBuy']} Strong Buy, {r['ratingBuy']} Buy, {r['ratingHold']} Hold" for r in analyst_ratings[:1]])
    news_string = "\n- ".join(news_headlines)
    prompt = f"""
    Act as a professional financial analyst. Based on the following data for {company_name}, provide a concise, insightful summary...
    DATA:
    - Analyst Ratings Breakdown: {ratings_summary}
    - Price Target Consensus: High: ${price_target.get('targetHigh')} Average: ${price_target.get('targetConsensus')} Low: ${price_target.get('targetLow')}
    - Key Financials: P/E Ratio: {key_stats.get('peRatio')} EPS: {key_stats.get('basicEPS')}
    - Recent News Headlines: - {news_string}
    Generate the two-paragraph summary now.
    """
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"An error occurred while generating forecast analysis: {e}")
        return "Could not generate AI-powered forecast analysis at this time."


def generate_investment_philosophy_assessment(company_name: str, key_metrics: dict):
    """
    Generates a qualitative assessment of a company against famous investment philosophies.
    """
    # --- NEW DEBUGGING STATEMENTS ---
    print("\n--- DEBUGGING AI PHILOSOPHY ASSESSMENT ---")
    print(f"Company Name for AI: {company_name}")
    print("Key Metrics Sent to AI:")
    # We print each key metric individually to spot any missing values.
    for key, value in key_metrics.items():
        print(f"  - {key}: {value}")
    print("------------------------------------------\n")
    
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    pe_ratio = key_metrics.get('peRatioTTM')
    earnings_yield = key_metrics.get('earningsYieldTTM')
    roc = key_metrics.get('returnOnCapitalEmployedTTM')
    
    # Add a check to ensure we have some data before building the prompt
    if pe_ratio is None or earnings_yield is None or roc is None:
        print("CRITICAL ERROR: Essential metrics for AI assessment are missing.")
        return "Could not generate assessment due to missing key financial metrics (P/E, ROC, Earnings Yield)."

    data_summary = f"""
    - Price to Earnings (P/E) Ratio: {pe_ratio:.2f}
    - Earnings Yield (E/P): {earnings_yield:.4f}
    - Return on Capital (ROC): {roc:.4f}
    """
    
    prompt = f"""
    Act as a world-class financial analyst. Based on the following key financial metrics for {company_name}, provide a one-line qualitative assessment for each of the three investment philosophies below.
    The output must be a clean, three-row table in Markdown format with the headers: "Formula", "Key Criteria", "Assessment".

    **Key Metrics:**
    {data_summary}

    **Your Task:**
    1.  **Magic Formula:** Based on the Earnings Yield and Return on Capital, what is the assessment? (e.g., "High ROC/earnings yield", "Moderate", "Low")
    2.  **Warren Buffett Formula:** Broadly consider if these metrics (high ROC is a proxy for a good business) suggest a solid, dependable company with a potential moat. (e.g., "Solid, dependable, moderate moat", "Aggressive growth, high valuation")
    3.  **Coffee Can Investing:** Based on the ROC (a proxy for long-term quality), does this seem like a stable, well-run company suitable for a long-term hold? (e.g., "Stable, modest, well-run", "Cyclical, requires monitoring")

    Generate the Markdown table now.
    """
    
    try:
        response = model.generate_content(prompt)
        # --- MORE DEBUGGING ---
        print("--- AI Raw Response ---")
        print(response.text)
        print("-----------------------\n")
        return response.text.strip()
    except Exception as e:
        print(f"An error occurred while generating investment philosophy assessment: {e}")
        return "Could not generate AI-powered assessment at this time."