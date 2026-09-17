from __future__ import annotations
import pandas as pd

REQUIRED_COLUMNS = ["timestamp", "return", "realized_vol", "volume", "spread", "imbalance"]

def load_feature_csv(path: str) -> pd.DataFrame:
    frame = pd.read_csv(path, parse_dates=["timestamp"]).sort_values("timestamp")
    missing = [column for column in REQUIRED_COLUMNS if column not in frame]
    if missing:
        raise ValueError(f"missing columns: {missing}")
    return frame[REQUIRED_COLUMNS].dropna().reset_index(drop=True)
