# 💼 SQL Billing Analyzer

A Streamlit-powered billing analytics dashboard with role-based login, anomaly detection, email reporting, and monthly billing automation. Perfect for telecom, SaaS, or utility companies looking to track and manage customer billing.

---

## 🚀 Features

- 📊 CSV-based billing data upload
- 👤 Role-based access: `admin`, `client`
- 📈 Monthly revenue and top customer analytics
- ⚠️ Anomaly detection using Z-score
- 📧 Email reporting with PDF export
- 🔐 Secure login with password hashing
- 🧾 Auto-generate monthly billing entries

---

## 📦 Tech Stack

- Python 3.8+
- Streamlit
- SQLite
- Pandas
- bcrypt
- dotenv
- Matplotlib/Altair
- Email utilities

---

## 🔧 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/sql-billing-analyzer.git
cd sql-billing-analyzer
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file from the template:

```bash
cp .env.example .env
```

Edit `.env` to add your email credentials:

```env
SENDER_EMAIL=youremail@example.com
SENDER_PASSWORD=your-app-password
```

---

## ▶️ Run the App

```bash
streamlit run app.py
```

---

## 👥 User Roles

- **Admin:** Can manage users, upload data, generate bills
- **Client:** Can view personal billing summaries and upload their own billing CSV

---

## 📁 File Structure

```
.
├── app.py
├── login.py
├── user_admin.py
├── anomaly_detector.py
├── email_sender.py
├── report_generator.py
├── sql/
│   ├── revenue_by_month.sql
│   └── top_customers.sql
├── .env.example
├── sample_data/
│   ├── demo_billing_data.csv
│   └── demo_client_upload.csv
```

---

## 📂 Sample CSV Format

| Customer ID | Billing Date | Cost |
|-------------|--------------|------|
| 101         | 2024-12-01   | 120  |
| 101         | 2024-12-15   | 80   |
| 102         | 2024-12-02   | 200  |

Ensure column names are correctly mapped when uploading.

---

## 📬 Emailing Reports

- Works only if `.env` is set with Gmail or SMTP credentials
- PDF reports are generated on anomalies and emailed directly from the app

---

## 💼 Use Cases

- Telecom or ISP billing audits  
- Enterprise cost monitoring  
- Freelancers offering billing dashboards or audit reports  
- Portfolio project to showcase Python + SQL + Streamlit + automation

---

## 🧑‍💻 Author

**Siphiwo Lumkwana (Spidjo)**  
GitHub: @spidjo(https://github.com/spidjo)

---

## 📝 License

MIT License – Free to use and modify