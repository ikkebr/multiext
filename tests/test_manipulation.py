import unittest
from pathlib import Path
from multiext.manipulation import (
    replace_multipart_suffix,
    add_suffix_part,
    remove_last_suffix_part
)

class TestManipulation(unittest.TestCase):

    def test_replace_multipart_suffix(self):
        self.assertEqual(replace_multipart_suffix("archive.tar.gz", ".zip"), "archive.zip")
        self.assertEqual(replace_multipart_suffix("image.jpeg", ".png"), "image.png")
        self.assertEqual(replace_multipart_suffix("no_suffix_file", ".txt"), "no_suffix_file.txt")
        self.assertEqual(replace_multipart_suffix(".bashrc", ".sh"), ".sh") # Stem is '', new_suffix is '.sh'
        self.assertEqual(replace_multipart_suffix(".config.json", ".yml"), ".yml") # Stem is '', new_suffix is '.yml'
        self.assertEqual(replace_multipart_suffix("archive.tar.gz", ""), "archive")
        self.assertEqual(replace_multipart_suffix("image.jpeg", ""), "image")
        self.assertEqual(replace_multipart_suffix("no_suffix_file", ""), "no_suffix_file")
        self.assertEqual(replace_multipart_suffix(".bashrc", ""), "")

        self.assertEqual(replace_multipart_suffix("archive.tar.gz", "zip"), "archive.zip") # Auto-prefix dot
        self.assertEqual(replace_multipart_suffix("image.jpeg", "png"), "image.png") # Auto-prefix dot

        self.assertEqual(replace_multipart_suffix("path/to/archive.tar.gz", ".zip"), str(Path("path/to/archive.zip")))
        self.assertEqual(replace_multipart_suffix(Path("path/to/archive.tar.gz"), ".zip"), str(Path("path/to/archive.zip")))

        self.assertEqual(replace_multipart_suffix("", ".txt"), ".txt") # Stem is '', new_suffix is '.txt'
        self.assertEqual(replace_multipart_suffix("", ""), "")
        self.assertEqual(replace_multipart_suffix(Path(""), ".txt"), ".txt")

        # Test with Path object inputs
        self.assertEqual(replace_multipart_suffix(Path("archive.tar.gz"), ".zip"), "archive.zip")
        self.assertEqual(replace_multipart_suffix(Path(".bashrc"), ".sh"), ".sh")

    def test_add_suffix_part(self):
        self.assertEqual(add_suffix_part("archive.tar", ".gz"), "archive.tar.gz")
        self.assertEqual(add_suffix_part("image", ".jpeg"), "image.jpeg")
        self.assertEqual(add_suffix_part("image.jpeg", ".bak"), "image.jpeg.bak")
        self.assertEqual(add_suffix_part("image.jpeg", "bak"), "image.jpeg.bak") # Auto-prefix dot
        self.assertEqual(add_suffix_part(".bashrc", ".bak"), ".bashrc.bak")
        self.assertEqual(add_suffix_part("file.config", "user"), "file.config.user")

        self.assertEqual(add_suffix_part("path/to/file.config", ".user"), str(Path("path/to/file.config.user")))
        self.assertEqual(add_suffix_part(Path("path/to/file.config"), ".user"), str(Path("path/to/file.config.user")))

        self.assertEqual(add_suffix_part("archive.tar", ""), "archive.tar") # Add empty part
        self.assertEqual(add_suffix_part("", ".txt"), ".txt") # Empty filename
        self.assertEqual(add_suffix_part(Path(""), ".txt"), "..txt") # Path("") is Path("."), name is ".". Result is "..txt"
        self.assertEqual(add_suffix_part("file", ""), "file")

        # Test with Path object inputs
        self.assertEqual(add_suffix_part(Path("archive.tar"), ".gz"), "archive.tar.gz")
        self.assertEqual(add_suffix_part(Path(".bashrc"), "bak"), ".bashrc.bak")

    def test_remove_last_suffix_part(self):
        self.assertEqual(remove_last_suffix_part("archive.tar.gz"), "archive.tar")
        self.assertEqual(remove_last_suffix_part("image.jpeg"), "image")
        self.assertEqual(remove_last_suffix_part("no_suffix_file"), "no_suffix_file")
        self.assertEqual(remove_last_suffix_part(".bashrc"), "")
        self.assertEqual(remove_last_suffix_part(".config.json"), ".config") # get_suffix_parts is ['.config', '.json'] -> join [:-1] is '.config', stem is ''

        self.assertEqual(remove_last_suffix_part("path/to/.bashrc"), "path/to") # Parent dir stringified
        self.assertEqual(remove_last_suffix_part("path/to/archive.tar.gz"), str(Path("path/to/archive.tar")))
        self.assertEqual(remove_last_suffix_part(Path("path/to/archive.tar.gz")), str(Path("path/to/archive.tar")))

        self.assertEqual(remove_last_suffix_part(""), "")
        self.assertEqual(remove_last_suffix_part(Path("")), "")
        self.assertEqual(remove_last_suffix_part("path/to/"), str(Path("path/to/"))) # Name is empty

        self.assertEqual(remove_last_suffix_part("a.b.c"), "a.b")
        self.assertEqual(remove_last_suffix_part("a.b"), "a")
        self.assertEqual(remove_last_suffix_part("a"), "a")
        self.assertEqual(remove_last_suffix_part(".a.b.c"), ".a.b") # stem="", parts=['.a','.b','.c'] -> .a.b
        self.assertEqual(remove_last_suffix_part(".a.b"), ".a")   # stem="", parts=['.a','.b'] -> .a
        self.assertEqual(remove_last_suffix_part(".a"), "")     # stem="", parts=['.a'] -> ""

        # Test with Path object inputs
        self.assertEqual(remove_last_suffix_part(Path("archive.tar.gz")), "archive.tar")
        self.assertEqual(remove_last_suffix_part(Path(".bashrc")), "")


if __name__ == '__main__':
    unittest.main()
