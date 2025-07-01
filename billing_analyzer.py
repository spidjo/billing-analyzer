import sqlite3
import pandas as pd
import os

# Config
DB_FILE = 'billing.db'
CSV_FILE = 'data/billing_data.csv'
SQL_DIR = 'sql'

def load_csv_to_sqlite(csv_path, db_conn):
    df = pd.read_csv(csv_path, parse_dates=['billing_date'])
    df.to_sql('cdrs', db_conn, if_exists='replace', index=False)
    print("[✔] Loaded CSV into SQLite")

def run_sql_query(conn, sql_file):
    with open(os.path.join(SQL_DIR, sql_file), 'r') as f:
        query = f.read()
    result = pd.read_sql_query(query, conn)
    print(f"\n📊 Result for {sql_file.replace('.sql', '')}:\n")
    print(result)
    result.to_csv(f"output_{sql_file.replace('.sql', '')}.csv", index=False)
    print(f"[↑] Saved to output_{sql_file.replace('.sql', '')}.csv")

def main():
    conn = sqlite3.connect(DB_FILE)
    load_csv_to_sqlite(CSV_FILE, conn)
    
    for sql_file in os.listdir(SQL_DIR):
        if sql_file.endswith(".sql"):
            run_sql_query(conn, sql_file)
    
    conn.close()

if __name__ == '__main__':
    main()
