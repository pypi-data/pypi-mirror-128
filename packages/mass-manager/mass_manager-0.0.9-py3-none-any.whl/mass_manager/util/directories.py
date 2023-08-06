from collections import OrderedDict, namedtuple
from pathlib import Path
from textwrap import dedent

from mass_manager.util.util import conditional_dedent_item


DEFAULT_DIRTYPES = ["main", "project", "project_subdir", "data", "models", "maps"]
DEFAULT_DATA_DIRTYPES = ["external", "interim", "processed", "raw"]

DirPathFormatter = namedtuple(
    "DirPathFormatter",
    [
        "main",
        "dirtype",
        "subdir",
        "project",
    ],
)

DirPathFormatter.__repr__ = lambda self: str(
    Path(
        str("{" + "}/{".join(list(OrderedDict(self._asdict()))) + "}").format(
            **self._asdict()
        )
    )
)
DirPathFormatter.__call__ = lambda self: Path(self.__repr__())

Directories = namedtuple("Directories", list(DEFAULT_DIRTYPES))
Directories.__repr__ = lambda self: dedent(
    "".join(
        [
            conditional_dedent_item(attr, str(getattr(self, attr, "")))
            for attr in self._fields
        ]
    )
)
