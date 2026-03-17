import os
import requests
import json
from dotenv import load_dotenv

# Load Env from Backend folder
load_dotenv("backend/.env")

KEY = os.getenv("EODHD_API_KEY")
SYMBOL = "RELIANCE.NSE" # Testing with Reliance

print("\n" + "="*50)
print(f"🔍 EODHD RAW FINANCIALS DEBUGGER")
print("="*50)

if not KEY:
    print("❌ ERROR: EODHD_API_KEY is missing.")
    exit()

url = f"https://eodhd.com/api/fundamentals/{SYMBOL}?api_token={KEY}&fmt=json"
print(f"📡 Fetching raw payload for {SYMBOL} (This may take a few seconds)...\n")

try:
    response = requests.get(url, timeout=15)
    if response.status_code != 200:
        print(f"❌ API ERROR: Status {response.status_code}")
        exit()
        
    data = response.json()
    financials = data.get("Financials", {})
    
    statements =["Income_Statement", "Balance_Sheet", "Cash_Flow"]
    
    for stmt in statements:
        print(f"\n📑 --- {stmt.replace('_', ' ').upper()} ---")
        yearly = financials.get(stmt, {}).get("yearly", {})
        
        if not yearly:
            print("   ❌ No yearly data found.")
            continue
            
        # Get the most recent year (First key in the dict)
        latest_date = list(yearly.keys())[0]
        latest_data = yearly[latest_date]
        
        print(f"📅 Latest Report Date: {latest_date}")
        print("-" * 30)
        
        for key, value in latest_data.items():
            # Formatting to align columns
            print(f"   {key:<35} : {value}")
            
    print("\n" + "="*50)
    print("✅ DEBUG COMPLETE. Copy the exact keys above if you need them mapped!")

except Exception as e:
    print(f"❌ CONNECTION FAILED: {e}")
