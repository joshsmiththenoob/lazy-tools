import requests
from bs4 import BeautifulSoup
from pathlib import Path
import pandas as pd
from io import StringIO
from utils.time_handler import TimeHandler

BASE_DIR = Path(__file__).resolve().parent # platform_market_comparator/ 
# saving dataframe in input folder so that comparator can process data
OUTPUT_DIR = BASE_DIR / "input"
URL = "https://ppg.naif.org.tw/naif/MarketInformation/Pig/twStatistics.aspx"

def fetch_pig_spec_table(start_date_str="2020-01-01", end_date_str="2025-09-24", exclude_penghu=True):
    s = requests.Session()

    # 1) 先 GET，拿 cookie + 三寶
    r = s.get(URL, timeout=20)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "lxml")
    form = soup.find("form")

    # 2) 把 form 內所有 input 集體撈成 dict
    payload = {}
    for inp in form.find_all("input"):
        name = inp.get("name")
        if name:
            payload[name] = inp.get("value", "")

    # 3) 覆蓋查詢條件（注意 name 要跟頁面一致）
    payload["ctl00$ContentPlaceHolder_main$time"] = "RadioButton_d"  # 日統計
    payload["ctl00$ContentPlaceHolder_main$TextBox_d_beg"] = start_date_str
    payload["ctl00$ContentPlaceHolder_main$TextBox_d_end"] = end_date_str
    payload["ctl00$ContentPlaceHolder_main$CheckBox_penghu"] = "on" if exclude_penghu else ""
    payload["ctl00$ContentPlaceHolder_main$Button_query"] = "查詢"
    payload["ctl00$ContentPlaceHolder_main$DropDownList_m_begYear"] = "2025"
    payload["ctl00$ContentPlaceHolder_main$DropDownList_m_begMonth"] = "1"
    payload["ctl00$ContentPlaceHolder_main$DropDownList_m_endYear"] = "2025"
    payload["ctl00$ContentPlaceHolder_main$DropDownList_m_endMonth"] = "1"
    payload["ctl00$ContentPlaceHolder_main$DropDownList_y_beg"] = "2025"
    payload["ctl00$ContentPlaceHolder_main$DropDownList_y_end"] = "2025"


    # 4) POST 回同頁
    r2 = s.post(URL, data=payload, timeout=30)
    r2.raise_for_status()

    # 5) 讀出所有表
    tables = pd.read_html(StringIO(r2.text))  # 已包 StringIO，避開 FutureWarning
    print(tables)
    def pick_from_multiindex(df: pd.DataFrame):
        if not isinstance(df.columns, pd.MultiIndex):
            return None
        # 找到「規格豬」這個上層分組的三欄
        spec_cols = [c for c in df.columns if str(c[0]).strip() == "規格豬"]
        if len(spec_cols) < 3:
            return None
        # 找「日期」欄（上/下層其一是「日期」）
        date_col = None
        for c in df.columns:
            parts = [str(x).strip() for x in (c if isinstance(c, tuple) else (c,))]
            if "日期" in parts:
                date_col = c
                break
        if date_col is None:
            return None
        sub = df[[date_col] + spec_cols].copy()
        sub.columns = ["日期", "成交頭數", "平均重量", "平均價格"]
        return sub

    def pick_from_flat(df: pd.DataFrame):
        # 把多層表頭攤平成 "上層_下層"
        if isinstance(df.columns, pd.MultiIndex):
            flat = []
            for tup in df.columns.to_list():
                parts = [str(x).strip() for x in tup if str(x).strip() not in ("", "nan")]
                flat.append("_".join(parts))
            df2 = df.copy()
            df2.columns = flat
        else:
            df2 = df.copy()
            df2.columns = [str(c).strip() for c in df2.columns]

        wanted = ["日期", "規格豬_成交頭數", "規格豬_平均重量", "規格豬_平均價格"]
        if all(c in df2.columns for c in wanted):
            sub = df2[wanted].rename(columns={
                "規格豬_成交頭數": "成交頭數",
                "規格豬_平均重量": "平均重量",
                "規格豬_平均價格": "平均價格",
            })
            return sub
        return None


    target = None
    for t in tables:
        cand = pick_from_multiindex(t)
        if cand is None:
            cand = pick_from_flat(t)
        if cand is not None:
            target = cand
            break

    if target is None:
        raise RuntimeError("找不到『規格豬』日統計的表格，可能頁面結構變更。")
    
    # 清理：轉日期、排序
    target["日期"] = pd.to_datetime(target["日期"], errors="coerce").dt.date
    target = target.dropna(subset=["日期"]).sort_values("日期").reset_index(drop=True)
    return target

if __name__ == "__main__":
    time_handler = TimeHandler()
    start_date_str = "2020-01-01"
    end_date_str = "2025-09-24"

    start_date_roc = time_handler.gregorian_str_to_roc(start_date_str)
    end_date_roc = time_handler.gregorian_str_to_roc(end_date_str)
    output_path = OUTPUT_DIR / f"{start_date_roc}-{end_date_roc}年交易市場-毛豬交易價量走勢圖資料.xlsx"

    df = fetch_pig_spec_table(start_date_str, end_date_str, exclude_penghu=True)
    df.to_excel(output_path, index=False)
    print(f"saved: {output_path}")