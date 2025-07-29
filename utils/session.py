# utils/session.py
import streamlit as st

def init_session_state():
    defaults = {
        "authenticated": False,
        "username": "",
        "role": "",
        "email_verified": False,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
