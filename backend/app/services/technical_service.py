import pandas as pd
import pandas_ta as ta
import numpy as np

# ==========================================
# 1. CHART RESAMPLING ENGINE (High-End Speed)
# ==========================================

def resample_chart_data(chart_data: list, target_interval: str):
    """
    Mathematically converts 5-Minute (Base) candles into higher timeframes.
    This enables INSTANT switching between 5M -> 15M -> 1H -> 4H without API calls.
    """
    if not chart_data or len(chart_data) < 2: 
        return []

    try:
        # 1. Convert list of dicts to DataFrame
        df = pd.DataFrame(chart_data)
        
        # 2. Set Index to Datetime (Required for resampling)
        df['datetime'] = pd.to_datetime(df['time'], unit='s')
        df.set_index('datetime', inplace=True)
        
        # 3. Map Frontend Timeframes to Pandas Offset Aliases
        # The frontend sends "15M", "1H", etc.
        mapping = {
            "15M": "15min",
            "30M": "30min",
            "1H": "1h",
            "4H": "4h"
        }
        
        rule = mapping.get(target_interval)
        
        # If no rule found (e.g. '1D' or '1W' which are fetched separately), return original
        if not rule: 
            return chart_data

        # 4. Resample Logic (OHLCV Aggregation)
        # Open  = First price of the bucket
        # High  = Max price of the bucket
        # Low   = Min price of the bucket
        # Close = Last price of the bucket
        # Volume = Sum of volume in the bucket
        resampled = df.resample(rule).agg({
            'open': 'first',
            'high': 'max',
            'low': 'min',
            'close': 'last',
            'volume': 'sum'
        })
        
        # 5. Cleanup
        # Remove rows with NaN (which happen during market close hours)
        resampled.dropna(inplace=True)
        
        # 6. Format back to Lightweight Charts format
        resampled.reset_index(inplace=True)
        
        # Convert timestamp back to Unix Seconds
        resampled['time'] = resampled['datetime'].astype('int64') // 10**9
        
        # Select and order columns
        final_data = resampled[['time', 'open', 'high', 'low', 'close', 'volume']].to_dict('records')
        
        return final_data

    except Exception as e:
        print(f"Resampling Error: {e}")
        # On error, fallback to returning the original data to prevent crash
        return chart_data

# ==========================================
# 2. INDICATORS (RSI, MACD, STOCH, ADX)
# ==========================================

def calculate_technical_indicators(df: pd.DataFrame):
    """
    Calculates RSI, MACD, Stoch, ADX, ATR using Pandas TA.
    Expects DataFrame with lowercase columns: 'open', 'high', 'low', 'close', 'volume'
    """
    if df is None or df.empty or len(df) < 50:
        return {}
    
    try:
        # Create a copy to prevent SettingWithCopy warnings
        wdf = df.copy()
        
        # Calculate Indicators
        wdf.ta.rsi(length=14, append=True)
        wdf.ta.macd(fast=12, slow=26, signal=9, append=True)
        wdf.ta.stoch(k=14, d=3, smooth_k=3, append=True)
        wdf.ta.adx(length=14, append=True)
        wdf.ta.atr(length=14, append=True)
        wdf.ta.willr(length=14, append=True)
        wdf.ta.bbands(length=20, std=2, append=True)

        # Get Latest Data Point
        latest = wdf.iloc[-1]
        prev = wdf.iloc[-2] if len(wdf) > 1 else latest
        
        # Helper to safely extract float values (Handles NaN/None)
        def get_val(key):
            val = latest.get(key)
            if val is None or pd.isna(val):
                return None
            return float(val)

        return {
            "rsi": get_val('RSI_14'),
            "macd": get_val('MACD_12_26_9'),
            "macdsignal": get_val('MACDs_12_26_9'),
            "stochasticsk": get_val('STOCHk_14_3_3'),
            "adx": get_val('ADX_14'),
            "atr": get_val('ATRr_14'),
            "williamsr": get_val('WILLR_14'),
            "bollingerBands": {
                "upperBand": get_val('BBU_20_2.0'),
                "middleBand": get_val('BBM_20_2.0'),
                "lowerBand": get_val('BBL_20_2.0'),
            },
            # Context for AI Analysis
            "price_action": {
                "current_close": get_val('close'),
                "prev_close": float(prev['close']),
                "trend": "UP" if get_val('close') > float(prev['close']) else "DOWN"
            }
        }
    except Exception as e:
        print(f"Technical Indicator Calc Error: {e}")
        return {}

# ==========================================
# 3. MOVING AVERAGES (SMA)
# ==========================================

def calculate_moving_averages(df: pd.DataFrame):
    """
    Calculates Simple Moving Averages (5, 10, 20, 50, 100, 200).
    """
    if df is None or df.empty: return {}
    
    try:
        wdf = df.copy()
        mas = {}
        
        periods = [5, 10, 20, 50, 100, 200]
        
        for p in periods:
            if len(wdf) >= p:
                # Rolling mean is faster than pandas_ta for simple SMA
                val = wdf['close'].rolling(window=p).mean().iloc[-1]
                mas[str(p)] = float(val)
            else:
                mas[str(p)] = None
                
        return mas
    except Exception as e:
        print(f"MA Calc Error: {e}")
        return {}

# ==========================================
# 4. PIVOT POINTS (Classic, Fib, Camarilla)
# ==========================================

def calculate_pivot_points(df: pd.DataFrame):
    """
    Calculates Pivots based on the PREVIOUS candle (High/Low/Close).
    """
    if df is None or len(df) < 2: return {}
    
    try:
        # We need the previous completed candle
        prev = df.iloc[-2]
        
        h = float(prev['high'])
        l = float(prev['low'])
        c = float(prev['close'])
        
        # Classic Pivot
        pp = (h + l + c) / 3
        range_val = h - l
        
        classic = {
            "pp": pp,
            "r1": (2 * pp) - l,
            "s1": (2 * pp) - h,
            "r2": pp + range_val,
            "s2": pp - range_val,
            "r3": h + 2 * (pp - l),
            "s3": l - 2 * (h - pp)
        }
        
        # Fibonacci Pivot
        fib = {
            "pp": pp,
            "r1": pp + (0.382 * range_val),
            "s1": pp - (0.382 * range_val),
            "r2": pp + (0.618 * range_val),
            "s2": pp - (0.618 * range_val),
            "r3": pp + range_val,
            "s3": pp - range_val
        }
        
        # Camarilla Pivot
        cam = {
            "pp": pp,
            "r1": c + (range_val * 1.1 / 12),
            "s1": c - (range_val * 1.1 / 12),
            "r2": c + (range_val * 1.1 / 6),
            "s2": c - (range_val * 1.1 / 6),
            "r3": c + (range_val * 1.1 / 4),
            "s3": c - (range_val * 1.1 / 4)
        }

        return {
            "classic": classic,
            "fibonacci": fib,
            "camarilla": cam
        }
    except Exception as e:
        print(f"Pivot Calc Error: {e}")
        return {}

# ==========================================
# 5. DARVAS BOX SCAN
# ==========================================

def calculate_darvas_box(hist_df: pd.DataFrame, quote: dict, currency: str = "USD"):
    """
    Checks if stock is in a Darvas Box (Consolidation near Highs).
    """
    if hist_df is None or len(hist_df) < 30 or not quote:
        return {"status": "Neutral", "message": "Insufficient data for Darvas scan."}

    try:
        current_price = quote.get('price')
        # Use chart high if quote yearHigh is missing
        year_high = quote.get('yearHigh') or hist_df['high'].max()
        
        if not current_price or not year_high:
            return {"status": "Neutral", "message": "Price data unavailable."}

        # 1. Price Proximity Check (Must be within 15% of 52W High)
        if current_price < (year_high * 0.85):
            return {
                "status": "Not a Candidate",
                "message": f"Price is {((year_high - current_price)/year_high)*100:.1f}% below 52-week high."
            }

        # 2. Box Formation Check (Last 20 days)
        recent = hist_df.tail(20)
        box_top = recent['high'].max()
        box_bottom = recent['low'].min()
        
        # Is the box tight? (< 15% depth)
        box_depth = (box_top - box_bottom) / box_top
        if box_depth > 0.15:
             return {
                "status": "Volatile",
                "message": "Consolidation is too loose (>15% range)."
            }

        # 3. Breakout Status
        currency_sym = "₹" if currency == "INR" else "$"
        
        if current_price >= box_top:
            return {
                "status": "Breakout!",
                "message": f"Breaking out of box ({currency_sym}{box_top:.2f}).",
                "box_top": box_top, "box_bottom": box_bottom, "result": "Pass"
            }
        elif current_price <= box_bottom:
             return {
                "status": "Breakdown",
                "message": f"Falling below support ({currency_sym}{box_bottom:.2f}).",
                "box_top": box_top, "box_bottom": box_bottom, "result": "Fail"
            }
        else:
            return {
                "status": "In Box",
                "message": f"Consolidating between {currency_sym}{box_bottom:.2f} and {currency_sym}{box_top:.2f}.",
                "box_top": box_top, "box_bottom": box_bottom, "result": "Neutral"
            }

    except Exception as e:
        print(f"Darvas Error: {e}")
        return {"status": "Error", "message": "Calculation failed."}

# ==========================================
# 6. EXTENDED TECHNICALS (Multi-Timeframe AI)
# ==========================================

def calculate_extended_technicals(df: pd.DataFrame):
    """
    Wraps standard calculation but flattens the structure for the AI prompt.
    """
    if df is None or df.empty: return None
    
    try:
        inds = calculate_technical_indicators(df)
        mas = calculate_moving_averages(df)
        pivots = calculate_pivot_points(df)
        
        return {
            "price": inds.get('price_action', {}).get('current_close'),
            "rsi": inds.get('rsi'),
            "macd": inds.get('macd'),
            "macd_signal": inds.get('macdsignal'),
            "stoch_k": inds.get('stochasticsk'),
            "adx": inds.get('adx'),
            "ema_20": mas.get('20'),
            "ema_50": mas.get('50'),
            "ema_200": mas.get('200'),
            "pivot": pivots.get('classic', {}).get('pp'),
            "support": {"s1": pivots.get('classic', {}).get('s1'), "s2": pivots.get('classic', {}).get('s2')},
            "resistance": {"r1": pivots.get('classic', {}).get('r1'), "r2": pivots.get('classic', {}).get('r2')}
        }
    except:
        return None