import pandas as pd

def calculate_piotroski_f_score(income_statements, balance_sheets, cash_flow_statements):
    """
    Calculates the Piotroski F-Score based on 9 criteria using historical financial data.
    """
    score = 0
    criteria_met = []

    # Ensure we have at least two years of data to compare for the calculations.
    if len(income_statements) < 2 or len(balance_sheets) < 2 or len(cash_flow_statements) < 2:
        return {"score": 0, "criteria": ["Not enough historical data."]}

    try:
        # Use pandas DataFrames for easier data manipulation and access.
        income_df = pd.DataFrame(income_statements).set_index('date').sort_index()
        balance_df = pd.DataFrame(balance_sheets).set_index('date').sort_index()
        cash_flow_df = pd.DataFrame(cash_flow_statements).set_index('date').sort_index()

        # Get the dates for the current and previous year for comparison.
        cy = income_df.index[-1] # Current Year
        py = income_df.index[-2] # Previous Year

        # --- Piotroski F-Score Criteria (9 points) ---

        # 1. Net Income (Profitability)
        net_income = income_df.loc[cy, 'netIncome']
        if net_income > 0:
            score += 1
            criteria_met.append("Positive Net Income")

        # 2. Operating Cash Flow (Profitability)
        op_cash_flow = cash_flow_df.loc[cy, 'operatingCashFlow']
        if op_cash_flow > 0:
            score += 1
            criteria_met.append("Positive Operating Cash Flow")

        # 3. Return On Assets (ROA) Trend (Profitability)
        total_assets_cy = balance_df.loc[cy, 'totalAssets']
        total_assets_py = balance_df.loc[py, 'totalAssets']
        roa_cy = net_income / total_assets_cy
        roa_py = income_df.loc[py, 'netIncome'] / total_assets_py
        if roa_cy > roa_py:
            score += 1
            criteria_met.append("Increasing Return on Assets (ROA)")

        # 4. Quality of Earnings (Profitability)
        if op_cash_flow > net_income:
            score += 1
            criteria_met.append("Operating Cash Flow > Net Income")

        # 5. Long-Term Debt vs Assets (Leverage)
        debt_cy = balance_df.loc[cy, 'longTermDebt'] / total_assets_cy
        debt_py = balance_df.loc[py, 'longTermDebt'] / total_assets_py
        if debt_cy < debt_py:
            score += 1
            criteria_met.append("Lower Long-term Debt Ratio")

        # 6. Current Ratio Trend (Liquidity)
        current_ratio_cy = balance_df.loc[cy, 'totalCurrentAssets'] / balance_df.loc[cy, 'totalCurrentLiabilities']
        current_ratio_py = balance_df.loc[py, 'totalCurrentAssets'] / balance_df.loc[py, 'totalCurrentLiabilities']
        if current_ratio_cy > current_ratio_py:
            score += 1
            criteria_met.append("Higher Current Ratio")

        # 7. Shares Outstanding (Dilution)
        shares_cy = income_df.loc[cy, 'weightedAverageShsOut']
        shares_py = income_df.loc[py, 'weightedAverageShsOut']
        if shares_cy <= shares_py:
            score += 1
            criteria_met.append("No new shares issued (no dilution)")

        # 8. Gross Margin Trend (Operating Efficiency)
        gross_margin_cy = income_df.loc[cy, 'grossProfit'] / income_df.loc[cy, 'revenue']
        gross_margin_py = income_df.loc[py, 'grossProfit'] / income_df.loc[py, 'revenue']
        if gross_margin_cy > gross_margin_py:
            score += 1
            criteria_met.append("Higher Gross Margin")

        # 9. Asset Turnover Trend (Operating Efficiency)
        asset_turnover_cy = income_df.loc[cy, 'revenue'] / total_assets_py
        asset_turnover_py = income_df.loc[py, 'revenue'] / (balance_df.iloc[-3]['totalAssets'] if len(balance_df) > 2 else total_assets_py)
        if asset_turnover_cy > asset_turnover_py:
            score += 1
            criteria_met.append("Higher Asset Turnover Ratio")
            
    except Exception as e:
        print(f"Could not calculate Piotroski score due to missing data or error: {e}")
        return {"score": 0, "criteria": [f"Piotroski calculation error: {e}"]}

    return {"score": score, "criteria": criteria_met}


def calculate_graham_scan(profile: dict, key_metrics: dict, income_statements: list):
    """
    Performs a Benjamin Graham scan based on 7 tenets for the defensive investor.
    """
    score = 0
    criteria_met = []

    if not profile or not key_metrics or len(income_statements) < 5:
        return {"score": 0, "criteria": ["Not enough historical data for a full Graham scan."]}

    try:
        # Tenet 1: Adequate Size (Market Cap > $2 Billion)
        market_cap = profile.get('mktCap')
        if market_cap and market_cap > 2_000_000_000:
            score += 1
            criteria_met.append(f"Adequate Size (Market Cap: ${market_cap / 1_000_000_000:.2f}B)")

        # Tenet 2: Strong Financial Condition (Current Ratio > 2.0)
        current_ratio = key_metrics.get('currentRatioTTM')
        if current_ratio and current_ratio > 2.0:
            score += 1
            criteria_met.append(f"Strong Financials (Current Ratio: {current_ratio:.2f})")

        # Tenet 3: Earnings Stability (Positive earnings for the last 5 years)
        earnings_stable = all(stmt.get('netIncome', 0) > 0 for stmt in income_statements)
        if earnings_stable:
            score += 1
            criteria_met.append("Earnings Stability (5 consecutive years of profit)")

        # Tenet 4: Dividend Record (Consistent dividends for the last 5 years)
        dividend_record = all(stmt.get('dividendsPaid', 0) != 0 for stmt in income_statements)
        if dividend_record:
            score += 1
            criteria_met.append("Consistent Dividend Record (5 years)")
        
        # Tenet 5: Earnings Growth (At least 33% growth over 5 years)
        eps_start = income_statements[-1].get('eps')
        eps_end = income_statements[0].get('eps')
        if eps_start is not None and eps_end is not None and eps_start > 0:
            growth = ((eps_end / eps_start) - 1) * 100
            if growth >= 33:
                score += 1
                criteria_met.append(f"Earnings Growth (>33% over 5 years, actual: {growth:.2f}%)")

        # Tenet 6: Moderate P/E Ratio (P/E < 15)
        pe_ratio = key_metrics.get('peRatioTTM')
        if pe_ratio and 0 < pe_ratio < 15:
            score += 1
            criteria_met.append(f"Moderate P/E Ratio (< 15, actual: {pe_ratio:.2f})")

        # Tenet 7: Moderate Price-to-Book (P/E * P/B < 22.5)
        pb_ratio = key_metrics.get('priceToBookRatioTTM')
        if pe_ratio and pb_ratio and (pe_ratio * pb_ratio) < 22.5:
            score += 1
            criteria_met.append(f"Moderate P/B Ratio (P/E * P/B < 22.5, actual: {(pe_ratio * pb_ratio):.2f})")

    except Exception as e:
        print(f"Error calculating Graham Scan: {e}")
        return {"score": score, "criteria": criteria_met + [f"Calculation error: {e}"]}

    return {"score": score, "criteria": criteria_met}