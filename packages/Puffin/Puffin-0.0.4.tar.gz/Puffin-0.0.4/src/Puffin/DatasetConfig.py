from abc import ABC
from dataclasses import dataclass
from pathlib import Path

import prettyprinter as pp

from Puffin.enums import FileType, StorageType
from Puffin.logger import logger_setup

logger = logger_setup()
import json

pp.install_extras()


@dataclass
class DatasetConfig(ABC):
    name: str

    def info(self):
        pp.pprint(self)

    # NOTE I might move this to a different class (paths or w/e)
    def create_dir(self, json_path: Path):
        if json_path.is_dir():
            json_path.mkdir(parents=True, exist_ok=True)
        elif json_path.suffix != '':
            json_path.parent.mkdir(parents=True, exist_ok=True)
        else:
            err_msg = "Path is not a directory or file"
            logger.error(err_msg)
            raise IOError(err_msg)


    def path_to_str(self, path: Path) -> str:
        return str(path)

    def str_to_path(self, string: str) -> Path:
        return Path(string)

    def to_dict(self):
        return {varname:str(varval) for varname, varval in vars(self).items()}

    def import_json(self, json_path: Path):
        json_str_path = self.path_to_str(path=json_path)

        with open(json_str_path, encoding='utf-8') as json_file:
            json_dict = json.load(json_file)
        
        if json_dict["storagetype"] == str(StorageType.file):
            return FileDatasetConfig(
                name=json_dict["name"],
                path=Path(json_dict["path"]),
                filetype=FileType.from_str(json_dict["filetype"]),
                storagetype=StorageType.from_str(json_dict["storagetype"]),
            )
        else:
            # NOTE - If I can log all printed info I dont need to log here
            err_msg = f"Importing from json with dataset storage type {StorageType.file} is not yet supported"
            logger.error(err_msg)
            raise ImportError(err_msg)

    def export_json(self, json_path: Path):
        self.create_dir(json_path)
        json_str_path = self.path_to_str(json_path)
        with open(json_str_path, encoding='utf-8', mode='w') as json_file:
            json.dump(self.to_dict(), json_file)


@dataclass
class FileDatasetConfig(DatasetConfig):
    path: Path
    filetype: FileType
    storagetype: StorageType = StorageType.file

@dataclass
class DatabaseDatasetConfig(DatasetConfig):
    env_file: Path
    query: str
    storagetype: StorageType = StorageType.db

    def connection_string_from_env(self):
        return self
