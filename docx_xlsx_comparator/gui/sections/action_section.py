"""
Duty on executing what user want to do like comparsion/clear all opetion etc.
"""

"""
Duty:
ActionSection is responsible for action buttons only.
It does not execute comparison logic directly.
"""

import tkinter as tk

from gui.configs import (
    FONT_FAMILY,
)


class ActionSection:
    def __init__(self, parent, on_compare=None, on_clear=None, theme=None):
        self.parent = parent
        self.on_compare = on_compare
        self.on_clear = on_clear
        self.theme = theme

        self.frame = self._build()

    def _build(self):
        frame = tk.LabelFrame(
            self.parent,
            text="  ▶ 比對操作區  ",
            font=(FONT_FAMILY, 11, "bold"),
            fg=self.theme["green"],
            bg=self.theme["panel_bg"],
            padx=12,
            pady=8
        )

        start_btn = tk.Button(
            frame,
            text="🔍 開始比對",
            font=(FONT_FAMILY, 13, "bold"),
            bg=self.theme["button_green"],
            fg="white",
            width=18,
            height=1,
            command=self._handle_compare_clicked
        )
        start_btn.grid(row=0, column=0, padx=80)

        clear_btn = tk.Button(
            frame,
            text="🧹 清除所有選擇",
            font=(FONT_FAMILY, 11, "bold"),
            bg="white",
            fg=self.theme["green"],
            width=18,
            height=1,
            command=self._handle_clear_clicked
        )
        clear_btn.grid(row=0, column=1, padx=20)

        tip_label = tk.Label(
            frame,
            text="小提示：請先選檔案，載入欄位後再開始比對。",
            font=(FONT_FAMILY, 9),
            bg=self.theme["panel_bg"],
            fg=self.theme["green"]
        )
        tip_label.grid(row=0, column=2, padx=20)

        return frame

    def _handle_compare_clicked(self):
        if self.on_compare:
            self.on_compare()

    def _handle_clear_clicked(self):
        if self.on_clear:
            self.on_clear()