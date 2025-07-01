# 📊 SQL Billing Analyzer Toolkit

A lightweight Python + SQL tool that loads CDR (Call Detail Records) data from CSV, analyzes it using SQL, and exports revenue and customer reports — perfect for telecom, SaaS billing, or subscription data.

## 🚀 Features

- Load CDR data (calls, duration, cost) into SQLite
- Run pre-built SQL queries to:
  - 📈 Summarize monthly revenue
  - 🏅 Identify top customers
- Output results to CSV
- Easily extendable with your own SQL scripts

---

## 🛠️ Requirements

- Python 3.7+
- `pandas` (install via `pip install -r requirements.txt`)

---

## 📁 Project Structure

```
sql-billing-analyzer/
├── data/                 # Input CSVs
├── sql/                  # SQL analysis scripts
├── billing_analyzer.py   # Main Python runner
├── requirements.txt
├── README.md
```

---

## 🧪 Sample Usage

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the analyzer
```bash
python billing_analyzer.py
```

### 3. Output

- Console prints results
- CSVs saved: `output_revenue_by_month.csv`, `output_top_customers.csv`

---

## 📝 Sample Input: `data/cdr_sample.csv`

```csv
cdr_id,subscriber_id,start_time,duration_seconds,cost
1001,2001,2025-06-01 08:00:00,180,2.50
1002,2001,2025-06-01 09:15:00,240,3.00
...
```

---

## 📦 Extend This Toolkit

- Add your own SQL scripts in the `sql/` folder
- Add Streamlit for dashboards
- Build anomaly detectors (e.g., flag high-cost users)

---

## 📄 License

MIT – free to use and modify!

---

## 💬 Feedback & Contributions

Open an issue or PR on [GitHub](https://github.com/spidjo/sql-billing-analyzer).
