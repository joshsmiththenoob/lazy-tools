# platform_market_comparator/adapters/base.py
from abc import ABC, abstractmethod
import pandas as pd
from pathlib import Path

class DataAdapter(ABC):
    @abstractmethod
    def load(self) -> pd.DataFrame:
        """Return a normalized DataFrame with unified columns."""
        if self.path is None:
            raise NotImplementedError('Class attribute PATH not advised at DataAdapter inheritance')