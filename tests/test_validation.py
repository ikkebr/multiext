import unittest
from pathlib import Path
from multiext.validation import has_multipart_suffix, is_valid_multipart_suffix

class TestValidation(unittest.TestCase):

    def test_has_multipart_suffix(self):
        # True cases
        self.assertTrue(has_multipart_suffix("archive.tar.gz"))
        self.assertTrue(has_multipart_suffix(".config.json")) # ['.config', '.json']
        self.assertTrue(has_multipart_suffix("file.tar.gz.bak")) # ['.tar', '.gz', '.bak']
        self.assertTrue(has_multipart_suffix("path/to/archive.tar.gz"))
        self.assertTrue(has_multipart_suffix(Path("archive.tar.gz")))
        self.assertTrue(has_multipart_suffix(Path(".config.json")))

        # False cases
        self.assertFalse(has_multipart_suffix("image.jpeg")) # ['.jpeg']
        self.assertFalse(has_multipart_suffix("no_suffix_file")) # []
        self.assertFalse(has_multipart_suffix(".bashrc")) # ['.bashrc']
        self.assertFalse(has_multipart_suffix("")) # []
        self.assertFalse(has_multipart_suffix("file")) # []
        self.assertFalse(has_multipart_suffix(Path("image.jpeg")))
        self.assertFalse(has_multipart_suffix(Path(".bashrc")))
        self.assertFalse(has_multipart_suffix(Path("no_suffix_file")))
        self.assertFalse(has_multipart_suffix("path/to/image.jpeg"))
        self.assertFalse(has_multipart_suffix(".")) # No suffix parts
        self.assertFalse(has_multipart_suffix("..")) # No suffix parts
        self.assertFalse(has_multipart_suffix("...")) # No suffix parts, get_full_suffix is "..."
                                                      # get_suffix_parts for "..." -> full_suffix = "..."
                                                      # name = "...", full_suffix.count('.') = 3. Skip first if.
                                                      # name.startswith('.') T, name.count('.')=3 > 1. Enter second if.
                                                      # parts = name.split('.') -> ['', '', '', '']
                                                      # return [f".{p}" for p in parts if p] -> []
                                                      # So len is 0. Correct.


    def test_is_valid_multipart_suffix(self):
        valid_set = {".tar.gz", ".zip", ".tar.bz2"}
        valid_list = [".tar.gz", ".zip", ".tar.bz2"]

        # Valid cases with list/set
        self.assertTrue(is_valid_multipart_suffix("data.tar.gz", valid_set))
        self.assertTrue(is_valid_multipart_suffix("archive.zip", valid_list))
        self.assertTrue(is_valid_multipart_suffix(Path("data.tar.gz"), valid_set))

        # Valid cases with single string
        self.assertTrue(is_valid_multipart_suffix("archive.zip", ".zip"))
        self.assertTrue(is_valid_multipart_suffix(Path("archive.zip"), ".zip"))

        # Case-insensitivity for filename
        self.assertTrue(is_valid_multipart_suffix("data.TAR.GZ", valid_set))
        self.assertTrue(is_valid_multipart_suffix("ARCHIVE.ZIP", ".zip"))

        # Case-insensitivity for valid_suffixes
        self.assertTrue(is_valid_multipart_suffix("data.tar.gz", {".TAR.GZ", ".ZIP"}))
        self.assertTrue(is_valid_multipart_suffix("archive.zip", ".ZIP"))

        # Invalid cases
        self.assertFalse(is_valid_multipart_suffix("image.jpeg", valid_set))
        self.assertFalse(is_valid_multipart_suffix("archive.rar", ".zip"))
        self.assertFalse(is_valid_multipart_suffix("no_suffix_file", valid_set)) # No suffix
        self.assertFalse(is_valid_multipart_suffix(Path("image.jpeg"), valid_set))

        # Empty filename
        self.assertFalse(is_valid_multipart_suffix("", valid_set))
        self.assertFalse(is_valid_multipart_suffix("", ".zip"))

        # Empty valid_suffixes (set/list)
        self.assertFalse(is_valid_multipart_suffix("data.tar.gz", []))
        self.assertFalse(is_valid_multipart_suffix("data.tar.gz", set()))

        # Empty valid_suffixes (string) - note: an empty string suffix is not typically valid
        self.assertFalse(is_valid_multipart_suffix("data.tar.gz", ""))
        # A file without a suffix ("data") will have full_file_suffix = "", causing an early return False.
        # Thus, it cannot match any valid_suffix, including "".
        self.assertFalse(is_valid_multipart_suffix("data", ""))

        # Filenames like ".bashrc", ".config.json"
        self.assertTrue(is_valid_multipart_suffix(".bashrc", {".bashrc", ".sh"}))
        self.assertTrue(is_valid_multipart_suffix(".bashrc", ".bashrc"))
        self.assertFalse(is_valid_multipart_suffix(".bashrc", ".config.json"))
        self.assertTrue(is_valid_multipart_suffix(".config.json", {".config.json"}))
        self.assertTrue(is_valid_multipart_suffix(".config.json", ".config.json"))
        self.assertTrue(is_valid_multipart_suffix(Path(".config.json"), ".config.json"))

        # Path-like objects
        self.assertTrue(is_valid_multipart_suffix(Path("path/to/data.tar.gz"), valid_set))
        self.assertFalse(is_valid_multipart_suffix(Path("path/to/image.jpeg"), valid_set))

        # Suffix is a substring of a valid one
        self.assertFalse(is_valid_multipart_suffix("archive.tar", valid_set)) # ".tar" is not ".tar.gz"
        self.assertTrue(is_valid_multipart_suffix("myfile.zst", ".zst"))
        self.assertTrue(is_valid_multipart_suffix("myfile.ZST", {".ZST"}))

    def test_is_valid_multipart_suffix_case_sensitive(self):
        # Case-sensitive True
        self.assertFalse(is_valid_multipart_suffix("archive.TAR.GZ", {".tar.gz"}, case_sensitive=True))
        self.assertTrue(is_valid_multipart_suffix("archive.tar.gz", {".tar.gz"}, case_sensitive=True))
        self.assertFalse(is_valid_multipart_suffix("archive.tar.gz", {".TAR.GZ"}, case_sensitive=True))
        self.assertTrue(is_valid_multipart_suffix("archive.TAR.GZ", {".TAR.GZ"}, case_sensitive=True))

        # Case-sensitive False (default behavior)
        self.assertTrue(is_valid_multipart_suffix("archive.TAR.GZ", {".tar.gz"}, case_sensitive=False))
        self.assertTrue(is_valid_multipart_suffix("archive.TAR.GZ", {".tar.gz"})) # Default
        self.assertTrue(is_valid_multipart_suffix("archive.tar.gz", {".TAR.GZ"}, case_sensitive=False))
        self.assertTrue(is_valid_multipart_suffix("archive.tar.gz", {".TAR.GZ"})) # Default

        # Single string valid_suffix
        self.assertFalse(is_valid_multipart_suffix("archive.TAR.GZ", ".tar.gz", case_sensitive=True))
        self.assertTrue(is_valid_multipart_suffix("archive.tar.gz", ".tar.gz", case_sensitive=True))
        self.assertTrue(is_valid_multipart_suffix("archive.TAR.GZ", ".tar.gz", case_sensitive=False))
        self.assertTrue(is_valid_multipart_suffix("archive.TAR.GZ", ".tar.gz")) # Default

    def test_is_valid_multipart_suffix_regex(self):
        # Basic regex
        self.assertTrue(is_valid_multipart_suffix("file.123.zip", {r"\.[0-9]+\.zip"}))
        self.assertTrue(is_valid_multipart_suffix("file.123.zip", r"\.[0-9]+\.zip"))
        self.assertTrue(is_valid_multipart_suffix("file.v1.tar.gz", {r"\.v\d+\.tar\.gz"}))
        self.assertFalse(is_valid_multipart_suffix("file.vA.tar.gz", {r"\.v\d+\.tar\.gz"}))

        # Regex with case_sensitive = True
        self.assertFalse(is_valid_multipart_suffix("file.ABC.zip", {r"\.[a-z]+\.zip"}, case_sensitive=True))
        self.assertTrue(is_valid_multipart_suffix("file.abc.zip", {r"\.[a-z]+\.zip"}, case_sensitive=True))
        self.assertTrue(is_valid_multipart_suffix("file.ABC.zip", {r"\.[A-Z]+\.zip"}, case_sensitive=True))
        self.assertFalse(is_valid_multipart_suffix("file.abc.zip", {r"\.[A-Z]+\.zip"}, case_sensitive=True))

        # Regex with case_sensitive = False (default)
        self.assertTrue(is_valid_multipart_suffix("file.ABC.zip", {r"\.[a-z]+\.zip"}, case_sensitive=False))
        self.assertTrue(is_valid_multipart_suffix("file.ABC.zip", {r"\.[a-z]+\.zip"})) # Default
        self.assertTrue(is_valid_multipart_suffix("file.abc.zip", {r"\.[A-Z]+\.zip"}, case_sensitive=False))
        self.assertTrue(is_valid_multipart_suffix("file.abc.zip", {r"\.[A-Z]+\.zip"})) # Default

        # Non-matching regex
        self.assertFalse(is_valid_multipart_suffix("file.txt", {r"\.tar\.gz$"}))
        self.assertFalse(is_valid_multipart_suffix("file.tar.gz", {r"^\.zip$"}))

        # Invalid regex pattern (should be treated as literal string)
        # `re.compile("*.gz")` would raise an error (nothing to repeat for *)
        # The function `is_valid_multipart_suffix` catches re.error and treats it as a string.
        self.assertFalse(is_valid_multipart_suffix("file.tar.gz", {"*.gz"})) # Not a regex match, not a string match for suffix ".gz"
        # For filename "*.gz", get_full_suffix("*.gz") is ".gz".
        # {"*.gz"} is treated as a literal string because "*.gz" is not a valid regex.
        # So, is_valid_multipart_suffix compares ".gz" (from filename) with "*.gz" (valid_suffix literal). They are not equal.
        self.assertFalse(is_valid_multipart_suffix("*.gz", {"*.gz"}))
        self.assertFalse(is_valid_multipart_suffix("file.gz", {"*.gz"})) # Suffix is ".gz", doesn't match "*.gz"

        # Test with a mix of regex and string suffixes
        valid_mix = {r"\.v\d+\.zip", ".tar.gz", ".data"}
        self.assertTrue(is_valid_multipart_suffix("backup.v123.zip", valid_mix))
        self.assertTrue(is_valid_multipart_suffix("archive.tar.gz", valid_mix))
        self.assertTrue(is_valid_multipart_suffix("my.data", valid_mix))
        self.assertFalse(is_valid_multipart_suffix("my.vABC.zip", valid_mix, case_sensitive=True))
        self.assertFalse(is_valid_multipart_suffix("my.vABC.zip", valid_mix, case_sensitive=False)) # Regex \d+ does not match ABC

        # Ensure fullmatch is used (implicitly by checking start/end)
        self.assertTrue(is_valid_multipart_suffix("file.log", {r"\.log"}))
        self.assertFalse(is_valid_multipart_suffix("file.log.txt", {r"\.log"}))
        self.assertTrue(is_valid_multipart_suffix("file.log.txt", {r"\.log\.txt"}))
        self.assertTrue(is_valid_multipart_suffix("file.log", {r".*\.log"})) # More flexible regex

if __name__ == '__main__':
    unittest.main()
