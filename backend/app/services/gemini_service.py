import os
import google.generativeai as genai
from dotenv import load_dotenv
import itertools

load_dotenv()

try:
    GEMINI_API_KEYS_STR = os.getenv("GEMINI_API_KEYS")
    if not GEMINI_API_KEYS_STR:
        single_key = os.getenv("GEMINI_API_KEY") 
        if single_key: GEMINI_API_KEYS = [single_key]
        else: GEMINI_API_KEYS = []
    else:
        GEMINI_API_KEYS = [key.strip() for key in GEMINI_API_KEYS_STR.split(',')]
    key_cycler = itertools.cycle(GEMINI_API_KEYS)
except:
    GEMINI_API_KEYS = []
    key_cycler = None

def configure_gemini_for_request():
    if key_cycler: genai.configure(api_key=next(key_cycler))

def identify_ticker_from_image(image_bytes: bytes):
    try:
        configure_gemini_for_request()
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = """
        Identify the financial asset in this chart image. Return ONLY the ticker symbol.
        
        RULES:
        1. Indian Stocks: Return with .NS suffix (e.g. "RELIANCE" -> "RELIANCE.NS", "TATA" -> "TATAMOTORS.NS").
        2. Indices: Nifty 50 -> "NSEI.INDX", Bank Nifty -> "NSEBANK.INDX", Sensex -> "BSESN.INDX".
        3. US Stocks: Just the ticker (e.g. "AAPL", "TSLA").
        4. Crypto: Add -USD (e.g. "BTC" -> "BTC-USD", "ETH" -> "ETH-USD").
        5. If unsure, return "NOT_FOUND".
        6. OUTPUT FORMAT: Just the string. No explanation.
        """
        
        response = model.generate_content([prompt, {"mime_type": "image/jpeg", "data": image_bytes}])
        return response.text.strip().upper().replace("", "").replace(" ", "")
    except Exception as e:
        print(f"Vision Error: {e}")
        return "NOT_FOUND"

# Keep existing text functions...
def get_ticker_from_query(query: str):
    try:
        configure_gemini_for_request()
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(f"Identify stock ticker for: {query}. Return ONLY the ticker (e.g. RELIANCE.NS).")
        return response.text.strip().replace("", "").upper()
    except: return "ERROR"

def generate_timeframe_analysis(symbol, timeframe, technicals, pivots, mas):
    return "Use Local Quant Engine" 
    # (We are bypassing this for the local engine, but keeping function to avoid import errors)
