def calculate_rsi(prices, window=14):
    delta = prices.diff()
    gains = delta.clip(lower=0)
    losses = -delta.clip(upper=0)

    avg_gain = gains.rolling(window).mean()
    avg_loss = losses.rolling(window).mean()

    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))


def add_technical_indicators(history):
    history = history.copy()
    history["MA50"] = history["Close"].rolling(window=50).mean()
    history["MA200"] = history["Close"].rolling(window=200).mean()
    history["RSI"] = calculate_rsi(history["Close"])
    return history


def get_return(history, days):
    if history is None or len(history) < days:
        return None
    return ((history["Close"].iloc[-1] / history["Close"].iloc[-days]) - 1) * 100
