"""
Duty on Hnadling everything about time including datetime, timezone etc.
"""
import re
import pandas as pd
from datetime import datetime, timedelta

class TimeHandler:
    def __init__(self):
        pass

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