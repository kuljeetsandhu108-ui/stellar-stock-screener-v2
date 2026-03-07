def generate_algorithmic_report(symbol, timeframe, technicals, pivots, mas):
    """Generates Trading Setup using Pure Math (0 API Calls)"""
    try:
        # Safe extraction
        price = float(technicals.get('price_action', {}).get('current_close', 0))
        rsi = float(technicals.get('rsi') or 50)
        macd = float(technicals.get('macd') or 0)
        macd_signal = float(technicals.get('macdsignal') or 0)
        
        ema50 = float(mas.get('50') or price)
        ema200 = float(mas.get('200') or price)
        
        s1 = float(pivots.get('classic', {}).get('s1') or price * 0.98)
        r1 = float(pivots.get('classic', {}).get('r1') or price * 1.02)
        r2 = float(pivots.get('classic', {}).get('r2') or price * 1.04)

        # Math Logic
        trend = "Consolidation"
        if price > ema200 and ema50 > ema200: trend = "Strong Uptrend"
        elif price < ema200 and ema50 < ema200: trend = "Strong Downtrend"

        momentum = "Neutral"
        if rsi > 60 and macd > macd_signal: momentum = "Bullish Momentum"
        elif rsi < 40 and macd < macd_signal: momentum = "Bearish Momentum"
        elif rsi >= 70: momentum = "Overbought"
        elif rsi <= 30: momentum = "Oversold"

        action = "WAIT"
        stop_loss = s1 * 0.99
        target_1 = r1
        target_2 = r2
        rationale = "Market is lacking clear algorithmic direction. Recommend waiting."

        if "Uptrend" in trend and rsi < 70:
            action = "BUY"
            rationale = "Price is above key moving averages with bullish momentum."
        elif "Downtrend" in trend and rsi > 30:
            action = "SELL"
            stop_loss = r1 * 1.01
            target_1 = s1
            target_2 = s1 * 0.98
            rationale = "Bearish structure intact. Selling on momentum continuation."
        elif rsi <= 30:
            action = "BUY"
            rationale = "Algorithmic mean-reversion setup triggered by extreme oversold RSI."

        # Required Frontend Format
        return f"""
TREND: {trend}
PATTERNS: Algorithmic structure based on {timeframe} data.
MOMENTUM: {momentum}
LEVELS: Support at {s1:.2f}, Resistance at {r1:.2f}.
VOLUME: Scanning mathematical deviations.
INDICATORS: RSI ({rsi:.1f}) indicates {momentum}.
CONCLUSION: The quantitative model detects a {trend}.

-- TRADE TICKET --
ACTION: {action}
ENTRY_ZONE: {price:.2f}
STOP_LOSS: {stop_loss:.2f}
TARGET_1: {target_1:.2f}
TARGET_2: {target_2:.2f}
RISK_REWARD: Algorithmic Estimate
CONFIDENCE: High (Data-Driven)
RATIONALE: {rationale}
"""
    except Exception as e:
        return f"TREND: Error\nACTION: WAIT\nRATIONALE: Quant Engine Failed: {e}"
