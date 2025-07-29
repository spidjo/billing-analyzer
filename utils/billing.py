
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
