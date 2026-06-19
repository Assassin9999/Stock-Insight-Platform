import streamlit as st
from utils.formatting import format_large_number, format_volume


def render_metrics(current_price, daily_change_pct, market_cap, pe_ratio, trend_score, high_52w, low_52w, latest_volume, volume_ratio):
    row1 = st.columns(4)
    row1[0].metric("Current Price", f"${current_price:,.2f}", f"{daily_change_pct:.2f}%")
    row1[1].metric("Market Cap", format_large_number(market_cap))
    row1[2].metric("P/E Ratio", f"{pe_ratio:.2f}" if pe_ratio else "N/A")
    row1[3].metric("Trend Score", f"{trend_score}/100")

    row2 = st.columns(4)
    row2[0].metric("52W High", f"${high_52w:,.2f}")
    row2[1].metric("52W Low", f"${low_52w:,.2f}")
    row2[2].metric("Volume", format_volume(latest_volume))
    row2[3].metric("Volume vs Avg", f"{volume_ratio:.2f}x")
