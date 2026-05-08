# platform_market_comparator/pipeline.py
import pandas as pd
from pathlib import Path
from openpyxl import load_workbook
from utils.excel_handler import ExcelHandler
from .excel_styler import PlatformMarketStyler
from .normalizer.schema import ensure_schema

def compare_and_save(platform_df: pd.DataFrame,
                     market_df: pd.DataFrame,
                     out_path: Path,
                     title="市場與價量平台數值對照表",
                     subtitle="",
                     include_weight=False):

    df = (platform_df.merge(market_df, on="date", how="inner").sort_values("date")).sort_values("date", ascending=False)

    # 差值欄
    df["avg_price_diff"] = df["avg_price_platform"] - df["avg_price_market"]
    df["volume_diff"]    = df["volume_platform"] - df["volume_market"]
    if include_weight:
      df["avg_weight_diff"] = df["avg_weight_platform"] - df["avg_weight_market"]

    # 日期格式
    if pd.api.types.is_datetime64_any_dtype(df["date"]):
        df["date"] = df["date"].dt.strftime("%Y-%m-%d")

    # 寫檔
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_excel(out_path, index=False)

    # 套版（沿用你現有 ExcelHandler + Styler）
    wb = load_workbook(out_path)
    ExcelHandler().save_with_style(
        wb, out_path,
        PlatformMarketStyler(),
        title=title,
        subtitle=subtitle,
        freeze_header=True
    )
    return out_path
