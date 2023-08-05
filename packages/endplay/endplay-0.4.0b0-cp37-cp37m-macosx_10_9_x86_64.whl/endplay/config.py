﻿"""
Configuration and versioning information
"""

# Packages metadata, used by setuptools etc
__version__ = """0.4.0-beta""".strip()
__version_info__ = tuple(int(i) if i.isdigit() else i for i in __version__.replace("-", ".").split("."))
__author__ = "Dominic Price"

# Configurable variables which control how the library functions
use_unicode = True # If set to False, the library will only print characters in the ASCII range
