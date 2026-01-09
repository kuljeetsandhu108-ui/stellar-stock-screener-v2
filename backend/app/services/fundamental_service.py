import pandas as pd

def calculate_piotroski_f_score(income_statements, balance_sheets, cash_flow_statements):
    """
    Calculates the Piotroski F-Score (0-9) to assess financial strength.
    Uses Pandas to ensure chronological accuracy.
    """
    score = 0
    criteria_met = []

    # 1. Validation: We need at least 2 years of data to compare trends
    if not income_statements or not balance_sheets or not cash_flow_statements:
        return {"score": 0, "criteria": ["Insufficient Data"]}
    
    if len(income_statements) < 2 or len(balance_sheets) < 2 or len(cash_flow_statements) < 2:
        return {"score": 0, "criteria": ["Insufficient Historical Data (Need 2+ years)"]}

    try:
        # 2. Data Preparation: Convert to DataFrames and Sort Chronologically
        # EODHD/FMP usually send Newest First. We sort by date ASCENDING.
        # Index -1 = Current Year, Index -2 = Previous Year
        inc_df = pd.DataFrame(income_statements).sort_values('date')
        bal_df = pd.DataFrame(balance_sheets).sort_values('date')
        cf_df = pd.DataFrame(cash_flow_statements).sort_values('date')

        # Align lengths (take the minimum common length to avoid index errors)
        min_len = min(len(inc_df), len(bal_df), len(cf_df))
        inc_df = inc_df.tail(min_len)
        bal_df = bal_df.tail(min_len)
        cf_df = cf_df.tail(min_len)

        cy = -1 # Current Year Index
        py = -2 # Previous Year Index

        # --- PROFITABILITY (4 Points) ---

        # 1. Return on Assets (ROA) > 0
        # Net Income / Total Assets
        net_income = float(inc_df.iloc[cy].get('netIncome', 0))
        total_assets = float(bal_df.iloc[cy].get('totalAssets', 1)) # Avoid div/0
        roa_current = net_income / total_assets
        if net_income > 0:
            score += 1
            criteria_met.append("Positive Net Income")

        # 2. Operating Cash Flow > 0
        ocf = float(cf_df.iloc[cy].get('operatingCashFlow', 0))
        if ocf > 0:
            score += 1
            criteria_met.append("Positive Operating Cash Flow")

        # 3. Change in ROA (Current > Previous)
        net_income_prev = float(inc_df.iloc[py].get('netIncome', 0))
        total_assets_prev = float(bal_df.iloc[py].get('totalAssets', 1))
        roa_prev = net_income_prev / total_assets_prev
        
        if roa_current > roa_prev:
            score += 1
            criteria_met.append("Increasing Return on Assets (ROA)")

        # 4. Quality of Earnings (Accruals): OCF > Net Income
        if ocf > net_income:
            score += 1
            criteria_met.append("High Quality Earnings (Cash Flow > Net Income)")

        # --- LEVERAGE, LIQUIDITY, SOURCE OF FUNDS (3 Points) ---

        # 5. Change in Leverage (Long Term Debt)
        # Current LTD should be <= Previous LTD
        ltd_curr = float(bal_df.iloc[cy].get('longTermDebt', 0))
        ltd_prev = float(bal_df.iloc[py].get('longTermDebt', 0))
        
        # We give points if debt decreased OR if debt is zero
        if ltd_curr <= ltd_prev:
            score += 1
            criteria_met.append("Lower or Stable Long-Term Debt")

        # 6. Change in Current Ratio (Current > Previous)
        # Current Assets / Current Liabilities
        ca_curr = float(bal_df.iloc[cy].get('totalCurrentAssets', 0))
        cl_curr = float(bal_df.iloc[cy].get('totalCurrentLiabilities', 1))
        current_ratio_curr = ca_curr / cl_curr if cl_curr else 0

        ca_prev = float(bal_df.iloc[py].get('totalCurrentAssets', 0))
        cl_prev = float(bal_df.iloc[py].get('totalCurrentLiabilities', 1))
        current_ratio_prev = ca_prev / cl_prev if cl_prev else 0

        if current_ratio_curr > current_ratio_prev:
            score += 1
            criteria_met.append("Improving Liquidity (Current Ratio)")

        # 7. Change in Shares Outstanding (No Dilution)
        # Current Shares <= Previous Shares
        shares_curr = float(inc_df.iloc[cy].get('weightedAverageShsOut', 0))
        shares_prev = float(inc_df.iloc[py].get('weightedAverageShsOut', 0))
        
        # Allow a tiny margin for rounding errors (e.g. 0.1%)
        if shares_curr <= shares_prev * 1.001:
            score += 1
            criteria_met.append("No Share Dilution")

        # --- OPERATING EFFICIENCY (2 Points) ---

        # 8. Change in Gross Margin
        # (Gross Profit / Revenue)
        rev_curr = float(inc_df.iloc[cy].get('revenue', 1))
        gp_curr = float(inc_df.iloc[cy].get('grossProfit', 0))
        gm_curr = gp_curr / rev_curr if rev_curr else 0

        rev_prev = float(inc_df.iloc[py].get('revenue', 1))
        gp_prev = float(inc_df.iloc[py].get('grossProfit', 0))
        gm_prev = gp_prev / rev_prev if rev_prev else 0

        if gm_curr > gm_prev:
            score += 1
            criteria_met.append("Improving Gross Margin")

        # 9. Change in Asset Turnover
        # (Revenue / Total Assets)
        at_curr = rev_curr / total_assets if total_assets else 0
        at_prev = rev_prev / total_assets_prev if total_assets_prev else 0

        if at_curr > at_prev:
            score += 1
            criteria_met.append("Improving Asset Turnover efficiency")

    except Exception as e:
        print(f"Piotroski Calculation Error: {e}")
        return {"score": score, "criteria": criteria_met + ["Calculation Error"]}

    return {"score": score, "criteria": criteria_met}


def calculate_graham_scan(profile: dict, key_metrics: dict, income_statements: list, cash_flow_statements: list = []):
    """
    Benjamin Graham 'Defensive Investor' Checklist (7 Tenets).
    Includes specific logic for Indian/Global markets.
    """
    score = 0
    criteria_met = []

    if not profile or not key_metrics or len(income_statements) < 3:
        return {"score": 0, "criteria": ["Insufficient Data for Graham Analysis."]}

    try:
        # --- 1. Adequate Size ---
        # Rule: Exclude small companies to avoid volatility.
        # Heuristic: Market Cap > 2 Billion USD (or approx 15,000 Cr INR)
        # Since API returns raw numbers, we check raw magnitude.
        mcap = float(key_metrics.get('marketCap') or profile.get('mktCap') or 0)
        
        # We assume 'Adequate' is > 2 Billion units of base currency (roughly works for USD and large INR caps)
        if mcap > 2_000_000_000: 
            score += 1
            criteria_met.append(f"Adequate Size (Market Cap > 2B)")

        # --- 2. Strong Financial Condition ---
        # Rule: Current Ratio >= 2.0
        current_ratio = key_metrics.get('currentRatioTTM')
        if current_ratio and current_ratio >= 2.0:
            score += 1
            criteria_met.append(f"Strong Financials (Current Ratio {current_ratio:.2f} >= 2.0)")
        elif current_ratio and current_ratio >= 1.5:
            # Partial credit/mention for decent companies
            pass 

        # --- 3. Earnings Stability ---
        # Rule: Positive earnings for the last 5-10 years.
        # We check whatever history we have (usually 5 years from API).
        earnings_history = [float(s.get('netIncome', 0)) for s in income_statements]
        if earnings_history and all(e > 0 for e in earnings_history):
            score += 1
            criteria_met.append(f"Earnings Stability ({len(earnings_history)} years of positive profit)")

        # --- 4. Dividend Record ---
        # Rule: Uninterrupted payments for 20 years (We check 5 years available).
        # We look at Cash Flow 'dividendsPaid'. Note: These are usually negative numbers (outflows).
        dividends = []
        if cash_flow_statements:
            dividends = [float(s.get('dividendsPaid', 0)) for s in cash_flow_statements]
        elif income_statements:
            # Fallback to income statement if specific CF field missing
            dividends = [float(s.get('dividendsPaid', 0)) for s in income_statements]
            
        # Check if any dividends were paid (non-zero) consistently
        # We allow one missed year in 5 years for strictness flexibility, but let's be strict here:
        if dividends and all(d != 0 for d in dividends):
            score += 1
            criteria_met.append("Consistent Dividend History")

        # --- 5. Earnings Growth ---
        # Rule: At least 33% growth in EPS over the last 10 years (We check 5).
        # List is typically Newest -> Oldest
        if len(income_statements) >= 3:
            # Safely get EPS
            def get_eps(item):
                if item.get('eps'): return float(item['eps'])
                if item.get('netIncome') and item.get('weightedAverageShsOut'):
                    return float(item['netIncome']) / float(item['weightedAverageShsOut'])
                return 0.0

            current_eps = get_eps(income_statements[0])
            past_eps = get_eps(income_statements[-1])
            
            if past_eps > 0 and current_eps > past_eps:
                growth = ((current_eps - past_eps) / past_eps) * 100
                if growth > 15: # Adjusted for shorter timeframe (5y)
                    score += 1
                    criteria_met.append(f"Earnings Growth (EPS grew {growth:.1f}%)")

        # --- 6. Moderate P/E Ratio ---
        # Rule: Current price should not be more than 15 times average earnings.
        pe = float(key_metrics.get('peRatioTTM') or 0)
        if 0 < pe < 15:
            score += 1
            criteria_met.append(f"Attractive Valuation (P/E {pe:.2f} < 15)")

        # --- 7. Moderate Price to Assets (Graham Number) ---
        # Rule: P/E * P/B should not exceed 22.5
        # OR Price to Book < 1.5
        pb = float(key_metrics.get('priceToBookRatioTTM') or 0)
        
        passed_valuation = False
        
        if 0 < pb < 1.5: 
            passed_valuation = True
            criteria_met.append(f"Assets Undervalued (P/B {pb:.2f} < 1.5)")
        elif pe > 0 and pb > 0 and (pe * pb) < 22.5:
            passed_valuation = True
            criteria_met.append(f"Graham Number Safe (P/E * P/B = {(pe*pb):.1f} < 22.5)")
            
        if passed_valuation:
            score += 1

    except Exception as e:
        print(f"Graham Scan Error: {e}")
        criteria_met.append("Analysis interrupted by missing data")

    return {"score": score, "criteria": criteria_met}