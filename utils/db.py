import sqlite3
import pandas as pd
import os

DB_FILE = "billing.db"
SQL_DIR = "sql"

def run_sql_query(sql_file):
    conn = sqlite3.connect(DB_FILE)
    with open(os.path.join(SQL_DIR, sql_file), 'r') as f:
        query = f.read()
    result = pd.read_sql_query(query, conn)
    conn.close()
    return result

def get_connection():
    return sqlite3.connect(DB_FILE, check_same_thread=False)

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