import os
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv()
env_path = BASE_DIR / ".env"
if os.path.exists(env_path):
    load_dotenv(dotenv_path=env_path)

print("🔧 CONFIG LOADED: Yahoo Finance & Binance Engines Active.")
