"""
Duty on optimization of excel file
ex: 
    1. Adjust column width
    2. Annotate record with color
"""
import pandas as pd
from pathlib import Path
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet
from typing import Protocol, Optional, Iterable, Union
from .common_excel_styler import WorksheetStyler  # 介面


class ExcelHandler:
    def __init__(self):
        pass 
    def add_title_row(self, 
                      work_sheet: Worksheet, 
                      title: str, 
                      subtitle: Union[str, None] = None,
                      font_size: int = 14):
        """
        Add the row as title (header), and 
        """
        last_col = get_column_letter(work_sheet.max_column)
        # 插入到最上面
        work_sheet.insert_rows(1)
        work_sheet.merge_cells(start_row=1, start_column=1, end_row=1, end_column=work_sheet.max_column)
        cell = work_sheet["A1"]
        cell.value = title if not subtitle else f"{title}  —  {subtitle}"
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.font = Font(bold=True, size=font_size)


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


    def save_with_style(self, work_book: Workbook, output_path: str, styler: Optional[WorksheetStyler] = None, title: str = None, subtitle: str = None , freeze_header: bool = False):
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
        
        # add title in the last 
        if title:
            self.add_title_row(ws, title, subtitle)
            if freeze_header:   
                # freeze header so that when we scroll dataset, the header will be freeze on the top
                ws.freeze_panes = "A3"
        else:
            if freeze_header:
                ws.freeze_panes = "A2"
        
        work_book.save(output_path)
        return output_path