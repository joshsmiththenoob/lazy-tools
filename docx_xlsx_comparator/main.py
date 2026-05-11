"""
This is where we start, buddy.
1. Let's call the Adapter to recives the Word and Excel data, and convert them into DataFrame.
"""
from pathlib import Path
from adapters.word_table_adapter import WordTableAdapter
from adapters.excel_table_adapter import ExcelTableAdapter
from utils.table_comparactor import TableComparator
from utils.report_exporter import ReportExporter
from gui.gui_app import ComparatorApp


BASE_DIR   = Path(__file__).resolve().parent
INPUT_DIR  = BASE_DIR / "input"
OUTPUT_DIR = BASE_DIR / "output"


def main():
    word_path =  INPUT_DIR / "03.資通系統防護基準_佐證資料_農業統計資料管理系統_(普)_(奕祥資訊股份有限公司) v4_A3版_修3.docx"
    word_adapter = WordTableAdapter(word_path)
    word_df = word_adapter.load()
    print(word_df.head())

    excel_path =  INPUT_DIR / "02.防護基準評估表.xlsx"
    excel_adapter = ExcelTableAdapter(excel_path)
    excel_df = excel_adapter.load()
    ## Excel preprocessing : 1. Drop '安全控制措施', 2. Drop rename '安全控制措施說明' as '安全控制措施'
    excel_df = (
            excel_df
            .drop(columns=["安全控制措施"])
            .rename(columns={"安全控制措施說明": "安全控制措施"})
            .reindex(columns=excel_df.columns)
            )
    
    # Note: Maybe there's some newline characters '\n' in the column names, we need to remove them.
    word_df.columns = word_df.columns.str.replace("\n", "", regex=False).str.strip()
    excel_df.columns = excel_df.columns.str.replace("\n", "", regex=False).str.strip()



    comparactor = TableComparator(word_df, excel_df)



    print(comparactor.find_common_columns())
    print(comparactor.get_common_row_keys(key_col="安全控制措施"))
    print(comparactor.get_rest_of_cols())


    # get selects options
    selected_rows = [
    "建立帳號管理機制，包含帳號之申請、建立、修改、啟用、停用及刪除之程序。",
    "資通系統閒置帳號應禁用。",
    ]
    print(f"Selected rows: {selected_rows}")

    selected_columns = [
        "符合性或不適用情況說明",
    ]
    print(f"Selected columns: {selected_columns}")




    # get result dataframe
    print("Word columns:")
    print([repr(col) for col in word_df.columns])

    print("Excel columns:")
    print([repr(col) for col in excel_df.columns])
    result_df = comparactor.compare_multiple_values(selected_rows, selected_columns)
    print(result_df)

    # Output result to Excel
    output_path = OUTPUT_DIR / "comparison_result.xlsx"
    report_exporter = ReportExporter(result_df)
    report_exporter.export_to_excel(output_path)

# if __name__ == "__main__":
#     # main()



if __name__ == "__main__":
    app = ComparatorApp()
    app.run()