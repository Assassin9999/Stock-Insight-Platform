def clamp_score(score):
    return max(0, min(100, round(score)))


def calculate_momentum_score(one_month_return, six_month_return, rsi):
    score = 50

    if one_month_return is not None:
        if one_month_return > 5:
            score += 15
        elif one_month_return < -5:
            score -= 15

    if six_month_return is not None:
        if six_month_return > 15:
            score += 20
        elif six_month_return < -10:
            score -= 20

    if 45 <= rsi <= 65:
        score += 10
    elif rsi > 75:
        score -= 10
    elif rsi < 30:
        score -= 5

    return clamp_score(score)


def calculate_valuation_score(pe_ratio):
    if pe_ratio is None:
        return 50
    if pe_ratio < 15:
        return 85
    if pe_ratio < 25:
        return 75
    if pe_ratio < 40:
        return 60
    if pe_ratio < 60:
        return 45
    return 30


def calculate_risk_score(volume_ratio, price_percentile, rsi):
    score = 70

    if price_percentile > 90:
        score -= 10
    if rsi > 70:
        score -= 10
    if volume_ratio > 2:
        score -= 10
    if volume_ratio < 0.5:
        score -= 5

    return clamp_score(score)


def calculate_growth_proxy_score(six_month_return):
    score = 50

    if six_month_return is not None:
        if six_month_return > 20:
            score += 30
        elif six_month_return > 10:
            score += 15
        elif six_month_return < -10:
            score -= 20

    return clamp_score(score)


def calculate_investment_scores(trend_score, pe_ratio, one_month_return, six_month_return, rsi, volume_ratio, price_percentile):
    momentum = calculate_momentum_score(one_month_return, six_month_return, rsi)
    valuation = calculate_valuation_score(pe_ratio)
    risk = calculate_risk_score(volume_ratio, price_percentile, rsi)
    growth = calculate_growth_proxy_score(six_month_return)

    overall = trend_score * 0.35 + momentum * 0.25 + valuation * 0.15 + risk * 0.15 + growth * 0.10

    return {
        "overall": clamp_score(overall),
        "trend": clamp_score(trend_score),
        "momentum": momentum,
        "valuation": valuation,
        "risk": risk,
        "growth": growth,
    }


def calculate_horizon_scores(scores, one_week_return, one_month_return, six_month_return, rsi, volume_ratio):
    long_term = clamp_score(
        scores["trend"] * 0.35
        + scores["valuation"] * 0.25
        + scores["risk"] * 0.20
        + scores["growth"] * 0.20
    )

    swing = clamp_score(
        scores["trend"] * 0.30
        + scores["momentum"] * 0.35
        + scores["risk"] * 0.15
        + scores["growth"] * 0.20
    )

    day_score = 50
    if one_week_return is not None:
        if one_week_return > 2:
            day_score += 15
        elif one_week_return < -2:
            day_score -= 15

    if 40 <= rsi <= 65:
        day_score += 10
    elif rsi > 75 or rsi < 25:
        day_score -= 10

    if volume_ratio >= 1.5:
        day_score += 15
    elif volume_ratio < 0.7:
        day_score -= 5

    return {
        "Long-Term Investor": long_term,
        "Swing Trader": swing,
        "Day Trader": clamp_score(day_score),
    }


def score_label(score):
    if score >= 80:
        return "Strong Profile"
    if score >= 65:
        return "Positive Profile"
    if score >= 50:
        return "Mixed Profile"
    return "Weak Profile"


def generate_score_reasoning(scores):
    positives = []
    cautions = []

    if scores["trend"] >= 70:
        positives.append("Strong trend profile")
    elif scores["trend"] < 50:
        cautions.append("Weak trend profile")

    if scores["momentum"] >= 70:
        positives.append("Positive momentum")
    elif scores["momentum"] < 50:
        cautions.append("Weak momentum")

    if scores["valuation"] >= 70:
        positives.append("Reasonable valuation score")
    elif scores["valuation"] < 50:
        cautions.append("Premium valuation risk")

    if scores["risk"] >= 65:
        positives.append("Manageable technical risk")
    elif scores["risk"] < 50:
        cautions.append("Elevated risk signals")

    if scores["growth"] >= 70:
        positives.append("Strong growth proxy based on price performance")
    elif scores["growth"] < 50:
        cautions.append("Weak recent growth proxy")

    return positives, cautions
