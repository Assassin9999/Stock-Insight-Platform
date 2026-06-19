def calculate_trend_score(current_price, ma50, ma200, rsi, one_month_return, volume_ratio):
    score = 50
    score += 15 if current_price > ma50 else -15
    score += 20 if current_price > ma200 else -20

    if one_month_return is not None:
        if one_month_return > 5:
            score += 10
        elif one_month_return < -5:
            score -= 10

    if rsi > 70:
        score -= 5
    elif rsi < 30:
        score += 5

    if volume_ratio > 1.5:
        score += 5

    return max(0, min(round(score), 100))


def get_price_percentile(history, current_price):
    prices = history["Close"].dropna()
    return (prices < current_price).mean() * 100
