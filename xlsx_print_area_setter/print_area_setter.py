from pathlib import Path
from openpyxl import load_workbook
from openpyxl.worksheet.pagebreak import Break

INPUT = r"C:\Users\ai\Desktop\smithfu\repositories\lazy-tools\xlsx_print_area_setter\input\114.10.30-114.11.05價格週四.xlsx"
OUTPUT = r"C:\Users\ai\Desktop\smithfu\repositories\lazy-tools\xlsx_print_area_setter\output\報表結果.xlsx"

path_in  = Path(INPUT)
path_out = Path(OUTPUT)
path_out.parent.mkdir(parents=True, exist_ok=True)

wb = load_workbook(path_in)

for ws in wb.worksheets:
    # 1) 清掉列印區與標題列/欄（設 None 即會移除對應的 defined name）
    try: ws.print_area = None
    except AttributeError: pass
    try: ws.print_title_rows = None
    except AttributeError: pass
    try: ws.print_title_cols = None
    except AttributeError: pass

    # 2) 回到百分比縮放並關閉 fit-to-page
    ps = ws.page_setup
    ps.fitToWidth = 0
    ps.fitToHeight = 0
    ps.scale = 100
    ps.orientation = "portrait"   # ← 用字串，不是常數

    # 列印區整段
    ws.print_area = "A1:U147"

    # 先清既有分頁，再在 101/102 之間加斷點
    ws.row_breaks = ws.row_breaks.__class__()  # 重置
    ws.row_breaks.append(Break(id=101))        # 101 與 102 之間換頁
    ps.fitToWidth = 1


wb.save(path_out)
print("Done: 已清空列印設定並設置列印範圍 A1:U147（openpyxl）")
