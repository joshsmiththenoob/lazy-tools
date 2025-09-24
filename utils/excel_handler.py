"""
Duty on optimization of excel file
ex: 
    1. Adjust column width
    2. Annotate record with color
"""
import pandas as pd
from pathlib import Path
from openpyxl import load_workbook
from openpyxl.styles import PatternFill
from openpyxl.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet
from typing import Protocol, Optional, Iterable
from .common_excel_styler import WorksheetStyler  # 介面


class ExcelHandler:
    def __init__(self):
        pass 

    def adjust_column_width(self, work_sheet: Workbook) -> Worksheet:
        # 1. 調整欄位寬度
        for col in work_sheet.columns:
            max_length = 0
            col_letter = col[0].column_letter
            for cell in col:
                if cell.value:
                    max_length = max(max_length, len(str(cell.value)))
            work_sheet.column_dimensions[col_letter].width = max_length + 2  # 加點 padding

        return work_sheet


    def save_with_style(self, work_book: Workbook, output_path: str, styler: Optional[WorksheetStyler] = None):
        """
        Use different solutions based on different project
        like:
            platform_market_comparator use PlatforMarketComaparator as project processor
            etc..
        """
        ws = work_book.active
        self.adjust_column_width(ws)
        if styler:
            styler.apply(ws)
        work_book.save(output_path)
        return output_path