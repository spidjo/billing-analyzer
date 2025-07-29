import streamlit as st
from utils.auth import fetch_users, delete_user, create_user
from utils.session import init_session_state

init_session_state()
if not st.session_state["authenticated"] or st.session_state["role"] != "admin":
    st.error("Admin access only.")
    st.stop()

st.title("🔐 Admin - User Management")

# Existing Users
st.subheader("👥 Existing Users")
users = fetch_users()
for uid, username, role in users:
    col1, col2, col3 = st.columns([4, 3, 1])
    col1.write(username)
    col2.write(role)
    if col3.button("❌ Delete", key=f"del_{uid}"):
        delete_user(uid)
        st.rerun()

st.markdown("---")

# New User Form
st.subheader("➕ Create New User")
with st.form("create_user_form"):
    new_username = st.text_input("Username")
    new_password = st.text_input("Password", type="password")
    new_role = st.selectbox("Role", ["admin", "client"])
    if st.form_submit_button("Create User"):
        if new_username and new_password:
            create_user(new_username, new_password, new_role)
        else:
            st.warning("Please fill in all fields.")
