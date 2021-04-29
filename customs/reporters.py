
import json
import pathlib
import pickle
from typing import List, Union
import uuid

from .core import Reporter

class PrintReporter(Reporter):
    """Just prints the list of imports out
    """

    def __call__(self, imports: List[str]) -> None:
        print(imports)


class FileReporter(Reporter):
    """Contract for reporters that write to files on disk
    """

    def __init__(self, path: Union[pathlib.Path, None] = None) -> None:
        self.path = path or self._default_path()

    def _default_path(self) -> pathlib.Path:
        return self.default_path_parent() / self.default_path_name()

    def default_path_parent(self) -> pathlib.Path:
        return pathlib.Path()

    def default_path_name(self) -> pathlib.Path:
        raise NotImplementedError


class PickleReporter(FileReporter):
    """Serializes the list of imports to a pickle file
    """

    def default_path_name(self) -> pathlib.Path:
        return f"customs-{uuid.uuid4().hex}.pkl"

    def __call__(self, imports: List[str]) -> None:
        with open(self.path, "wb") as stream:
            pickle.dump(imports, stream)


class TextFileReporter(FileReporter):
    """Writes the list of imports to a text file, one per line
    """

    def default_path_name(self) -> pathlib.Path:
        return f"customs-{uuid.uuid4().hex}.txt"

    def __call__(self, imports: List[str]) -> None:
        with open(self.path, "w") as stream:
            for entry in imports:
                stream.write(f"{entry}\n")


class JSONFileReporter(FileReporter):
    """JSON is hip
    """

    def default_path_name(self) -> pathlib.Path:
        return f"customs-{uuid.uuid4().hex}.json"

    def __call__(self, imports: List[str]) -> None:
        with open(self.path, "w") as stream:
            json.dump(imports, stream)
