"""
The class on duty of comparasion between two tables
then return the result in a DataFrame format for further processing.
"""
import pandas as pd


class TableComparator:
    def __init__(self, word_df, excel_df):
        self.word_df = word_df
        self.excel_df = excel_df
        self.key_col = None
        self.report_exporter = None

    def find_common_columns(self):
        word_cols = set(self.word_df.columns)
        excel_cols = set(self.excel_df.columns)
        common_cols = list(word_cols & excel_cols)
        return common_cols

    def get_common_row_keys(self, key_col: str):

        # Initialize key col
        self.key_col = key_col

        word_keys = set(self.word_df[self.key_col].dropna().astype(str).str.strip())
        print(word_keys)
        excel_keys = set(self.excel_df[self.key_col].dropna().astype(str).str.strip())
        print(excel_keys)
        common_keys = list(word_keys & excel_keys)
        return common_keys
    

    def get_rest_of_cols(self):
        return [col for col in self.find_common_columns() if col not in [self.key_col]]
    

    def compare_multiple_values(self, selected_rows, selected_columns):
        print("key_col:", self.key_col)
        results = []

        for row_key in selected_rows:
            # Per raw in selected_rows -> find matching raws in both DataFrames based on key_col
            word_match = self.word_df[
                self.word_df[self.key_col].astype(str).str.strip() == str(row_key).strip()
            ]

            excel_match = self.excel_df[
                self.excel_df[self.key_col].astype(str).str.strip() == str(row_key).strip()
            ]

            for col in selected_columns:
                # Then find the value in selected_columns, if the column doesn't exist, mark as "Word/Excel 找不到列"
                
                if word_match.empty:
                    word_value = None
                    status = "Word 找不到列"
                else:
                    word_value = word_match[col].iloc[0]
                    status = "可比較"


                if excel_match.empty:
                    excel_value = None
                    status = "Excel 找不到列"
                else:
                    excel_value = excel_match[col].iloc[0]



                if word_match.empty or excel_match.empty:
                    is_equal = False
                else:
                    is_equal = str(word_value).strip() == str(excel_value).strip()

                results.append({
                    "主要欄位": self.key_col,
                    "列名稱": row_key,
                    "比對欄位": col,
                    "Word值": word_value,
                    "Excel值": excel_value,
                    "是否相同": is_equal,
                    "狀態": status,
                })

        return pd.DataFrame(results)
    
    
