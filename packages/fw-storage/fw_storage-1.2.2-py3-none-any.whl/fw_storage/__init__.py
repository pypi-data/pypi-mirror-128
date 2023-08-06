"""Flywheel storage library."""
import importlib.metadata as importlib_metadata

from .errors import *
from .storage import Storage, get_storage

__all__ = [
    "FileExists",
    "FileNotFound",
    "IsADirectory",
    "NotADirectory",
    "PermError",
    "Storage",
    "StorageError",
    "get_storage",
]
__version__ = importlib_metadata.version(__name__)
