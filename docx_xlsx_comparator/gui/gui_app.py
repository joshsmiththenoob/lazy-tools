import tkinter as tk
from tkinter import ttk
from pathlib import Path
from PIL import Image, ImageTk


class ComparatorApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Word / Excel 比對工具")
        # self.root.geometry("900x600")
        self.root.resizable(False, False)

        self.base_dir = Path(__file__).resolve().parent
        self.assets_dir = self.base_dir / "assets"

        self._build_ui()

    def _build_ui(self):
        self._build_background()
        self._build_file_section()
        self._build_column_section()
        self._build_action_section()
        self._build_status_section()

    def _build_background(self):
        bg_path = self.assets_dir / "background.png"

        bg_image = Image.open(bg_path)
        bg_image = bg_image.resize((900, 600))
        self.bg_photo = ImageTk.PhotoImage(bg_image)

        self.canvas = tk.Canvas(
            self.root,
            width=900,
            height=600,
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

    def _build_file_section(self):
        frame = tk.LabelFrame(
            self.root,
            text="  📁 檔案選擇區  ",
            font=("Microsoft JhengHei", 11, "bold"),
            fg="#1F6B36",
            bg="#FAFFFA",
            padx=12,
            pady=10
        )

        self.canvas.create_window(
            450, 230,
            window=frame,
            width=840,
            height=105
        )

        # Word row
        word_label = tk.Label(
            frame,
            text="Word 檔案 (.docx)",
            font=("Microsoft JhengHei", 10, "bold"),
            bg="#FAFFFA",
            fg="#163F22"
        )
        word_label.grid(row=0, column=0, sticky="w", padx=8, pady=6)

        self.word_path_var = tk.StringVar(value="尚未選擇檔案")
        word_entry = tk.Entry(
            frame,
            textvariable=self.word_path_var,
            font=("Microsoft JhengHei", 10),
            width=45
        )
        word_entry.grid(row=0, column=1, padx=8, pady=6)

        word_btn = tk.Button(
            frame,
            text="瀏覽",
            font=("Microsoft JhengHei", 10, "bold"),
            bg="#3A9B47",
            fg="white",
            width=10
        )
        word_btn.grid(row=0, column=2, padx=8, pady=6)

        # Excel row
        excel_label = tk.Label(
            frame,
            text="Excel 檔案 (.xlsx)",
            font=("Microsoft JhengHei", 10, "bold"),
            bg="#FAFFFA",
            fg="#163F22"
        )
        excel_label.grid(row=1, column=0, sticky="w", padx=8, pady=6)

        self.excel_path_var = tk.StringVar(value="尚未選擇檔案")
        excel_entry = tk.Entry(
            frame,
            textvariable=self.excel_path_var,
            font=("Microsoft JhengHei", 10),
            width=45
        )
        excel_entry.grid(row=1, column=1, padx=8, pady=6)

        excel_btn = tk.Button(
            frame,
            text="瀏覽",
            font=("Microsoft JhengHei", 10, "bold"),
            bg="#3A9B47",
            fg="white",
            width=10
        )
        excel_btn.grid(row=1, column=2, padx=8, pady=6)

    def _build_column_section(self):
        frame = tk.LabelFrame(
            self.root,
            text="  ⚙ 欄位選擇區  ",
            font=("Microsoft JhengHei", 11, "bold"),
            fg="#1F6B36",
            bg="#FAFFFA",
            padx=12,
            pady=10
        )

        self.canvas.create_window(
            450, 385,
            window=frame,
            width=840,
            height=190
        )

        # 1. Key column
        key_frame = tk.Frame(frame, bg="#FAFFFA")
        key_frame.grid(row=0, column=0, padx=8, pady=4, sticky="n")

        tk.Label(
            key_frame,
            text="1. 選擇主要欄位",
            font=("Microsoft JhengHei", 10, "bold"),
            bg="#FAFFFA",
            fg="#1F6B36"
        ).pack(anchor="w")

        self.key_col_var = tk.StringVar()
        key_combo = ttk.Combobox(
            key_frame,
            textvariable=self.key_col_var,
            values=["安全控制措施", "類別", "年度"],
            width=22,
            state="readonly"
        )
        key_combo.pack(pady=8)

        tk.Label(
            key_frame,
            text="此欄位用來找出兩份檔案\n共同的列名稱。",
            font=("Microsoft JhengHei", 9),
            bg="#EEF8EA",
            fg="#395C3D",
            justify="left",
            padx=8,
            pady=8
        ).pack(fill="x", pady=8)

        # 2. Row keys
        row_frame = tk.Frame(frame, bg="#FAFFFA")
        row_frame.grid(row=0, column=1, padx=8, pady=4, sticky="n")

        tk.Label(
            row_frame,
            text="2. 選擇要比對的列",
            font=("Microsoft JhengHei", 10, "bold"),
            bg="#FAFFFA",
            fg="#1F6B36"
        ).pack(anchor="w")

        self.row_key_listbox = tk.Listbox(
            row_frame,
            selectmode="multiple",
            width=28,
            height=6,
            font=("Microsoft JhengHei", 9)
        )
        self.row_key_listbox.pack(pady=8)

        for item in ["列名稱範例 1", "列名稱範例 2", "列名稱範例 3", "列名稱範例 4"]:
            self.row_key_listbox.insert(tk.END, item)

        # 3. Compare columns
        compare_frame = tk.Frame(frame, bg="#FAFFFA")
        compare_frame.grid(row=0, column=2, padx=8, pady=4, sticky="n")

        tk.Label(
            compare_frame,
            text="3. 選擇要比對的欄位",
            font=("Microsoft JhengHei", 10, "bold"),
            bg="#FAFFFA",
            fg="#1F6B36"
        ).pack(anchor="w")

        self.compare_col_listbox = tk.Listbox(
            compare_frame,
            selectmode="multiple",
            width=28,
            height=6,
            font=("Microsoft JhengHei", 9)
        )
        self.compare_col_listbox.pack(pady=8)

        for item in ["符合性或不適用情況說明", "佐證資料說明", "數值", "備註"]:
            self.compare_col_listbox.insert(tk.END, item)

    def _build_action_section(self):
        frame = tk.LabelFrame(
            self.root,
            text="  ▶ 比對操作區  ",
            font=("Microsoft JhengHei", 11, "bold"),
            fg="#1F6B36",
            bg="#FAFFFA",
            padx=12,
            pady=8
        )

        self.canvas.create_window(
            450, 510,
            window=frame,
            width=840,
            height=65
        )

        start_btn = tk.Button(
            frame,
            text="🔍 開始比對",
            font=("Microsoft JhengHei", 13, "bold"),
            bg="#3A9B47",
            fg="white",
            width=18,
            height=1
        )
        start_btn.grid(row=0, column=0, padx=80)

        clear_btn = tk.Button(
            frame,
            text="🧹 清除所有選擇",
            font=("Microsoft JhengHei", 11, "bold"),
            bg="white",
            fg="#1F6B36",
            width=18,
            height=1
        )
        clear_btn.grid(row=0, column=1, padx=20)

        tip_label = tk.Label(
            frame,
            text="小提示：請先選檔案，載入欄位後再開始比對。",
            font=("Microsoft JhengHei", 9),
            bg="#FAFFFA",
            fg="#5C6F5C"
        )
        tip_label.grid(row=0, column=2, padx=20)

    def _build_status_section(self):
        frame = tk.Frame(
            self.root,
            bg="#FAFFFA",
            highlightbackground="#D6E8D1",
            highlightthickness=1
        )

        self.canvas.create_window(
            450, 570,
            window=frame,
            width=840,
            height=40
        )

        self.status_var = tk.StringVar(value="狀態：尚未執行")
        self.output_var = tk.StringVar(value="輸出檔案：尚未產生")

        status_label = tk.Label(
            frame,
            textvariable=self.status_var,
            font=("Microsoft JhengHei", 10, "bold"),
            bg="#FAFFFA",
            fg="#1F6B36"
        )
        status_label.pack(side="left", padx=24)

        output_label = tk.Label(
            frame,
            textvariable=self.output_var,
            font=("Microsoft JhengHei", 10),
            bg="#FAFFFA",
            fg="#333333"
        )
        output_label.pack(side="left", padx=40)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = ComparatorApp()
    app.run()