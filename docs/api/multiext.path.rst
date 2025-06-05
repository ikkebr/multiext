multiext.path
=============

The `multiext.path` module introduces the `MultiExtPath` class, an extension of the standard `pathlib.Path`. This specialized class is designed to simplify and enhance interactions with file paths that feature multipart extensions (e.g., ``archive.tar.gz``, ``data.project.snapshot``).

**Benefits of using `MultiExtPath`**

While `pathlib.Path` is powerful, its handling of suffixes is typically limited to the final part of an extension (e.g., ``.gz`` in ``archive.tar.gz``). `MultiExtPath` offers a more nuanced approach:

- **Accurate Multipart Suffix Handling:** Properties like `full_suffix` correctly identify the entire sequence of extensions (e.g., ``.tar.gz``).
- **Precise Stem Extraction:** The `stem_multipart` property provides the true stem of the filename before any extension part (e.g., ``archive`` from ``archive.tar.gz``).
- **Simplified Suffix Manipulation:** Methods like `replace_multipart_suffix` allow for easy and reliable modification of complex extensions.
- **Consistency:** It seamlessly integrates the parsing and manipulation logic from other `multiext` modules in an object-oriented manner.
- **Inheritance:** As a subclass of `pathlib.Path`, it retains all the standard path manipulation capabilities, ensuring drop-in compatibility where `Path` objects are expected.

This makes `MultiExtPath` particularly useful in applications that frequently deal with compressed files, versioned files, or any naming convention that utilizes multiple dot-separated segments in the extension.

**Usage and Examples**

Below are examples demonstrating key features of `MultiExtPath`.

**Properties:**

*   **`full_suffix`**: Retrieves the complete multipart suffix.
    ```python
    >>> from multiext import MultiExtPath
    >>> p = MultiExtPath("backup.v2.tar.gz")
    >>> p.full_suffix
    '.v2.tar.gz'
    >>> p = MultiExtPath("myfile.json")
    >>> p.full_suffix
    '.json'
    >>> p = MultiExtPath("nodotextension")
    >>> p.full_suffix
    ''
    ```

*   **`stem_multipart`**: Retrieves the base name before any part of the extension.
    ```python
    >>> from multiext import MultiExtPath
    >>> p = MultiExtPath("backup.v2.tar.gz")
    >>> p.stem_multipart
    'backup'
    >>> p = MultiExtPath("document.draft")
    >>> p.stem_multipart
    'document'
    >>> p = MultiExtPath(".configfile") # Hidden file
    >>> p.stem_multipart
    ''
    ```

**Methods:**

*   **`replace_multipart_suffix(new_suffix)`**: Replaces the entire multipart suffix with a new one.
    ```python
    >>> from multiext import MultiExtPath
    >>> p = MultiExtPath("archive.old.tar.gz")
    >>> p.replace_multipart_suffix(".zip")
    MultiExtPath('archive.old.zip')

    >>> p = MultiExtPath("project_data.csv.bak")
    >>> p.replace_multipart_suffix(".csv")
    MultiExtPath('project_data.csv')

    >>> p = MultiExtPath("image.jpeg")
    >>> p.replace_multipart_suffix(".png")
    MultiExtPath('image.png')

    >>> p = MultiExtPath("script") # No suffix
    >>> p.replace_multipart_suffix(".py")
    MultiExtPath('script.py')

    >>> p = MultiExtPath(".profile") # Hidden file
    >>> p.replace_multipart_suffix(".sh") # stem_multipart is '', new_suffix is '.sh'
    MultiExtPath('.sh')

    >>> p = MultiExtPath("path/to/somefile.tar.gz")
    >>> p.replace_multipart_suffix(".backup.zip")
    MultiExtPath('path/to/somefile.backup.zip')
    ```
    *Use Case Scenario:*
    Imagine you have a batch of files like ``report-2023-final.docx.backup`` and you want to restore them by removing the ``.backup`` part, but keeping ``.docx``.
    While `MultiExtPath`'s `replace_multipart_suffix` replaces the *entire* suffix, you'd typically use functions from `multiext.manipulation` for more granular suffix changes. However, if you wanted to change all ``.docx.backup`` files to ``.docx.final``:
    ```python
    # This example is more about direct replacement
    # files = [MultiExtPath("reportA.docx.backup"), MultiExtPath("reportB.docx.backup")]
    # for f_path in files:
    #   if f_path.full_suffix == ".docx.backup":
    #     new_path = f_path.replace_multipart_suffix(".docx.final")
    #     print(f"Renaming {f_path} to {new_path}")
    # This would result in reportA.docx.final, reportB.docx.final
    ```

**Integration with `pathlib.Path` features:**

Since `MultiExtPath` is a subclass of `pathlib.Path`, all standard `Path` methods and properties are available and work as expected, returning `MultiExtPath` instances where appropriate.
    ```python
    >>> from multiext import MultiExtPath
    >>> p = MultiExtPath("/usr/local/bin/my_script.sh.template")
    >>> p.name
    'my_script.sh.template'
    >>> p.parent
    MultiExtPath('/usr/local/bin')
    >>> isinstance(p.parent, MultiExtPath)
    True
    >>> new_p = p.parent / "another_file.txt"
    >>> isinstance(new_p, MultiExtPath) # Joining paths also produces MultiExtPath
    True
    >>> new_p
    MultiExtPath('/usr/local/bin/another_file.txt')
    ```

.. automodule:: multiext.path
   :members:
   :undoc-members:
   :show-inheritance:
