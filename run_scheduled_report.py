from anomaly_detector import detect_anomalies
from report_generator import generate_anomaly_report
from email_sender import send_email_with_attachment
from dotenv import load_dotenv
import pandas as pd
import os
import schedule
import time
from datetime import datetime


load_dotenv()
EMAIL_SENDER = os.getenv("SENDER_EMAIL")
EMAIL_PASSWORD = os.getenv("SENDER_PASSWORD")
RECIPIENT = os.getenv("REPORT_RECIPIENT")

def run_report():
    # Load billing data (adjust path or source as needed)
    df = pd.read_csv("data/billing_data.csv")
    
    anomalies = detect_anomalies(df, column='cost', threshold=3.0)
    stats = {
        'mean': df['cost'].mean(),
        'std': df['cost'].std(),
        'count': len(anomalies)
    }

    pdf_path = generate_anomaly_report(anomalies, stats)

    send_email_with_attachment(
        sender_email=EMAIL_SENDER,
        receiver_email=RECIPIENT,
        subject="📊 Scheduled Billing Anomaly Report",
        body="Hello,\n\nPlease find the scheduled anomaly report attached.\n\nRegards,\nBilling Analyzer",
        pdf_path=pdf_path,
        sender_password=EMAIL_PASSWORD
    )
    
    with open("logs/report_log.csv", "a") as log_file:
        log_file.write(f"{datetime.now()}, {len(anomalies)} anomalies\n")

def job():
    print("Generating and sending report...")
    run_report()

# Schedule job every day at 9 AM
schedule.every().day.at("09:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(60)
    
if __name__ == "__main__":
    run_report()
