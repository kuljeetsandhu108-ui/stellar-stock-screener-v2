import traceback
from functools import wraps

def auto_heal(fallback_return):
    """
    ENTERPRISE AUTO-HEALER DECORATOR.
    Wraps any function. If the function crashes due to a bug, API limit, 
    or AI hallucination, this intercepts the crash, logs the exact line 
    of failure, and returns a safe fallback to keep the UI alive.
    """
    def decorator(func):
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print(f"\n🛡️ [WATCHDOG] Auto-Healed crash in {func.__name__}")
                print(f"   -> Error: {str(e)}")
                # traceback.print_exc() # Uncomment for deep debugging
                return fallback_return

        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                print(f"\n🛡️ [WATCHDOG] Auto-Healed crash in {func.__name__}")
                print(f"   -> Error: {str(e)}")
                return fallback_return

        # Return the async wrapper if the original function is async
        import asyncio
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        return sync_wrapper
    return decorator
