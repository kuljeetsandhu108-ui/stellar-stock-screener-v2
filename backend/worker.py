import asyncio
import os
import sys
import logging
from dotenv import load_dotenv

# Ensure import path is correct
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load Env
load_dotenv()

# Force Unbuffered Output (So logs appear in Railway instantly)
os.environ["PYTHONUNBUFFERED"] = "1"

# Logging Setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Worker")

# Import Services
from backend.app.services.stream_hub import producer
from backend.app.services.redis_service import redis_client

async def run_worker():
    print("==================================================")
    print("👷 TICKER WORKER STARTING (High-Speed Mode)")
    print("==================================================")
    
    # 1. Test Redis Connection Explicitly
    print("🔍 Testing Redis Connection...")
    try:
        # We assume redis_client handles the connection logic
        # Just triggering a dummy publish to verify connectivity
        await redis_client.publish_update("HEARTBEAT", {"status": "alive"})
        print("✅ Redis Pub/Sub is ACTIVE.")
    except Exception as e:
        print(f"❌ Redis Connection FAILED: {e}")
        return # Exit if Redis is dead

    # 2. Start the Data Producer
    print("🚀 Launching Data Producer Engine...")
    await producer.start()

    # 3. Keep Alive Loop
    counter = 0
    while True:
        await asyncio.sleep(10)
        counter += 10
        if counter % 60 == 0:
            print(f"💓 Worker is alive and processing ({counter}s uptime)...")

if __name__ == "__main__":
    try:
        asyncio.run(run_worker())
    except KeyboardInterrupt:
        print("🛑 Worker shutting down.")
    except Exception as e:
        print(f"❌ Worker Fatal Error: {e}")