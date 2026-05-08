"""
This is where we start, buddy.
1. Let's call the Adapter to recives the Word and Excel data, and convert them into DataFrame.
"""
from pathlib import Path
from adapters.word_table_adapter import WordTableAdapter
from adapters.excel_table_adapter import ExcelTableAdapter


BASE_DIR   = Path(__file__).resolve().parent
INPUT_DIR  = BASE_DIR / "input"
OUTPUT_DIR = BASE_DIR / "output"


def main():
    word_path =  INPUT_DIR / "03.資通系統防護基準_佐證資料_農業統計資料管理系統_(普)_(奕祥資訊股份有限公司) v4_A3版_修3.docx"
    word_adapter = WordTableAdapter(word_path)
    word_df = word_adapter.load()
    print(word_df.head())



if __name__ == "__main__":
    main()