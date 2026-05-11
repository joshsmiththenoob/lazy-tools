"""
Duty on optimization of excel file
ex: 
    1. Adjust column width
    2. Annotate record with color
"""
import math
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


    def adjust_column_width_better(self,
                                  ws: Worksheet,
                                  min_width=12,
                                  max_width=80,
                                  header_weight=1.5,
                                  value_percentile=0.95,
                                  wrap_header=True,
                                  header_row_height=30,
                                  wrap_value_cols=("地址",)):
        """
        讓欄位名稱與內容都能清楚顯示的欄寬調整。
        - 表頭：非 ASCII 以 1.8 倍寬估算，並給額外權重 header_weight
        - 內容：使用 value_percentile 百分位估算需求寬（抗極端值）
        - 超過 max_width 的表頭 → 啟用換行並提高表頭列高
        - wrap_value_cols 這些欄位一律啟用換行（例如地址）
        """
        def visible_len(s: str) -> float:
            if s is None:
                return 0.0
            s = str(s)
            w = 0.0
            for ch in s:
                w += 1.8 if ord(ch) > 127 else 1.0  # 中文/全形給較大寬度
            return w

        max_col = ws.max_column
        max_row = ws.max_row

        # 先建立標題映射，後面也能用來判斷 wrap_value_cols
        headers = {c: str(ws.cell(row=1, column=c).value or "") for c in range(1, max_col+1)}

        # 內容長度的百分位函式
        def percentile(values, p):
            if not values:
                return 0.0
            values = sorted(values)
            k = max(0, min(len(values)-1, int(math.floor((len(values)-1) * p))))
            return values[k]

        for c in range(1, max_col+1):
            col_letter = get_column_letter(c)
            title = headers[c]

            # 1) 表頭需求寬
            need_header = visible_len(title) * header_weight + 2

            # 2) 內容需求寬（用百分位避免被極端值影響）
            vals = [visible_len(ws.cell(row=r, column=c).value) + 2 for r in range(2, max_row+1)]
            need_value = percentile(vals, value_percentile)

            # 3) 欄寬決策
            width = max(need_header, need_value, min_width)
            if width > max_width:
                width = max_width
                if wrap_header and title:
                    cell = ws.cell(row=1, column=c)
                    cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
                    ws.row_dimensions[1].height = header_row_height  # 調高表頭列

            ws.column_dimensions[col_letter].width = width

            # # 4) 針對「值很長的欄」（例如地址）啟用換行，讓內容不把欄寬撐太大
            # if any(key in title for key in wrap_value_cols):
            #     for r in range(2, max_row+1):
            #         ws.cell(row=r, column=c).alignment = Alignment(wrap_text=True, vertical="top")

        # 表頭置中（看起來更整齊）
        for c in range(1, max_col + 1):
            cell = ws.cell(row=1, column=c)
            # 若前面已經設定 wrap_text，這裡不要覆蓋 wrap_text 的 True
            cur = cell.alignment
            cell.alignment = Alignment(horizontal="center",
                                    vertical="center",
                                    wrap_text=(cur.wrap_text if cur else False))

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