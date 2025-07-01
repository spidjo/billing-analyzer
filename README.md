# 📊 SQL Billing Analyzer

A Streamlit-powered anomaly detection dashboard for analyzing telecom billing data using SQL & Python. Built to help identify unusual billing patterns, generate PDF reports, and email them to stakeholders.

---

## 🚀 Features

✅ Load and analyze telecom billing data  
✅ Detect anomalies in cost using Z-score method  
✅ Interactive Streamlit dashboard  
✅ Visualizations (scatter, box plots) of costs vs z-scores  
✅ Generate PDF anomaly reports  
✅ Email reports directly via the dashboard  
✅ Monthly simulated billing data generator  
✅ Support for automated scheduled email reports  

---

## 📁 Project Structure

```
sql-billing-analyzer/
│
├── data/
│   └── monthly_billing/         # Simulated monthly billing CSVs
├── anomaly_detector.py          # Z-score based anomaly detection logic
├── report_generator.py          # PDF generator for anomaly summaries
├── email_sender.py              # Sends email with PDF attachments
├── streamlit_app.py             # Main dashboard app
├── generate_test_data.py        # One-off data generator
├── generate_monthly_billing_data.py  # Monthly data simulation
├── run_scheduled_report.py      # Daily/weekly auto reporting
├── requirements.txt             # Python dependencies
├── .env                         # Email credentials (not committed)
└── README.md
```

---

## 📷 Dashboard Preview

![screenshot](assets/streamlit_dashboard.png) *(Optional: add a real screenshot)*

---

## 🛠️ Installation

```bash
git clone https://github.com/yourusername/sql-billing-analyzer.git
cd sql-billing-analyzer
pip install -r requirements.txt
```

---

## 🧪 Generate Simulated Billing Data

```bash
# Generate 12 months of billing data (200 records each)
python generate_monthly_billing_data.py
```

Data will be saved under `data/monthly_billing/`.

---

## 📊 Launch the Streamlit Dashboard

```bash
streamlit run streamlit_app.py
```

Use the sidebar to upload a billing CSV or choose from monthly samples.

---

## 🧠 Anomaly Detection

- Uses **Z-score** method to flag billing cost anomalies.
- Displays:
  - Box and scatter plots (cost vs z-score)
  - Summary stats (mean, std dev, count)
  - Anomalous customer highlights

---

## 📄 Generate PDF Report

Click **"Generate PDF"** in the Anomaly tab to export a summary of outliers.

---

## ✉️ Email PDF Report

1. Enter recipient email
2. (Optional) Check “CC me”
3. Click **Send Report**

Includes validation via `email-validator`.

---

## 🔁 Scheduled Report Delivery

To email daily reports automatically, set up:

### Option A: Cron Job (Linux/Mac)
```bash
crontab -e
```

```cron
0 9 * * * /usr/bin/python3 /full/path/run_scheduled_report.py
```

### Option B: Python `schedule` (Cross-platform)

```bash
python run_scheduled_report.py
```

---

## 🔐 .env Setup 

Create a `.env` file in root:

```
SENDER_EMAIL=you@gmail.com
SENDER_PASSWORD=your_app_password
REPORT_RECIPIENT=manager@example.com
```

Use [Gmail App Passwords](https://support.google.com/accounts/answer/185833) or similar.

---

## ✅ Requirements

```txt
pandas
numpy
streamlit
matplotlib
email-validator
reportlab
faker
python-dotenv
schedule
```

Install with:

```bash
pip install -r requirements.txt
```

---

## 📬 Future Improvements

- Anomaly detection via ML (Isolation Forest, etc.)
- Role-based login for clients
- REST API for integrations
- Cloud deployment (e.g., Streamlit Cloud, Railway)

---

## 💼 Use Cases

- Telecom or ISP billing audits  
- Enterprise cost monitoring  
- Freelancers offering billing dashboards or audit reports  
- Portfolio project to showcase Python + SQL + Streamlit + automation

---

## 🧑‍💻 Author

**Siphiwo Lumkwana (Spidjo)**  

---

## 🛡️ License

MIT License – Free to use and modify
