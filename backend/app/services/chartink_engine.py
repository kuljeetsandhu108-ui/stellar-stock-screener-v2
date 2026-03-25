import requests
from bs4 import BeautifulSoup

# --- CENTRALIZED SCREENER REGISTRY ---
SCREENERS = {
    "bullish_reversal": {
        "id": "bullish_reversal",
        "name": "Bullish Reversal",
        "description": "RSI Crossover + Stochastic Momentum + Volume Expansion",
        "url": "https://chartink.com/screener/copy-bullish-reversal-538",
        "scan_clause": "( {cash} (  daily slow stochastic %d( 14,3 ) <=  70 and  daily slow stochastic %k( 14,3 ) >  daily slow stochastic %d( 14,3 ) and  daily rsi( 14 ) >  1 day ago rsi( 14 ) and  1 day ago  rsi( 14 ) <=  2 day ago  rsi( 14 ) and  daily rsi( 14 ) <=  80 and  daily volume >  150000 and  daily slow stochastic %k( 14,3 ) >  1 day ago slow stochastic %k( 14,3 ) and  1 day ago slow stochastic %k( 14,3 ) <  2 days ago slow stochastic %k( 14,3 ) and  daily close >=  10 and  2 days ago slow stochastic %k( 14,3 ) <  3 days ago slow stochastic %k( 14,3 ) ) )"
    },
    "momentum_vidya": {
        "id": "momentum_vidya",
        "name": "Momentum Swing",
        "description": "Futures Segment: High momentum stocks surging from recent swing lows.",
        "url": "https://chartink.com/screener/momentum-stocks-vidya",
        "scan_clause": "( {33489} (  daily close >  30 and  daily sma(  daily volume , 50 ) >=  50000 and( {cash} (  daily close >=  5 days ago low *  1.2 or  daily close >=  30 days ago low *  1.3 or  daily close >=  90 days ago low *  1.3 ) ) ) )"
    },
    "longterm_value": {
        "id": "longterm_value",
        "name": "Longterm Value Buy",
        "description": "Nifty 200: High liquidity stocks with stabilizing RSI and trading above 50 SMA.",
        "url": "https://chartink.com/screener/longterm-value-buy",
        "scan_clause": "( {46553} (  daily close *  daily volume >  10000000 and  1 month ago rsi( 14 ) >  54 and  1 month ago rsi( 14 ) <  59 and  daily close >  daily sma( close,50 ) and  2 months ago rsi( 14 ) <  55 ) )"
    },
    "orb_15m_vwap": {
        "id": "orb_15m_vwap",
        "name": "15M VWAP Breakout",
        "description": "Nifty 50 Intraday: High volume stocks breaking above/below the 1st 15-minute candle VWAP.",
        "url": "https://chartink.com/screener/orb-15-min-vwap-bo-59",
        "scan_clause": "( {33492} (  daily volume >  10000000 and( {cash} (  [0] 15 minute vwap >[=1] 15 minute high or  [0] 15 minute vwap <  [=1] 15 minute low ) ) ) )"
    },
    "bullish_next_day": {
        "id": "bullish_next_day",
        "name": "Bullish For Next Day",
        "description": "Futures Segment: Multi-indicator confluence (Ichimoku, MACD, RSI, ADX) for gap-up/momentum plays.",
        "url": "https://chartink.com/screener/copy-bullish-for-next-day-51382",
        "scan_clause": "( {33489} (  daily ema( close,20 ) >  20 and  daily sma( volume,20 ) >=  100000 and  daily ichimoku conversion line( 3,7,14 ) >=  daily ichimoku base line( 3,7,14 ) and  daily ichimoku span a( 3,7,14 ) >=  daily ichimoku span b( 3,7,14 ) and  daily close >=  daily ichimoku cloud bottom( 3,7,14 ) and( {33489} (  daily close >=  daily parabolic sar( 0.02,0.02,0.2 ) and  daily rsi( 10 ) >=  20 and  daily stochrsi( 10 ) >=  20 and  daily cci( 10 ) >=  0 and  daily mfi( 10 ) >=  20 and  daily williams %r( 10 ) >=  -80 and  daily close >=  daily ema( close,14 ) and  daily adx di positive( 10 ) >=  daily adx di negative( 10 ) and  daily aroon up( 10 ) >=  daily aroon down( 10 ) and  daily slow stochastic %k( 5,3 ) >=  daily slow stochastic %d( 5,3 ) and  daily fast stochastic %k( 5,3 ) >=  daily fast stochastic %d( 5,3 ) and  daily close >=  daily sma( close,10 ) ) ) and( {33489} (  daily macd line( 14,5,3 ) >=  daily macd signal( 14,5,3 ) and  daily macd histogram( 14,5,3 ) >=  0 ) ) and( {33489} (  daily rsi( 14 ) >  50 and  daily stochrsi( 14 ) >  50 and  daily rsi( 10 ) <  80 and  daily close >=  daily upper bollinger band( 20,2 ) and  daily close >=  daily ichimoku cloud bottom( 9,26,52 ) and  daily close >  daily open and  daily volume >  100000 and  daily ema( close,5 ) >  daily ema( close,20 ) and  daily ema( close,20 ) >  daily ema( close,50 ) and  daily close >  daily ema( close,50 ) ) ) ) )"
    },
    "top_gainers_today": {
        "id": "top_gainers_today",
        "name": "Today's Top Gainers",
        "description": "Cash Segment: High volume stocks closing higher than yesterday, priced above 100.",
        "url": "https://chartink.com/screener/today-s-top-gainers",
        "scan_clause": "( {cash} (  daily close >  1 day ago close and  daily close >  100 and  daily volume >  100000 ) )"
    },
    "top_losers": {
        "id": "top_losers",
        "name": "Top Losers",
        "description": "Cash Segment: Stocks closing lower than yesterday.",
        "url": "https://chartink.com/screener/top-losers-1",
        "scan_clause": "( {cash} (  daily close <  1 day ago close ) )"
    }
}

def fetch_screener(screener_key: str):
    """Stealth Scraping Engine: Mimics Chrome & Bypasses CSRF"""
    config = SCREENERS.get(screener_key)
    if not config: return[]
    
    try:
        with requests.Session() as s:
            # 1. Stealth Headers
            s.headers.update({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
            })
            
            # 2. Extract specific CSRF token from the exact URL
            r = s.get(config['url'], timeout=10)
            soup = BeautifulSoup(r.text, 'html.parser')
            meta = soup.select_one('meta[name="csrf-token"]')
            
            if not meta: return[]
                
            # 3. Post Payload with AJAX Headers
            s.headers.update({
                'X-CSRF-TOKEN': meta['content'],
                'X-Requested-With': 'XMLHttpRequest',
                'Origin': 'https://chartink.com',
                'Referer': config['url']
            })
            
            res = s.post('https://chartink.com/screener/process', data={'scan_clause': config['scan_clause']}, timeout=10)
            
            if res.status_code == 200:
                data = res.json().get('data', [])
                return data[:20] # Top 20 results for UI performance
                
        return[]
    except Exception as e:
        print(f"⚠️ Chartink Engine Error [{screener_key}]: {e}")
        return[]

def get_all_screener_configs():
    """Returns metadata for the React UI Tabs"""
    return[{"key": k, "name": v["name"], "description": v["description"]} for k, v in SCREENERS.items()]
