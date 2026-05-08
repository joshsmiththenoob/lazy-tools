# platform_market_comparator/cli.py
import argparse
from pathlib import Path
from utils.time_handler import TimeHandler
from .adapters.csv_seafood_market_adapter import CSVSeafoodMarketAdapter
from .adapters.ods_market_adapter import ODSCropMarketAdapter
from .adapters.xls_platform_adapter import XLSXPlatformAdapter
from .adapters.hog_market_crawler import HogMarketCrawlerAdapter
from .pipeline import compare_and_save

BASE_DIR   = Path(__file__).resolve().parent
INPUT_DIR  = BASE_DIR / "input"
OUTPUT_DIR = BASE_DIR / "output"

def main():
    platform_path = INPUT_DIR / "歷史價量平台(生產環境)-龍虎班-1174(全部市場).xlsx"
    market_path   = INPUT_DIR / "109-114年交易市場-龍虎斑交易價量走勢圖資料(全部市場).csv"
    time_handler = TimeHandler()
    today_str = time_handler.now_str("%Y%m%d%H%M%S")

    output_type = "龍虎斑"    
    output_path = OUTPUT_DIR / f"{today_str}_{output_type}_compare_price_volume.xlsx"    
    
    
    # Get platform dataframe
    include_weight = False
    if platform_path:
        if (output_type.startswith("毛豬")):
            include_weight = True
        plat_df = XLSXPlatformAdapter(platform_path, include_weight).load()


    # Get market dataframe
    if (output_type.startswith("毛豬")):
        start_date_str = "2020-01-01"
        end_date_str = "2025-09-24"
        market_df = HogMarketCrawlerAdapter(start_date_str, end_date_str).load()
    
    else:
        # ods / xlsx 自動選擇不同 adapter（如需要可分開兩個）
        if market_path.suffix.lower() == ".ods":
            market_df = ODSCropMarketAdapter(Path(market_path)).load()
        elif market_path.suffix.lower() == ".csv":
            market_df = CSVSeafoodMarketAdapter(market_path, include_weight=include_weight).load()
        else:
            # 若某些單位提供 xlsx，可做個 XLSXMarketAdapter（同 ODS 邏輯）
            market_df = XLSXPlatformAdapter(Path(market_path)).load()
    print(market_df)

    # 輸出檔名
    compare_and_save(plat_df, market_df, output_path, subtitle=output_type, include_weight= include_weight)
    print(f"saved: {output_path}")

if __name__ == "__main__":
    main()
