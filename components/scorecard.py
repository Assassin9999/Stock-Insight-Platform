import streamlit as st
import plotly.graph_objects as go
from utils.scoring import generate_score_reasoning, score_label


def render_progress(label, value):
    st.write(f"**{label}: {value}/100**")
    st.progress(value / 100)


def render_scorecard(scores, horizon_scores):
    st.subheader("Investment Scorecard")

    overall = scores["overall"]
    label = score_label(overall)

    st.markdown(
        f"""
        <div class="score-card">
            <div class="badge bullish">{label}</div>
            <h2>★★★★☆ Overall AlphaLens Score: {overall}/100</h2>
            <p class="summary-text">Scores are educational research signals, not buy/sell instructions.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    h1, h2, h3 = st.columns(3)
    h1.metric("Long-Term Investor", f"{horizon_scores['Long-Term Investor']}/100", score_label(horizon_scores["Long-Term Investor"]))
    h2.metric("Swing Trader", f"{horizon_scores['Swing Trader']}/100", score_label(horizon_scores["Swing Trader"]))
    h3.metric("Day Trader", f"{horizon_scores['Day Trader']}/100", score_label(horizon_scores["Day Trader"]))

    c1, c2 = st.columns([1, 1])

    with c1:
        render_progress("Trend", scores["trend"])
        render_progress("Momentum", scores["momentum"])
        render_progress("Valuation", scores["valuation"])
        render_progress("Risk", scores["risk"])
        render_progress("Growth", scores["growth"])

    with c2:
        categories = ["Trend", "Momentum", "Valuation", "Risk", "Growth"]
        values = [scores["trend"], scores["momentum"], scores["valuation"], scores["risk"], scores["growth"]]

        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(r=values + [values[0]], theta=categories + [categories[0]], fill="toself", name="Score"))
        fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=False, height=350)
        st.plotly_chart(fig, use_container_width=True)

    positives, cautions = generate_score_reasoning(scores)

    left, right = st.columns(2)
    with left:
        st.success("Strengths")
        if positives:
            for item in positives:
                st.write(f"✓ {item}")
        else:
            st.write("No major strengths detected.")

    with right:
        st.warning("Risks / Cautions")
        if cautions:
            for item in cautions:
                st.write(f"• {item}")
        else:
            st.write("No major cautions detected.")
