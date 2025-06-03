from typing import Iterable
import os # Required for os.PathLike type hint
import re # For regex matching
from multiext.parser import get_full_suffix, get_suffix_parts

def has_multipart_suffix(filename_or_path: str | os.PathLike) -> bool:
    """
    Checks if a filename or path has a multipart suffix (e.g., ".tar.gz").

    A multipart suffix is defined as a suffix containing more than one dot.
    Filenames like ".bashrc" are considered to have a single-part suffix.
    Filenames like ".config.json" are considered to have a multipart suffix.

    Args:
        filename_or_path: The filename or path string.

    Returns:
        True if the filename has a multipart suffix, False otherwise.

    Examples:
        >>> has_multipart_suffix("archive.tar.gz")
        True
        >>> has_multipart_suffix("image.jpeg")
        False
        >>> has_multipart_suffix("no_suffix_file")
        False
        >>> has_multipart_suffix(".bashrc") # Single part, even if it starts with dot
        False
        >>> has_multipart_suffix("archive.tar.gz.bak")
        True
        >>> has_multipart_suffix(".config.json") # Multipart
        True
    """
    suffix_parts = get_suffix_parts(filename_or_path)
    # A multipart suffix means more than one part in the list from get_suffix_parts
    # e.g. ".tar.gz" -> [".tar", ".gz"] (len 2)
    # e.g. ".jpeg" -> [".jpeg"] (len 1)
    # e.g. ".bashrc" -> [".bashrc"] (len 1)
    # e.g. ".config.json" -> [".config", ".json"] (len 2)
    return len(suffix_parts) > 1

def is_valid_multipart_suffix(
    filename_or_path: str | os.PathLike,
    valid_suffixes: Iterable[str] | str,
    case_sensitive: bool = False
) -> bool:
    """
    Validates if the full suffix of a filename matches any of the provided valid suffixes.

    This function compares the complete suffix (e.g., ".tar.gz") against a list of
    acceptable full suffixes. It can perform case-sensitive or case-insensitive
    comparisons and also supports regex matching for suffixes.

    Args:
        filename_or_path: The filename or path string.
        valid_suffixes: An iterable of valid full suffixes (e.g., {".tar.gz", ".zip"})
                          or a single suffix string (e.g., ".tar.gz").
                          Each suffix should include the leading dot.
                          Suffixes can be strings or regex patterns.
        case_sensitive: If True, the comparison is case-sensitive. Defaults to False.

    Returns:
        True if the filename's full suffix matches any of the valid_suffixes,
        respecting case_sensitive and regex rules. False otherwise.
        Also returns False if the filename has no suffix.

    Examples:
        >>> is_valid_multipart_suffix("archive.tar.gz", {".tar.gz", ".zip"})
        True
        >>> is_valid_multipart_suffix("archive.TAR.GZ", {".tar.gz", ".zip"}) # Case-insensitive by default
        True
        >>> is_valid_multipart_suffix("archive.TAR.GZ", {".tar.gz", ".zip"}, case_sensitive=True)
        False
        >>> is_valid_multipart_suffix("archive.tar.gz", ".tar.gz", case_sensitive=True)
        True
        >>> is_valid_multipart_suffix("image.jpeg", {".tar.gz", ".zip"})
        False
        >>> is_valid_multipart_suffix("archive.zip", ".zip") # Single suffix string
        True
        >>> is_valid_multipart_suffix("archive.zip", ".tar.gz")
        False
        >>> is_valid_multipart_suffix("no_suffix_file", {".tar.gz"})
        False
        >>> is_valid_multipart_suffix(".bashrc", {".bashrc", ".config"})
        True
        >>> is_valid_multipart_suffix("myfile.tar.zst", {".tar.zst", ".tar.gz"})
        True
        >>> is_valid_multipart_suffix("myfile.ZST", ".zst") # Validating against a simple suffix
        True
        >>> is_valid_multipart_suffix("myfile.zst", r".*\.zst$", case_sensitive=False) # Regex example
        True
        >>> is_valid_multipart_suffix("myfile.ZST", r".*\.zst$", case_sensitive=True) # Regex case-sensitive
        False
        >>> is_valid_multipart_suffix("myfile.ZST", r".*\.ZST$", case_sensitive=True) # Regex case-sensitive
        True
    """
    full_file_suffix = get_full_suffix(filename_or_path)

    if not full_file_suffix:
        return False

    suffixes_to_check = [valid_suffixes] if isinstance(valid_suffixes, str) else valid_suffixes

    for vs_item in suffixes_to_check:
        try:
            # Attempt to compile the suffix item as a regex
            # This is a simple way to check if it might be a regex.
            # More robust checking might be needed for complex scenarios.
            re.compile(vs_item)
            is_regex = True
        except re.error:
            is_regex = False

        if is_regex:
            flags = 0 if case_sensitive else re.IGNORECASE
            if re.fullmatch(vs_item, full_file_suffix, flags):
                return True
        else:
            # Plain string comparison
            s_to_compare = full_file_suffix
            vs_to_compare = vs_item
            if not case_sensitive:
                s_to_compare = full_file_suffix.lower()
                vs_to_compare = vs_item.lower()

            if s_to_compare == vs_to_compare:
                return True

    return False
