import streamlit as st
import pandas as pd
import sqlite3
import os
import numpy as np
from anomaly_detector import detect_anomalies
import matplotlib.pyplot as plt
from report_generator import generate_anomaly_report
from email_sender import send_email_with_attachment
from dotenv import load_dotenv
from email_validator import validate_email, EmailNotValidError


load_dotenv()
EMAIL_SENDER = os.getenv("SENDER_EMAIL")
EMAIL_PASSWORD = os.getenv("SENDER_PASSWORD")

DB_FILE = 'billing.db'
SQL_DIR = 'sql'

def load_csv(csv_file):
    df = pd.read_csv(csv_file, parse_dates=['billing_date'])
    conn = sqlite3.connect(DB_FILE)
    df.to_sql('cdrs', conn, if_exists='replace', index=False)
    return df

def run_sql_query(sql_file):
    conn = sqlite3.connect(DB_FILE)
    with open(os.path.join(SQL_DIR, sql_file), 'r') as f:
        query = f.read()
    result = pd.read_sql_query(query, conn)
    return result

st.set_page_config(page_title="SQL Billing Analyzer", layout="wide")

st.title("📊 SQL Billing Analyzer Dashboard")

uploaded_file = st.file_uploader("📂 Upload your CDR CSV", type=["csv"])

if uploaded_file:
    df = load_csv(uploaded_file)
    st.success("✅ Data loaded!")

    tab1, tab2, tab3 = st.tabs(["📈 Revenue", "🏅 Top Customers", "🔍 Anomalies"])

    with tab1:
        st.subheader("💰 Monthly Revenue")
        revenue = run_sql_query("revenue_by_month.sql")
        st.dataframe(revenue)
        st.bar_chart(revenue.set_index('month'))

    with tab2:
        st.subheader("🏅 Top Customers")
        top_customers = run_sql_query("top_customers.sql")
        st.dataframe(top_customers)


    with tab3:
        st.subheader("🔍 Cost Anomaly Detection")

        threshold = st.slider("Z-score Threshold", min_value=1.0, max_value=5.0, value=3.0, step=0.1,
                            help="Lower values flag more records as anomalies.")

        # Detect anomalies
        anomalies = detect_anomalies(df, column='cost', threshold=threshold)

        # Add z-score column to full dataset for charting
        df['z_score'] = (df['cost'] - df['cost'].mean()) / df['cost'].std()

        # Summary stats 
        st.markdown("### 📌 Summary Stats")
        col1, col2, col3 = st.columns(3)
        col1.metric("Mean Cost", f"{df['cost'].mean():.2f}")
        col2.metric("Std Dev", f"{df['cost'].std():.2f}")
        col3.metric("Anomalies", len(anomalies))

        # Scatter Plot
        st.markdown("### 📉 Cost vs Z-score")
        fig, ax = plt.subplots()
        ax.scatter(df['z_score'], df['cost'], alpha=0.5, label='All')
        if not anomalies.empty:
            ax.scatter(anomalies['z_score'], anomalies['cost'], color='red', label='Anomalies')
        ax.axvline(x=threshold, color='orange', linestyle='--', label='Threshold')
        ax.axvline(x=-threshold, color='orange', linestyle='--')
        ax.set_xlabel('Z-score')
        ax.set_ylabel('Cost')
        ax.legend()
        st.pyplot(fig)

        # Table of anomalies
        st.markdown("### 🔍 Anomalous Records")
        if not anomalies.empty:
            st.dataframe(anomalies)
            csv = anomalies.to_csv(index=False).encode('utf-8')
            st.download_button("⬇️ Download Anomalies CSV", csv, "anomalies.csv", "text/csv")
        else:
            st.info("No anomalies detected at this threshold.")

        # Top subscribers by anomaly count
        if not anomalies.empty and 'subscriber_id' in anomalies.columns:
            st.markdown("### 🧑‍💼 Subscribers with Most Anomalies")
            top_subs = anomalies['subscriber_id'].value_counts().reset_index()
            top_subs.columns = ['subscriber_id', 'anomaly_count']
            st.dataframe(top_subs)


        if not anomalies.empty:
            stats = {
                'mean': df['cost'].mean(),
                'std': df['cost'].std(),
                'count': len(anomalies)
            }

            if st.button("🧾 Generate PDF Summary Report"):
                pdf_path = generate_anomaly_report(anomalies, stats)
                with open(pdf_path, "rb") as f:
                    st.download_button("⬇️ Download PDF Report", f.read(), "anomaly_report.pdf", "application/pdf")


    st.markdown("### 📤 Email PDF Report")

    with st.form("email_form"):
        recipient = st.text_input("Recipient Email", placeholder="client@example.com")
        cc_me = st.checkbox("CC me")
        custom_message = st.text_area("Email Message", value="Please find attached the latest billing anomaly report.")
        submit_email = st.form_submit_button("📧 Send Report")

        if submit_email:
            try:
                # ✅ Validate recipient email
                recipient = validate_email(recipient).email

                # 👤 Add CC to sender
                recipients = [recipient]
                if cc_me and EMAIL_SENDER:
                    recipients.append(EMAIL_SENDER)

                stats = {
                    'mean': df['cost'].mean(),
                    'std': df['cost'].std(),
                    'count': len(anomalies)
                }

                pdf_path = generate_anomaly_report(anomalies, stats)

                send_email_with_attachment(
                    sender_email=EMAIL_SENDER,
                    receiver_email=recipients,
                    subject="📊 SQL Billing Anomaly Report",
                    body=custom_message,
                    pdf_path=pdf_path,
                    sender_password=EMAIL_PASSWORD
                )
                st.success(f"Email sent to {', '.join(recipients)} ✅")

            except EmailNotValidError as e:
                st.error(f"Invalid email: {str(e)}")
            except Exception as e:
                st.error(f"Failed to send email: {e}")
