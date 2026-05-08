# platform_market_comparator/adapters/xlsx_platform.py
import pandas as pd
from pathlib import Path
from utils.time_handler import TimeHandler

class XLSXPlatformAdapter:
    def __init__(self, path: Path, include_weight: bool=False):
        self.path = path
        self.time_handler = TimeHandler()
        self.include_weight = include_weight

    def load(self) -> pd.DataFrame:
        df = pd.read_excel(self.path, engine="openpyxl")
        df.columns = df.iloc[0]
        df = df.iloc[1:].reset_index(drop=True)

        base_map = {
                    "日期":"date",
                    "日均價格":"avg_price_platform",
                    "總交易量":"volume_platform"
                    }
        if self.include_weight:
            base_map["日均重量"] = "avg_weight_platform"

        df = df.rename(columns=base_map)
        df["date"] = self.time_handler.to_datetime_any(df["date"])
        df["avg_price_platform"] = pd.to_numeric(df["avg_price_platform"], errors="coerce")
        df["volume_platform"]    = pd.to_numeric(df["volume_platform"], errors="coerce")
        if self.include_weight and "avg_weight_platform" in df:
            df["avg_weight_platform"] = pd.to_numeric(df["avg_weight_platform"], errors="coerce")

        return df.dropna(subset=["date"])
    
