import streamlit as st
from utils.scoring import score_label


def generate_research_report(company_name, ticker, sector, industry, current_price, daily_change_pct, trend_score, rsi, one_month_return, six_month_return, volume_ratio, price_percentile, scores, horizon_scores, context, market_status):
    outlook = score_label(scores["overall"])

    return f"""
# {company_name} Research Report

**Ticker:** {ticker}  
**Sector:** {sector}  
**Industry:** {industry}  

## Data Status

**Market Status:** {market_status['status']}  
**Current Time:** {market_status['current_time']}  
**Latest Data Timestamp:** {market_status['latest_data_time']}  

## Overall AlphaLens Score

**{outlook}** — Overall score: **{scores['overall']}/100**.

## Horizon-Based Scores

- Long-Term Investor: **{horizon_scores['Long-Term Investor']}/100**
- Swing Trader: **{horizon_scores['Swing Trader']}/100**
- Day Trader: **{horizon_scores['Day Trader']}/100**

## Price Action

The stock is currently trading at **${current_price:,.2f}**, with a daily move of **{daily_change_pct:.2f}%**.

Over the last month, the stock returned **{one_month_return:.2f}%**.  
Over the last six months, the stock returned **{six_month_return:.2f}%**.

The current price is higher than **{price_percentile:.1f}%** of closing prices from the last two years.

## Historical Context

- {context["higher_text"]}
- {context["lower_text"]}

## Score Breakdown

- Trend: **{scores['trend']}/100**
- Momentum: **{scores['momentum']}/100**
- Valuation: **{scores['valuation']}/100**
- Risk: **{scores['risk']}/100**
- Growth: **{scores['growth']}/100**

## Momentum

The current RSI is **{rsi:.2f}**.

## Volume

Current trading volume is **{volume_ratio:.2f}x** its recent average.

## Disclaimer

This report is generated for educational research only and is not financial advice.
"""


def render_report_section(company_name, ticker, sector, industry, current_price, daily_change_pct, trend_score, rsi, one_month_return, six_month_return, volume_ratio, price_percentile, scores, horizon_scores, context, market_status):
    st.subheader("Research Report")

    report = generate_research_report(
        company_name, ticker, sector, industry, current_price, daily_change_pct,
        trend_score, rsi, one_month_return, six_month_return, volume_ratio,
        price_percentile, scores, horizon_scores, context, market_status
    )

    if st.button("Generate Research Report"):
        st.markdown(report)
        st.download_button(
            label="Download Report",
            data=report,
            file_name=f"{ticker}_research_report.md",
            mime="text/markdown",
        )
