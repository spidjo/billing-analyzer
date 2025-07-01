import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta
import os

fake = Faker()
np.random.seed(42)

def generate_monthly_files(
    months_back=12,
    records_per_month=200,
    anomaly_fraction=0.05,
    output_dir="data/monthly_billing"
):
    os.makedirs(output_dir, exist_ok=True)
    today = datetime.today()

    for m in range(months_back):
        month_date = today.replace(day=1) - pd.DateOffset(months=m)
        billing_date = (month_date + pd.DateOffset(days=32)).replace(day=1) - pd.DateOffset(days=1)
        month_str = billing_date.strftime("%Y_%m")

        data = []
        for _ in range(records_per_month):
            subscriber_id = f"CUST{random.randint(1000, 9999)}"

            # Simulate minor monthly variation in usage behavior
            usage_minutes = np.random.normal(300 + 10 * np.sin(m), 50)
            data_gb = np.random.normal(5 + 0.5 * np.cos(m), 2)
            sms_count = np.random.poisson(20 + (m % 3))

            # Calculate cost
            base_cost = usage_minutes * 0.05 + data_gb * 10 + sms_count * 0.2
            noise = np.random.normal(0, 5)
            cost = max(0, base_cost + noise)

            data.append([
                subscriber_id,
                round(usage_minutes, 2),
                round(data_gb, 2),
                sms_count,
                round(cost, 2),
                billing_date.date()
            ])

        df = pd.DataFrame(data, columns=["subscriber_id", "usage_minutes", "data_gb", "sms_count", "cost", "billing_date"])

        # Inject anomalies
        num_anomalies = int(records_per_month * anomaly_fraction)
        anomaly_indices = np.random.choice(df.index, size=num_anomalies, replace=False)
        for idx in anomaly_indices:
            df.loc[idx, "cost"] = round(random.choice([
                df["cost"].mean() * random.uniform(3.5, 6.0),
                df["cost"].mean() * random.uniform(0.1, 0.3)
            ]), 2)

        output_file = os.path.join(output_dir, f"billing_{month_str}.csv")
        df.to_csv(output_file, index=False)

        print(f"✅ Generated {output_file} with {len(df)} rows")

if __name__ == "__main__":
    generate_monthly_files()
