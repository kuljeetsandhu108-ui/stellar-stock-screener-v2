def calculate_technical_sentiment(technicals: dict):
    """
    Helper function to calculate technical score (0-100) and label
    based on RSI and MACD.
    """
    # --- CRASH GUARD 1: Input Validation ---
    if not technicals or not isinstance(technicals, dict):
        return {"score": 50, "label": "Neutral"}

    rsi = technicals.get('rsi')
    macd = technicals.get('macd')
    macd_signal = technicals.get('macdsignal')
    
    # --- RSI Score (Momentum) ---
    rsi_score = 50
    if rsi is not None:
        if rsi > 70: rsi_score = 85      # Overbought (Strong Momentum)
        elif rsi > 60: rsi_score = 75    # Bullish
        elif rsi > 50: rsi_score = 60    # Mild Bullish
        elif rsi < 30: rsi_score = 35    # Oversold (Weak)
        elif rsi < 40: rsi_score = 40    # Bearish
        else: rsi_score = 45             # Neutral/Weak
        
    # --- MACD Score (Trend) ---
    macd_score = 50
    if macd is not None and macd_signal is not None:
        if macd > macd_signal: 
            macd_score = 80 # Bullish Trend
        else: 
            macd_score = 20 # Bearish Trend
        
    # Combine (Equal Weight)
    t_score = (rsi_score + macd_score) / 2
    
    # Determine Label
    label = "Neutral"
    if t_score >= 60: label = "Bullish"
    elif t_score <= 40: label = "Bearish"
    
    return {"score": t_score, "label": label}


def calculate_overall_sentiment(piotroski_score: int, key_metrics: dict, technicals: dict, analyst_ratings: list):
    """
    Calculates unified sentiment.
    
    CRITICAL FIX: This function now strictly enforces input types.
    If 'key_metrics' comes in as a list (which happens for Commodities/Crypto), 
    it is converted to an empty dict to prevent 'AttributeError'.
    """
    scores = {}
    breakdown = {}

    # --- CRASH GUARD 2: Type Sanitization ---
    # This prevents the specific crash you saw in the screenshot.
    if not isinstance(key_metrics, dict):
        key_metrics = {}
    
    if not isinstance(technicals, dict):
        technicals = {}
        
    if not isinstance(analyst_ratings, list):
        analyst_ratings = []

    # --- 1. FUNDAMENTAL HEALTH (Piotroski) ---
    f_score = 50 # Default neutral
    if piotroski_score is not None:
        # Map 0-9 scale to 0-100
        f_score = (piotroski_score / 9) * 100
    
    scores['fundamental'] = f_score
    breakdown['fundamental'] = {
        "score": f_score,
        "label": "Strong" if f_score > 70 else "Weak" if f_score < 40 else "Stable"
    }

    # --- 2. FINANCIAL PERFORMANCE (Valuation & Efficiency) ---
    # Safe .get() calls on the now-guaranteed dictionary
    pe = key_metrics.get('peRatioTTM')
    roe = key_metrics.get('returnOnCapitalEmployedTTM')

    # Valuation Score
    val_score = 50
    if pe is not None and pe > 0:
        if pe < 15: val_score = 100  # Undervalued
        elif pe < 25: val_score = 75 # Fair
        elif pe < 40: val_score = 40 # Expensive
        else: val_score = 20         # Very Expensive
    
    # Efficiency Score
    eff_score = 50
    if roe is not None:
        if roe > 0.20: eff_score = 100 # Excellent
        elif roe > 0.12: eff_score = 75 # Good
        elif roe > 0.05: eff_score = 50 # Average
        else: eff_score = 25 # Poor

    # Weighted Score (only if data exists)
    fin_score = 50
    if pe is not None or roe is not None:
        fin_score = (val_score * 0.6) + (eff_score * 0.4)
    
    scores['financial'] = fin_score
    breakdown['financial'] = {
        "score": fin_score,
        "label": "Undervalued" if val_score > 70 else "Overvalued" if val_score < 40 else "Fair Value"
    }

    # --- 3. ANALYST CONSENSUS ---
    a_score = 50
    if analyst_ratings and len(analyst_ratings) > 0:
        latest = analyst_ratings[0]
        # Ensure 'latest' is a dict before accessing
        if isinstance(latest, dict):
            total_votes = (
                latest.get('ratingStrongBuy', 0) + 
                latest.get('ratingBuy', 0) + 
                latest.get('ratingHold', 0) + 
                latest.get('ratingSell', 0) + 
                latest.get('ratingStrongSell', 0)
            )
            
            if total_votes > 0:
                weighted_sum = (
                    (latest.get('ratingStrongBuy', 0) * 100) + 
                    (latest.get('ratingBuy', 0) * 75) + 
                    (latest.get('ratingHold', 0) * 50) + 
                    (latest.get('ratingSell', 0) * 25)
                )
                a_score = weighted_sum / total_votes
            
    scores['analyst'] = a_score
    breakdown['analyst'] = {
        "score": a_score,
        "label": "Buy" if a_score > 60 else "Sell" if a_score < 40 else "Hold"
    }

    # --- 4. TECHNICAL MOMENTUM ---
    tech_data = calculate_technical_sentiment(technicals)
    scores['technical'] = tech_data['score']
    breakdown['technical'] = tech_data

    # --- FINAL CALCULATION ---
    total_score = (scores['fundamental'] + scores['financial'] + scores['analyst'] + scores['technical']) / 4

    verdict = "Neutral"
    if total_score >= 75: verdict = "Strong Buy"
    elif total_score >= 60: verdict = "Buy"
    elif total_score <= 25: verdict = "Strong Sell"
    elif total_score <= 40: verdict = "Sell"

    return {
        "score": total_score, 
        "verdict": verdict,
        "breakdown": breakdown
    }