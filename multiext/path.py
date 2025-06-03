import pathlib # Import the whole module to access _flavour
import os # For os.name
from typing import Type, TypeVar
import sys

from .parser import get_full_suffix, get_stem_multipart, split_multipart_ext
from .manipulation import replace_multipart_suffix as replace_multipart_suffix_func

_P = TypeVar("_P", bound="MultiExtPath")


class MultiExtPath(pathlib.Path):
    """
    A pathlib.Path subclass providing enhanced functionality for multipart extensions.
    """
    
    # Set the appropriate _flavour for the current OS
    this_python = sys.version_info[:2]
    if this_python < (3,12):
        _flavour = pathlib._windows_flavour if os.name == 'nt' else pathlib._posix_flavour
    
    
    def __new__(cls: Type[_P], *args, **kwargs) -> _P:
        """
        Constructs a new MultiExtPath instance. Ensures that methods returning
        new path objects (like parent or joinpath) still return MultiExtPath instances.
        """
        return super().__new__(cls, *args, **kwargs)

    @property
    def full_suffix(self) -> str:
        """
        The full suffix of the path, including all parts after the first dot.
        For example, for "archive.tar.gz", it returns ".tar.gz".
        """
        return get_full_suffix(self.name)

    @property
    def stem_multipart(self) -> str:
        """
        The multipart stem of the path, which is the part before the first dot.
        For example, for "archive.tar.gz", it returns "archive".
        """
        return get_stem_multipart(self.name)

    def replace_multipart_suffix(self: _P, new_suffix: str) -> _P:
        """
        Replaces the full multipart suffix of the path with a new one.

        Args:
            new_suffix: The new suffix (e.g., ".zip", ".tar.bz2").
                        It should include the leading dot.

        Returns:
            A new MultiExtPath instance with the replaced suffix.

        Examples:
            >>> p = MultiExtPath("archive.tar.gz")
            >>> p.replace_multipart_suffix(".zip")
            MultiExtPath('archive.zip')
            >>> p = MultiExtPath("document") # No suffix
            >>> p.replace_multipart_suffix(".txt")
            MultiExtPath('document.txt')
            >>> p = MultiExtPath(".bashrc") # Hidden file with single part suffix
            >>> p.replace_multipart_suffix(".sh") # stem_multipart is '', full_suffix is '.bashrc'
            MultiExtPath('.sh')
            >>> MultiExtPath("archive.tar.gz").replace_multipart_suffix(".zip").name
            'archive.zip'
            >>> MultiExtPath("file.old.ext").replace_multipart_suffix(".new")
            MultiExtPath('file.new')
        """
        # The replace_multipart_suffix_func from manipulation is expected to handle
        # the actual logic of finding the stem and joining the new suffix.
        # It should return a string representing the new filename.
        new_name = replace_multipart_suffix_func(self.name, new_suffix)

        # Construct the new path using the original path's parent
        # and the new name.
        return self.__class__(self.parent, new_name)

    # To ensure that methods like `with_name`, `with_suffix` (from Path)
    # still return MultiExtPath, we might need to override them if they don't
    # preserve the type correctly by default when __new__ is defined as above.
    # pathlib.Path's methods like `with_name` and `with_suffix` are implemented
    # using `self.__class__(...)` so they should correctly return MultiExtPath.

    # Example of how to ensure doctests can find the class
    # This is a common pattern for doctests in classes.
    # We need to be able to refer to MultiExtPath within the doctests.
    # One way is to ensure it's in the globals() for the doctest execution.
    # For now, the example `MultiExtPath('archive.zip')` in the docstring
    # might require the test runner to correctly set up the environment
    # or we might need to adjust how tests are run or written.

    # Let's add a simple __str__ and __repr__ for clarity, though Path provides them.
    # No, Path's __repr__ is good, it shows the class name.
    # For example: PosixPath('archive.tar.gz')
    # Our __new__ should ensure it becomes MultiExtPath('archive.tar.gz')
    # Let's test this with a doctest.
    """
    Examples for __new__ and basic Path operations:
        >>> MultiExtPath("/tmp/some.file.tar.gz").name
        'some.file.tar.gz'
        >>> isinstance(MultiExtPath("."), MultiExtPath)
        True
        >>> isinstance(MultiExtPath(".").parent, MultiExtPath) # Parent should also be MultiExtPath
        True
        >>> MultiExtPath("a/b.txt").parent.name # Simplified to avoid resolve()
        'a'
        >>> MultiExtPath("/a/b/c.txt").parent == MultiExtPath("/a/b")
        True
    """
# Doctests should be run using 'python -m doctest multiext/path.py' from the package root.
