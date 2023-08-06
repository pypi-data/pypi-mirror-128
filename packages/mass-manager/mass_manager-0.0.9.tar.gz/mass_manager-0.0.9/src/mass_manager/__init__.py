import re
from pathlib import Path

from mass_manager.mass_manager import MassManager
from mass_manager.util import Directories, DirPathFormatter, show_mass_dependencies


_BASE_DIR = Path(__file__).resolve().parent.parent.parent

__version__ = "0.0.9"
