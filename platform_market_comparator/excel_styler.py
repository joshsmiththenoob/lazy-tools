# platform_market_styler.py
from openpyxl.worksheet.worksheet import Worksheet
from utils.common_excel_styler import WorksheetStyler, color_if, FILL_ORANGE

class PlatformMarketStyler(WorksheetStyler):
    def apply(self, ws: Worksheet) -> None:
        # 規則：只要 diff ≠ 0 就標淺橘
        color_if(ws, "avg_price_diff", lambda v: abs(v) > 0.01 and v not in (None, 0), FILL_ORANGE)
        color_if(ws, "volume_diff",    lambda v: abs(v) > 0 and v not in (None, 0), FILL_ORANGE)
