import os
import json
import redis
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Railway automatically provides REDIS_URL. 
# If running locally without Redis, this defaults to localhost which might fail gracefully.
REDIS_URL = os.getenv("REDIS_URL")

# Global Redis Client
redis_client = None

def initialize_redis():
    """
    Attempts to connect to Redis. 
    If successful, returns the client. 
    If failed (or no URL), prints a warning and returns None (Caching Disabled).
    """
    global redis_client
    
    if not REDIS_URL:
        print("⚠️  REDIS_URL not found. Caching is DISABLED (Dev Mode).")
        return None

    try:
        # decode_responses=True ensures we get Python Strings back, not Bytes
        client = redis.from_url(REDIS_URL, decode_responses=True)
        
        # Test the connection immediately
        client.ping()
        print("✅ Redis Connected Successfully (High-Speed Cache Active)")
        return client
    except Exception as e:
        print(f"❌ Redis Connection Failed: {e}")
        print("   -> Running in Direct-API Mode (No Caching)")
        return None

# Initialize on startup
redis_client = initialize_redis()

def get_cache(key: str):
    """
    Retrieve data from fast memory.
    Returns: Dict/List if found, None if missing or error.
    """
    if not redis_client: 
        return None
        
    try:
        data = redis_client.get(key)
        if data:
            return json.loads(data)
        return None
    except Exception as e:
        print(f"Redis Read Error ({key}): {e}")
        return None

def set_cache(key: str, data: any, ttl: int = 60):
    """
    Save data to fast memory.
    Args:
        key: Unique identifier string
        data: Python Dict or List (will be JSON stringified)
        ttl: Time To Live in seconds (Default 60s)
    """
    if not redis_client: 
        return
        
    try:
        # Convert Python Object -> JSON String
        json_data = json.dumps(data)
        # Set value with Expiration (ex=ttl)
        redis_client.set(name=key, value=json_data, ex=ttl)
    except TypeError as e:
        print(f"Redis Serialization Error (Data not JSON serializable): {e}")
    except Exception as e:
        print(f"Redis Write Error ({key}): {e}")

def clear_cache_pattern(pattern: str):
    """
    Advanced: clear all keys matching a specific pattern (e.g. 'chart_*')
    Useful for admin tools or manual refresh.
    """
    if not redis_client: return
    try:
        keys = redis_client.keys(pattern)
        if keys:
            redis_client.delete(*keys)
            print(f"Cleared {len(keys)} keys matching '{pattern}'")
    except Exception as e:
        print(f"Redis Clear Error: {e}")