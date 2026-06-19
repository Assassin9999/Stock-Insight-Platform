import streamlit as st


def get_rating_label(score):
    if score >= 80:
        return "Strong", "bullish", "★★★★★"
    if score >= 65:
        return "Positive", "bullish", "★★★★☆"
    if score >= 50:
        return "Neutral", "neutral", "★★★☆☆"
    return "Weak", "bearish", "★★☆☆☆"


def render_summary_card(score, summary_text):
    rating_label, rating_class, stars = get_rating_label(score)

    st.markdown(
        f"""
        <div class="summary-card">
            <div class="badge {rating_class}">{rating_label}</div>
            <h2>{stars} Rating: {score}/100</h2>
            <p class="summary-text">{summary_text}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
