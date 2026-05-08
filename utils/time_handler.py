"""
Duty on Hnadling everything about time including datetime, timezone etc.
"""
import re
import pandas as pd
from datetime import datetime, timedelta

class TimeHandler:
    def __init__(self):
        pass
    
    def now_str(self, fmt: str = "%Y%m%d") -> str:
        """回傳現在時間的字串，例如 '20250923'"""
        return datetime.now().strftime(fmt)

    def roc_to_gregorian_str(self, s: str) -> str:
        s = str(s).strip()
        m = re.match(r"^(\d{2,3})[./-](\d{1,2})[./-](\d{1,2})$", s)
        if m:
            y, mo, d = map(int, m.groups())
            if y < 1911:
                y += 1911
            return f"{y:04d}-{mo:02d}-{d:02d}"
        return s

    def to_datetime_any(self, date_series):
        return pd.to_datetime(
            date_series.astype(str).map(self.roc_to_gregorian_str).str.replace(r"[./]", "-", regex=True),
            errors="coerce"
        )
    
    def gregorian_str_to_roc(self, dt_str: str, fmt: str = "%Y-%m-%d") -> str:
        """
        通用方法：西元時間字串 → 民國時間字串
        支援 'YYYY-MM-DD' / 'YYYY-MM-DD HH:mm:SS'
        fmt 控制輸出，例如:
          "%Y-%m-%d"      -> '114-09-24'
          "%Y/%m/%d %H:%M:%S" -> '114/09/24 15:30:45'
        """
        dt = datetime.strptime(dt_str, "%Y-%m-%d" if len(dt_str) == 10 else "%Y-%m-%d %H:%M:%S")
        roc_year = dt.year - 1911
        roc_year = str(int(roc_year))

        # 先把西元部分格式化
        formatted = dt.strftime(fmt)
        
        # 把格式裡的西元年替換掉
        if "%Y" in fmt:
            formatted = formatted.replace(str(dt.year), str(roc_year))

        return formatted