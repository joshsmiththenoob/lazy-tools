import tkinter as tk
from tkinter import ttk, filedialog
from pathlib import Path
from PIL import Image, ImageTk
from gui.sections.file_section import FileSection
from gui.sections.column_section import ColumnSection
from gui.sections.action_section import ActionSection
from gui.sections.status_section import StatusSection
from gui.configs import WINDOW_WIDTH, WINDOW_HEIGHT, FONT_FAMILY, THEMES


from adapters.word_table_adapter import WordTableAdapter
from adapters.excel_table_adapter import ExcelTableAdapter
from utils.table_comparactor import TableComparator
from utils.report_exporter import ReportExporter


import sys
from pathlib import Path


def resource_path(relative_path: str) -> Path:
    if hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS) / relative_path

    return Path(__file__).resolve().parent / relative_path
class ComparatorApp:
    def __init__(self):
        # Main application window setup
        self.root = tk.Tk()                      # Main application window
        self.root.title("Word / Excel 比對工具")
        self.root.geometry("900x600")
        self.root.resizable(False, False)
        self.theme_name = "light"
        self.theme = THEMES[self.theme_name]

        self.base_dir = Path(__file__).resolve().parent
        self.assets_dir = self.base_dir / "assets"

        self.project_dir = self.base_dir.parent
        self.output_dir = self.project_dir / "output"
        self.output_dir.mkdir(exist_ok=True)

        self._build_ui()

    def _build_ui(self):
        # Canvas allows custom drawing, background images, and coordinate-based placement (The regular layout is Frame).
        # Therefore, the canvas and background must be created first in this UI.
        self._build_background() 
        self._build_title_section()
        self._build_theme_button()
        self._build_file_section()
        self._build_column_section()
        self._build_action_section()
        self._build_status_section()


    def _build_background(self):
        bg_filename = self.theme["background_image"]
        bg_path = resource_path(f"gui/assets/{bg_filename}")
        # bg_path = resource_path(f"assets/{bg_filename}")

        # Initialize background image
        bg_image = Image.open(bg_path)
        bg_image = bg_image.resize((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.bg_photo = ImageTk.PhotoImage(bg_image)

        # Create canvas f
        self.canvas = tk.Canvas(
            self.root,
            width=WINDOW_WIDTH,
            height=WINDOW_HEIGHT,
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")


    def _build_title_section(self):
        self.canvas.create_text(
            65, 72,
            text="Word / Excel",
            font=(FONT_FAMILY, 20, "bold"),
            fill=self.theme["title"],
            anchor="w"
        )

        self.canvas.create_text(
            65, 105,
            text="數值比對工具",
            font=(FONT_FAMILY, 20, "bold"),
            fill=self.theme["title"],
            anchor="w"
        )

        self.canvas.create_text(
            650, 72,
            text="快速比對 Excel 與 Word 表格內容，",
            font=(FONT_FAMILY, 11, "bold"),
            fill=self.theme["subtitle"],
            anchor="w"
        )

        self.canvas.create_text(
            650, 105,
            text="讓數值比對更輕鬆、更有效率！",
            font=(FONT_FAMILY, 11, "bold"),
            fill=self.theme["subtitle"],
            anchor="w"
        )

    def _build_theme_button(self):
        button_text = "🌙 深色模式" if self.theme_name == "light" else "☀ 淺色模式"

        self.theme_button = tk.Button(
            self.root,
            text=button_text,
            font=(FONT_FAMILY, 9, "bold"),
            bg=self.theme["panel_bg"],
            fg=self.theme["green"],
            activebackground=self.theme["hint_bg"],
            activeforeground=self.theme["text"],
            relief="ridge",
            command=self.handle_theme_toggle
        )

        self.canvas.create_window(
            790, 145,
            window=self.theme_button,
            width=120,
            height=30
        )

    def _build_file_section(self):
        self.file_section = FileSection(
            self.root,
            on_file_selected=self.handle_file_selected,
            theme=self.theme
        )

        self.canvas.create_window(
            450, 230,
            window=self.file_section.frame,
            width=840,
            height=105
        )


    def _build_column_section(self):
        self.column_section = ColumnSection(
            self.root,
            on_key_col_selected=self.handle_key_col_selected,
            theme=self.theme
        )

        self.canvas.create_window(
            450, 385,
            window=self.column_section.frame,
            width=840,
            height=190
        )


    def _build_action_section(self):
        self.action_section = ActionSection(
            self.root,
            on_compare=self.handle_compare_clicked,
            on_clear=self.handle_clear_clicked,
            theme=self.theme
        )

        self.canvas.create_window(
            450, 510,
            window=self.action_section.frame,
            width=840,
            height=65
        )


    def handle_file_selected(self):
        word_path = self.file_section.get_word_path()
        excel_path = self.file_section.get_excel_path()

        if not word_path or not excel_path:
            self.status_section.set_status("請選擇 Word 與 Excel 檔案")
            return

        self.status_section.set_status("正在讀取 Word / Excel 檔案...")

        try:
            word_adapter = WordTableAdapter(word_path)
            excel_adapter = ExcelTableAdapter(excel_path)

            self.word_df = word_adapter.load()
            self.excel_df = excel_adapter.load()

            # 欄位名稱清理
            self.word_df.columns = (
                self.word_df.columns
                .str.replace("\n", "", regex=False)
                .str.strip()
            )

            self.excel_df.columns = (
                self.excel_df.columns
                .str.replace("\n", "", regex=False)
                .str.strip()
            )

            ### tempoary : 先把 Excel 的 '安全控制措施說明' 欄位改名為 '安全控制措施'，等之後正式版本再改回來
            self.excel_df = (
                self.excel_df
                .drop(columns=["安全控制措施"])
                .rename(columns={"安全控制措施說明": "安全控制措施"})
                .reindex(columns=self.excel_df.columns)
            )

            self.comparator = TableComparator(self.word_df, self.excel_df)

            common_columns = self.comparator.find_common_columns()

            self.column_section.set_key_columns(common_columns)
            self.column_section.set_row_keys([])
            self.column_section.set_compare_columns([])

            self.status_section.set_status("檔案讀取完成，請選擇主要欄位")

        except Exception as e:
            self.status_section.set_status(f"檔案讀取失敗：{e}")


    def handle_key_col_selected(self, key_col):
        if not hasattr(self, "comparator"):
            self.status_section.set_status("請先選擇 Word 與 Excel 檔案")
            return

        try:
            common_row_keys = self.comparator.get_common_row_keys(key_col)
            compare_cols = self.comparator.get_rest_of_cols()

            self.column_section.set_row_keys(common_row_keys)
            self.column_section.set_compare_columns(compare_cols)

            self.status_section.set_status("共同列與比對欄位已更新")

        except Exception as e:
            self.status_section.set_status(f"欄位處理失敗：{e}")

        # 之後這裡才會真的呼叫 TableComparator
        # result_df = self.comparator.compare_multiple_values(
        #     selected_rows,
        #     selected_columns
        # )
        # report_exporter = ReportExporter(result_df)
        # report_exporter.export_to_excel(output_path)

        ####

        # if not key_col:
        #     self.status_section.set_status("請先選擇主要欄位")
        #     return

        # if not selected_rows:
        #     self.status_section.set_status("請至少選擇一個共同列")
        #     return

        # if not selected_columns:
        #     self.status_section.set_status("請至少選擇一個比對欄位")
        #     return

        # result_df = self.comparator.compare_multiple_values(
        #     selected_rows,
        #     selected_columns
        # )

        # output_path = self.output_dir / "comparison_result.xlsx"

        # report_exporter = ReportExporter(result_df)
        # report_exporter.export_to_excel(output_path)

        # self.status_section.set_status("比對完成")
        # self.status_section.set_output_path(str(output_path))


    def handle_clear_clicked(self):
        print("使用者按下清除所有選擇")
        self.column_section.clear_selection()
        self.status_section.reset()


    def handle_compare_clicked(self):
        print("使用者按下開始比對")

        if not hasattr(self, "comparator"):
            self.status_section.set_status("請先選擇 Word 與 Excel 檔案")
            return

        key_col = self.column_section.get_key_column()
        selected_rows = self.column_section.get_selected_row_keys()
        selected_columns = self.column_section.get_selected_compare_columns()

        if not key_col:
            self.status_section.set_status("請先選擇主要欄位")
            return

        if not selected_rows:
            self.status_section.set_status("請至少選擇一個共同列")
            return

        if not selected_columns:
            self.status_section.set_status("請至少選擇一個比對欄位")
            return

        try:
            self.status_section.set_status("比對中...")

            result_df = self.comparator.compare_multiple_values(
                selected_rows,
                selected_columns
            )

            self.status_section.set_status("請選擇儲存位置...")
            self.root.update_idletasks()

            output_path = filedialog.asksaveasfilename(
                parent=self.root,
                title="儲存比對結果",
                initialdir=self.output_dir,
                initialfile="comparison_result.xlsx",
                defaultextension=".xlsx",
                filetypes=[
                    ("Excel files", "*.xlsx"),
                    ("All files", "*.*")
                ]
            )

            if not output_path:
                self.status_section.set_status("已取消儲存")
                return

            report_exporter = ReportExporter(result_df)
            report_exporter.export_to_excel(output_path)

            self.status_section.set_status("比對完成")
            self.status_section.set_output_path(Path(output_path).name)

            print("比對完成:", output_path)

        except Exception as e:
            self.status_section.set_status(f"比對失敗：{e}")

        # 之後這裡才會接真正的 TableComparator
        # result_df = self.comparator.compare_multiple_values(
        #     selected_rows,
        #     selected_columns
        # )
        #
        # output_path = self.output_dir / "comparison_result.xlsx"
        # report_exporter = ReportExporter(result_df)
        # report_exporter.export_to_excel(output_path)
        #
        # self.status_section.set_status("比對完成")
        # self.status_section.set_output_path(str(output_path))

        print("key_col:", key_col)
        print("selected_rows:", selected_rows)
        print("selected_columns:", selected_columns)


    def handle_theme_toggle(self):
        self.theme_name = "dark" if self.theme_name == "light" else "light"
        self.theme = THEMES[self.theme_name]

        
        # Destroy all existing widgets before rebuilding the UI
        for child in self.root.winfo_children():
            child.destroy()

            
        # Rebuild the entire UI with the selected theme
        self._build_ui()

    def _build_status_section(self):
        self.status_section = StatusSection(self.root, theme=self.theme)

        self.canvas.create_window(
            450, 570,
            window=self.status_section.frame,
            width=840,
            height=40
        )


    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = ComparatorApp()
    app.run()