# My Python Utils Library

This is a collection of Python utilities that I use in my projects.

> To use them, follow each specific utility instructions here or on it's folder.

## Badges

![Python](https://img.shields.io/badge/python-3670A0?style=social&logo=python&logoColor=ffdd54)
![GitHub](https://img.shields.io/github/license/dversoza/python-utils)
![GitHub last commit](https://img.shields.io/github/last-commit/dversoza/python-utils)
![GitHub issues](https://img.shields.io/github/issues/dversoza/python-utils)
![GitHub pull requests](https://img.shields.io/github/issues-pr/dversoza/python-utils)

## Table of Contents

- [My Python Utils Library](#my-python-utils-library)
  - [Badges](#badges)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Utilities](#utilities)
    - [Folder parser to CSV/JSON](#folder-parser-to-csvjson)

## Installation

1. Clone this repository

    ```bash
    git clone
    ```

2. Enter the folder

    ```bash
    cd python-utils
    ```

3. Create a virtual environment

    ```bash
    python3 -m venv .venv
    ```

4. Activate the virtual environment

    ```bash
    source .venv/bin/activate
    ```

5. Install the dependencies

    ```bash
    pip install -r requirements.txt
    ```

6. Run the desired utility!

    ```bash
    python3 <utility_name>.py <args>
    ```

## Utilities

### Folder parser to CSV/JSON

Script: [**`parse_folder.py`**](parse_folder.py)

This utility parses a folder and its sub-folders and stores the results either in a JSON or in a CSV file.

---

- Usage

  1. To export the results in a JSON file, run the following command:

      ```bash
      python parse_folder.py <path> --json
      ```

  2. To export the results in a CSV file, run the following command:

      ```bash
      python parse_folder.py <path> --csv
      ```

- Example

  - Existing directory structure:

    ```text
    project
    │   README.md
    │   file001.txt
    │
    └───folder1
    │   │   file011.txt
    │   │   file012.txt
    │   │
    │   └───subfolder1
    │       │   file111.txt
    │       │   file112.txt
    │       │   ...
    │
    └───folder2
        │   file021.txt
        │   file022.txt
    ```

  - To get a JSON file, you should run the following command:

    ```bash
    python parse_folder.py project --json
    ```

    Output:

    ```json
    [
        {
            "file": "README.md",
            "parent_dir": "project",
            "other_parent_dirs": "",
        },
        [...]
        {
            "file": "file011.txt",
            "parent_dir": "project",
            "other_parent_dirs": "folder1",
        },
        [...]
        {
            "file": "file112.txt",
            "parent_dir": "project",
            "other_parent_dirs": "folder1, subfolder1",
        },
        [...]
    ]
    ```

  - Or, to get a CSV file, you should run the following command:

    ```bash
    python parse_folder.py project --csv
    ```

    And, you will get:

    |file       |parent_dir|other_parent_dirs  |
    |-----------|----------|-------------------|
    |README.md  |project   |                   |
    |[...]      |          |                   |
    |file011.txt|project   |folder1            |
    |[...]      |          |                   |
    |file112.txt|project   |folder1, subfolder1|
