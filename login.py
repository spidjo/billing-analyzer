import streamlit as st
import sqlite3
import bcrypt
import datetime
import secrets
from email_validator import validate_email, EmailNotValidError
from dotenv import load_dotenv
import os
from email_sender import send_plain_email  # Replace with your simple email sender if needed

load_dotenv()
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
DB_FILE = "billing.db"

# === DB Initialization ===
def init_user_table():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password BLOB NOT NULL,
            role TEXT NOT NULL DEFAULT 'client',
            first_name TEXT,
            last_name TEXT,
            company_name TEXT,
            email TEXT UNIQUE NOT NULL,
            registration_date TEXT,
            is_verified INTEGER DEFAULT 0,
            verification_token TEXT
        );
    """)
    conn.commit()
    conn.close()

# === Strong Password Validation ===
def is_strong_password(password):
    return (
        len(password) >= 8 and
        any(c.islower() for c in password) and
        any(c.isupper() for c in password) and
        any(c.isdigit() for c in password) and
        any(c in "!@#$%^&*()-_=+[{]};:'\",<.>/?\\|" for c in password)
    )

# === Registration ===
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

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO users (username, password, first_name, last_name, company_name, email, registration_date, verification_token)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (username, hashed_pw, first_name, last_name, company, valid_email, reg_date, token))
        conn.commit()

        # Send confirmation email
        verify_link = f"https://billing-analyzer-app.streamlit.app/?verify={token}"  # Adjust for production
        body = f"Hello {first_name},\n\nPlease verify your email address by clicking the link below:\n{verify_link}"
        send_plain_email(
            sender_email=SENDER_EMAIL,
            sender_password=SENDER_PASSWORD,
            receiver_email=[valid_email],
            subject="Email Verification Required",
            body=body
        )

        return token
    except sqlite3.IntegrityError as e:
        st.warning(f"Registration failed: {e}")
        return False
    finally:
        conn.close()

# === Email Verification ===
def verify_email_token(token):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE verification_token = ?", (token,))
    row = cursor.fetchone()
    if row:
        cursor.execute("""
            UPDATE users SET is_verified = 1, verification_token = NULL
            WHERE id = ?
        """, (row[0],))
        conn.commit()
        st.success("✅ Email verified! You may now log in.")
    else:
        st.error("Invalid or expired verification link.")
    conn.close()

# === Authentication ===
def authenticate_user(username, password):
    conn = sqlite3.connect(DB_FILE)
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

# === Main Login Form ===
def login_form():
    init_user_table()

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if st.query_params.get("verify"):
        verify_email_token(st.query_params["verify"])
        st.query_params

    tab_login, tab_register = st.tabs(["🔐 Login", "📝 Register"])

    with tab_login:
        st.subheader("Login")
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login"):
            result, role = authenticate_user(username, password)
            if result == "unverified":
                st.warning("Email not verified. Please check your inbox.")
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
                st.warning("Please fill in all fields.")
            else:
                token = register_user(new_username, new_password, first_name, last_name, company, email)
                if token:
                    st.success("✅ Registration successful. Check your email for verification.")
                    st.query_params  # Clean URL

# === Logout ===
def logout():
    st.session_state.clear()
