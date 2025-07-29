import streamlit as st
from utils.session import init_session_state

init_session_state()
if not st.session_state["authenticated"] or st.session_state["role"] != "client":
    st.error("Access denied. Clients only.")
    st.stop()

st.title("📈 Client Dashboard")
st.write("Here you can view usage stats, recent charges, and submit billing queries.")
