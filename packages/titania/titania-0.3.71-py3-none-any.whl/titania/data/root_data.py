import uproot
import pandas as pd
from titania.data.data_core import TitaniaDataInterface

class RootData(TitaniaDataInterface):
    def __init__(self, file_path):
        """
        Reads root files and outputs them as pandas dataframe using uproot
        Args:
            file_path:
        """
        self.file_path = file_path

    def fetch(self) -> pd.DataFrame:
        """
        Returns: pandas dataframe

        """
        upr = uproot.open(self.file_path)
        df = upr['tree;1'].tree.arrays(library="pandas")
        return df
