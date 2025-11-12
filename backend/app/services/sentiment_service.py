def calculate_overall_sentiment(piotroski_score: int, pe_ratio, analyst_ratings: list, rsi):
    """
    Calculates a hybrid sentiment score from 0 to 100 based on four pillars:
    Fundamental Health, Valuation, Analyst Opinion, and Technical Momentum.
    """
    scores = {}
    
    # Pillar 1: Fundamental Health (Piotroski Score) - Weight: 30%
    if piotroski_score is not None:
        # Scale 0-9 score to 0-100
        scores['fundamental'] = (piotroski_score / 9) * 100
    
    # Pillar 2: Valuation (P/E Ratio) - Weight: 20%
    if pe_ratio is not None and pe_ratio > 0:
        if pe_ratio < 15: scores['valuation'] = 100  # Very Undervalued
        elif pe_ratio < 25: scores['valuation'] = 75   # Fairly Valued
        elif pe_ratio < 40: scores['valuation'] = 40   # Expensive
        else: scores['valuation'] = 10               # Very Expensive
        
    # Pillar 3: Analyst Opinion - Weight: 30%
    if analyst_ratings and len(analyst_ratings) > 0:
        latest_rating = analyst_ratings[0]
        strong_buy = latest_rating.get('ratingStrongBuy', 0)
        buy = latest_rating.get('ratingBuy', 0)
        hold = latest_rating.get('ratingHold', 0)
        sell = latest_rating.get('ratingSell', 0)
        strong_sell = latest_rating.get('ratingStrongSell', 0)
        
        total_analysts = strong_buy + buy + hold + sell + strong_sell
        if total_analysts > 0:
            # Weighted score: Strong Buy=5, Buy=4, Hold=3, Sell=2, Strong Sell=1
            score = (strong_buy*5 + buy*4 + hold*3 + sell*2 + strong_sell*1) / total_analysts
            # Scale 1-5 score to 0-100
            scores['analyst'] = ((score - 1) / 4) * 100
            
    # Pillar 4: Technical Momentum (RSI) - Weight: 20%
    if rsi is not None:
        # We treat RSI as a contrarian indicator for sentiment.
        # Very oversold (<30) is bullish, very overbought (>70) is bearish.
        if rsi < 30: scores['technical'] = 100 # Oversold (Bullish sentiment)
        elif rsi > 70: scores['technical'] = 0  # Overbought (Bearish sentiment)
        else:
            # Linear scale for the neutral zone
            scores['technical'] = 100 - ((rsi - 30) / (70 - 30)) * 100
            
    # --- Final Calculation ---
    if not scores:
        return {"score": 50, "verdict": "Neutral"} # Default if no data is available

    # Weighted average of all available scores
    total_score = 0
    total_weight = 0
    weights = {'fundamental': 0.3, 'valuation': 0.2, 'analyst': 0.3, 'technical': 0.2}
    
    for pillar, score in scores.items():
        total_score += score * weights[pillar]
        total_weight += weights[pillar]
        
    final_score = total_score / total_weight if total_weight > 0 else 50

    # Determine a human-readable verdict
    verdict = "Neutral"
    if final_score > 75: verdict = "Very Bullish"
    elif final_score > 60: verdict = "Bullish"
    elif final_score < 25: verdict = "Very Bearish"
    elif final_score < 40: verdict = "Bearish"

    return {"score": final_score, "verdict": verdict}