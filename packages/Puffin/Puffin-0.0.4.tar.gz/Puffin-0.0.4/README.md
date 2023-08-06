# Puffin
Simplify IO for your data science projects!

## Example code
```python
"""Puffin package"""

from pathlib import Path

from Puffin.DatasetConfig import DatabaseDatasetConfig, DatasetConfig, FileDatasetConfig
from Puffin.DatasetLibrary import DatasetLibrary
from Puffin.enums import FileType

if __name__ == "__main__":
    # define a dataset config from file
    file_dataset_config = FileDatasetConfig(
        name="train_in_file",
        path=Path("src/Puffin/tests/data/test.csv"),
        filetype=FileType.csv,
    )

    # ...or from a database query
    db_dataset_config = DatabaseDatasetConfig(
        name="train_in_db",
        query='SELECT first, last FROM DB.dbo.Names',
        env_file=Path('.env')
    ).connection_string_from_env()

    # print config info in a readable way
    file_dataset_config.info()

    # create dataset library and load dataset
    dsl = DatasetLibrary()
    dsl.add_dataset_config(file_dataset_config)
    dsl.add_dataset_config(db_dataset_config)
    df = dsl.load_df("train_in_file")
    print(df)

    # export and import functionality
    EXPORT_PATH = Path("exports/fds.json")
    file_dataset_config.export_json(EXPORT_PATH)
    file_dataset_config2 = DatasetConfig(name='train_in2').import_json(EXPORT_PATH)
    file_dataset_config2

```