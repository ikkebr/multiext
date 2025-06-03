"""
MultiExt: A Python library for manipulating multipart file extensions.
"""

from .parser import (
    get_full_suffix,
    get_stem_multipart,
    split_multipart_ext,
    get_suffix_parts,
    normalize_suffix
)
from .validation import (
    is_valid_multipart_suffix,
    has_multipart_suffix
)
from .manipulation import (
    replace_multipart_suffix,
    add_suffix_part,
    remove_last_suffix_part
)
from .path import MultiExtPath

__all__ = [
    # from parser
    "get_full_suffix",
    "get_stem_multipart",
    "split_multipart_ext",
    "get_suffix_parts",
    "normalize_suffix",
    # from validation
    "is_valid_multipart_suffix",
    "has_multipart_suffix",
    # from manipulation
    "replace_multipart_suffix",
    "add_suffix_part",
    "remove_last_suffix_part",
    # from path
    "MultiExtPath",
]

__version__ = "0.1.0" # Placeholder for versioning
