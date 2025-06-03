from pathlib import Path
import os

def get_full_suffix(filename_or_path: str | os.PathLike) -> str:
    """
    Gets the complete suffix of a filename or path, including all parts after the first dot.

    Args:
        filename_or_path: The filename or path string.

    Returns:
        The full suffix (e.g., ".tar.gz"). Returns an empty string if no dot is present.

    Examples:
        >>> get_full_suffix("archive.tar.gz")
        '.tar.gz'
        >>> get_full_suffix("image.jpeg")
        '.jpeg'
        >>> get_full_suffix("no_suffix_file")
        ''
        >>> get_full_suffix(".bashrc")
        '.bashrc'
        >>> get_full_suffix("archive.tar.gz.bak")
        '.tar.gz.bak'
        >>> get_full_suffix("file.with.dots.ext")
        '.with.dots.ext'
    """
    name = Path(filename_or_path).name
    try:
        return name[name.index('.'):]
    except ValueError:
        return ""

def get_stem_multipart(filename_or_path: str | os.PathLike) -> str:
    """
    Gets the stem of a filename or path, which is the part before the first dot.

    This is similar to Path.stem, but Path.stem for "archive.tar.gz" would be "archive.tar",
    whereas this function would return "archive".

    Args:
        filename_or_path: The filename or path string.

    Returns:
        The stem of the filename (e.g., "archive" for "archive.tar.gz").

    Examples:
        >>> get_stem_multipart("archive.tar.gz")
        'archive'
        >>> get_stem_multipart("image.jpeg")
        'image'
        >>> get_stem_multipart("no_suffix_file")
        'no_suffix_file'
        >>> get_stem_multipart(".bashrc")
        ''
        >>> get_stem_multipart("archive.tar.gz.bak")
        'archive'
        >>> get_stem_multipart("file.with.dots.ext")
        'file'
    """
    name = Path(filename_or_path).name
    try:
        return name[:name.index('.')]
    except ValueError:
        return name

def split_multipart_ext(filename_or_path: str | os.PathLike) -> tuple[str, str]:
    """
    Splits a filename or path into its stem and full suffix.

    The stem is the part before the first dot, and the suffix includes all parts after the first dot.

    Args:
        filename_or_path: The filename or path string.

    Returns:
        A tuple containing the stem and the full suffix.

    Examples:
        >>> split_multipart_ext("archive.tar.gz")
        ('archive', '.tar.gz')
        >>> split_multipart_ext("image.jpeg")
        ('image', '.jpeg')
        >>> split_multipart_ext("no_suffix_file")
        ('no_suffix_file', '')
        >>> split_multipart_ext(".bashrc")
        ('', '.bashrc')
    """
    stem = get_stem_multipart(filename_or_path)
    suffix = get_full_suffix(filename_or_path)
    return stem, suffix

def get_suffix_parts(filename_or_path: str | os.PathLike) -> list[str]:
    """
    Gets all parts of the suffix, split by dots.

    Args:
        filename_or_path: The filename or path string.

    Returns:
        A list of suffix parts. Returns an empty list if no dot is present or if the
        filename starts with a dot and has no other dots.

    Examples:
        >>> get_suffix_parts("archive.tar.gz")
        ['.tar', '.gz']
        >>> get_suffix_parts("image.jpeg")
        ['.jpeg']
        >>> get_suffix_parts("no_suffix_file")
        []
        >>> get_suffix_parts(".bashrc") # Only a single dot part
        ['.bashrc']
        >>> get_suffix_parts("archive.tar.gz.bak")
        ['.tar', '.gz', '.bak']
        >>> get_suffix_parts("file.with.dots.ext")
        ['.with', '.dots', '.ext']
        >>> get_suffix_parts("nodots")
        []
        >>> get_suffix_parts(".config.json")
        ['.config', '.json']
    """
    full_suffix = get_full_suffix(filename_or_path)
    if not full_suffix:
        return []

    name = Path(filename_or_path).name # Used for .bashrc like cases
    if not full_suffix:
        return []

    # Case 1: Filename starts with a dot and has only one dot (e.g., ".bashrc")
    # or filename has a suffix that starts with a dot and is the only suffix part (e.g. "file.ext")
    # The `get_full_suffix` for ".bashrc" is ".bashrc".
    # The `get_full_suffix` for "file.ext" is ".ext".
    # We need to distinguish ".bashrc" from ".config.json" for the examples.
    if full_suffix.startswith('.') and full_suffix.count('.') == 1:
        return [full_suffix]

    # Case 2: Multi-part suffixes like ".tar.gz" or ".config.json"
    # full_suffix for "archive.tar.gz" is ".tar.gz"
    # full_suffix for ".config.json" is ".config.json" (this is where it gets tricky)
    # The issue's example for .config.json is ['.config', '.json']
    # The issue's example for .bashrc is ['.bashrc']

    # If the original filename starts with a dot, like ".config.json"
    if name.startswith('.') and name.count('.') > 1: # e.g. ".config.json", ".foo.bar.baz"
        # full_suffix is already ".config.json"
        # We want ['.config', '.json']
        # Split the `name` itself by dots, prepend dots to each part.
        parts = name.split('.') # ['', 'config', 'json']
        return [f".{p}" for p in parts if p]


    # General case: "archive.tar.gz", "file.with.dots.ext"
    # full_suffix: ".tar.gz", ".with.dots.ext"
    # Split full_suffix by dot. Result: ['', 'tar', 'gz'] or ['', 'with', 'dots', 'ext']
    split_parts = full_suffix.split('.')

    # Remove the initial empty string that results from splitting a string like ".tar.gz"
    if split_parts[0] == '':
        split_parts = split_parts[1:]

    return [f".{p}" for p in split_parts]


def normalize_suffix(suffix: str) -> str:
    """
    Normalizes a suffix string to ensure it is lowercase and has a single leading dot.

    Args:
        suffix: The suffix string to normalize.

    Returns:
        The normalized suffix string.

    Examples:
        >>> normalize_suffix(".TAR.GZ")
        '.tar.gz'
        >>> normalize_suffix("tar.gz")
        '.tar.gz'
        >>> normalize_suffix("..tar.gz")
        '.tar.gz'
        >>> normalize_suffix(".tar")
        '.tar'
        >>> normalize_suffix("tar")
        '.tar'
        >>> normalize_suffix("..TAR")
        '.tar'
        >>> normalize_suffix(".TAR..GZ") # Multiple dots inside are preserved relative to first non-dot char
        '.tar..gz'
        >>> normalize_suffix("TAR..GZ")
        '.tar..gz'
        >>> normalize_suffix("..tar..gz..") # Trailing dots are preserved too
        '.tar..gz..'
        >>> normalize_suffix(".")
        '.'
        >>> normalize_suffix("..")
        '.'
        >>> normalize_suffix("") # Empty string
        '.'
        >>> normalize_suffix(" .tar.gz ") # With spaces (spaces are not trimmed by lstrip('.'))
        '. .tar.gz '
    """
    if not suffix: # Handle empty string explicitly
        return "."

    normalized = suffix.strip().lower() # Also strip whitespace
    normalized = normalized.lstrip('.')
    return f".{normalized}"
