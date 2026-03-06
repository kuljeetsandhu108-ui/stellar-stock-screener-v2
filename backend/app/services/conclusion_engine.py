def generate_algorithmic_conclusion(company_name, p_data, g_data, d_data, key_stats):
    """Generates a structured A-F Grade and Thesis using weighted math, completely bypassing AI."""
    
    # 1. Safe Data Extraction
    p_score = p_data.get('score', 0) if isinstance(p_data, dict) else 0
    g_score = g_data.get('score', 0) if isinstance(g_data, dict) else 0
    d_status = d_data.get('status', 'Neutral') if isinstance(d_data, dict) else 'Neutral'
    pe = key_stats.get('peRatio') or 0
    
    # 2. Weighted Scoring Algorithm (Max 100 Points)
    # Piotroski (Financial Health): 40% weight
    score = (p_score / 9.0) * 40.0
    
    # Graham (Value & Safety): 30% weight
    score += (g_score / 7.0) * 30.0
    
    # Valuation (P/E Penalty/Bonus): 15% weight
    if 0 < pe < 15: score += 15
    elif 15 <= pe < 25: score += 10
    elif 25 <= pe < 40: score += 5
    # pe > 40 or negative pe gets 0 points
    
    # Momentum (Darvas Box): 15% weight
    if "Breakout" in d_status: score += 15
    elif "Box" in d_status: score += 10
    elif "Not" in d_status: score += 5
    
    # 3. Grade Assignment
    if score >= 80:
        grade = "A"
        thesis = f"Outstanding fundamental strength and attractive valuation. {company_name} demonstrates excellent operational efficiency and a high margin of safety."
    elif score >= 65:
        grade = "B"
        thesis = f"Solid financials with reasonable growth prospects. {company_name} is a strong candidate for accumulation on market dips."
    elif score >= 50:
        grade = "C"
        thesis = f"Neutral fundamentals. {company_name} shows mixed signals between its current valuation and underlying financial health."
    elif score >= 35:
        grade = "D"
        thesis = f"Weak financial structure or severe overvaluation. {company_name} carries high fundamental risk at current levels."
    else:
        grade = "F"
        thesis = f"Critical financial weakness or massive speculative premium. Algorithm strongly suggests avoiding {company_name} until metrics improve."

    # 4. Dynamic Takeaways Generation
    takeaways =[]
    
    # Financial Health Takeaway
    if p_score >= 7: takeaways.append(f"High Piotroski F-Score ({p_score}/9) confirms robust profitability, liquidity, and operating efficiency.")
    elif p_score <= 3: takeaways.append(f"Low Piotroski F-Score ({p_score}/9) warns of deteriorating cash flow or rising leverage.")
    else: takeaways.append(f"Average Piotroski F-Score ({p_score}/9) indicates stable but unexceptional financial health.")
        
    # Value Takeaway
    if g_score >= 5: takeaways.append(f"Passes {g_score}/7 of Benjamin Graham's strict defensive criteria, indicating a deep value profile.")
    elif g_score <= 2: takeaways.append(f"Fails most Graham value checks ({g_score}/7), suggesting it is priced for high growth rather than value.")
        
    # Valuation & Momentum Takeaway
    if 0 < pe < 20: takeaways.append(f"Trading at an attractive P/E multiple of {pe:.1f}.")
    elif pe > 40: takeaways.append(f"Trading at a steep premium (P/E: {pe:.1f}), requiring flawless future execution to justify the price.")
    
    takeaways.append(f"Technical momentum context: {d_status}.")

    # 5. Format exactly to match React Frontend Parser
    takeaways_str = "\n".join([f"- {t}" for t in takeaways])
    
    final_output = f"GRADE: {grade}\nTHESIS: {thesis}\nTAKEAWAYS:\n{takeaways_str}"
    
    return final_output
