import streamlit as st
import plotly.graph_objects as go


def render_price_chart(history):
    st.subheader("Price Chart")

    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=history.index,
        open=history["Open"],
        high=history["High"],
        low=history["Low"],
        close=history["Close"],
        name="Price"
    ))

    fig.add_trace(go.Scatter(x=history.index, y=history["MA50"], mode="lines", name="50-Day Moving Average"))
    fig.add_trace(go.Scatter(x=history.index, y=history["MA200"], mode="lines", name="200-Day Moving Average"))

    fig.update_layout(height=600, xaxis_title="Date", yaxis_title="Price ($)", xaxis_rangeslider_visible=False)
    st.plotly_chart(fig, use_container_width=True)


def render_rsi_chart(history):
    st.subheader("RSI Momentum Indicator")

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=history.index, y=history["RSI"], mode="lines", name="RSI"))
    fig.add_hline(y=70, line_dash="dash", annotation_text="Overbought")
    fig.add_hline(y=30, line_dash="dash", annotation_text="Oversold")

    fig.update_layout(height=300, xaxis_title="Date", yaxis_title="RSI")
    st.plotly_chart(fig, use_container_width=True)
