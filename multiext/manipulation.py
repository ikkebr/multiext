import os
from pathlib import Path
from multiext.parser import get_stem_multipart, get_suffix_parts

def replace_multipart_suffix(
    filename_or_path: str | os.PathLike,
    new_suffix: str
) -> str:
    """
    Replaces the existing multipart suffix of a filename or path with a new suffix.

    The stem is determined by `get_stem_multipart`. The new suffix should include
    a leading dot if one is desired (e.g., ".new.ext" or ".ext").

    Args:
        filename_or_path: The filename or path string (e.g., "archive.tar.gz").
        new_suffix: The new suffix to apply (e.g., ".zip" or ".tar.bz2").
                    If an empty string, the suffix is effectively removed.
                    If no leading dot is provided, it will be added if new_suffix is not empty.

    Returns:
        The filename or path with the suffix replaced. Preserves the original path structure.

    Examples:
        >>> replace_multipart_suffix("archive.tar.gz", ".zip")
        'archive.zip'
        >>> replace_multipart_suffix("image.jpeg", ".png")
        'image.png'
        >>> replace_multipart_suffix("no_suffix_file", ".txt")
        'no_suffix_file.txt'
        >>> replace_multipart_suffix(".bashrc", ".sh")
        '.sh'
        >>> replace_multipart_suffix("data.multi.part.ext", ".new")
        'data.new'
        >>> replace_multipart_suffix("path/to/archive.tar.gz", ".zip")
        'path/to/archive.zip'
        >>> replace_multipart_suffix("archive.tar.gz", "") # Remove suffix
        'archive'
        >>> replace_multipart_suffix("archive.tar.gz", "zip") # Auto-prefix dot
        'archive.zip'
    """
    # Handle empty or "." filename_or_path explicitly to avoid Path(".").with_name() quirks if they cause issues
    # and to ensure predictable behavior like ("","foo") -> ".foo"
    if filename_or_path == "" or str(filename_or_path) == ".":
        if not new_suffix:
            return "" # Remove suffix from "" or "." is ""
        if not new_suffix.startswith('.'):
            return f".{new_suffix}"
        return new_suffix

    p = Path(filename_or_path)
    stem = get_stem_multipart(p.name)

    if not new_suffix:
        new_name = stem
    elif not new_suffix.startswith('.'):
        new_name = f"{stem}.{new_suffix}"
    else:
        new_name = f"{stem}{new_suffix}"

    if filename_or_path == "" or filename_or_path == ".": # Handle cases where input is effectively no filename
        if new_name == "": return ""
        # If new_name is just a suffix (e.g. ".txt"), pathlib handles Path(".").with_name(".txt") fine.
        # However, if stem was empty (as it is for "" or "."), new_name is just new_suffix (or new_suffix with a dot).
        # So, effectively, if original is "" or ".", result is new_suffix (normalized).
        # The existing new_name calculation: stem is "". new_name becomes new_suffix (possibly with added dot).
        # This is simple: if input is "" or ".", the result is new_name.
        # Path(".").with_name(".foo") is ".foo". Path(".").with_name("foo") is "foo".
        # This seems fine. The issue is if new_name itself is empty.
        if new_name == "": return "" # Already handled by below, but for clarity.

    if new_name == "":
        # If new_name is empty, it implies the stem was empty and new_suffix was empty.
        # This means an operation like replace_suffix(".bashrc", "")
        return ""
    return str(p.with_name(new_name))

def add_suffix_part(
    filename_or_path: str | os.PathLike,
    suffix_part_to_add: str
) -> str:
    """
    Adds a new part to the existing suffix of a filename or path.

    If the filename has no suffix, the new part becomes the suffix.
    The part to add should include a leading dot (e.g., ".ext"). If not provided,
    a dot will be prepended.

    Args:
        filename_or_path: The filename or path string (e.g., "archive.tar").
        suffix_part_to_add: The suffix part to add (e.g., ".gz").

    Returns:
        The filename or path with the new suffix part appended.

    Examples:
        >>> add_suffix_part("archive.tar", ".gz")
        'archive.tar.gz'
        >>> add_suffix_part("image", ".jpeg")
        'image.jpeg'
        >>> add_suffix_part("image.jpeg", "bak") # Auto-prefix dot
        'image.jpeg.bak'
        >>> add_suffix_part("no_suffix_file", ".old")
        'no_suffix_file.old'
        >>> add_suffix_part(".bashrc", ".bak")
        '.bashrc.bak'
        >>> add_suffix_part("path/to/file.config", "user")
        'path/to/file.config.user'
    """
    p = Path(filename_or_path)
    original_name = p.name

    if not suffix_part_to_add:
        return str(filename_or_path) # No change if part is empty

    # Handle empty or "." filename_or_path explicitly
    if filename_or_path == "" or str(filename_or_path) == ".":
        if not suffix_part_to_add: # Adding empty part to "" or "."
             return str(filename_or_path) # Return original "" or "."
        _norm_part = suffix_part_to_add if suffix_part_to_add.startswith('.') else f".{suffix_part_to_add}"
        if filename_or_path == "": return _norm_part # "" + ".txt" -> ".txt"
        if str(filename_or_path) == ".": return f".{_norm_part}" # "." + ".txt" -> "..txt" (as Path(".").name is ".")
                                                                # This is consistent with p.name + part if p = Path(".")

    p = Path(filename_or_path) # Moved down
    original_name = p.name   # Moved down

    if not suffix_part_to_add.startswith('.'):
        part_to_add_with_dot = f".{suffix_part_to_add}"
    else:
        part_to_add_with_dot = suffix_part_to_add

    new_name = f"{original_name}{part_to_add_with_dot}"
    return str(p.with_name(new_name))

def remove_last_suffix_part(filename_or_path: str | os.PathLike) -> str:
    """
    Removes the last part of a multipart suffix from a filename or path.

    If the filename has a single-part suffix (e.g., ".jpeg"), it removes that suffix.
    If the filename has no suffix, it returns the original filename unchanged.
    If the filename is like ".bashrc" (starts with dot, one suffix part), it removes the suffix,
    resulting in an empty string for the name part if not in a path.

    Args:
        filename_or_path: The filename or path string.

    Returns:
        The filename or path with the last suffix part removed.

    Examples:
        >>> remove_last_suffix_part("archive.tar.gz")
        'archive.tar'
        >>> remove_last_suffix_part("image.jpeg")
        'image'
        >>> remove_last_suffix_part("no_suffix_file")
        'no_suffix_file'
        >>> remove_last_suffix_part(".bashrc") # Path(".bashrc").with_suffix('') would be ""
        ''
        >>> remove_last_suffix_part("path/to/.bashrc")
        'path/to/'
        >>> remove_last_suffix_part("archive.tar.gz.bak")
        'archive.tar.gz'
        >>> remove_last_suffix_part("file.ext")
        'file'
        >>> remove_last_suffix_part("path/to/file.ext")
        'path/to/file'
        >>> remove_last_suffix_part("") # Explicit test for empty string
        ''
        >>> remove_last_suffix_part(Path("")) # Explicit test for Path("")
        ''
    """
    # Handle empty string or Path(".") explicitly at the beginning
    if filename_or_path == "" or (isinstance(filename_or_path, Path) and str(filename_or_path) == "."):
        return ""

    p = Path(filename_or_path)
    name = p.name

    if not name: # Handles cases like "path/to/"
        return str(p)

    suffix_parts = get_suffix_parts(name)

    if not suffix_parts: # No suffix to remove
        return str(p)

    if len(suffix_parts) == 1:
        # This is like '.jpeg' or '.bashrc'
        # For '.bashrc', stem is '', full_suffix is '.bashrc'
        # For 'image.jpeg', stem is 'image', full_suffix is '.jpeg'
        stem = get_stem_multipart(name)
        new_name = stem
    else:
        # Multipart suffix like ['.tar', '.gz']
        # We want to remove the last part, so reconstruct with parts[:-1]
        # Full original stem + all but last suffix part
        stem = get_stem_multipart(name)
        new_suffix = "".join(suffix_parts[:-1])
        new_name = f"{stem}{new_suffix}"

    if new_name == "":
        # If the original name (p.name) was not empty, but new_name is,
        # it means we removed the entire name (e.g. ".bashrc" -> "").
        # If there's a parent path, with_name("") would correctly give parent path.
        # But we want to return "" as the name part.
            if not name: # Original name was empty (e.g. path was "/"), new_name is also empty
                return str(p) # Return original "/"
            # Original name was not empty (e.g. ".bashrc" or "foo/.bashrc")
            if p.parent != Path("."): # Has a real parent (e.g. "foo/.bashrc")
                return str(p.parent) # Return "foo/"
            else: # Parent is "." (e.g. ".bashrc")
                return "" # Return "" for the name part
    return str(p.with_name(new_name)) # Only reached if new_name is not empty
