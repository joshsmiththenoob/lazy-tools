# platform_market_comparator/normalizers/schema.py
import pandas as pd

COMMON_COLS = ["date"]
MARKET_COLS = ["avg_price_market","volume_market"]
PLAT_COLS   = ["avg_price_platform","volume_platform"]
HOG_EXTRA   = ["avg_weight_market","avg_weight_platform"]

def ensure_schema(df: pd.DataFrame, want_weight=False) -> pd.DataFrame:
    # 補齊缺欄（不存在就建空欄），讓後段 merge 不會炸
    print(df.columns)
    for c in MARKET_COLS + PLAT_COLS + (HOG_EXTRA if want_weight else []):
        if c not in df.columns:
            raise IndexError(f"No column {c} in dataframe. Please check the file")
    return df
