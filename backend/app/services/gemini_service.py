import os
import google.generativeai as genai
from dotenv import load_dotenv
import itertools

load_dotenv()

# --- ROBUST KEY ROTATION ---
try:
    GEMINI_API_KEYS_STR = os.getenv("GEMINI_API_KEYS")
    if not GEMINI_API_KEYS_STR:
        single_key = os.getenv("GEMINI_API_KEY") 
        if single_key: GEMINI_API_KEYS = [single_key]
        else: GEMINI_API_KEYS = []
    else:
        GEMINI_API_KEYS =[key.strip() for key in GEMINI_API_KEYS_STR.split(',')]
    key_cycler = itertools.cycle(GEMINI_API_KEYS)
except:
    GEMINI_API_KEYS =[]
    key_cycler = None

def configure_gemini_for_request():
    if key_cycler:
        try: genai.configure(api_key=next(key_cycler))
        except: pass

# *** DYNAMIC MODEL SELECTOR ***
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-3-flash-preview")
print(f"🤖 AI Engine Initialized with Model: {MODEL_NAME}")

# --- VISION AI (Chart Identification) ---
def identify_ticker_from_image(image_bytes: bytes):
    try:
        configure_gemini_for_request()
        model = genai.GenerativeModel(MODEL_NAME)
        
        # Safe string concatenation (No triple quotes to cause errors)
        prompt = (
            "Look at this stock chart. Read the main Ticker Symbol text (top left usually). "
            "Return ONLY the ticker string. "
            "Examples: "
            "- If you see 'NIFTY 50', return 'NIFTY' "
            "- If you see 'RELIANCE', return 'RELIANCE' "
            "- If you see 'BTC/USD', return 'BTC' "
            "Do not add suffixes like .NS or .INDX. Just the raw name."
        )
        
        response = model.generate_content([prompt, {"mime_type": "image/jpeg", "data": image_bytes}])
        return response.text.strip().upper().replace("", "").replace(" ", "")
    except Exception as e:
        print(f"❌ VISION ERROR: {e}")
        return "NOT_FOUND"

def analyze_pure_vision(image_bytes: bytes):
    try:
        configure_gemini_for_request()
        model = genai.GenerativeModel(MODEL_NAME)
        prompt = "Act as a Quant Analyst. Analyze this chart based purely on geometry. Output VERDICT, MARKET STRUCTURE, GEOMETRIC SIGNALS, and TRADE SETUP."
        response = model.generate_content([prompt, {"mime_type": "image/jpeg", "data": image_bytes}])
        return response.text.strip()
    except Exception as e:
        print(f"❌ PURE VISION ERROR: {e}")
        return f"**VERDICT:** ERROR\n**ANALYSIS:** {str(e)}"

# --- TEXT GENERATION ---
def get_ticker_from_query(query: str):
    try:
        configure_gemini_for_request()
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(f"Identify stock ticker for: {query}. Return ONLY the ticker (e.g. RELIANCE.NS).")
        return response.text.strip().replace("", "").upper()
    except Exception as e:
        print(f"❌ SEARCH ERROR: {e}")
        return "ERROR"

def generate_forecast_analysis(company_name: str, analyst_ratings: list, price_target: dict, key_stats: dict, news_headlines: list, currency: str = "USD"):
    try:
        configure_gemini_for_request()
        model = genai.GenerativeModel(MODEL_NAME)
        prompt = f"Write a 2-paragraph forecast summary for {company_name} using this data: Targets: {price_target}, Currency: {currency}."
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"❌ FORECAST ERROR: {e}")
        return "Forecast analysis temporarily unavailable."

def find_peer_tickers_by_industry(company_name: str, sector: str, industry: str, country: str):
    try:
        configure_gemini_for_request()
        model = genai.GenerativeModel(MODEL_NAME)
        prompt = f"List 5 major competitor tickers for {company_name} ({industry}, {country}). Comma separated only. Example: RELIANCE.NS, TCS.NS"
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"❌ PEER ERROR: {e}")
        return ""

# --- LEGACY PLACEHOLDERS (Handled by Math Engine now) ---
def generate_swot_analysis(company_name, description, news): return "Use Local Math Engine"
def generate_investment_philosophy_assessment(company_name, metrics): return "Use Local Math Engine"
def generate_canslim_assessment(company_name, quote, q, y, i): return "Use Local Math Engine"
def generate_fundamental_conclusion(company_name, p, g, d, k, n): return "Use Local Math Engine"
def generate_timeframe_analysis(symbol, timeframe, technicals, pivots, mas): return "Use Local Quant Engine"


def analyze_chart_technicals_from_image(image_bytes: bytes):
    try:
        configure_gemini_for_request()
        model = genai.GenerativeModel(MODEL_NAME)
        prompt = '''Act as an expert Chartered Market Technician. Analyze this stock chart image.
        Provide a professional technical analysis and a precision trade setup based on the timeframe shown in the image.

        STRICT RESPONSE FORMAT (Do not deviate):

        TREND:[Uptrend / Downtrend / Sideways]
        PATTERNS: [List key patterns or "None"]
        MOMENTUM: [Bullish / Bearish / Neutral]
        LEVELS:[List key Support and Resistance price levels visible]
        VOLUME: [Describe volume behavior]
        INDICATORS: [Mention visible indicators]
        CONCLUSION: [A professional 2-sentence summary]
        
        -- TRADE TICKET --
        ACTION:[BUY / SELL / WAIT]
        ENTRY_ZONE:[Price ONLY. e.g., "150.00"]
        STOP_LOSS:[Price ONLY. e.g., "145.00"]
        TARGET_1: [Price ONLY. e.g., "160.00"]
        TARGET_2: [Price ONLY. e.g., "165.00"]
        RISK_REWARD: [Ratio. e.g., "1:3"]
        CONFIDENCE:[High / Medium / Low]
        RATIONALE: [One clear sentence explaining the strategy.]'''
        
        response = model.generate_content([prompt, {"mime_type": "image/jpeg", "data": image_bytes}])
        return response.text.strip()
    except Exception as e:
        print(f"❌ VISION CHART ANALYSIS ERROR: {e}")
        return "TREND: Error\nACTION: WAIT\nRATIONALE: AI failed to process image."
