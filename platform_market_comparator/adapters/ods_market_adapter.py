# platform_market_comparator/adapters/ods_market.py
import pandas as pd
from pathlib import Path
from utils.time_handler import TimeHandler

class ODSCropMarketAdapter:
    """
    適用於蔬果市場的交易
    """
    def __init__(self, path: Path, include_weight: bool=False):
        self.path = path
        self.time_handler = TimeHandler()
        self.include_weight = include_weight


    def load(self) -> pd.DataFrame:
        df = pd.read_excel(self.path, engine="odf")
        # 依你現有清理邏輯：跳過表頭列、改名、轉型
        df.columns = df.iloc[1]
        df = df.iloc[2:].reset_index(drop=True)

        base_map = {"交易日期":"date","平均價":"avg_price_market","交易量":"volume_market"}
        if self.include_weight:
            pass

        df = df.rename(columns=base_map)
        df["date"] = self.time_handler.to_datetime_any(df["date"])
        df["avg_price_market"] = pd.to_numeric(df["avg_price_market"], errors="coerce")
        df["volume_market"] = pd.to_numeric(df["volume_market"], errors="coerce")

        return df.dropna(subset=["date"])