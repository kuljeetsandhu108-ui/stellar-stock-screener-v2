import os
import requests
from dotenv import load_dotenv

# Load Env from Backend folder
load_dotenv("backend/.env")

KEY = os.getenv("EODHD_API_KEY")
SYMBOL = "RELIANCE.NSE" # We can use Reliance as a solid test case

print("\n" + "="*60)
print(f"🔍 EODHD RAW HISTORICAL SHARES DEBUGGER [{SYMBOL}]")
print("="*60)

if not KEY:
    print("❌ ERROR: EODHD_API_KEY is missing in backend/.env")
    exit()

url = f"https://eodhd.com/api/fundamentals/{SYMBOL}?api_token={KEY}&fmt=json"
print("📡 Fetching raw historical payload (This may take a few seconds)...\n")

try:
    response = requests.get(url, timeout=15)
    if response.status_code != 200:
        print(f"❌ API ERROR: Status {response.status_code}")
        exit()
        
    data = response.json()
    financials = data.get("Financials", {})
    
    # 1. Check Income Statement (weightedAverageShsOut)
    print("📑 --- INCOME STATEMENT (weightedAverageShsOut) ---")
    inc_yearly = financials.get("Income_Statement", {}).get("yearly", {})
    if inc_yearly:
        for date_str, record in list(inc_yearly.items())[:5]:
            shares1 = record.get("weightedAverageShsOut")
            shares2 = record.get("WeightedAverageShsOut") # Check alternate capitalization
            val = shares1 if shares1 is not None else shares2
            print(f"   📅 {date_str} : {val}")
    else:
        print("   ❌ No Income Statement data found.")

    # 2. Check Balance Sheet (commonStockSharesOutstanding)
    print("\n📑 --- BALANCE SHEET (commonStockSharesOutstanding) ---")
    bal_yearly = financials.get("Balance_Sheet", {}).get("yearly", {})
    if bal_yearly:
        for date_str, record in list(bal_yearly.items())[:5]:
            shares1 = record.get("commonStockSharesOutstanding")
            shares2 = record.get("CommonStockSharesOutstanding")
            val = shares1 if shares1 is not None else shares2
            print(f"   📅 {date_str} : {val}")
    else:
        print("   ❌ No Balance Sheet data found.")
        
    print("\n" + "="*60)
    print("✅ DEBUG COMPLETE. Please paste this terminal output back to me!")

except Exception as e:
    print(f"❌ CONNECTION FAILED: {e}")
