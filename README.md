# MultiExt: Advanced File Extension Toolkit

**multiext** is a Python library for advanced parsing, validation, and manipulation of multipart file extensions (e.g., `.tar.gz`, `.b.c`). It provides a more comprehensive way to work with complex file suffixes than the standard `os.path` or `pathlib` modules alone, offering robust tools for developers who need to reliably identify, validate, and transform filenames based on their complete extension chains.

## Key Features & Modules

The library is organized into several main categories:

-   **Parsing (`multiext.parser`)**: This module provides robust tools for dissecting filenames and paths with complex, multi-part extensions (e.g., `.tar.gz`, `.project.snapshot.zip`). Key functions allow you to:
    -   Extract the full multipart suffix (e.g., `get_full_suffix()`).
    -   Get the base stem before any multipart suffix (e.g., `get_stem_multipart()`).
    -   Split a filename into its stem and full suffix (e.g., `split_multipart_ext()`).
    -   Break down a full suffix into its parts (e.g., `get_suffix_parts()`).
    -   Normalize suffix strings (e.g., `normalize_suffix()`).
    -   **Common Use Cases**: File type detection beyond simple suffixes, automatic categorization/routing of files, extracting embedded filename information (like version numbers), and normalizing suffixes for consistent processing and comparison.

-   **Validation (`multiext.validation`)**: This module offers functions to verify if filenames possess multipart suffixes and to validate these against defined criteria, crucial for ensuring compliance before processing. Key functions allow you to:
    -   Check if a filename has a multipart suffix (e.g., `has_multipart_suffix()`).
    -   Validate a filename's full suffix against a list of valid ones (e.g., `is_valid_multipart_suffix()`), supporting case-sensitive/insensitive comparisons and regex patterns.
    -   **Common Use Cases**: Input file validation (e.g., for uploads or CLI arguments), filtering files by complex extension patterns, security checks for filename conformity, and implementing conditional logic based on suffix recognition.

-   **Manipulation (`multiext.manipulation`)**: This module provides powerful functions for modifying filenames and paths involving multipart extensions, offering precise control over adding, removing, or replacing extensions. Key functions allow you to:
    -   Replace the entire multipart suffix (e.g., `replace_multipart_suffix()`).
    -   Add a new part to an existing suffix chain (e.g., `add_suffix_part()`).
    -   Remove the last part of a multipart suffix (e.g., `remove_last_suffix_part()`).
    -   **Common Use Cases**: Renaming files during conversion processes (e.g., `data.tar.gz` to `data.zip`), versioning or backing up files (e.g., `config.json` to `config.json.bak`), standardizing filenames by altering suffix parts, and programmatically constructing output filenames.

-   **Path Object (`multiext.path`)**: This module introduces `MultiExtPath`, a `pathlib.Path` subclass designed to simplify interactions with paths featuring multipart extensions. It offers:
    -   Integrated access to multipart suffix properties (e.g., `p.full_suffix`, `p.stem_multipart`) and manipulation methods (e.g., `p.replace_multipart_suffix()`) directly on path objects.
    -   **Benefits**: Accurate multipart suffix handling, precise stem extraction, simplified suffix manipulation, consistency with other `multiext` modules, and full `pathlib.Path` compatibility. This is useful for applications dealing with compressed files, versioned files, or any naming convention with multiple dot-separated extension segments.

## Installation

Once the package is available on PyPI, you can install it using pip:

```bash
pip install multiext
```

For now, if you want to install it from source (e.g., to get the latest development version):

1.  Clone the repository:
    ```bash
    git clone https://github.com/ikkebr/multiext.git
    cd multiext
    ```

2.  Install in editable mode:
    ```bash
    pip install -e .
    ```
    Or, to include development dependencies:
    ```bash
    pip install -e .[dev]
    ```

## Usage

Here are some basic examples of how to use key functions from the `multiext` library:

```python
import multiext
from pathlib import Path # For Path object examples
from multiext import MultiExtPath # For MultiExtPath examples

# --- Parsing Examples ---
filename1 = "archive.tar.gz"
filename2 = "document.doc"
filename3 = ".bash_profile"
filename4 = "backup.tar.gz.bak"

print(f"'{filename1}' full suffix: {multiext.get_full_suffix(filename1)}")
# Output: '.tar.gz'
print(f"'{filename2}' full suffix: {multiext.get_full_suffix(filename2)}")
# Output: '.doc'
print(f"'{filename3}' full suffix: {multiext.get_full_suffix(filename3)}")
# Output: '.bash_profile'

print(f"'{filename1}' multipart stem: {multiext.get_stem_multipart(filename1)}")
# Output: 'archive'
print(f"'{filename3}' multipart stem: {multiext.get_stem_multipart(filename3)}")
# Output: ''

print(f"'{filename1}' suffix parts: {multiext.get_suffix_parts(filename1)}")
# Output: ['.tar', '.gz']
print(f"'{filename4}' suffix parts: {multiext.get_suffix_parts(filename4)}")
# Output: ['.tar', '.gz', '.bak']
print(f"'{filename3}' suffix parts: {multiext.get_suffix_parts(filename3)}")
# Output: ['.bash_profile']

# Normalizing a suffix
raw_suffix = ".TAR.GZ"
normalized = multiext.normalize_suffix(raw_suffix)
print(f"Normalized '{raw_suffix}': {normalized}")
# Output: Normalized '.TAR.GZ': .tar.gz

another_raw_suffix = "tar..gz" # No leading dot, multiple internal dots
normalized2 = multiext.normalize_suffix(another_raw_suffix)
print(f"Normalized '{another_raw_suffix}': {normalized2}")
# Output: Normalized 'tar..gz': .tar..gz

# --- Validation Examples ---
print(f"'{filename1}' has multipart suffix? {multiext.has_multipart_suffix(filename1)}")
# Output: True
print(f"'{filename2}' has multipart suffix? {multiext.has_multipart_suffix(filename2)}")
# Output: False
print(f"'{filename3}' has multipart suffix? {multiext.has_multipart_suffix(filename3)}") # .bash_profile is considered single part
# Output: False
print(f"'{Path('.config.json')}' has multipart suffix? {multiext.has_multipart_suffix(Path('.config.json'))}")
# Output: True

valid_archive_suffixes = {".tar.gz", ".zip", ".tar.xz"}
print(f"Is '{filename1}' a valid archive? {multiext.is_valid_multipart_suffix(filename1, valid_archive_suffixes)}")
# Output: True
print(f"Is 'archive.rar' a valid archive? {multiext.is_valid_multipart_suffix('archive.rar', valid_archive_suffixes)}")
# Output: False
print(f"Is 'backup.ZIP' a valid archive (default case-insensitive check)? {multiext.is_valid_multipart_suffix('backup.ZIP', valid_archive_suffixes)}")
# Output: True

# Case-sensitive validation for is_valid_multipart_suffix
print(f"Is 'backup.ZIP' a valid archive (case-sensitive)? {multiext.is_valid_multipart_suffix('backup.ZIP', {'.zip'}, case_sensitive=True)}")
# Output: False
print(f"Is 'backup.zip' a valid archive (case-sensitive)? {multiext.is_valid_multipart_suffix('backup.zip', {'.zip'}, case_sensitive=True)}")
# Output: True

# Regex validation for is_valid_multipart_suffix
image_suffixes_regex = {r"\.jpe?g$", r"\.png$", r"\.gif$"} # Matches .jpg, .jpeg, .png, .gif
print(f"Is 'photo.jpeg' a valid image (regex)? {multiext.is_valid_multipart_suffix('photo.jpeg', image_suffixes_regex)}")
# Output: True
print(f"Is 'photo.JPG' a valid image (regex, case-insensitive default)? {multiext.is_valid_multipart_suffix('photo.JPG', image_suffixes_regex)}")
# Output: True
print(f"Is 'photo.JPG' a valid image (regex, case-sensitive)? {multiext.is_valid_multipart_suffix('photo.JPG', {r"\.jpe?g$"}, case_sensitive=True)}")
# Output: False
print(f"Is 'photo.tiff' a valid image (regex)? {multiext.is_valid_multipart_suffix('photo.tiff', image_suffixes_regex)}")
# Output: False

# --- Manipulation Examples ---
new_filename1 = multiext.replace_multipart_suffix(filename1, ".zip")
print(f"Replacing suffix of '{filename1}' with '.zip': {new_filename1}")
# Output: 'archive.zip'

path_obj = Path("path/to/data.tar.gz")
new_path_obj_str = multiext.replace_multipart_suffix(path_obj, ".pkg") # Function returns string
print(f"Replacing suffix of '{path_obj}' with '.pkg': {new_path_obj_str}")
# Output: path/to/data.pkg

added_part_filename = multiext.add_suffix_part(filename1, ".bak")
print(f"Adding '.bak' to '{filename1}': {added_part_filename}")
# Output: 'archive.tar.gz.bak'

added_to_nosuffix = multiext.add_suffix_part("report", "docx") # Will add .docx
print(f"Adding 'docx' to 'report': {added_to_nosuffix}")
# Output: report.docx

removed_part_filename = multiext.remove_last_suffix_part(filename1)
print(f"Removing last suffix part from '{filename1}': {removed_part_filename}")
# Output: 'archive.tar'

removed_single_suffix = multiext.remove_last_suffix_part("image.jpg")
print(f"Removing last suffix part from 'image.jpg': {removed_single_suffix}")
# Output: 'image'

removed_from_dotfile = multiext.remove_last_suffix_part(".bash_profile")
print(f"Removing last suffix part from '.bash_profile': {removed_from_dotfile}")
# Output: ''

# --- Working with MultiExtPath ---
# The MultiExtPath class is a subclass of pathlib.Path and provides
# convenient access to multipart extension information and operations.

p_mep = MultiExtPath("archive.tar.gz")
p_mep_dir = MultiExtPath("path/to/another.document.pdf.backup")

# Access properties
print(f"Path: {p_mep}, Full Suffix: {p_mep.full_suffix}")
# Output: Path: archive.tar.gz, Full Suffix: .tar.gz
print(f"Path: {p_mep_dir}, Full Suffix: {p_mep_dir.full_suffix}")
# Output: Path: path/to/another.document.pdf.backup, Full Suffix: .pdf.backup

print(f"Path: {p_mep}, Multipart Stem: {p_mep.stem_multipart}")
# Output: Path: archive.tar.gz, Multipart Stem: archive
print(f"Path: {p_mep_dir}, Multipart Stem: {p_mep_dir.stem_multipart}")
# Output: Path: path/to/another.document.pdf.backup, Multipart Stem: another.document

# Replace suffix using the method
new_p_mep = p_mep.replace_multipart_suffix(".zip")
print(f"Path: {new_p_mep}, Name: {new_p_mep.name}")
# Output: Path: archive.zip, Name: archive.zip

new_p_mep_dir = p_mep_dir.replace_multipart_suffix(".final.docx")
print(f"Path: {new_p_mep_dir}, Name: {new_p_mep_dir.name}")
# Output: Path: path/to/another.document.final.docx, Name: another.document.final.docx

# It's still a Path object
print(f"Parent of '{p_mep_dir}': {p_mep_dir.parent}")
# Output: Parent of 'path/to/another.document.pdf.backup': path/to
print(f"'{new_p_mep_dir}' exists? {new_p_mep_dir.exists()}") # Example of other Path methods
# Output: 'path/to/another.document.final.docx' exists? False
```

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any bugs, feature requests, or improvements.

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.
