multiext.manipulation
=====================

The `multiext.manipulation` module provides powerful functions for modifying filenames and paths that involve multipart extensions. These utilities allow for precise control over how extensions are added, removed, or replaced, going beyond the standard library's capabilities which typically only handle the final suffix part.

Common use cases include:
  - **File Conversion Processes:** Renaming files after converting them from one format to another where multipart extensions are involved (e.g., changing ``data.tar.gz`` to ``data.tar.bz2`` or ``data.zip``).
  - **Versioning and Backup:** Adding suffix parts to indicate versions or backup status (e.g., ``config.json`` to ``config.json.bak`` or ``report.v1.docx``).
  - **Standardizing Filenames:** Removing or replacing non-standard or intermediate suffix parts to achieve a consistent naming scheme.
  - **Generating Output Filenames:** Programmatically constructing filenames with specific multipart extensions based on input files or processing steps.

These functions simplify common filename transformation tasks, especially when dealing with complex extension structures.

.. automodule:: multiext.manipulation
   :members:
   :undoc-members:
   :show-inheritance:
