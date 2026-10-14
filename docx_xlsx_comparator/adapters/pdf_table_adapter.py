"""
The PDF Adapter is responsible for 
1. loading PDF files like .pdf
2. then converting them into a common DataFrame format for comparison.
"""
import re
import pdfplumber
import pandas as pd
import unicodedata
from .base import DataAdapter

def clean_label(text: str | None) -> str:
    text = unicodedata.normalize("NFKC", text or "")
    return re.sub(r"\s+", "", text)


class PDFTableAdapter(DataAdapter):
    def __init__(self, path: str, sheet_name= 0):
        self.path = path
        self.sheet_name = sheet_name

    def load(self) -> pd.DataFrame:
        """Load the Excel file and convert it to a Standardized DataFrame."""
        d = pd.DataFrame()
        expected_columns = None
        skipped_pages = []
        with pdfplumber.open("附件1_115年度農業生產目標-各品項總表(核定版).pdf") as pdf:
            for page_number, page in enumerate(pdf.pages, start=1):
                try:
                    table_data = page.extract_table()

                    if not table_data:
                        raise ValueError("找不到表格")

                    # 清理欄名；空欄名先給唯一名稱，保留原本的資料欄
                    columns = [clean_label(column) or f"unnamed_{index}" for index, column in enumerate(table_data[0])]

                    # 暫時只處理和第一張表相同的欄位結構
                    if expected_columns is not None and columns != expected_columns:
                        raise ValueError("欄位結構不同，暫不處理")

                    df = pd.DataFrame(table_data[1:], columns=columns)
                    d = pd.concat([d, df], ignore_index=True)

                    # 第一張成功合併的表，作為後續參考
                    if expected_columns is None:
                        expected_columns = columns

                except Exception as e:
                    skipped_pages.append({
                        "頁碼": page_number,
                        "原因": str(e),
                    })
                    print(f"跳過第 {page_number} 頁：{e}")
                    continue


            return d




        
        # raw_df = pd.read_excel(self.path, sheet_name=self.sheet_name)



        # return self.__convert_to_dataframe(raw_df)
    