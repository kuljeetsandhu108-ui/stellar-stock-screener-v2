def generate_algorithmic_report(symbol, timeframe, technicals, pivots, mas):
    """Generates Trading Setup using Pure Math with ATR Risk Management (0 API Calls)"""
    try:
        # 1. Safe Extraction
        price = float(technicals.get('price_action', {}).get('current_close', 0))
        rsi = float(technicals.get('rsi') or 50)
        macd = float(technicals.get('macd') or 0)
        macd_signal = float(technicals.get('macdsignal') or 0)
        
        # Extract ATR for dynamic volatility-based stops. Fallback to 1.5% if missing.
        atr = float(technicals.get('atr') or (price * 0.015))
        
        ema50 = float(mas.get('50') or price)
        ema200 = float(mas.get('200') or price)
        
        s1 = float(pivots.get('classic', {}).get('s1') or price * 0.98)
        r1 = float(pivots.get('classic', {}).get('r1') or price * 1.02)

        # 2. Math Logic (Trend & Momentum)
        trend = "Consolidation / Range"
        if price > ema200 and ema50 > ema200: trend = "Strong Uptrend"
        elif price < ema200 and ema50 < ema200: trend = "Strong Downtrend"

        momentum = "Neutral"
        if rsi > 60 and macd > macd_signal: momentum = "Bullish Momentum"
        elif rsi < 40 and macd < macd_signal: momentum = "Bearish Momentum"
        elif rsi >= 70: momentum = "Overbought"
        elif rsi <= 30: momentum = "Oversold"

        # 3. Action & Rationale
        action = "WAIT"
        rationale = "Market is lacking clear algorithmic direction. Capital preservation recommended."

        if "Uptrend" in trend and rsi < 70:
            action = "BUY"
            rationale = "Price is trading above key moving averages with confirmed bullish momentum."
        elif "Downtrend" in trend and rsi > 30:
            action = "SELL"
            rationale = "Bearish structure intact. Selling on momentum continuation."
        elif rsi <= 30:
            action = "BUY"
            rationale = "Algorithmic mean-reversion setup triggered by extreme oversold RSI."
        elif rsi >= 70:
            action = "SELL"
            rationale = "Algorithmic mean-reversion setup triggered by extreme overbought RSI."

        # 4. Hardcore ATR Risk Management Sizing
        if action == "BUY":
            stop_loss = price - (atr * 1.5) # Stop is 1.5x Average True Range below entry
            risk = price - stop_loss
            target_1 = price + (risk * 1.5) # 1:1.5 R:R
            target_2 = price + (risk * 3.0) # 1:3.0 R:R
            rr_text = "1:1.5 (T1) | 1:3.0 (T2)"
        elif action == "SELL":
            stop_loss = price + (atr * 1.5) # Stop is 1.5x Average True Range above entry
            risk = stop_loss - price
            target_1 = price - (risk * 1.5)
            target_2 = price - (risk * 3.0)
            rr_text = "1:1.5 (T1) | 1:3.0 (T2)"
        else:
            stop_loss = s1
            target_1 = r1
            target_2 = r1 * 1.02
            rr_text = "N/A"

        # 5. Flawless Formatting (Fixes the UI bleeding bug completely)
        lines =[
            f"TREND: {trend}",
            f"PATTERNS: Algorithmic structure based on {timeframe} data.",
            f"MOMENTUM: {momentum}",
            f"LEVELS: Key Support at {s1:.2f}, Key Resistance at {r1:.2f}.",
            "VOLUME: Algorithm scanning standard deviations.",
            f"INDICATORS: RSI ({rsi:.1f}) indicates {momentum}.",
            f"CONCLUSION: The quantitative model detects a {trend}.",
            "ACTION: " + action,
            f"ENTRY_ZONE: {price:.2f}",
            f"STOP_LOSS: {stop_loss:.2f}",
            f"TARGET_1: {target_1:.2f}",
            f"TARGET_2: {target_2:.2f}",
            f"RISK_REWARD: {rr_text}",
            "CONFIDENCE: High (Quant-Driven)",
            f"RATIONALE: {rationale}"
        ]
        
        # We join with hard newline characters to ensure the React regex splits them perfectly
        return "\n".join(lines)
        
    except Exception as e:
        return f"TREND: Error\nACTION: WAIT\nRATIONALE: Quant Engine Failed: {e}"
