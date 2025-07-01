import pandas as pd

def detect_anomalies(df: pd.DataFrame, column: str = 'cost', threshold: float = 3.0) -> pd.DataFrame:
    """
    Detects anomalies using z-score on a specified column.
    
    Parameters:
        df (pd.DataFrame): Input CDR data
        column (str): The numeric column to evaluate
        threshold (float): Z-score threshold (default = 3.0)
    
    Returns:
        pd.DataFrame: Rows flagged as anomalies with z_score and is_anomaly
    """
    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found in DataFrame")

    mean = df[column].mean()
    std = df[column].std()
    df['z_score'] = (df[column] - mean) / std
    df['is_anomaly'] = df['z_score'].abs() > threshold
    return df[df['is_anomaly']].copy()
