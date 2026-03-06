def generate_canslim_check(master_data):
    """
    Hardcore CANSLIM Logic with Edge-Case Protection.
    Returns: Criteria | Assessment | Result
    """
    if not master_data: return "Data unavailable.|System could not retrieve metrics.|NEUTRAL"
    
    # --- SAFE DATA EXTRACTION ---
    km = master_data.get('key_metrics') or {}
    quote = master_data.get('quote') or {}
    q_earnings = master_data.get('quarterly_income_statements') or []
    y_earnings = master_data.get('annual_revenue_and_profit') or []
    share_bd = master_data.get('shareholding_breakdown') or {}
    
    output_rows = []

    # 1. C - CURRENT EARNINGS (The "Explosive" Check)
    # Target: EPS growth > 18-25% in recent quarters
    c_status = "⚠️ NEUTRAL"
    c_text = "Insufficient quarterly data available."
    
    if len(q_earnings) >= 5:
        curr_eps = q_earnings[0].get('eps') or 0
        prev_eps = q_earnings[4].get('eps') or 0
        
        if prev_eps > 0:
            growth = ((curr_eps - prev_eps) / prev_eps) * 100
            if growth >= 25:
                c_status = "✅ PASS"
                c_text = f"Explosive Growth! Quarterly EPS surged {growth:.1f}% YoY (Target: >25%)."
            elif growth >= 15:
                c_status = "✅ PASS"
                c_text = f"Solid Growth. EPS up {growth:.1f}% YoY."
            elif growth > 0:
                c_status = "❌ FAIL"
                c_text = f"Sluggish. EPS grew only {growth:.1f}% (Needs >18%)."
            else:
                c_status = "❌ FAIL"
                c_text = f"Negative Growth. EPS fell by {abs(growth):.1f}%."
        elif prev_eps <= 0 and curr_eps > 0:
            c_status = "✅ PASS"
            c_text = "Turnaround Play. Company swung from Loss to Profit this quarter."
        else:
            c_status = "❌ FAIL"
            c_text = "Company is currently unprofitable."
            
    output_rows.append(f"**C - Current Earnings**|{c_text}|{c_status}")

    # 2. A - ANNUAL GROWTH (The "Proven" Check)
    # Target: >25% Annual CAGR
    a_status = "⚠️ NEUTRAL"
    a_text = "Insufficient annual data."
    
    if len(y_earnings) >= 2:
        curr_y = y_earnings[0].get('eps') or 0
        prev_y = y_earnings[1].get('eps') or 0
        
        if prev_y > 0:
            growth = ((curr_y - prev_y) / prev_y) * 100
            if growth >= 25:
                a_status = "✅ PASS"
                a_text = f"Stellar Track Record. Annual EPS jumped {growth:.1f}%."
            elif growth > 0:
                a_status = "❌ FAIL"
                a_text = f"Mediocre. Annual growth is {growth:.1f}% (Target >25%)."
            else:
                a_status = "❌ FAIL"
                a_text = "Earnings Contracting. Annual EPS declined."
        elif prev_y <= 0 and curr_y > 0:
            a_status = "✅ PASS"
            a_text = "Turnaround. Annual earnings moved into positive territory."
        else:
            a_status = "❌ FAIL"
            a_text = "Loss Making. Company reported an annual net loss."
            
    output_rows.append(f"**A - Annual Growth**|{a_text}|{a_status}")

    # 3. N - NEW (Highs/Products)
    # Proxy: Near 52W High implies "New" momentum
    price = quote.get('price') or 0
    high52 = quote.get('yearHigh') or price or 1
    
    dist_high = ((high52 - price) / high52) * 100
    
    if dist_high < 5:
        n_status = "✅ PASS"
        n_text = "Breakout Mode. Trading within 5% of 52-Week High."
    elif dist_high < 15:
        n_status = "⚠️ NEAR"
        n_text = f"Setting Up. Stock is {dist_high:.1f}% below the 52-Week High."
    else:
        n_status = "❌ FAIL"
        n_text = f"Correction. Trading {dist_high:.1f}% below highs (Lacks 'New' momentum)."
        
    output_rows.append(f"**N - New Highs**|{n_text}|{n_status}")

    # 4. S - SUPPLY (Volume)
    # Check if recent volume is higher than average
    vol = quote.get('volume') or 0
    avg_vol = quote.get('avgVolume') or vol or 1
    
    if vol > avg_vol * 1.5:
        s_status = "✅ PASS"
        s_text = "High Demand. Volume is 50%+ above average (Institutional Accumulation)."
    elif vol > avg_vol:
        s_status = "✅ PASS"
        s_text = "Active. Volume is above average."
    else:
        s_status = "⚠️ WEAK"
        s_text = "Low Liquidity. Volume is below average (Lack of conviction)."
        
    output_rows.append(f"**S - Supply/Demand**|{s_text}|{s_status}")

    # 5. L - LEADER (Relative Strength)
    # Using Beta and Price vs 200 EMA
    beta = km.get('beta') or 1.0
    mas = master_data.get('moving_averages') or {}
    ema200 = mas.get('200') or 0
    
    if price > ema200 and beta > 1:
        l_status = "✅ PASS"
        l_text = f"Market Leader. Beta {beta:.2f} & trading above 200-EMA."
    elif price > ema200:
        l_status = "⚠️ NEUTRAL"
        l_text = "Stable. Trading above 200-EMA but Beta is low."
    else:
        l_status = "❌ FAIL"
        l_text = "Laggard. Trading below key 200-day trendline."
        
    output_rows.append(f"**L - Leader/Laggard**|{l_text}|{l_status}")

    # 6. I - INSTITUTIONAL SPONSORSHIP
    inst_own = share_bd.get('fii', 0) + share_bd.get('dii', 0)
    
    if inst_own > 30:
        i_status = "✅ PASS"
        i_text = f"Strong Backing. {inst_own:.1f}% held by Institutions."
    elif inst_own > 15:
        i_status = "✅ PASS"
        i_text = f"Moderate Backing. {inst_own:.1f}% institutional holding."
    else:
        i_status = "❌ FAIL"
        i_text = f"Retail Heavy. Only {inst_own:.1f}% institutional ownership."
        
    output_rows.append(f"**I - Sponsorship**|{i_text}|{i_status}")

    # 7. M - MARKET DIRECTION
    m_status = "⚠️ CHECK"
    m_text = "Always verify NIFTY/SENSEX is in a confirmed uptrend before entering."
    output_rows.append(f"**M - Market Direction**|{m_text}|{m_status}")

    return "\n".join(output_rows)


def generate_value_philosophy(master_data):
    """
    Hardcore Value Logic (Graham & Lynch).
    Returns: Formula | Assessment
    """
    if not master_data: return "Data unavailable|N/A"

    km = master_data.get('key_metrics') or {}
    quote = master_data.get('quote') or {}
    
    pe = km.get('peRatioTTM') or 0
    pb = km.get('priceToBookRatioTTM') or 0
    roe = km.get('returnOnCapitalEmployedTTM') or 0
    growth = km.get('revenueGrowth') or 0.01 # Avoid div/0
    
    output_rows = []

    # 1. GRAHAM NUMBER (Intrinsic Value)
    # Formula: SqRt(22.5 * EPS * BookValue)
    try:
        eps = km.get('epsTTM') or 0
        # Estimate Book Value from P/B if raw BV is missing
        price = quote.get('price') or 0
        bvps = price / pb if pb > 0 else 0
        
        if eps > 0 and bvps > 0:
            graham_num = (22.5 * eps * bvps) ** 0.5
            diff = ((graham_num - price) / price) * 100
            
            if price < graham_num:
                g_text = f"✅ **UNDERVALUED**. Intrinsic Value is {graham_num:.2f} (Upside: +{diff:.1f}%)."
            else:
                g_text = f"❌ **OVERVALUED**. Intrinsic Value is {graham_num:.2f} (Premium: {abs(diff):.1f}%)."
        else:
            g_text = "⚠️ **N/A**. Cannot calculate (Negative Earnings or Book Value)."
    except:
        g_text = "⚠️ **Error**. Insufficient data."
        
    output_rows.append(f"**Ben Graham's Intrinsic Value**|{g_text}")

    # 2. PETER LYNCH (PEG Ratio)
    # Formula: P/E divided by Growth Rate
    # Fair value is PEG = 1.0. < 0.5 is cheap. > 2.0 is expensive.
    try:
        growth_rate = growth * 100 # Convert to percentage
        if growth_rate > 0:
            peg = pe / growth_rate
            if peg < 0.5:
                p_text = f"✅ **SCREAMING BUY**. PEG is {peg:.2f} (Extremely Cheap for its growth)."
            elif peg < 1.0:
                p_text = f"✅ **BUY**. PEG is {peg:.2f} (Growth is cheap)."
            elif peg < 2.0:
                p_text = f"⚠️ **HOLD**. PEG is {peg:.2f} (Fairly priced)."
            else:
                p_text = f"❌ **SELL**. PEG is {peg:.2f} (Growth is too expensive)."
        else:
            p_text = "❌ **AVOID**. Company has negative growth."
    except:
        p_text = "⚠️ **N/A**. Missing growth metrics."
        
    output_rows.append(f"**Peter Lynch Fair Value (PEG)**|{p_text}")

    # 3. WARREN BUFFETT (Moat Check)
    if roe > 0.20:
        b_text = f"✅ **WIDE MOAT**. Incredible efficiency (ROE: {roe*100:.1f}%)."
    elif roe > 0.12:
        b_text = f"✅ **STABLE**. Decent returns (ROE: {roe*100:.1f}%)."
    else:
        b_text = f"❌ **NO MOAT**. Poor capital returns (ROE: {roe*100:.1f}%)."
        
    output_rows.append(f"**Buffett Moat Indicator**|{b_text}")

    return "\n".join(output_rows)
