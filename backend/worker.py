import asyncio
import os
import sys
import logging
from dotenv import load_dotenv

# Ensure we can import from the app folder
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load Env
load_dotenv()

# Setup Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Worker")

# Import the Producer
from backend.app.services.stream_hub import producer
from backend.app.services.redis_service import redis_client

async def run_worker():
    print("==================================================")
    print("👷 DEDICATED TICKER WORKER STARTED")
    print("==================================================")
    
    # 1. Force Redis Connection Check
    print("🔍 Checking Redis Connection...")
    # We call a private method to force check, or just add a dummy symbol
    await redis_client.add_active_symbol("HEARTBEAT_CHECK")
    
    # 2. Start the Producer
    # The producer handles the Fyers/FMP loops internally
    print("🚀 Launching Stream Producer...")
    await producer.start()

    # 3. Keep Alive Loop
    # This prevents the script from exiting
    while True:
        await asyncio.sleep(60)
        print("💓 Worker Heartbeat: Still running...")

if __name__ == "__main__":
    try:
        # Use asyncio.run for the top-level entry point
        asyncio.run(run_worker())
    except KeyboardInterrupt:
        print("🛑 Worker shutting down gracefully.")
    except Exception as e:
        print(f"❌ Worker Crashed: {e}")