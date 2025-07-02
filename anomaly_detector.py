def detect_anomalies(df, threshold=3.0):
    df = df.copy()
    mean = df["cost"].mean()
    std = df["cost"].std()
    df["z_score"] = (df["cost"] - mean) / std
    df["is_anomaly"] = df["z_score"].abs() > threshold

    stats = {
        "mean": mean,
        "std": std,
        "outlier_count": df["is_anomaly"].sum()
    }

    return df, stats