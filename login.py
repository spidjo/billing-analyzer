import streamlit as st
import sqlite3
import bcrypt

DB_FILE = "billing.db"

# Hashing functions
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())

# Authenticate user from DB
def authenticate_user(username, password):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT password, role FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()
    if result and check_password(password, result[0]):
        return result[1]  # Return user role
    return None

# Registration (for admin use only)
def register_user(username, password, role):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    hashed = hash_password(password)
    try:
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                       (username, hashed, role))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

# Login UI

def login_form():
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
        st.session_state["role"] = None

    if not st.session_state["authenticated"]:
        with st.form("login_form"):
            st.subheader("🔐 Login")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login")
            if submitted:
                role = authenticate_user(username, password)
                if role:
                    st.session_state["authenticated"] = True
                    st.session_state["role"] = role
                    st.success(f"Welcome, {username}! Role: {role}")
                    st.rerun()
                else:
                    st.error("Invalid username or password")

# Logout UI
def logout():
    st.session_state["authenticated"] = False
    st.session_state["role"] = None
    st.rerun()
