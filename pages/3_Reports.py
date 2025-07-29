import streamlit as st
from utils.session import init_session_state

init_session_state()
if not st.session_state["authenticated"]:
    st.error("Login required.")
    st.stop()

st.title("📑 Billing Reports")
st.write("Generate monthly, quarterly, and custom usage reports here.")
