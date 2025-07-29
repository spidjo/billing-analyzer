# utils/auth.py
import streamlit as st
import datetime
import secrets
import bcrypt
from email_validator import validate_email, EmailNotValidError
from dotenv import load_dotenv
import os

from utils.db import get_connection, init_user_table
from email_sender import send_plain_email
from utils.session import init_session_state

load_dotenv()
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")

# ----------------- Utility Functions -----------------
def is_strong_password(password):
    return (
        len(password) >= 8 and
        any(c.islower() for c in password) and
        any(c.isupper() for c in password) and
        any(c.isdigit() for c in password) and
        any(c in "!@#$%^&*()-_=+[{]};:'\",<.>/?\\|" for c in password)
    )

# ----------------- Database Interactions -----------------
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

# ----------------- Authentication Logic -----------------
def authenticate_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT password, role, is_verified FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()

    if row:
        stored_hash, role, is_verified = row
        if not is_verified:
            return "unverified", None
        if bcrypt.checkpw(password.encode(), stored_hash):
            return True, role
    return False, None

def register_user(username, password, first_name, last_name, company, email):
    try:
        valid_email = validate_email(email).email
    except EmailNotValidError as e:
        st.error(f"Invalid email: {e}")
        return False

    if not is_strong_password(password):
        st.warning("Password must be at least 8 characters long and include uppercase, lowercase, number, and special character.")
        return False

    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    reg_date = datetime.date.today().isoformat()
    token = secrets.token_urlsafe(32)

    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO users (username, password, first_name, last_name, company_name, email, registration_date, verification_token)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (username, hashed_pw, first_name, last_name, company, valid_email, reg_date, token))
        conn.commit()

        verify_link = f"http://localhost:8501/Home?verify={token}"
        body = f"Hi {first_name},\n\nPlease verify your email address:\n{verify_link}"
        send_plain_email(
            sender_email=SENDER_EMAIL,
            sender_password=SENDER_PASSWORD,
            receiver_email=[valid_email],
            subject="Verify your email",
            body=body
        )

        return token
    except sqlite3.IntegrityError as e:
        st.warning(f"Registration failed: {e}")
        return False
    finally:
        conn.close()

def verify_email_token(token):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE verification_token = ?", (token,))
    row = cursor.fetchone()
    if row:
        cursor.execute("""
            UPDATE users
            SET is_verified = 1, verification_token = NULL
            WHERE id = ?
        """, (row[0],))
        conn.commit()
        st.success("✅ Email verified! You may now log in.")
    else:
        st.error("Invalid or expired verification link.")
    conn.close()

# ----------------- Streamlit Forms -----------------
def login_form():
    init_session_state()
    init_user_table()

    query_params = st.query_params
    if "verify" in query_params:
        verify_email_token(query_params["verify"])
        st.query_params.clear()

    tab_login, tab_register = st.tabs(["🔐 Login", "📝 Register"])

    with tab_login:
        st.subheader("Login")
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login"):
            result, role = authenticate_user(username, password)
            if result == "unverified":
                st.warning("Please verify your email.")
            elif result:
                st.session_state.authenticated = True
                st.session_state.username = username
                st.session_state.role = role
                st.rerun()
            else:
                st.error("Invalid credentials.")

    with tab_register:
        st.subheader("Register as Client")
        new_username = st.text_input("Username", key="reg_user")
        new_password = st.text_input("Password", type="password", key="reg_pass")
        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
        company = st.text_input("Company")
        email = st.text_input("Email")

        if st.button("Register"):
            if not all([new_username, new_password, first_name, last_name, company, email]):
                st.warning("All fields are required.")
            else:
                token = register_user(new_username, new_password, first_name, last_name, company, email)
                if token:
                    st.success("✅ Registration successful. Please check your email to verify.")

def logout():
    st.session_state.clear()
