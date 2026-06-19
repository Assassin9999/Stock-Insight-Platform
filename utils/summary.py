def generate_executive_summary(company, overall_score, rsi, volume_ratio, one_month_return, peer_difference=None):
    if overall_score >= 80:
        profile = "strong"
    elif overall_score >= 65:
        profile = "positive"
    elif overall_score >= 50:
        profile = "mixed"
    else:
        profile = "weak"

    summary = (
        f"{company} currently shows a {profile} AlphaLens profile based on trend, "
        f"momentum, valuation, risk, and recent price behavior. "
    )

    if one_month_return is not None:
        if one_month_return > 5:
            summary += "Recent price performance has been strong over the last month. "
        elif one_month_return < -5:
            summary += "Recent price performance has weakened over the last month. "
        else:
            summary += "Recent price performance has been relatively stable. "

    if rsi > 70:
        summary += "RSI suggests the stock may be overbought. "
    elif rsi < 30:
        summary += "RSI suggests the stock may be oversold. "
    else:
        summary += "Momentum indicators remain balanced. "

    if volume_ratio > 1.5:
        summary += "Trading volume is elevated compared to normal levels. "
    elif volume_ratio < 0.7:
        summary += "Trading volume is below its recent average. "
    else:
        summary += "Trading volume is close to its recent average. "

    if peer_difference is not None:
        if peer_difference > 3:
            summary += "The stock is outperforming its peer group over the past month."
        elif peer_difference < -3:
            summary += "The stock is underperforming its peer group over the past month."
        else:
            summary += "The stock is performing roughly in line with its peers."

    return summary
