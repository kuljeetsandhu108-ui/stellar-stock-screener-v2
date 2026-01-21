import os
from dotenv import load_dotenv

# Try loading from specific path to be sure
load_dotenv("backend/.env")

print("--- DIAGNOSTIC ---")
print(f"EODHD Key: {os.getenv('EODHD_API_KEY')}")
print(f"FMP Key:   {os.getenv('FMP_API_KEY')}")
print(f"Redis URL: {os.getenv('REDIS_URL')}")
print("------------------")