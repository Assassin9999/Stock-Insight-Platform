def get_historical_context(history):
    current_price = history["Close"].iloc[-1]
    previous = history.iloc[:-1]

    previous_higher = previous[previous["Close"] >= current_price]
    previous_lower = previous[previous["Close"] <= current_price]

    result = {}

    if previous_higher.empty:
        result["higher_text"] = "This is the highest closing price in the available 2-year history."
    else:
        last_date = previous_higher.index[-1]
        days = (history.index[-1] - last_date).days
        result["higher_text"] = (
            f"The stock has not closed this high since "
            f"{last_date.strftime('%B %d, %Y')} ({days} days ago)."
        )

    if previous_lower.empty:
        result["lower_text"] = "This is the lowest closing price in the available 2-year history."
    else:
        last_date = previous_lower.index[-1]
        days = (history.index[-1] - last_date).days
        result["lower_text"] = (
            f"The stock has not closed this low since "
            f"{last_date.strftime('%B %d, %Y')} ({days} days ago)."
        )

    percentile = (history["Close"] < current_price).mean() * 100
    result["percentile"] = percentile
    result["days_higher_percent"] = 100 - percentile
    return result
