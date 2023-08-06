"""Module for various helper functions and other utilities."""
import importlib
from pathlib import Path
from textwrap import dedent


DEFAULT_DEP_NAME_MAP = {
    "cobra": "COBRApy",
    "mass_manager": "MASS-manager",
    "mass": "MASSpy",
}


def show_mass_dependencies(deps=None):
    """Print the versions of MASS dependencies."""

    if deps is None:
        deps = list(DEFAULT_DEP_NAME_MAP)
        dep_name_map = DEFAULT_DEP_NAME_MAP
    elif isinstance(deps, dict):
        dep_name_map = deps
        deps = list(deps)
    elif not hasattr(deps, "__iter__"):
        deps = [deps]
        dep_name_map = deps
    else:
        raise TypeError("`deps` must be an iterable or a dict")
    longest_str = len(max(dep_name_map.values(), key=len))
    version_str = ""
    for dep in deps:
        try:
            version = f"""{importlib.import_module(dep).__version__}"""
        except ImportError:
            version = "None"
        name = dep_name_map.get(dep, dep)
        name = " " * (longest_str - len(name)) + name
        version_str += f"""{": ".join((name, version))}""" + "\n"
    print(version_str.rstrip())


def conditional_dedent_item(attr, item):
    """Utility method to make conditionals when textwrapping."""
    return dedent(
        f"""
        {"" if not bool(item) else ": ".join((attr, item))}
        """.rstrip()
    )


def make_filename(name, filetype):
    """TODO DOCSTRING."""
    return Path(".".join((str(name), filetype)))


def make_full_filename(directory, name, filetype):
    """TODO DOCSTRING."""
    return directory.joinpath(make_filename(name, filetype))
