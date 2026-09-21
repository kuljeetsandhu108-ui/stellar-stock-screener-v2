import requests
import json
from datetime import datetime
import yfinance as yf

BINANCE_MIRRORS = [
    "https://data-api.binance.vision/api/v3",
    "https://api.binance.com/api/v3",
    "https://api1.binance.com/api/v3",
    "https://api3.binance.com/api/v3"
]

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
})

# ==========================================
# 1. CLEAN SYMBOL RESOLVER (BUG FIXED)
# ==========================================

def format_symbol_for_binance(symbol: str) -> str:
    if not symbol:
        return "BTCUSDT"
    s = symbol.upper().strip()
    
    # Clean suffix stripping in strict order
    for suffix in ["-USD.CC", ".CC", "-USDT", "-USD", "USDT", "USD", ".NS", ".BO"]:
        if s.endswith(suffix):
            s = s[:-len(suffix)]
            break
            
    s = s.replace("-", "").replace("/", "").replace(" ", "")
    return f"{s}USDT"

def is_crypto_symbol(symbol: str) -> bool:
    if not symbol:
        return False
    s = symbol.upper().strip()
    known = ["BTC", "ETH", "SOL", "XRP", "DOGE", "ADA", "MATIC", "DOT", "LTC", "SHIB", "AVAX", "BNB", "LINK", "UNI", "PEPE", "NEAR", "SUI"]
    return any(k in s for k in known) or ".CC" in s or "USDT" in s or ("-USD" in s and not any(idx in s for idx in ["^", ".NS", ".BO"]))

# ==========================================
# 2. REAL-TIME QUOTE (MULTI-MIRROR + YAHOO FAILOVER)
# ==========================================

def get_crypto_price(symbol: str) -> dict:
    pair = format_symbol_for_binance(symbol)
    
    # 1. Try Binance Dedicated Public Mirrors
    for base in BINANCE_MIRRORS:
        try:
            url = f"{base}/ticker/24hr?symbol={pair}"
            res = session.get(url, timeout=3)
            if res.status_code == 200:
                data = res.json()
                price = float(data.get("lastPrice", 0.0))
                chg = float(data.get("priceChange", 0.0))
                pct = float(data.get("priceChangePercent", 0.0))
                return {
                    "price": round(price, 2),
                    "change": round(chg, 2),
                    "changesPercentage": round(pct, 2),
                    "percent_change": round(pct, 2),
                    "high": round(float(data.get("highPrice", price)), 2),
                    "low": round(float(data.get("lowPrice", price)), 2),
                    "volume": float(data.get("volume", 0.0)),
                    "previousClose": round(float(data.get("prevClosePrice", price)), 2),
                    "timestamp": int(datetime.now().timestamp())
                }
        except Exception:
            continue

    # 2. Instant Failover to Yahoo Finance Crypto (e.g. BTC-USD)
    try:
        base_sym = pair.replace("USDT", "")
        t = yf.Ticker(f"{base_sym}-USD")
        fi = t.fast_info
        price = float(fi.last_price or 0.0)
        prev = float(fi.previous_close or price)
        chg = price - prev
        pct = (chg / prev) * 100 if prev else 0.0
        return {
            "price": round(price, 2),
            "change": round(chg, 2),
            "changesPercentage": round(pct, 2),
            "percent_change": round(pct, 2),
            "high": round(float(fi.day_high or price), 2),
            "low": round(float(fi.day_low or price), 2),
            "volume": int(fi.last_volume or 0),
            "previousClose": round(prev, 2),
            "timestamp": int(datetime.now().timestamp())
        }
    except Exception as e:
        print(f"⚠️ Crypto quote error: {e}")

    return {}

# ==========================================
# 3. HISTORICAL CANDLESTICK DATA (KLINES)
# ==========================================

def get_crypto_klines(symbol: str, range_type: str = "1D") -> list:
    pair = format_symbol_for_binance(symbol)
    
    interval_map = {
        "1M": "1m", "5M": "5m", "15M": "15m", "30M": "30m",
        "1H": "1h", "4H": "4h", "1D": "1d", "1W": "1w"
    }
    interval = interval_map.get(range_type.upper(), "1d")
    
    # 1. Try Binance Mirrors
    for base in BINANCE_MIRRORS:
        try:
            url = f"{base}/klines?symbol={pair}&interval={interval}&limit=500"
            res = session.get(url, timeout=4)
            if res.status_code == 200:
                raw_klines = res.json()
                candles = []
                for k in raw_klines:
                    candles.append({
                        "time": int(k[0] // 1000),
                        "open": round(float(k[1]), 2),
                        "high": round(float(k[2]), 2),
                        "low": round(float(k[3]), 2),
                        "close": round(float(k[4]), 2),
                        "volume": float(k[5])
                    })
                candles.sort(key=lambda x: x["time"])
                if candles:
                    return candles
        except Exception:
            continue

    # 2. Yahoo Crypto History Failover
    try:
        base_sym = pair.replace("USDT", "")
        t = yf.Ticker(f"{base_sym}-USD")
        df = t.history(period="1y" if range_type.upper() == "1D" else "5d", interval="1d" if range_type.upper() == "1D" else "5m")
        if df is not None and not df.empty:
            df.reset_index(inplace=True)
            date_col = "Datetime" if "Datetime" in df.columns else "Date"
            candles = []
            for _, row in df.iterrows():
                dt_val = row[date_col]
                ts = int(dt_val.timestamp()) if hasattr(dt_val, "timestamp") else int(pd.to_datetime(dt_val).timestamp())
                candles.append({
                    "time": ts,
                    "open": round(float(row["Open"]), 2),
                    "high": round(float(row["High"]), 2),
                    "low": round(float(row["Low"]), 2),
                    "close": round(float(row["Close"]), 2),
                    "volume": float(row.get("Volume", 0.0))
                })
            candles.sort(key=lambda x: x["time"])
            return candles
    except Exception:
        pass

    return []
