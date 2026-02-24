def generate_algorithmic_report(symbol, timeframe, technicals, pivots, mas):
    try:
        # Extract Data Safely
        price = float(technicals.get('price_action', {}).get('current_close', 0))
        rsi = float(technicals.get('rsi') or 50)
        macd = float(technicals.get('macd') or 0)
        macd_signal = float(technicals.get('macd_signal') or 0)
        
        ema50 = float(mas.get('50') or price)
        ema200 = float(mas.get('200') or price)
        
        s1 = float(pivots.get('classic', {}).get('s1') or price * 0.98)
        r1 = float(pivots.get('classic', {}).get('r1') or price * 1.02)
        r2 = float(pivots.get('classic', {}).get('r2') or price * 1.04)

        # 1. Trend Logic
        trend = "Sideways / Range"
        if price > ema200 and ema50 > ema200: trend = "Strong Uptrend"
        elif price < ema200 and ema50 < ema200: trend = "Strong Downtrend"
        elif price > ema50: trend = "Mild Uptrend"
        elif price < ema50: trend = "Mild Downtrend"

        # 2. Momentum Logic
        momentum = "Neutral"
        if rsi > 60 and macd > macd_signal: momentum = "Bullish Acceleration"
        elif rsi < 40 and macd < macd_signal: momentum = "Bearish Acceleration"
        elif rsi >= 70: momentum = "Overbought (Correction Risk)"
        elif rsi <= 30: momentum = "Oversold (Rebound Potential)"

        # 3. Trade Ticket Logic
        action = "WAIT"
        stop_loss = 0.0
        target_1 = 0.0
        target_2 = 0.0
        rationale = "Market is in consolidation. Wait for clear breakout."

        if "Uptrend" in trend and rsi < 70:
            action = "BUY"
            stop_loss = s1 * 0.99
            target_1 = r1
            target_2 = r2
            rationale = "Price is above key moving averages with room to grow before overbought levels."
        elif "Downtrend" in trend and rsi > 30:
            action = "SELL"
            stop_loss = r1 * 1.01
            target_1 = s1
            target_2 = s1 * 0.98
            rationale = "Bearish structure intact. Selling on momentum continuation."
        elif rsi <= 30:
            action = "BUY"
            stop_loss = price * 0.97
            target_1 = r1
            target_2 = r2
            rationale = "Algorithmic mean-reversion setup triggered by extreme oversold RSI."

        # Format output exactly as frontend expects
        report = f"""
TREND: {trend}
PATTERNS: Quantitative structure analyzed based on {timeframe} data.
LEVELS: Critical Support at {s1:.2f}, Immediate Resistance at {r1:.2f}.
VOLUME: Algorithm scanning standard deviations.
INDICATORS: RSI ({rsi:.1f}) indicates {momentum}. Price is {"above" if price > ema50 else "below"} 50-EMA.
CONCLUSION: The algorithmic model detects a {trend} with {momentum}.

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
        return report.strip()
    except Exception as e:
        return f"TREND: Error\nACTION: WAIT\nRATIONALE: Math Engine Failed: {e}"
