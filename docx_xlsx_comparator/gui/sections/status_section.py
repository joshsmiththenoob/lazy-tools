"""
Duty on Showing the comparison result status.
"""

import tkinter as tk

from gui.configs import (
    FONT_FAMILY,
)


class StatusSection:
    def __init__(self, parent, theme=None):
        self.parent = parent

        self.status_var = tk.StringVar(value="狀態：尚未執行")
        self.output_var = tk.StringVar(value="輸出檔案：尚未產生")
        self.theme = theme

        self.frame = self._build()

    def _build(self):
        frame = tk.Frame(
            self.parent,
            bg=self.theme["panel_bg"],
            highlightbackground=self.theme["green"],
            highlightthickness=1
        )

        status_label = tk.Label(
            frame,
            textvariable=self.status_var,
            font=(FONT_FAMILY, 10, "bold"),
            bg=self.theme["panel_bg"],
            fg=self.theme["green"]
        )
        status_label.pack(side="left", padx=24)

        output_label = tk.Label(
            frame,
            textvariable=self.output_var,
            font=(FONT_FAMILY, 10),
            bg=self.theme["panel_bg"],
            fg=self.theme["green"]
        )
        output_label.pack(side="left", padx=40)

        return frame

    def set_status(self, message: str):
        self.status_var.set(f"狀態：{message}")

    def set_output_path(self, output_path: str):
        self.output_var.set(f"輸出檔案：{output_path}")

    def reset(self):
        self.status_var.set("狀態：尚未執行")
        self.output_var.set("輸出檔案：尚未產生")