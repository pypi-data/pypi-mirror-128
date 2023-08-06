from typing import List

from Puffin.Dataset import DataFrameDataset
from Puffin.DatasetConfig import DatasetConfig
from Puffin.enums import VarType


class DatasetLibrary:
    def add_dataset_config(self, config:DatasetConfig):
        if not hasattr(self, config.name):
            setattr(self, config.name, config)
        else:
            print(f'library already contains dataset with name {config.name}, skipping')

    def add_dataset_configs(self, configs:List[DatasetConfig]):
        for config in configs:
            self.add_dataset_config(config)

    def load_df(self, config_name):
        config = self.select_config(config_name)
        config.vartype = VarType.df

        df_ds = DataFrameDataset(config)
        df = df_ds.load_from_file()
        return df

    def save_df(self):
        pass

    def select_config(self, config_name):
        try:
            config = getattr(self, config_name)
        except AttributeError:
            print(f'config name {config_name} not found')
            config = None
        return config
