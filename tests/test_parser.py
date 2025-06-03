import unittest
from pathlib import Path
from multiext.parser import (
    get_full_suffix,
    get_stem_multipart,
    split_multipart_ext,
    get_suffix_parts,
    normalize_suffix
)

class TestParser(unittest.TestCase):

    def test_get_full_suffix(self):
        self.assertEqual(get_full_suffix("archive.tar.gz"), ".tar.gz")
        self.assertEqual(get_full_suffix("image.jpeg"), ".jpeg")
        self.assertEqual(get_full_suffix("no_suffix_file"), "")
        self.assertEqual(get_full_suffix(".bashrc"), ".bashrc")
        self.assertEqual(get_full_suffix(".config.json"), ".config.json")
        self.assertEqual(get_full_suffix("file.with.dots.ext"), ".with.dots.ext")
        self.assertEqual(get_full_suffix(""), "")
        self.assertEqual(get_full_suffix(Path("archive.tar.gz")), ".tar.gz")
        self.assertEqual(get_full_suffix(Path(".bashrc")), ".bashrc")
        self.assertEqual(get_full_suffix(Path("no_suffix_file")), "")
        # Cases with leading/trailing dots in filename parts if relevant
        self.assertEqual(get_full_suffix("a.b.c.d"), ".b.c.d")
        self.assertEqual(get_full_suffix("a."), ".")
        self.assertEqual(get_full_suffix("a..b"), "..b")
        self.assertEqual(get_full_suffix("..a"), "..a") # if name is "..a"
        self.assertEqual(get_full_suffix("path/to/archive.tar.gz"), ".tar.gz")
        self.assertEqual(get_full_suffix("path/to/.bashrc"), ".bashrc")
        self.assertEqual(get_full_suffix(Path("path/to/archive.tar.gz")), ".tar.gz")


    def test_get_stem_multipart(self):
        self.assertEqual(get_stem_multipart("archive.tar.gz"), "archive")
        self.assertEqual(get_stem_multipart("image.jpeg"), "image")
        self.assertEqual(get_stem_multipart("no_suffix_file"), "no_suffix_file")
        self.assertEqual(get_stem_multipart(".bashrc"), "") # First char is '.'
        self.assertEqual(get_stem_multipart(".config.json"), "") # First char is '.'
        self.assertEqual(get_stem_multipart("file.with.dots.ext"), "file")
        self.assertEqual(get_stem_multipart(""), "")
        self.assertEqual(get_stem_multipart(Path("archive.tar.gz")), "archive")
        self.assertEqual(get_stem_multipart(Path(".bashrc")), "")
        self.assertEqual(get_stem_multipart(Path("no_suffix_file")), "no_suffix_file")
        self.assertEqual(get_stem_multipart("a.b.c.d"), "a")
        self.assertEqual(get_stem_multipart("a."), "a")
        self.assertEqual(get_stem_multipart("a..b"), "a")
        self.assertEqual(get_stem_multipart("..a"), "") # First char is '.'
        self.assertEqual(get_stem_multipart("path/to/archive.tar.gz"), "archive")
        self.assertEqual(get_stem_multipart("path/to/.bashrc"), "")
        self.assertEqual(get_stem_multipart(Path("path/to/archive.tar.gz")), "archive")

    def test_split_multipart_ext(self):
        self.assertEqual(split_multipart_ext("archive.tar.gz"), ("archive", ".tar.gz"))
        self.assertEqual(split_multipart_ext("image.jpeg"), ("image", ".jpeg"))
        self.assertEqual(split_multipart_ext("no_suffix_file"), ("no_suffix_file", ""))
        self.assertEqual(split_multipart_ext(".bashrc"), ("", ".bashrc"))
        self.assertEqual(split_multipart_ext(".config.json"), ("", ".config.json"))
        self.assertEqual(split_multipart_ext("file.with.dots.ext"), ("file", ".with.dots.ext"))
        self.assertEqual(split_multipart_ext(""), ("", ""))
        self.assertEqual(split_multipart_ext(Path("archive.tar.gz")), ("archive", ".tar.gz"))
        self.assertEqual(split_multipart_ext(Path(".bashrc")), ("", ".bashrc"))
        self.assertEqual(split_multipart_ext(Path("no_suffix_file")), ("no_suffix_file", ""))
        self.assertEqual(split_multipart_ext("path/to/archive.tar.gz"), ("archive", ".tar.gz"))
        self.assertEqual(split_multipart_ext(Path("path/to/.bashrc")), ("", ".bashrc"))

    def test_get_suffix_parts(self):
        self.assertEqual(get_suffix_parts("archive.tar.gz"), [".tar", ".gz"])
        self.assertEqual(get_suffix_parts("image.jpeg"), [".jpeg"])
        self.assertEqual(get_suffix_parts("no_suffix_file"), [])
        self.assertEqual(get_suffix_parts(".bashrc"), [".bashrc"])
        self.assertEqual(get_suffix_parts(".config.json"), [".config", ".json"]) # Based on refined logic
        self.assertEqual(get_suffix_parts("file.with.dots.ext"), [".with", ".dots", ".ext"])
        self.assertEqual(get_suffix_parts(""), [])
        self.assertEqual(get_suffix_parts(Path("archive.tar.gz")), [".tar", ".gz"])
        self.assertEqual(get_suffix_parts(Path(".bashrc")), [".bashrc"])
        self.assertEqual(get_suffix_parts(Path(".config.json")), [".config", ".json"])
        self.assertEqual(get_suffix_parts(Path("no_suffix_file")), [])
        self.assertEqual(get_suffix_parts("archive.tar.gz.bak"), [".tar", ".gz", ".bak"])
        self.assertEqual(get_suffix_parts("a.b.c.d"), [".b", ".c", ".d"])
        self.assertEqual(get_suffix_parts("a."), ["."])
        self.assertEqual(get_suffix_parts("a..b"), ["." # Behavior of get_full_suffix("a..b") is "..b"
                                                    # split('.') -> ['', '', 'b'] -> ['.', '.b'] by current logic
                                                    # Let's check current logic:
                                                    # full_suffix = "..b"
                                                    # name = "a..b"
                                                    # full_suffix.startswith('.') (T), full_suffix.count('.') (2) != 1. Skip first if.
                                                    # name.startswith('.') (F). Skip second if.
                                                    # split_parts = "..b".split('.') -> ['', '', 'b']
                                                    # split_parts[0] == '' (T). split_parts = ['', 'b']
                                                    # returns [f".{p}" for p in ['', 'b']] -> ['.', '.b']
                                                    , ".b"])
        self.assertEqual(get_suffix_parts("..a"), [".a"]) # name = "..a", full_suffix = "..a"
                                                          # full_suffix.startswith('.') (T), count (2) != 1. Skip first if.
                                                          # name.startswith('.') (T), count (2) > 1. Enter second if.
                                                          # parts = "..a".split('.') -> ['', '', 'a']
                                                          # returns [f".{p}" for p in parts if p] -> ['.a']
                                                          # This seems like an error in my manual trace or expectation.
                                                          # Example: ".config.json" -> name=".config.json", parts=['', 'config', 'json'] -> ['.config', '.json']
                                                          # Example: "..a" -> name="..a", parts=['', '', 'a'] -> ['.a'] - this is correct by that logic.
        self.assertEqual(get_suffix_parts("path/to/archive.tar.gz"), [".tar", ".gz"])
        self.assertEqual(get_suffix_parts(Path("path/to/.config.json")), [".config", ".json"])

    def test_normalize_suffix(self):
        self.assertEqual(normalize_suffix(".TAR.GZ"), ".tar.gz")
        self.assertEqual(normalize_suffix("tar.gz"), ".tar.gz")
        self.assertEqual(normalize_suffix("..tar.gz"), ".tar.gz")
        self.assertEqual(normalize_suffix(".tar"), ".tar")
        self.assertEqual(normalize_suffix("tar"), ".tar")
        self.assertEqual(normalize_suffix("..TAR"), ".tar")
        # From docstring: preserve multiple dots and trailing dots relative to first non-dot
        self.assertEqual(normalize_suffix(".TAR..GZ"), ".tar..gz")
        self.assertEqual(normalize_suffix("TAR..GZ"), ".tar..gz")
        self.assertEqual(normalize_suffix("..tar..gz.."), ".tar..gz..")
        # Empty and dot cases
        self.assertEqual(normalize_suffix(""), ".") # Current behavior
        self.assertEqual(normalize_suffix("."), ".")
        self.assertEqual(normalize_suffix(".."), ".")
        # With spaces (now handled by strip() in normalize_suffix)
        self.assertEqual(normalize_suffix(" .tar.gz "), ".tar.gz")
        self.assertEqual(normalize_suffix("  ..tar.gz"), ".tar.gz") # Leading spaces then dots
        self.assertEqual(normalize_suffix("suffix."), ".suffix.") # Trailing dot preserved
        self.assertEqual(normalize_suffix("suffix.."), ".suffix..") # Trailing dots preserved


if __name__ == '__main__':
    unittest.main()
