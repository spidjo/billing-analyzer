import streamlit as st
import sqlite3
import pandas as pd
import os
import bcrypt
import datetime

from anomaly_detector import detect_anomalies
from report_generator import generate_pdf_report
from email_sender import send_email_with_attachment
from io import BytesIO
from dotenv import load_dotenv
from email_validator import validate_email, EmailNotValidError
from login import login_form, logout


# === Setup ===
st.set_page_config(page_title="Billing Analyzer", layout="wide")
load_dotenv()
EMAIL_SENDER = os.getenv("SENDER_EMAIL")
EMAIL_PASSWORD = os.getenv("SENDER_PASSWORD")

DB_FILE = "billing.db"
SQL_DIR = "sql"

def run_sql_query(sql_file):
    conn = sqlite3.connect(DB_FILE)
    with open(os.path.join(SQL_DIR, sql_file), 'r') as f:
        query = f.read()
    result = pd.read_sql_query(query, conn)
    conn.close()
    return result

# === Role-Specific Views ===
def show_admin_panel():
    st.header("👑 Admin Panel")
    st.write("Manage users, roles, and access control.")
    from user_admin import fetch_users, delete_user, create_user
    users = fetch_users()
    if users:
        for uid, username, user_role in users:
            col1, col2, col3 = st.columns([4, 3, 1])
            col1.write(username)
            col2.write(user_role)
            if col3.button("❌ Delete", key=f"del_{uid}"):
                delete_user(uid)
                st.rerun()
    else:
        st.info("No users found.")

    st.markdown("---")
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
    
    if st.sidebar.button("⚙️ Run Monthly Billing"):
        new_bills = generate_monthly_bills()
        st.success(f"✅ {new_bills} new bills generated.")

def show_analyst_dashboard():
    st.header("📊 Analyst Dashboard")
    st.write("Access analytics, trends, and anomalies.")
    revenue = run_sql_query("revenue_by_month.sql")
    top_customers = run_sql_query("top_customers.sql")

    st.subheader("💰 Monthly Revenue")
    st.bar_chart(revenue.set_index("month"))
    st.subheader("🏅 Top Customers")
    st.dataframe(top_customers)

def show_client_summary():
    st.header("👤 Client Summary")
    st.write("Your billing performance and recent activity.")
    username = st.session_state.get("username")
    query = f"""
        SELECT billing_date, cost 
        FROM billing_records 
        WHERE customer_id = (SELECT id FROM users WHERE username = ?) 
        ORDER BY billing_date DESC LIMIT 12;
    """
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query(query, conn, params=(username,))
    conn.close()

    if df.empty:
        st.warning("No billing data available.")
        return

    df["billing_date"] = pd.to_datetime(df["billing_date"])
    df = df.set_index("billing_date")
    st.line_chart(df["cost"], use_container_width=True)
    st.bar_chart(df["cost"], use_container_width=True)

# === Main Dashboard Navigation ===
def main_dashboard():
    role = st.session_state.get("role")
    username = st.session_state.get("username")
    st.sidebar.write(f"👤 Logged in as: {username} ({role})")
    st.sidebar.button("Logout", on_click=logout)

    if role == "admin":
        page = st.sidebar.radio("Admin Menu", ["Admin Panel", "Upload Billing CSV"])
        if page == "Admin Panel":
            show_admin_panel()
        else:
            show_csv_analyzer()

    elif role == "client":
        page = st.sidebar.radio("Client Menu", ["Upload Billing CSV", "Client Summary"])
        if page == "Upload Billing CSV":
            show_csv_analyzer()
        else:
            show_client_summary()

    else:
        st.error("Unknown role.")

# === CSV Analyzer ===
def show_csv_analyzer():
    uploaded_file = st.file_uploader("Upload billing CSV", type=["csv"])
    if not uploaded_file:
        return
    
    try:
        df = pd.read_csv(uploaded_file)
    except Exception as e:
        st.error(f"❌ Failed to read CSV: {e}")
        return

    st.subheader("Map Your Data Columns")
    if "mapping_done" not in st.session_state:
        st.session_state["mapping_done"] = False

    if "last_uploaded_filename" not in st.session_state or \
        st.session_state["last_uploaded_filename"] != uploaded_file.name:
        st.session_state["mapping_done"] = False
        st.session_state["last_uploaded_filename"] = uploaded_file.name

    if not st.session_state["mapping_done"]:
        with st.form("column_mapping"):
            customer_col = st.selectbox("Customer ID column", df.columns)
            date_col = st.selectbox("Billing Date column", df.columns)
            cost_col = st.selectbox("Billing Amount/Cost column", df.columns)
            submitted = st.form_submit_button("Apply Mapping")
            if submitted:
                st.session_state["mapping_done"] = True
                st.session_state["customer_col"] = customer_col
                st.session_state["date_col"] = date_col
                st.session_state["cost_col"] = cost_col
                st.rerun()
    else:
        
        df = df.rename(columns={
            st.session_state["customer_col"]: "customer_id",
            st.session_state["date_col"]: "billing_date",
            st.session_state["cost_col"]: "cost"
        })

        # === Clean and validate data ===
        df["billing_date"] = pd.to_datetime(df["billing_date"], errors="coerce")
        df["cost"] = pd.to_numeric(df["cost"], errors="coerce")
        df = df.dropna(subset=["customer_id", "billing_date", "cost"])
        
        # === Deduplicate to avoid re-inserts ===
        conn = sqlite3.connect(DB_FILE)
        existing = pd.read_sql_query("SELECT customer_id, billing_date FROM billing_records", conn)

        # Normalize both to same format — date only
        # existing["billing_date"] = pd.to_datetime(existing["billing_date"]).dt.date
        df["billing_date"] = pd.to_datetime(df["billing_date"]).dt.date

        # Merge to find new records only
        merged = df.merge(existing, on=["customer_id", "billing_date"], how="left", indicator=True)
        new_records = merged[merged["_merge"] == "left_only"].drop(columns=["_merge"])

        # Insert only new records
        if not new_records.empty:
            new_records.to_sql("billing_records", conn, if_exists="append", index=False)
            st.success(f"✅ {len(new_records)} new billing records inserted into the database.")
        else:
            st.info("No new records to insert (duplicates or invalid rows).")

        conn.close()

        
        tab1, tab2, tab3 = st.tabs(["📈 Revenue", "🏅 Top Customers", "🔍 Anomalies"])

        with tab1:
            df["billing_date"] = pd.to_datetime(df["billing_date"], errors="coerce")
            revenue_df = df.groupby(df["billing_date"].dt.to_period("M"))["cost"].sum().reset_index()
            revenue_df["billing_date"] = revenue_df["billing_date"].astype(str)
            st.bar_chart(revenue_df.set_index("billing_date"))

        with tab2:
            top_customers = df.groupby("customer_id")["cost"].sum().sort_values(ascending=False).head(10).reset_index()
            st.dataframe(top_customers)

        with tab3:
            threshold = st.slider("Z-score Threshold", 1.0, 5.0, 3.0, 0.1)
            df["billing_date"] = pd.to_datetime(df["billing_date"], errors="coerce")
            df = df.dropna(subset=["billing_date", "cost"])
            df["cost"] = pd.to_numeric(df["cost"], errors="coerce")
            df, stats = detect_anomalies(df, threshold)
            anomalies_df = df[df["is_anomaly"]]

            st.write(f"📉 Anomalies Found: {len(anomalies_df)} | Mean: {stats['mean']:.2f}, Std: {stats['std']:.2f}")

            if not anomalies_df.empty:
                st.dataframe(anomalies_df)

                with st.form("report_email_form"):
                    recipient = st.text_input("Recipient email")
                    cc_me = st.checkbox("CC me")
                    send_btn = st.form_submit_button("📧 Send Report")

                    if not EMAIL_SENDER or not EMAIL_PASSWORD:
                        st.warning("⚠️ Email credentials not configured in .env. Email features will be disabled.")

                    if send_btn:
                        try:
                            recipient = validate_email(recipient).email
                            recipients = [recipient]
                            if cc_me and EMAIL_SENDER:
                                recipients.append(EMAIL_SENDER)
                            pdf_buffer = BytesIO()
                            with st.spinner("Generating report..."):
                                generate_pdf_report(anomalies_df, stats, pdf_buffer)
                            pdf_buffer.seek(0)
                            with st.spinner("📤 Sending email..."):
                                send_email_with_attachment(
                                    sender_email=EMAIL_SENDER,
                                    sender_password=EMAIL_PASSWORD,
                                    receiver_email=recipients,
                                    subject="📊 Anomaly Report",
                                    body="Please find attached the anomaly report.",
                                    attachment_buffer=pdf_buffer,
                                    file_name="anomaly_report.pdf"
                                )
                            st.success("✅ Report emailed!")
                        except Exception as e:
                            st.error("❌ Failed to send email. Please check the recipient address and your .env credentials.")
                            st.exception(e)


def generate_monthly_bills():
    today = datetime.date.today()
    first_of_month = today.replace(day=1)

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Fetch all clients
    cursor.execute("SELECT id, username FROM users WHERE role = 'client'")
    clients = cursor.fetchall()

    new_bills = 0
    for customer_id, username in clients:
        # Check if a bill already exists for this month
        cursor.execute("""
            SELECT COUNT(*) FROM billing_records 
            WHERE customer_id = ? AND billing_date = ?
        """, (customer_id, first_of_month))
        already_billed = cursor.fetchone()[0]

        if already_billed == 0:
            # Example logic: flat monthly charge
            flat_fee = 49.99  # Or pull from a plan table if available
            cursor.execute("""
                INSERT INTO billing_records (customer_id, billing_date, cost, usage_details)
                VALUES (?, ?, ?, ?)
            """, (customer_id, first_of_month, flat_fee, "Auto-billed monthly charge"))
            new_bills += 1

    conn.commit()
    conn.close()
    return new_bills

# === Entry Point ===
login_form()
if st.session_state.get("authenticated"):
    main_dashboard()
else:
    st.stop()
