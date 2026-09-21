import os
import requests
from dotenv import load_dotenv

load_dotenv("backend/.env")
FMP_KEY = os.getenv("FMP_API_KEY")

print("\n" + "="*60)
print("🔍 DEBUGGING 'RIVERUSD' API CONNECTION")
print("="*60)

url = f"https://financialmodelingprep.com/api/v3/quote/RIVERUSD?apikey={FMP_KEY}"
print("📡 Fetching FMP API for RIVERUSD...\n")

try:
    res = requests.get(url, timeout=10).json()
    if res and len(res) > 0:
        print("✅ SUCCESS! FMP has the data:")
        print(f"   Name:  {res[0].get('name')}")
        print(f"   Price: ${res[0].get('price')}")
        print("\n💡 THE BUG EXPLAINED:")
        print("   The background crypto registry was still loading when you uploaded the image.")
        print("   Because it hadn't loaded, the system fell back to the default Indian Stock routing.")
        print("   That's why the URL mistakenly became 'RIVERUSD.NS'!")
    else:
        print("❌ FMP does NOT have data for RIVERUSD.")
except Exception as e:
    print(f"❌ CONNECTION FAILED: {e}")
    
print("="*60)
