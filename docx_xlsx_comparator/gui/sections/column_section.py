"""
Duty:
1. Select key column
2. Show common row keys based on key column
3. Select compare columns
"""

import tkinter as tk
from tkinter import ttk

from gui.configs import (
    FONT_FAMILY,
)


class ColumnSection:
    def __init__(self, parent, on_key_col_selected=None, theme=None):
        self.parent = parent
        self.on_key_col_selected = on_key_col_selected
        self.theme = theme

        self.key_col_var = tk.StringVar()

        self.frame = self._build()

    def _build(self):
        frame = tk.LabelFrame(
            self.parent,
            text="  ⚙ 欄位選擇區  ",
            font=(FONT_FAMILY, 11, "bold"),
            fg=self.theme["green"],
            bg=self.theme["panel_bg"],
            padx=12,
            pady=10
        )

        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_columnconfigure(2, weight=1)

        self._build_key_column_area(frame)
        self._build_row_key_area(frame)
        self._build_compare_column_area(frame)

        return frame

    def _build_key_column_area(self, parent):
        key_frame = tk.Frame(parent, bg=self.theme["panel_bg"])
        key_frame.grid(row=0, column=0, padx=8, pady=4, sticky="n")

        tk.Label(
            key_frame,
            text="1. 選擇主要欄位",
            font=(FONT_FAMILY, 10, "bold"),
            bg=self.theme["panel_bg"],
            fg=self.theme["green"]
        ).pack(anchor="w")

        self.key_col_combo = ttk.Combobox(
            key_frame,
            textvariable=self.key_col_var,
            values=[],
            width=22,
            state="readonly"
        )
        self.key_col_combo.pack(pady=8)

        self.key_col_combo.bind(
            "<<ComboboxSelected>>",
            self._handle_key_col_selected
        )

        tk.Label(
            key_frame,
            text="此欄位用來找出兩份檔案\n共同的列名稱。",
            font=(FONT_FAMILY, 9),
            bg=self.theme["hint_bg"],
            fg=self.theme["green"],
            justify="left",
            padx=8,
            pady=8
        ).pack(fill="x", pady=8)

    def _build_row_key_area(self, parent):
        row_frame = tk.Frame(parent, bg=self.theme["panel_bg"])
        row_frame.grid(row=0, column=1, padx=8, pady=4, sticky="n")

        tk.Label(
            row_frame,
            text="2. 選擇共同列",
            font=(FONT_FAMILY, 10, "bold"),
            bg=self.theme["panel_bg"],
            fg=self.theme["green"]
        ).pack(anchor="w")

        # Initialize row key listbox (Listbox for selecting common row keys based on the selected key column)
        self.row_key_listbox = tk.Listbox(
            row_frame,
            selectmode="multiple",
            width=28,
            height=6,
            font=(FONT_FAMILY, 9),
            bg=self.theme["listbox_bg"],
            fg=self.theme["listbox_fg"],
            selectbackground=self.theme["button_green"],
            selectforeground="white",
            exportselection=False
        )
        self.row_key_listbox.pack(pady=8)

    def _build_compare_column_area(self, parent):
        compare_frame = tk.Frame(parent, bg=self.theme["panel_bg"])
        compare_frame.grid(row=0, column=2, padx=8, pady=4, sticky="n")

        tk.Label(
            compare_frame,
            text="3. 選擇比對欄位",
            font=(FONT_FAMILY, 10, "bold"),
            bg=self.theme["panel_bg"],
            fg=self.theme["green"]
        ).pack(anchor="w")

        # Initialize compare column listbox (Listbox for selecting columns to compare)
        self.compare_col_listbox = tk.Listbox(
            compare_frame,
            selectmode="multiple",
            width=28,
            height=6,
            font=(FONT_FAMILY, 9),
            bg=self.theme["listbox_bg"],
            fg=self.theme["listbox_fg"],
            selectbackground=self.theme["button_green"],
            selectforeground="white",
            exportselection=False
        )
        self.compare_col_listbox.pack(pady=8)

    def _handle_key_col_selected(self, event=None):
        key_col = self.get_key_column()

        if self.on_key_col_selected:
            self.on_key_col_selected(key_col)

    # ---------- 外部更新畫面用 ----------

    def set_key_columns(self, columns):
        self.key_col_combo["values"] = columns

        if columns:
            self.key_col_var.set(columns[0])

    def set_row_keys(self, row_keys):
        self.row_key_listbox.delete(0, tk.END)

        for row_key in row_keys:
            self.row_key_listbox.insert(tk.END, row_key)

    def set_compare_columns(self, columns):
        self.compare_col_listbox.delete(0, tk.END)

        for col in columns:
            self.compare_col_listbox.insert(tk.END, col)

    def clear_selection(self):
        self.row_key_listbox.selection_clear(0, tk.END)
        self.compare_col_listbox.selection_clear(0, tk.END)

    # ---------- 外部取得使用者選擇用 ----------

    def get_key_column(self):
        return self.key_col_var.get()

    def get_selected_row_keys(self):
        selected_indices = self.row_key_listbox.curselection()
        return [
            self.row_key_listbox.get(i)
            for i in selected_indices
        ]

    def get_selected_compare_columns(self):
        selected_indices = self.compare_col_listbox.curselection()
        return [
            self.compare_col_listbox.get(i)
            for i in selected_indices
        ]