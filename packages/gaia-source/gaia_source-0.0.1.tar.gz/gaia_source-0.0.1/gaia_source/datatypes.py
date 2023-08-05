import enum
import os
import typing

class DownloadOptions(enum.Enum):
    Zero = 'zero-files'
    Five = 'only-five'

class DataPath(typing.NamedTuple):
    path: str
    csv_path: str
    @property
    def abs_csv_filepath(self):
        return os.path.abspath(os.path.join(os.getcwd(), self.csv_path))

class InstallOptions(enum.Enum):
    Nothing = 'nothing'
    Everything = 'everything'
