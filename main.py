# main.py
import streamlit as st
from utils.auth import login_form, logout
from utils.session import init_session_state
from utils.menu import get_menu_by_role

st.set_page_config(page_title="Billing Analyzer", layout="wide")
init_session_state()

if not st.session_state["authenticated"]:
    login_form()
    st.stop()

role = st.session_state["role"]
username = st.session_state["username"]
menu_items = get_menu_by_role(role)

# Sidebar Header
st.sidebar.title("📊 Billing Analyzer")
st.sidebar.markdown(f"**User:** `{username}`")
st.sidebar.markdown(f"**Role:** `{role}`")

# Sidebar Navigation
selected_page = st.sidebar.radio("📌 Navigation", list(menu_items.values()))
st.session_state["selected_page"] = selected_page

st.title("📊 Welcome to MzansiTel Billing Analyzer")
st.info("Use the sidebar to navigate to different sections.")

