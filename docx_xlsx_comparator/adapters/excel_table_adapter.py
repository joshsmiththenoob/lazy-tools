"""
The Excel Adapter is responsible for 
1. loading Excel files like .xlsx, .xls
2. then converting them into a common DataFrame format for comparison.
"""

from .base import DataAdapter
import pandas as pd
import re
from ..utils.normalization import (
    COMMON_COLUMNS, clean_label, normalize_value
)

class ExcelTableAdapter(DataAdapter):
    def __init__(self, path: str, sheet_name= 0):
        self.path = path
        self.sheet_name = sheet_name

    def load(self) -> pd.DataFrame:
        """Load the Excel file and convert it to a Standardized DataFrame."""
        raw_df = pd.read_excel(
        self.path,
        sheet_name= self.sheet_name,
        header=None,
        dtype=object,
        keep_default_na=False,
    )
        return self._normalize(raw_df)
        # return self.__convert_to_dataframe(raw_df)
    
    def __convert_to_dataframe(self, raw_df: pd.DataFrame) -> pd.DataFrame:
        return raw_df

    # def load(self) -> pd.DataFrame:
    #     """Load the Excel file and convert it to a Standardized DataFrame."""
    #     raw_df = pd.read_excel(self.path, sheet_name=self.sheet_name)
    #     return self.__convert_to_dataframe(raw_df)
    
    # def __convert_to_dataframe(self, raw_df: pd.DataFrame) -> pd.DataFrame:
    #     return raw_df


    def _normalize(self, raw: pd.DataFrame) -> pd.DataFrame:
        # 第二列年度：只補表頭，不補數值
        years = raw.iloc[1].replace("", pd.NA).ffill()
        records = []

        # 第五列開始是指標資料
        for _, row in raw.iloc[4:].iterrows():
            match = re.fullmatch(
                r"(.*?)(種植面積|收穫面積|產量|產值)\(([^()]+)\)",
                clean_label(row.iloc[0]),
            )
            if not match:
                continue

            category, metric, unit = match.groups()

            for column in range(1, raw.shape[1]):
                year = re.fullmatch(
                    r"(\d+)年", clean_label(years.iloc[column])
                )
                crop = clean_label(raw.iloc[3, column])

                if year and crop:
                    records.append([
                        category,
                        crop,
                        int(year.group(1)),
                        "實績",
                        metric,
                        unit,
                        normalize_value(
                            row.iloc[column], round_integer=True
                        ),
                    ])

        return pd.DataFrame(records, columns=COMMON_COLUMNS)