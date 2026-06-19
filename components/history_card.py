import streamlit as st


def render_history_card(context):
    st.subheader("Historical Context")
    st.info(context["higher_text"])
    st.info(context["lower_text"])
    st.success(
        f"Current price is higher than {context['percentile']:.1f}% of all closing prices "
        f"in the available 2-year history. Only {context['days_higher_percent']:.1f}% of closes were higher."
    )
