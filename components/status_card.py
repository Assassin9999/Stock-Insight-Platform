import streamlit as st


def render_status_card(status):
    if status["status_type"] == "open":
        st.success(f"🟢 {status['status']}")
    else:
        st.info(f"🔴 {status['status']}")

    c1, c2 = st.columns(2)
    c1.write(f"**Current time:** {status['current_time']}")
    c2.write(f"**Latest data timestamp:** {status['latest_data_time']}")
