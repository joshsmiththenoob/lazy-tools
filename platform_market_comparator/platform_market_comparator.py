"""
Just Handle data of DataFrame from .ods, .xlsx, .csv etc..
"""
import pandas as pd
from pathlib import Path
from openpyxl import load_workbook
from .excel_styler import PlatformMarketStyler
from utils.time_handler import TimeHandler
from utils.excel_handler import ExcelHandler

BASE_DIR = Path(__file__).resolve().parent # platform_market_comparator/ 
INPUT_DIR = BASE_DIR / "input"
OUTPUT_DIR = BASE_DIR / "output"

class PlatformMarketComparator:
    def __init__(self):
        self.__time_handler = TimeHandler()

    def load_platform(self, path: Path) -> pd.DataFrame:
        df = pd.read_excel(path, engine="openpyxl")
        df.columns = df.iloc[0]
        df = df.iloc[1:].reset_index(drop=True)
        df = df.rename(columns={"日期":"date","日均價格":"avg_price_platform","總交易量":"volume_platform"})
        df["date"] = self.__time_handler.to_datetime_any(df["date"])
        df["avg_price_platform"] = pd.to_numeric(df["avg_price_platform"], errors="coerce")
        df["volume_platform"] = pd.to_numeric(df["volume_platform"], errors="coerce")
        return df.dropna(subset=["date"])

    def load_market(self, path: Path) -> pd.DataFrame: 
        df = pd.read_excel(path, engine="odf")
        df.columns = df.iloc[1]
        df = df.iloc[2:].reset_index(drop=True)
        df = df.rename(columns={"交易日期":"date","平均價":"avg_price_market","交易量":"volume_market"})
        df["date"] = self.__time_handler.to_datetime_any(df["date"])
        df["avg_price_market"] = pd.to_numeric(df["avg_price_market"], errors="coerce")
        df["volume_market"] = pd.to_numeric(df["volume_market"], errors="coerce")
        return df.dropna(subset=["date"])
    
    def load_hog_platform(self, path: Path) -> pd.DataFrame:
        df = pd.read_excel(path, engine="openpyxl")
        df.columns = df.iloc[0]
        df = df.iloc[1:].reset_index(drop=True)
        df = df.rename(columns={"日期":"date","日均價格":"avg_price_platform","總交易量":"volume_platform", "日均重量": "avg_weight_platform"})
        df["date"] = self.__time_handler.to_datetime_any(df["date"])
        df["avg_price_platform"] = pd.to_numeric(df["avg_price_platform"], errors="coerce")
        df["volume_platform"] = pd.to_numeric(df["volume_platform"], errors="coerce")
        return df.dropna(subset=["date"])

    def load_hog_market(self, path: Path) -> pd.DataFrame: 
        df = pd.read_excel(path, engine="openpyxl")
        df = df.iloc[:].reset_index(drop=True)
        df = df.rename(columns={"日期":"date","平均價格": "avg_price_market","成交頭數": "volume_market", "平均重量": "avg_weight_market"})
        df["date"] = self.__time_handler.to_datetime_any(df["date"])
        df["avg_price_market"] = pd.to_numeric(df["avg_price_market"], errors="coerce")
        df["volume_market"] = pd.to_numeric(df["volume_market"], errors="coerce")
        return df.dropna(subset=["date"])



    def compare(self, platform_path: str, market_path: str, out_path: str):
        plat = self.load_platform(Path(platform_path))
        mkt  = self.load_market(Path(market_path))
        # Use merge method to JOIN another dataframe (table) like we used to do in SQL 
        df = (plat.merge(mkt, on="date", how="inner").sort_values("date")).sort_values("date", ascending=False)
        df["avg_price_diff"] = df["avg_price_platform"] - df["avg_price_market"]
        df["volume_diff"]    = df["volume_platform"] - df["volume_market"]
        # Format date column from "yyyy-MM-dd HH:mm:ss" to "yyyy-MM-dd" 
        df["date"] = df["date"].dt.strftime("%Y-%m-%d")
        df.to_excel(out_path, index=False)
        print(f"saved: {out_path}")


    def compare_hog(self, platform_path: str, market_path: str, out_path: str):
        plat = self.load_hog_platform(Path(platform_path))
        mkt  = self.load_hog_market(Path(market_path))
        # Use merge method to JOIN another dataframe (table) like we used to do in SQL 
        df = (plat.merge(mkt, on="date", how="inner").sort_values("date")).sort_values("date", ascending=False)
        df["avg_price_diff"] = df["avg_price_platform"] - df["avg_price_market"]
        df["volume_diff"]    = df["volume_platform"] - df["volume_market"]
        df["avg_weight_diff"] = df["avg_weight_platform"] - df["avg_weight_market"]
        # Format date column from "yyyy-MM-dd HH:mm:ss" to "yyyy-MM-dd" 
        df["date"] = df["date"].dt.strftime("%Y-%m-%d")
        df.to_excel(out_path, index=False)
        print(f"saved: {out_path}")

if __name__ == "__main__":
    platform_path = INPUT_DIR / "歷史價量平台(生產環境)毛豬-批發合計.xlsx"
    market_path   = INPUT_DIR / "109-01-01-114-09-24年交易市場-毛豬交易價量走勢圖資料.xlsx"
    time_handler = TimeHandler()
    today_str = time_handler.now_str("%Y%m%d%H%M%S")

    output_type = "毛豬"    
    output_path = OUTPUT_DIR / f"{today_str}_{output_type}_compare_price_volume.xlsx"    
    
    csv_handler = PlatformMarketComparator()
    csv_handler.compare_hog(platform_path, market_path, output_path)

    wb = load_workbook(output_path)
    excel_handler = ExcelHandler()
    excel_styler = PlatformMarketStyler()
    excel_handler.save_with_style(wb, 
                                  output_path, 
                                  excel_styler,
                                  title= "市場與價量平台數值對照表",
                                  subtitle= output_type,
                                  freeze_header= True)
    