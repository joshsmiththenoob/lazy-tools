"""
Duty on Selecting Word and Excel Files
"""

import tkinter as tk
from tkinter import filedialog
from pathlib import Path
from gui.configs import (
    FONT_FAMILY,
)


class FileSection:
    def __init__(self, parent, on_file_selected=None, theme=None):
        self.parent = parent
        self.on_file_selected = on_file_selected
        self.theme = theme

        self.word_path_var = tk.StringVar(value="尚未選擇檔案")
        self.excel_path_var = tk.StringVar(value="尚未選擇檔案")

        self.frame = self._build()

    def _build(self):
        frame = tk.LabelFrame(
            self.parent,
            text="  📁 檔案選擇區  ",
            font=(FONT_FAMILY, 11, "bold"),
            bg=self.theme["panel_bg"],
            fg=self.theme["green"],
            padx=12,
            pady=10
        )

        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)

        self._build_word_area(frame)
        self._build_excel_area(frame)

        return frame

    def _build_word_area(self, parent):
        word_frame = tk.Frame(parent, bg=self.theme["panel_bg"])
        word_frame.grid(row=0, column=0, sticky="w", padx=10, pady=8)

        tk.Label(
            word_frame,
            text="Word 檔案 (.docx)",
            font=(FONT_FAMILY, 10, "bold"),
            bg=self.theme["panel_bg"],
            fg=self.theme["green"],
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 6))

        tk.Entry(
            word_frame,
            textvariable=self.word_path_var,
            font=(FONT_FAMILY, 9),
            width=26,
            bg=self.theme["entry_bg"],
            fg=self.theme["entry_fg"],
            insertbackground=self.theme["entry_fg"]
        ).grid(row=1, column=0, padx=(0, 8))

        tk.Button(
            word_frame,
            text="瀏覽",
            font=(FONT_FAMILY, 9, "bold"),
            bg=self.theme["button_green"],
            fg="white",
            width=8,
            command=self._select_word_file
        ).grid(row=1, column=1)

    def _build_excel_area(self, parent):
        excel_frame = tk.Frame(parent, bg=self.theme["panel_bg"])
        excel_frame.grid(row=0, column=1, sticky="w", padx=10, pady=8)

        tk.Label(
            excel_frame,
            text="Excel 檔案 (.xlsx)",
            font=(FONT_FAMILY, 10, "bold"),
            bg=self.theme["panel_bg"],
            fg=self.theme["green"]
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 6))

        tk.Entry(
            excel_frame,
            textvariable=self.excel_path_var,
            font=(FONT_FAMILY, 9),
            bg=self.theme["entry_bg"],
            fg=self.theme["entry_fg"],
            width=26
        ).grid(row=1, column=0, padx=(0, 8))

        tk.Button(
            excel_frame,
            text="瀏覽",
            font=(FONT_FAMILY, 9, "bold"),
            bg=self.theme["button_green"],
            fg="white",
            width=8,
            command=self._select_excel_file
        ).grid(row=1, column=1)


    def _select_word_file(self):
        file_path = filedialog.askopenfilename(
            title="選擇 Word 檔案",
            filetypes=[
                ("Word files", "*.docx"),
                ("All files", "*.*")
            ]
        )

        if file_path:
            self.word_file_path = file_path
            self.word_path_var.set(Path(file_path).name)
        
            if self.on_file_selected:
                self.on_file_selected()


    def _select_excel_file(self):
        file_path = filedialog.askopenfilename(
            title="選擇 Excel 檔案",
            filetypes=[
                ("Excel files", "*.xlsx *.xls"),
                ("All files", "*.*")
            ]
        )

        if file_path:
            self.excel_file_path = file_path
            self.excel_path_var.set(Path(file_path).name)

            if self.on_file_selected:
                self.on_file_selected()

    def get_word_path(self):
        return getattr(self, "word_file_path", None)

    def get_excel_path(self):
        return getattr(self, "excel_file_path", None)