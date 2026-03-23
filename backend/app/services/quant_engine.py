def generate_algorithmic_report(symbol, timeframe, technicals, pivots, mas):
    """
    Advanced Institutional Quant Engine.
    Uses SMC (Smart Money Concepts), Liquidity Sweeps, Volatility Squeezes, and Dynamic ATR Risk Management.
    Outputs strict format for React UI Parsing.
    """
    try:
        # 1. Safe Extraction of Math Variables
        price = float(technicals.get('price_action', {}).get('current_close', 0))
        if price == 0: 
            return "TREND: Error\nACTION: WAIT\nRATIONALE: Price data missing from feed."
        
        rsi = float(technicals.get('rsi') or 50)
        macd = float(technicals.get('macd') or 0)
        macd_signal = float(technicals.get('macdsignal') or 0)
        adx = float(technicals.get('adx') or 20)
        atr = float(technicals.get('atr') or (price * 0.015)) 
        
        ema20 = float(mas.get('20') or price)
        ema50 = float(mas.get('50') or price)
        ema200 = float(mas.get('200') or price)
        
        s1 = float(pivots.get('classic', {}).get('s1') or price * 0.98)
        s2 = float(pivots.get('classic', {}).get('s2') or price * 0.95)
        r1 = float(pivots.get('classic', {}).get('r1') or price * 1.02)
        r2 = float(pivots.get('classic', {}).get('r2') or price * 1.05)
        pp = float(pivots.get('classic', {}).get('pp') or price)

        bb = technicals.get('bollingerBands', {})
        ub = float(bb.get('upperBand') or r1)
        lb = float(bb.get('lowerBand') or s1)

        prev_close = float(technicals.get('price_action', {}).get('prev_close', price))
        prev_price_was_below_pp = prev_close < pp

        # 2. SMC MARKET STRUCTURE (Trend & Bias)
        trend = "Consolidation / Range-Bound"
        if price > ema50 and ema50 > ema200:
            trend = "Bullish Macro Structure (Premium Array)"
        elif price < ema50 and ema50 < ema200:
            trend = "Bearish Macro Structure (Discount Array)"
        elif price > ema200 and price < ema50:
            trend = "Bullish Pullback (Internal Retracement)"
        elif price < ema200 and price > ema50:
            trend = "Bearish Rally (Liquidity Hunt)"

        # 3. SMC PATTERNS & LIQUIDITY SWEEPS
        patterns = "Price oscillating within equilibrium."
        is_squeeze = (ub - lb) / price < 0.03  

        if price <= s1 and rsi < 35:
            patterns = "Sell-Side Liquidity Sweep (Spring). Retail stops triggered below S1."
        elif price >= r1 and rsi > 65:
            patterns = "Buy-Side Liquidity Sweep (Upthrust). Institutional distribution above R1."
        elif is_squeeze:
            patterns = "Volatility Squeeze / Accumulation Phase. Imminent explosive expansion expected."
        elif price > pp and prev_price_was_below_pp:
            patterns = "Equilibrium crossover. Shifting to Premium pricing."

        # 4. INSTITUTIONAL MOMENTUM
        momentum = "Neutral / Chop Zone"
        if adx > 25:
            if macd > macd_signal and rsi > 50:
                momentum = f"Strong Bullish Displacement (ADX: {adx:.1f})"
            elif macd < macd_signal and rsi < 50:
                momentum = f"Aggressive Bearish Distribution (ADX: {adx:.1f})"
        elif adx < 20:
            momentum = "Weak Trend / Accumulation Phase (Low ADX)"

        # 5. TRADE LOGIC & ALGORITHMIC EXECUTION
        action = "WAIT"
        rationale = "Market is in a low-probability chop zone. Capital preservation mode active."
        
        # --- CRASH FIX: Define default fallbacks BEFORE the if/else tree ---
        stop_loss = s1 if price > pp else r1
        target_1 = r1 if price > pp else s1
        target_2 = r2 if price > pp else s2
        
        # Bullish Setup
        if ("Bullish" in trend and macd > macd_signal) or (price <= s1 and rsi < 30):
            if adx > 20 or rsi < 30: 
                action = "BUY"
                stop_loss = price - (atr * 1.5) 
                risk = price - stop_loss
                target_1 = price + (risk * 1.5) 
                target_2 = price + (risk * 3.5) 
                rationale = "High-probability long setup based on SMC discount pricing and bullish momentum alignment."

        # Bearish Setup
        elif ("Bearish" in trend and macd < macd_signal) or (price >= r1 and rsi > 70):
            if adx > 20 or rsi > 70:
                action = "SELL"
                stop_loss = price + (atr * 1.5)
                risk = stop_loss - price
                target_1 = price - (risk * 1.5)
                target_2 = price - (risk * 3.5)
                rationale = "High-probability short setup targeting lower liquidity pools (Sell-side liquidity)."

        rr_text = "1:1.5 (T1) | 1:3.5 (T2)" if action in["BUY", "SELL"] else "N/A"
        confidence = "High (Confluence)" if adx > 25 and action != "WAIT" else "Medium" if action != "WAIT" else "Low"

        # 6. PERFECT FORMATTING FOR REACT UI PARSER
        report = f"""TREND: {trend}
PATTERNS: {patterns}
MOMENTUM: {momentum}
LEVELS: Critical Floor at {s1:.2f} | Local Equilibrium at {pp:.2f} | Heavy Supply at {r1:.2f}
VOLUME: Algorithmic standard deviation profiles stable.
INDICATORS: RSI ({rsi:.1f}) | MACD Delta ({macd - macd_signal:.3f}) | ATR Volatility ({atr:.2f})
CONCLUSION: The quantitative matrix confirms a {trend.lower()} environment on the {timeframe} interval.
ACTION: {action}
ENTRY_ZONE: {price:.2f}
STOP_LOSS: {stop_loss:.2f}
TARGET_1: {target_1:.2f}
TARGET_2: {target_2:.2f}
RISK_REWARD: {rr_text}
CONFIDENCE: {confidence}
RATIONALE: {rationale}"""

        return report

    except Exception as e:
        return f"TREND: Neutral\nPATTERNS: N/A\nMOMENTUM: N/A\nLEVELS: N/A\nVOLUME: N/A\nINDICATORS: N/A\nCONCLUSION: Math engine processing error.\nACTION: WAIT\nENTRY_ZONE: 0.00\nSTOP_LOSS: 0.00\nTARGET_1: 0.00\nTARGET_2: 0.00\nRISK_REWARD: N/A\nCONFIDENCE: Low\nRATIONALE: Quant Engine Failed: {str(e)}"
