def generate_algorithmic_swot(company_name, master_data=None):
    """Generates a highly detailed, data-driven SWOT analysis using pure mathematics."""
    if not master_data:
        master_data = {}
        
    km = master_data.get('key_metrics') or {}
    quote = master_data.get('quote') or {}
    techs = master_data.get('technical_indicators') or {}
    mas = master_data.get('moving_averages') or {}
    piotroski = master_data.get('piotroski_f_score', {}).get('score', 5)
    share_bd = master_data.get('shareholding_breakdown') or {}
    
    # --- SAFE EXTRACTION ---
    pe = km.get('peRatioTTM') or 0
    rev_growth = km.get('revenueGrowth') or 0
    margins = km.get('grossMargins') or 0
    beta = km.get('beta') or 1.0
    roc = km.get('returnOnCapitalEmployedTTM') or 0
    
    price = quote.get('price') or 0
    year_high = quote.get('yearHigh') or 0
    year_low = quote.get('yearLow') or 0
    
    rsi = techs.get('rsi') or 50
    macd = techs.get('macd') or 0
    macd_signal = techs.get('macdsignal') or 0
    ema200 = mas.get('200') or 0
    
    # Calculate "Smart Money" Holdings
    inst_holding = share_bd.get('fii', 0) + share_bd.get('dii', 0)
    
    strengths =[]
    weaknesses = []
    opportunities = []
    threats =[]
    
    # ==========================================
    # 1. CALCULATE STRENGTHS
    # ==========================================
    if piotroski >= 7: strengths.append(f"Exceptional fundamental health with a Piotroski F-Score of {piotroski}/9.")
    if margins > 0.3: strengths.append("High gross profit margins (>30%), indicating strong pricing power and a competitive moat.")
    if roc > 0.15: strengths.append(f"Excellent Return on Capital ({roc*100:.1f}%), showing highly efficient management.")
    if price > ema200 and ema200 > 0: strengths.append("Stock is currently trading above its 200-day moving average, confirming a long-term macro uptrend.")
    if inst_holding > 40: strengths.append(f"Strong 'Smart Money' backing with {inst_holding:.1f}% institutional ownership (FII/DII).")
    
    # Fix the astronomical revenue bug (Ensures it's a valid percentage ratio)
    if 0 < rev_growth < 5: strengths.append(f"Consistent top-line revenue growth ({rev_growth*100:.1f}% YoY).")
        
    if not strengths: strengths.append(f"{company_name} maintains a steady presence in its core market.")

    # ==========================================
    # 2. CALCULATE WEAKNESSES
    # ==========================================
    if piotroski <= 3: weaknesses.append(f"Weak fundamental financial stability (Piotroski F-Score: {piotroski}/9).")
    if pe > 40: weaknesses.append(f"High valuation premium (P/E: {pe:.1f}), reducing the margin of safety for value investors.")
    elif pe < 0: weaknesses.append("Currently operating with negative earnings (Net Loss).")
    if rev_growth < 0: weaknesses.append(f"Declining revenue trend over the past year ({rev_growth*100:.1f}%).")
    if price < ema200 and ema200 > 0: weaknesses.append("Trading below the 200-day moving average, signaling long-term bearish momentum.")
    
    if not weaknesses: weaknesses.append("Susceptible to broader macroeconomic downturns and sector rotations.")

    # ==========================================
    # 3. CALCULATE OPPORTUNITIES
    # ==========================================
    if rsi < 35: opportunities.append(f"Technically oversold conditions (RSI: {rsi:.1f}), presenting a potential mean-reversion buying opportunity.")
    if macd > macd_signal and rsi < 60: opportunities.append("Bullish MACD crossover suggests accelerating short-term upward momentum.")
    if year_low > 0 and price < (year_low * 1.1): opportunities.append("Trading near 52-week lows, potentially offering an attractive risk-to-reward entry for value buyers.")
    opportunities.append("Potential for market share expansion through new product cycles or regional scaling.")
    opportunities.append("Strategic M&A or partnerships could act as significant fundamental catalysts.")

    # ==========================================
    # 4. CALCULATE THREATS
    # ==========================================
    if rsi > 70: threats.append(f"Technically overbought (RSI: {rsi:.1f}), increasing the risk of a sharp short-term price correction.")
    if macd < macd_signal and rsi > 40: threats.append("Bearish MACD crossover indicates building downward sell pressure.")
    if beta > 1.5: threats.append(f"High Beta ({beta:.2f}) indicates the stock is significantly more volatile than the broader market.")
    if year_high > 0 and price > (year_high * 0.95): threats.append("Approaching 52-week highs, which historically acts as heavy overhead resistance.")
    if pe > 50: threats.append("Highly vulnerable to severe valuation contraction if future earnings growth misses expectations.")
    
    threats.append("Regulatory changes and aggressive competitive pressures in the industry.")

    # ==========================================
    # 5. FORMAT AND LIMIT OUTPUT (Max 4 bullets each)
    # ==========================================
    swot_markdown = "**Strengths**\n" + "\n".join([f"- {s}" for s in strengths[:4]]) + "\n\n"
    swot_markdown += "**Weaknesses**\n" + "\n".join([f"- {w}" for w in weaknesses[:4]]) + "\n\n"
    swot_markdown += "**Opportunities**\n" + "\n".join([f"- {o}" for o in opportunities[:4]]) + "\n\n"
    swot_markdown += "**Threats**\n" + "\n".join([f"- {t}" for t in threats[:4]])
    
    return swot_markdown
