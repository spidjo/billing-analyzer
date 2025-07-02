import streamlit as st
import sqlite3
import bcrypt

DB_FILE = "billing.db"

def get_connection():
    return sqlite3.connect(DB_FILE, check_same_thread=False)

def fetch_users():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, role FROM users")
    users = cursor.fetchall()
    conn.close()
    return users

def create_user(username, password, role):
    conn = get_connection()
    cursor = conn.cursor()
    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    try:
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, hashed_pw, role))
        conn.commit()
        st.success("User created successfully!")
    except sqlite3.IntegrityError:
        st.error("Username already exists.")
    conn.close()

def delete_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    st.success("User deleted.")

# Streamlit admin panel
st.set_page_config(page_title="User Management", layout="centered")
st.title("🔐 Admin - User Management")

# Session-based access control (you should integrate this with login module)
if st.session_state["role"] != "admin":
    st.error("Access denied. Admins only.")
    st.stop()

# Display users
st.subheader("👥 Existing Users")
users = fetch_users()
if users:
    for uid, username, role in users:
        col1, col2, col3 = st.columns([4, 3, 1])
        col1.write(username)
        col2.write(role)
        if col3.button("❌ Delete", key=f"del_{uid}"):
            delete_user(uid)
            st.rerun()
else:
    st.info("No users found.")

st.markdown("---")

# Create new user
st.subheader("➕ Create New User")
with st.form("create_user_form"):
    new_username = st.text_input("Username")
    new_password = st.text_input("Password", type="password")
    new_role = st.selectbox("Role", ["admin", "client"])
    submit = st.form_submit_button("Create User")
    if submit:
        if not new_username or not new_password:
            st.warning("Please provide both username and password.")
        else:
            create_user(new_username, new_password, new_role)
