import pandas as pd

from Puffin.DatasetConfig import DatasetConfig
from Puffin.enums import FileType


class DataFrameDataset:
    def __init__(self, config:DatasetConfig):
        self.config = config

    def load_from_file(self):
        self.config.str_path = self.config.path_to_str(self.config.path)
        if self.config.filetype == FileType.csv:
            df = self.load_from_csv()

        return df
    
    def load_from_csv(self):
        df = pd.read_csv(self.config.str_path)
        return df
