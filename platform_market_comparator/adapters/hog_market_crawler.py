# platform_market_comparator/adapters/hog_market_crawler.py
from pathlib import Path
import pandas as pd
from utils.time_handler import TimeHandler
from .base import DataAdapter
from ..livestock_web_crawler import fetch_pig_spec_table  # 直接複用你寫好的

class HogMarketCrawlerAdapter(DataAdapter):
    def __init__(self, start_date: str, end_date: str):
        self.start = start_date
        self.end   = end_date
        self.time_handler = TimeHandler()


    def load(self) -> pd.DataFrame:
        df = fetch_pig_spec_table(self.start, self.end, exclude_penghu=True)
        df = df.iloc[:].reset_index(drop=True)
        # df 目前欄位：「日期 / 成交頭數 / 平均重量 / 平均價格」
        df = df.rename(columns={"日期":"date","平均價格": "avg_price_market","成交頭數": "volume_market", "平均重量": "avg_weight_market"})
        df["date"] = self.time_handler.to_datetime_any(df["date"])
        df["avg_price_market"] = pd.to_numeric(df["avg_price_market"], errors="coerce")
        df["volume_market"] = pd.to_numeric(df["volume_market"], errors="coerce")
        # 指定欄位順序
        df = df[["date", "avg_price_market", "volume_market", "avg_weight_market"]]

        return df.dropna(subset=["date"])
