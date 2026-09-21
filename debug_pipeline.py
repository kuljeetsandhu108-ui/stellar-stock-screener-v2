import sys
import os
import requests
import json

print("="*60)
print("🔍 TESTING STELLAR DATA PIPELINES")
print("="*60)

# 1. Test Binance Dedicated Public Market Endpoint
print("\n1. Testing Binance Public Crypto REST...")
binance_urls = [
    "https://data-api.binance.vision/api/v3/ticker/24hr?symbol=BTCUSDT",
    "https://api.binance.com/api/v3/ticker/24hr?symbol=BTCUSDT",
    "https://api1.binance.com/api/v3/ticker/24hr?symbol=BTCUSDT"
]

binance_success = False
for url in binance_urls:
    try:
        r = requests.get(url, timeout=4)
        if r.status_code == 200:
            data = r.json()
            print(f"   ✅ SUCCESS ({url.split('/')[2]}): BTC Price = ${float(data['lastPrice']):,.2f} | 24h Chg = {data['priceChangePercent']}%")
            binance_success = True
            break
        else:
            print(f"   ⚠️ Failed {url.split('/')[2]} (Status: {r.status_code})")
    except Exception as e:
        print(f"   ⚠️ Connection blocked on {url.split('/')[2]}: {e}")

# 2. Test Yahoo Finance Indian Equities
print("\n2. Testing Yahoo Finance Indian Stocks...")
try:
    import yfinance as yf
    t = yf.Ticker("RELIANCE.NS")
    fi = t.fast_info
    print(f"   ✅ SUCCESS: RELIANCE.NS Price = ₹{fi.last_price:,.2f} | MCap = ₹{fi.market_cap:,.0f}")
except Exception as e:
    print(f"   ❌ Yahoo Indian Stocks Failed: {e}")

# 3. Test Yahoo Finance Indices
print("\n3. Testing Yahoo Finance Indices & Commodities...")
try:
    t_nifty = yf.Ticker("^NSEI")
    t_gold = yf.Ticker("GC=F")
    print(f"   ✅ SUCCESS: NIFTY 50 = {t_nifty.fast_info.last_price:,.2f} | GOLD = ${t_gold.fast_info.last_price:,.2f}")
except Exception as e:
    print(f"   ❌ Yahoo Indices Failed: {e}")

print("\n" + "="*60)
print("🎯 PIPELINE DIAGNOSTIC COMPLETE")
print("="*60)
