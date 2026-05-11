"""
Duty of exporting the report after comparsion between two tables.
"""
import pandas as pd
from openpyxl import load_workbook
from utils.excel_handler import ExcelHandler

class ReportExporter:
    def __init__(self, result_df):
        self.result_df = result_df
    def export_to_excel(self, output_path: str, saved_sheet_name: str = "Comparison Result"):
        with pd.ExcelWriter(output_path, engine="openpyxl") as w:
            self.result_df.to_excel(w, sheet_name=saved_sheet_name, index=False)

        wb = load_workbook(output_path)
        ws = wb[saved_sheet_name]
        ws = ExcelHandler().adjust_column_width_better(ws)
        wb.save(output_path)