import streamlit as st
import plotly.graph_objects as go

from components.sidebar import render_sidebar
from components.summary_card import render_summary_card
from components.metrics import render_metrics
from components.charts import render_price_chart, render_rsi_chart
from components.peers import build_peer_dataframe, get_peer_difference
from components.report import render_report_section
from components.scorecard import render_scorecard
from components.history_card import render_history_card
from components.status_card import render_status_card

from data.stock_data import load_stock_data
from utils.indicators import get_return
from utils.insights import calculate_trend_score, get_price_percentile
from utils.summary import generate_executive_summary
from utils.scoring import calculate_investment_scores, calculate_horizon_scores
from utils.history_context import get_historical_context
from utils.market_status import get_market_status


st.set_page_config(page_title="AlphaLens Stock Insight", layout="wide")

st.markdown(
    """
    <style>
    .big-title { font-size: 44px; font-weight: 800; margin-bottom: 0px; }
    .subtitle { font-size: 18px; color: #6B7280; margin-bottom: 25px; }
    .summary-card, .score-card {
        background-color: #F8FAFC;
        padding: 24px;
        border-radius: 18px;
        border: 1px solid #E5E7EB;
        margin-bottom: 20px;
        color: #111827;
    }
    .summary-text { font-size: 17px; line-height: 1.65; color: #374151; }
    .badge {
        padding: 8px 14px;
        border-radius: 999px;
        font-weight: 700;
        display: inline-block;
        margin-bottom: 10px;
    }
    .bullish { background-color: #D1FAE5; color: #065F46; }
    .neutral { background-color: #FEF3C7; color: #92400E; }
    .bearish { background-color: #FEE2E2; color: #991B1B; }
    </style>
    """,
    unsafe_allow_html=True,
)

ticker = render_sidebar()
info, history = load_stock_data(ticker)

if history.empty:
    st.error("No stock data found. Try AAPL, MSFT, NVDA, AMD, TSLA, SHOP, TD, RY, SPY, or QQQ.")
    st.stop()

company_name = info.get("longName", ticker)
sector = info.get("sector", "N/A")
industry = info.get("industry", "N/A")

current_price = history["Close"].iloc[-1]
previous_price = history["Close"].iloc[-2]
daily_change_pct = ((current_price - previous_price) / previous_price) * 100

high_52w = history.tail(252)["Close"].max()
low_52w = history.tail(252)["Close"].min()

market_cap = info.get("marketCap")
pe_ratio = info.get("trailingPE")

latest_volume = history["Volume"].iloc[-1]
avg_volume_30d = history["Volume"].tail(30).mean()
volume_ratio = latest_volume / avg_volume_30d if avg_volume_30d != 0 else 0

one_week_return = get_return(history, 5)
one_month_return = get_return(history, 22)
six_month_return = get_return(history, 126)

ma50 = history["MA50"].iloc[-1]
ma200 = history["MA200"].iloc[-1]
rsi = history["RSI"].iloc[-1]

trend_score = calculate_trend_score(current_price, ma50, ma200, rsi, one_month_return, volume_ratio)
price_percentile = get_price_percentile(history, current_price)

investment_scores = calculate_investment_scores(
    trend_score, pe_ratio, one_month_return, six_month_return, rsi, volume_ratio, price_percentile
)

horizon_scores = calculate_horizon_scores(
    investment_scores, one_week_return, one_month_return, six_month_return, rsi, volume_ratio
)

historical_context = get_historical_context(history)
market_status = get_market_status(history)

peer_df = build_peer_dataframe(ticker, one_month_return)
peer_difference = get_peer_difference(peer_df, ticker, one_month_return)

summary_text = generate_executive_summary(
    company_name, investment_scores["overall"], rsi, volume_ratio, one_month_return, peer_difference
)

st.markdown('<div class="big-title">AlphaLens Stock Insight</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Investment research made clearer with technical analysis, peer comparison, historical context, and market insights.</div>',
    unsafe_allow_html=True,
)

render_status_card(market_status)

st.header(company_name)
st.write(f"**Ticker:** {ticker} | **Sector:** {sector} | **Industry:** {industry}")

render_summary_card(investment_scores["overall"], summary_text)

render_metrics(
    current_price, daily_change_pct, market_cap, pe_ratio, trend_score,
    high_52w, low_52w, latest_volume, volume_ratio
)

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Overview", "Technical Analysis", "Peer Comparison", "Research Report", "Raw Data"
])

with tab1:
    st.subheader("Market Snapshot")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("1W Return", f"{one_week_return:.2f}%" if one_week_return is not None else "N/A")
    c2.metric("1M Return", f"{one_month_return:.2f}%" if one_month_return is not None else "N/A")
    c3.metric("6M Return", f"{six_month_return:.2f}%" if six_month_return is not None else "N/A")
    c4.metric("Price Percentile", f"{price_percentile:.1f}%")

    render_scorecard(investment_scores, horizon_scores)
    render_history_card(historical_context)

    st.subheader("Key Insights")

    distance_from_high = ((high_52w - current_price) / high_52w) * 100
    distance_from_low = ((current_price - low_52w) / low_52w) * 100

    st.write(f"- {ticker} is trading **{distance_from_high:.2f}% below** its 52-week high.")
    st.write(f"- {ticker} is trading **{distance_from_low:.2f}% above** its 52-week low.")
    st.write(f"- Current price is higher than **{price_percentile:.1f}%** of closes over the last 2 years.")

    if current_price > ma50 and current_price > ma200:
        st.success("The stock is trading above both major moving averages.")
    elif current_price < ma50 and current_price < ma200:
        st.warning("The stock is trading below both major moving averages.")
    else:
        st.info("The stock is between its 50-day and 200-day moving averages.")

with tab2:
    render_price_chart(history)

    st.subheader("Technical Indicators")
    c1, c2, c3 = st.columns(3)
    c1.metric("RSI", f"{rsi:.2f}")
    c2.metric("50-Day MA", f"${ma50:,.2f}")
    c3.metric("200-Day MA", f"${ma200:,.2f}")

    render_rsi_chart(history)

with tab3:
    st.subheader("Peer Comparison")
    st.dataframe(peer_df, use_container_width=True)

    fig = go.Figure()
    fig.add_trace(go.Bar(x=peer_df["Ticker"], y=peer_df["1M Return (%)"], name="1M Return"))
    fig.update_layout(height=400, xaxis_title="Ticker", yaxis_title="1M Return (%)")
    st.plotly_chart(fig, use_container_width=True)

    if peer_difference is not None:
        if peer_difference > 3:
            st.success(f"{ticker} is outperforming its peer group by about {peer_difference:.2f}% over the past month.")
        elif peer_difference < -3:
            st.warning(f"{ticker} is underperforming its peer group by about {abs(peer_difference):.2f}% over the past month.")
        else:
            st.info(f"{ticker} is performing roughly in line with its peer group over the past month.")

with tab4:
    render_report_section(
        company_name, ticker, sector, industry, current_price, daily_change_pct,
        trend_score, rsi, one_month_return, six_month_return, volume_ratio,
        price_percentile, investment_scores, horizon_scores, historical_context, market_status
    )

with tab5:
    st.subheader("Recent Historical Data")
    st.dataframe(history.tail(30), use_container_width=True)
