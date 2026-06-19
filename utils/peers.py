def get_peer_list(ticker):
    peers = {
        "AAPL": ["MSFT", "GOOGL", "AMZN", "META"],
        "MSFT": ["AAPL", "GOOGL", "AMZN", "ORCL"],
        "GOOGL": ["MSFT", "META", "AMZN", "AAPL"],
        "AMZN": ["AAPL", "MSFT", "GOOGL", "WMT"],
        "META": ["GOOGL", "SNAP", "PINS", "MSFT"],
        "NVDA": ["AMD", "AVGO", "INTC", "TSM"],
        "AMD": ["NVDA", "INTC", "QCOM", "AVGO"],
        "TSLA": ["F", "GM", "RIVN", "NIO"],
        "SHOP": ["AMZN", "EBAY", "MELI", "WMT"],
        "TD": ["RY", "BNS", "BMO", "CM"],
        "RY": ["TD", "BNS", "BMO", "CM"],
        "SPY": ["QQQ", "VOO", "DIA", "IWM"],
        "QQQ": ["SPY", "VOO", "DIA", "IWM"],
    }
    return peers.get(ticker, ["SPY", "QQQ", "VOO"])
