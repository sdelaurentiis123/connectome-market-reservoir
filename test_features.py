import pandas as pd
from features import load_feature_csv

def test_loader_sorts_and_validates(tmp_path):
    path = tmp_path / "features.csv"
    pd.DataFrame({
        "timestamp": ["2026-01-02", "2026-01-01"], "return": [0.1, -0.1],
        "realized_vol": [0.2, 0.3], "volume": [1, 2], "spread": [0.01, 0.02],
        "imbalance": [0.4, -0.2],
    }).to_csv(path, index=False)
    result = load_feature_csv(str(path))
    assert result.timestamp.is_monotonic_increasing
