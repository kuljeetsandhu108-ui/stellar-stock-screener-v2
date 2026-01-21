import os
from dotenv import load_dotenv
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# 1. Try loading from the current directory (Root)
load_dotenv()

# 2. Try loading from the backend directory (Explicit fallback)
env_path = BASE_DIR / ".env"
if os.path.exists(env_path):
    load_dotenv(dotenv_path=env_path)

print(f"🔧 CONFIG LOADED. EODHD Key found: {'YES' if os.getenv('EODHD_API_KEY') else 'NO'}")