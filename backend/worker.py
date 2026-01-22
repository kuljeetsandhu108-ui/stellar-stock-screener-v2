import asyncio
import os
import sys
from dotenv import load_dotenv

# Ensure we can import from the app folder
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load Env
load_dotenv()

# Import the Producer
from backend.app.services.stream_hub import producer

async def main():
    print("👷 DEDICATED TICKER WORKER STARTED")
    print("   -> Maintaining 1 Stable Connection to Fyers/FMP")
    print("   -> Broadcasting to Redis Pub/Sub")
    
    # This runs forever
    await producer.start()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Worker shutting down")