"""
The Excel Adapter is responsible for 
1. loading Excel files like .xlsx, .xls
2. then converting them into a common DataFrame format for comparison.
"""

from .base import DataAdapter
import pandas as pd

class ExcelTableAdapter(DataAdapter):
    def __init__(self, path: str, sheet_name= 0):
        self.path = path
        self.sheet_name = sheet_name

    def load(self) -> pd.DataFrame:
        """Load the Excel file and convert it to a Standardized DataFrame."""
        raw_df = pd.read_excel(self.path, sheet_name=self.sheet_name)
        return self.__convert_to_dataframe(raw_df)
    
    def __convert_to_dataframe(self, raw_df: pd.DataFrame) -> pd.DataFrame:
        pass