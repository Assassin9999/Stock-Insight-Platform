import streamlit as st
import yfinance as yf

from utils.indicators import add_technical_indicators


@st.cache_data(ttl=300)
def load_stock_data(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info
    history = stock.history(period="2y")

    if not history.empty:
        history = add_technical_indicators(history)

    return info, history


@st.cache_data(ttl=300)
def load_peer_history(ticker):
    stock = yf.Ticker(ticker)
    return stock.history(period="3mo")
