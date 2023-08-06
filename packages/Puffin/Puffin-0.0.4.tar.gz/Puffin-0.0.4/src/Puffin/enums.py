import sys
from enum import Enum, auto

# local, aws, azure etc (auth should be variable)

class DatasetEnumeration(Enum):
    @classmethod
    def from_str(cls, dataset_enum_str: str) -> Enum:
        dataset_enum_class_str = dataset_enum_str.split('.')[0]
        dataset_enum_var_str = dataset_enum_str.split('.')[-1]
        dataset_enum_class = getattr(sys.modules[__name__], dataset_enum_class_str)
        return dataset_enum_class[dataset_enum_var_str]
        
class StorageType(DatasetEnumeration):
    db = auto()
    file = auto()

class FileType(DatasetEnumeration):
    csv = auto()
    parquet = auto()
    json = auto()



class VarType(DatasetEnumeration):
    df = auto()
