# platform_market_comparator/adapters/csv_seafood_market_adapter.py
from __future__ import annotations
import csv
from pathlib import Path
from typing import Optional

import pandas as pd
from utils.time_handler import TimeHandler


class CSVSeafoodMarketAdapter:
    """
    適用於漁產品交易市場下載的 .csv
    會輸出欄位順序：
        ["date", "avg_price_market", "volume_market"] (+ 可選 "avg_weight_market")
    """
    def __init__(self, path: Path, include_weight: bool = False, encoding: Optional[str] = None):
        self.path = Path(path)
        self.include_weight = include_weight
        self.encoding = encoding  # 若不指定，會自動嘗試 UTF-8-SIG -> Big5(cp950)
        self.time = TimeHandler()

    # ---- helpers ---------------------------------------------------------
    @staticmethod
    def _guess_encoding(path: Path, fallback: str = "cp950") -> str:
        # 一般政府網站 CSV 多為 UTF-8-BOM 或 Big5
        for enc in ("utf-8-sig", "utf-8", fallback):
            try:
                with open(path, "r", encoding=enc) as f:
                    f.readline()
                return enc
            except UnicodeDecodeError:
                continue
        return fallback

    @staticmethod
    def _find_header_row(df: pd.DataFrame) -> int:
        """
        找出包含『交易日期』『平均價』等關鍵字的那一列，回傳 row index。
        """
        keys = ("交易日期", "平均價")
        for i in range(min(10, len(df))):
            row_vals = [str(v) for v in df.iloc[i].tolist()]
            if any(k in " ".join(row_vals) for k in keys):
                return i
        return 0  # 如果找不到就當作第一行是表頭

    @staticmethod
    def _is_roc_date(s: str) -> bool:
        # 例如 109.1.1 / 112/09/24 之類
        return isinstance(s, str) and any(ch in s for ch in (".", "/")) and len(s.split()[0].split(".")[0].split("/")[0]) <= 3

    def _parse_date(self, val):
        """
        把 民國 或 西元 轉成 pandas datetime（只保留日期）。
        """
        if pd.isna(val):
            return pd.NaT
        s = str(val).strip()
        # 民國年處理
        if self._is_roc_date(s):
            sep = "." if "." in s else "/"
            y, m, d = s.split(sep)[:3]
            try:
                y = int(y) + 1911
                return pd.to_datetime(f"{y}-{int(m):02d}-{int(d):02d}", errors="coerce")
            except Exception:
                return pd.NaT
        # 直接嘗試西元轉 datetime
        return pd.to_datetime(s, errors="coerce").normalize()

    # ---- main ------------------------------------------------------------
    def load(self) -> pd.DataFrame:
        import io

        # 1) 讀 bytes -> 逐一嘗試解碼
        raw_bytes = Path(self.path).read_bytes()
        tried = (self.encoding,) if self.encoding else ("utf-8-sig", "utf-8", "cp950")
        text = None
        for enc in [e for e in tried if e]:
            try:
                print(enc)
                text = raw_bytes.decode(enc)
                break
            except UnicodeDecodeError:
                continue
        if text is None:  # 最後再用 cp950 試一次
            text = raw_bytes.decode("cp950", errors="ignore")
        
        
        # 2) 正規化換行與雜訊
        text = (
            text.replace("\ufeff", "")       # BOM
                .replace("\u3000", " ")      # 全形空白
                .replace("\r\n", "\n")
                .replace("\r", "\n")
        )

        # 3) 用 csv.reader 解析
        rows = list(csv.reader(io.StringIO(text), delimiter=",", quotechar='"'))
        df_raw = pd.DataFrame(rows)
        # 丟掉全空列
        df_raw = df_raw.replace("", pd.NA).dropna(how="all")

        # 4) 找真正表頭（包含「交易日期」「平均價」的那列）
        header_row = self._find_header_row(df_raw)
        print(header_row)
        df = df_raw.copy()
        df.columns = df.iloc[header_row].tolist()
        df = df.iloc[header_row + 1:].reset_index(drop=True)

        # 5) 欄名清理（去單位、空白）
        df.columns = [str(c).strip().replace("\xa0", " ") for c in df.columns]
        df.columns = [c.split("(", 1)[0].strip() for c in df.columns]

        # 6) 對應成標準欄位
        col_map = {
            "交易日期": "date",
            "平均價": "avg_price_market",
            "平均價元/公斤": "avg_price_market",
            "平均價元／公斤": "avg_price_market",
            "交易量": "volume_market",
            "交易量公斤": "volume_market",
            "交易量（公斤）": "volume_market",
            "平均重量": "avg_weight_market",
        }
        # 盡量把原欄名壓成無標點來比對
        def _norm(s: str) -> str:
            return (
                str(s).replace("/", "").replace("／", "").replace("（", "").replace("）", "")
                    .replace(" ", "")
            )

        rename_map = {}
        for c in df.columns:
            key = _norm(c)
            for k, v in col_map.items():
                if _norm(k) == key:
                    rename_map[c] = v
                    break
        df = df.rename(columns=rename_map)

        # 只保留認得的欄
        keep = [c for c in ("date", "avg_price_market", "volume_market", "avg_weight_market") if c in df.columns]
        df = df[keep]

        # 7) 數字欄位清理
        for col in ("avg_price_market", "volume_market", "avg_weight_market"):
            if col in df.columns:
                df[col] = (
                    df[col].astype(str)
                        .str.replace(",", "", regex=False)
                        .str.replace("—", "", regex=False)
                        .str.strip()
                )
                df[col] = pd.to_numeric(df[col], errors="coerce")
        # 8) 日期轉西元 datetime（支援 109.1.1 / 112/09/24 / 2025-09-24）
        # 在 date apply 前
        df = df[~df["date"].astype(str).str.contains("合計", na=False)]
        df["date"] = df["date"].apply(self._parse_date)
        df = df.dropna(subset=["date"])

        # 9) 欄位順序
        cols = ["date", "avg_price_market", "volume_market"]
        if self.include_weight and "avg_weight_market" in df.columns:
            cols.append("avg_weight_market")

        # 10) 去重並依日期排序
        df = df[cols].drop_duplicates(subset=["date"]).sort_values("date").reset_index(drop=True)
        return df


if __name__ == "__main__":
    market_path = r"C:\Users\ai\Desktop\smithfu\repositories\lazy-tools\platform_market_comparator\input\109-114年交易市場-吳郭魚交易價量走勢圖資料.csv" 
    csv_seafood_adapter = CSVSeafoodMarketAdapter(market_path)

    raw_data = csv_seafood_adapter.load()
    # raw_data = pd.read_csv(market_path)
    print(raw_data)
