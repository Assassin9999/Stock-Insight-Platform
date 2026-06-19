import streamlit as st


def render_sidebar():
    st.sidebar.title("AlphaLens")
    st.sidebar.caption("Stock research dashboard")

    ticker = st.sidebar.text_input("Search ticker", "AAPL").upper().strip()

    st.sidebar.divider()
    st.sidebar.subheader("Watchlist")

    watchlist = [
        "AAPL", "MSFT", "NVDA", "AMD", "TSLA",
        "GOOGL", "AMZN", "META", "NFLX", "AVGO",
        "JPM", "V", "MA", "COST", "WMT",
        "SHOP", "TD", "RY", "BNS", "BMO",
        "SPY", "QQQ", "VOO"
    ]

    selected = st.sidebar.radio("Quick select", watchlist, index=0)

    if st.sidebar.button("Load selected ticker"):
        ticker = selected

    st.sidebar.divider()
    st.sidebar.caption("Educational use only. Not financial advice.")

    return ticker
