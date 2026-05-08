#!/usr/bin/env python3
# -*- coding: utf-8 -*-

r"""
Merge PDFs by leading prefix like '0-1', '1-2', ..., 'F-2'.

Sorting rule:
  1) 以檔名開頭的模式 r'^([0-9A-Fa-f])-(\d+)' 擷取兩段：
     第一段視為 16 進位數字(0-9,A-F)，第二段為十進位整數。
     以 (第一段轉十進位, 第二段) 排序。
  2) 若某檔名沒有符合前綴，會排到最後，並以自然排序作為次序。
  3) 同一前綴多檔時，再用自然排序當次鍵穩定排序。
"""

from __future__ import annotations
import re
import sys
from pathlib import Path
from typing import Tuple, Optional, List
from pypdf import PdfReader, PdfWriter

# ====== 你只需要改下面這 4 行 ======
input_path  = r"pdf_merger\input\便簽"   # 資料夾：放很多 pdf 的地方
output_path = r"pdf_merger\output\便簽(全).pdf" # 輸出檔案（會自動建立資料夾）
recursive   = True                             # 要不要找子資料夾
dry_run     = False                            # 只看排序結果不輸出
# =====================================

PREFIX_RE = re.compile(r"^([0-9A-Fa-f])-(\d+)")


def natural_key(s: str):
    """Split string into digit/non-digit chunks for natural sort."""
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", s)]


def parse_prefix(filename: str) -> Optional[Tuple[int, int]]:
    """回傳 (十六進位前綴值, 後段整數)；不匹配則回傳 None。"""
    m = PREFIX_RE.match(filename)
    if not m:
        return None
    x_hex, y_dec = m.groups()
    try:
        return int(x_hex, 16), int(y_dec)
    except ValueError:
        return None


def find_pdfs(input_dir: Path, recursive: bool) -> List[Path]:
    pattern = "**/*.pdf" if recursive else "*.pdf"
    return sorted(input_dir.glob(pattern))


def sort_pdfs(files: List[Path]) -> List[Path]:
    def key_fn(p: Path):
        prefix = parse_prefix(p.name)
        if prefix is not None:
            x_val, y_val = prefix
            return (0, x_val, y_val, natural_key(p.name))
        else:
            return (1, 9999, 9999, natural_key(p.name))
    return sorted(files, key=key_fn)


def merge_pdfs(files: List[Path], out_path: Path, dry_run: bool=False) -> None:
    if dry_run:
        print("Dry-run 排序結果（實際未輸出）：")
        for i, f in enumerate(files, 1):
            print(f"{i:03d}. {f.name}")
        return

    writer = PdfWriter()
    appended = 0
    for f in files:
        try:
            reader = PdfReader(str(f))
            for page in reader.pages:
                writer.add_page(page)
            appended += 1
            print(f"[OK] {f.name}  ({len(reader.pages)} pages)")
        except Exception as e:
            print(f"[SKIP] {f.name}  ->  {e}", file=sys.stderr)

    if appended == 0:
        raise SystemExit("沒有可合併的 PDF（可能都壞掉或讀取失敗）")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("wb") as fp:
        writer.write(fp)
    print(f"\n完成！輸出：{out_path} ；合併檔數：{appended}")


def main():
    # 1) 把字串路徑轉成 Path（解決 .glob 的問題）
    in_dir = Path(input_path).resolve()
    if not in_dir.exists():
        raise SystemExit(f"找不到資料夾：{in_dir}")

    # 2) 掃檔、排序
    files = find_pdfs(in_dir, recursive=recursive)
    if not files:
        raise SystemExit("此資料夾找不到任何 .pdf 檔")
    files_sorted = sort_pdfs(files)

    # 3) 提醒未符合 'X-Y' 前綴的檔案
    unmatched = [p.name for p in files_sorted if parse_prefix(p.name) is None]
    if unmatched:
        print("注意：下列檔名未匹配 'X-Y' 前綴，已排到最後並以自然排序處理：")
        for n in unmatched:
            print("  -", n)
        print()

    # 4) 輸出
    out_path = Path(output_path).resolve()
    merge_pdfs(files_sorted, out_path, dry_run=dry_run)


if __name__ == "__main__":
    main()
