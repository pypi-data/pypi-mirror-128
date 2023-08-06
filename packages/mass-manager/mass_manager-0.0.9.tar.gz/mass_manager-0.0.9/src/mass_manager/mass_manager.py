"""TODO DOCSTRING."""
from collections import OrderedDict
from pathlib import Path
from textwrap import dedent

from cobra.util.util import format_long_string

from mass_manager.models import load_model_filetype, save_model_filetype
from mass_manager.util.directories import (
    DEFAULT_DATA_DIRTYPES,
    DEFAULT_DIRTYPES,
    Directories,
    DirPathFormatter,
)
from mass_manager.util.singleton import Singleton
from mass_manager.util.util import make_full_filename, show_mass_dependencies


class MassManager(metaclass=Singleton):
    """TODO DOCSTRING."""

    mass_dependencies = OrderedDict(
        {
            "mass_manager": "MASS-manager",
            "masspy": "MASSpy",
        }
    )
    default_model_filetype = "json"
    verbosity = 0

    def __init__(self, **kwargs):
        """Initialize the manager object with its default attribute values."""
        super().__init__(**kwargs)

        self._dirpath_formatters = None
        self._directories = None

        self._set_default_formatter_and_directories()

    @property
    def directories(self):
        """TODO DOCSTRING."""
        return getattr(self, "_directories")

    @property
    def dirpath_formatter(self):
        """TODO DOCSTRING."""
        return getattr(self, "_dirpath_formatter")

    @property
    def main_directory(self):
        """TODO DOCSTRING."""
        return getattr(self.directories, "main")()

    @main_directory.setter
    def main_directory(self, path_args):
        """TODO DOCSTRING."""
        self._set_directory("main", path_args)
        self._update_directories(DEFAULT_DIRTYPES[3:])

    @property
    def project_directory(self):
        """TODO DOCSTRING."""
        return getattr(self.directories, "project")()

    @project_directory.setter
    def project_directory(self, path_args):
        """TODO DOCSTRING."""
        self._set_directory("project", path_args)
        self._update_directories(DEFAULT_DIRTYPES[3:])

    @property
    def project_subdirectory(self):
        """TODO DOCSTRING."""
        return getattr(self.directories, "project_subdir")()

    @project_subdirectory.setter
    def project_subdirectory(self, path_args):
        """TODO DOCSTRING."""
        self._set_directory("project_subdir", path_args)
        self._update_directories(DEFAULT_DIRTYPES[3:])

    @property
    def data_directory(self):
        """TODO DOCSTRING."""
        return getattr(self.directories, "data")().relative_to(self.main_directory)

    @data_directory.setter
    def data_directory(self, path_args):
        """TODO DOCSTRING."""
        self._set_directory("data", path_args)

    @property
    def maps_directory(self):
        """TODO DOCSTRING."""
        return getattr(self.directories, "maps")().relative_to(self.main_directory)

    @maps_directory.setter
    def maps_directory(self, path_args):
        """TODO DOCSTRING."""
        self._set_directory("maps", path_args)

    @property
    def models_directory(self):
        """TODO DOCSTRING."""
        return getattr(self.directories, "models")().relative_to(self.main_directory)

    @models_directory.setter
    def models_directory(self, path_args):
        """TODO DOCSTRING."""
        self._set_directory("models", path_args)

    def save_model(self, model, filetype=None, module="mass", **kwargs):
        if filetype is None:
            filetype = self.default_model_filetype
        filename = make_full_filename(
            self.main_directory.joinpath(self.models_directory), model, filetype
        )
        verbose = (
            bool(self.verbosity) if "verbose" not in kwargs else kwargs.pop("verbose")
        )
        save_model_filetype(model, filename, module, verbose=verbose, **kwargs)

    def load_model(self, model, filetype=None, module="mass", **kwargs):
        if filetype is None:
            filetype = self.default_model_filetype
        filename = make_full_filename(
            self.main_directory.joinpath(self.models_directory), model, filetype
        )
        verbose = (
            bool(self.verbosity) if "verbose" not in kwargs else kwargs.pop("verbose")
        )
        return load_model_filetype(filename, module, verbose=verbose, **kwargs)

    @classmethod
    def show_mass_dependencies(cls):
        """TODO DOCSTRING."""
        show_mass_dependencies(cls.mass_dependencies)

    def _set_default_formatter_and_directories(self):
        setattr(self, "_dirpath_formatter", DirPathFormatter)
        setattr(self, "_directories", Directories)
        self._update_directories(DEFAULT_DIRTYPES)

    def _set_directory(self, dirtype, path_args=None):
        """TODO DOCSTRING."""
        try:
            dir_kwargs = self.directories._asdict()
        except TypeError:
            dir_kwargs = {attr: Path(".") for attr in self.directories._fields}
        dirformatter_kwargs = {
            attr: Path(".") for attr in self.dirpath_formatter._fields
        }
        if path_args is None:
            path_args = "."
        if isinstance(path_args, (str, Path)):
            path_args = [str(path_args)]

        if dirtype in ["main"]:
            dirformatter_kwargs["main"] = Path("/".join(path_args)).resolve()
        elif dirtype in ["project"]:
            dirformatter_kwargs["project"] = Path("/".join(path_args))
        elif dirtype.endswith("subdir"):
            dirformatter_kwargs["subdir"] = Path("/".join(path_args))
        else:
            dirformatter_kwargs.update(
                {
                    "main": self.directories.main(),
                    "project": Path(
                        "/".join(
                            (
                                str(self.directories.project()),
                                str(self.directories.project_subdir()),
                            )
                        )
                    ),
                    "dirtype": Path(dirtype),
                    "subdir": Path("/".join(path_args)),
                }
            )
        dir_kwargs[dirtype] = self.dirpath_formatter(**dirformatter_kwargs)
        # TODO Add update_dirpahts method where tne directory is rebuilt based on new kwargs passed.
        setattr(self, "_directories", Directories(**dir_kwargs))

    def _update_directories(self, dirtypes):
        for dirtype in dirtypes:
            self._set_directory(dirtype)

    def __repr__(self):
        """TODO DOCSTRING."""
        directories = {
            attr: getattr(
                self,
                attr.replace("_subdir", "_subdirectory")
                if attr.endswith("_subdir")
                else attr + "_directory",
            )
            for attr in self.directories._fields
        }
        return dedent(
            "".join(
                [
                    f"""
                    {attr}: {format_long_string(str(directory), 200)}""".rstrip()
                    for attr, directory in directories.items()
                ]
            )
        )
