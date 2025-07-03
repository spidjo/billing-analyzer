import streamlit as st
import sqlite3
import bcrypt
import datetime
from email_validator import validate_email, EmailNotValidError

DB_FILE = "billing.db"

# === Database Setup ===
def init_user_table():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password BLOB NOT NULL,
            role TEXT NOT NULL,
            first_name TEXT,
            last_name TEXT,
            company_name TEXT,
            email TEXT,
            registration_date TEXT
        );
    """)
    conn.commit()
    conn.close()

# === Authentication ===
def authenticate_user(username, password):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT password, role FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()
    if row:
        stored_hash, role = row
        if bcrypt.checkpw(password.encode(), stored_hash):
            return True, role
    return False, None

# === Registration ===
def register_user(username, password, first_name, last_name, company, email):
    try:
        valid = validate_email(email).email
    except EmailNotValidError as e:
        st.error(f"Invalid email: {e}")
        return False

    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    registration_date = datetime.date.today().isoformat()

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO users (username, password, role, first_name, last_name, company_name, email, registration_date)
            VALUES (?, ?, 'client', ?, ?, ?, ?, ?)
        """, (username, hashed_pw, first_name, last_name, company, valid, registration_date))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        st.warning("Username already exists.")
        return False
    finally:
        conn.close()

# === Login Form ===
def login_form():
    init_user_table()
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    login_tab, register_tab = st.tabs(["🔐 Login", "📝 Register"])

    with login_tab:
        st.subheader("Login")
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        login_btn = st.button("Login")

        if login_btn:
            valid, role = authenticate_user(username, password)
            if valid:
                st.session_state.authenticated = True
                st.session_state.username = username
                st.session_state.role = role
                st.success(f"Welcome, {username}!")
                st.rerun()
            else:
                st.error("Invalid username or password.")

    with register_tab:
        st.subheader("Client Registration")
        new_username = st.text_input("Username", key="reg_username")
        new_password = st.text_input("Password", type="password", key="reg_password")
        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
        company = st.text_input("Company Name")
        email = st.text_input("Email Address")
        register_btn = st.button("Register")

        if register_btn:
            if not new_username or not new_password or not first_name or not last_name or not company or not email:
                st.warning("All fields are required.")
            else:
                success = register_user(new_username, new_password, first_name, last_name, company, email)
                if success:
                    st.success("✅ Registration successful. Please log in.")
                    st.rerun()

# === Logout Function ===
def logout():
    for key in ["authenticated", "username", "role"]:
        st.session_state.pop(key, None)
    st.rerun()
