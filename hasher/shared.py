"""
This module contains all the shared code, constants for hasher package.
"""
import hashlib
from . import __version__

SUPPORTED_HASH = hashlib.algorithms_available
PROG_NAME = "hasher"
VERSION = __version__

