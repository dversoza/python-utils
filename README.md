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
    - [WebScrapper - Portal da Transparência TJPR](#webscrapper---portal-da-transparência-tjpr)

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

### WebScrapper - Portal da Transparência TJPR

Script: [**`transparency_TJPR.py`**](transparency_TJPR.py)

This script simply extracts data from Paraná's Court of Justice and returns simple and queryable CSV with a summary of the financial results of the notaries and other agencies linked to the Court.

> Transparência: verdadeira e simplificada

- Atualmente extraí apenas dados de resultados financeiros das Serventias Extrajudiciais do TJPR

---

- Usage

1. To run it, ensure that you have the `requests` library installed, with:

    ```bash
    pip install requests
    ```

2. Then, just run the `transparency_TJPR.py` in your terminal and choose the simple or detailed option.

    ```bash
    python transparency_TJPR.py
    ```

> With the simple option, you will see only the final result of the extraction when finished.
>
> With the detailed option, you will see line by line the extraction of the data.

- Examples

At the end, you will have a CSV with all the data, and you can view them in a table with a structure similar to this:

| Comarca / Serventia Extrajudicial                                                                                         |      2018       |       2019       |      2020       |       2021       |   Total Geral    |
| ------------------------------------------------------------------------------------------------------------------------- | :-------------: | :--------------: | :-------------: | :--------------: | :--------------: |
| 8º Serviço de Registro de Imóveis do Foro Central da Comarca da Região Metropolitana de Curitiba                          | R$ 5.440.730,81 | R$ 12.778.474,63 | R$ 9.861.284,99 | R$ 13.257.083,50 | R$ 41.337.573,93 |
| 1º Serviço de Registro de Imóveis do Foro Central da Comarca da Região Metropolitana de Londrina                          | R$ 3.837.116,05 | R$ 9.120.386,31  | R$ 8.458.784,80 | R$ 6.567.534,67  | R$ 27.983.821,83 |
| 6º Serviço de Registro de Imóveis do Foro Central da Comarca da Região Metropolitana de Curitiba                          | R$ 3.253.248,89 | R$ 8.508.878,89  | R$ 6.801.850,23 | R$ 4.325.247,56  | R$ 22.889.225,57 |
| 1º Serviço de Registro de Imóveis do Foro Central da Comarca da Região Metropolitana de Maringá                           | R$ 2.543.310,21 | R$ 5.260.576,85  | R$ 5.528.040,95 | R$ 5.256.915,15  | R$ 18.588.843,16 |
| 2º Serviço de Registro de Imóveis do Foro Central da Comarca da Região Metropolitana de Curitiba                          | R$ 1.707.215,29 | R$ 6.224.611,35  | R$ 4.721.166,74 | R$ 5.913.923,44  | R$ 18.566.916,82 |
| \*\*\*                                                                                                                    |     \*\*\*      |      \*\*\*      |     \*\*\*      |      \*\*\*      |      \*\*\*      |
| 1º Serviço de Registro de Imóveis do Foro Regional de São José dos Pinhais da Comarca da Região Metropolitana de Curitiba | R$ 2.200.614,00 | R$ 5.196.023,24  | R$ 4.662.502,86 | R$ 5.850.969,91  | R$ 17.910.110,01 |
| 2º Serviço de Registro de Imóveis do Foro Central da Comarca da Região Metropolitana de Maringá                           | R$ 2.618.460,03 | R$ 4.887.744,57  | R$ 4.999.803,24 | R$ 4.307.329,32  | R$ 16.813.337,16 |

- TODO

- [ ] Adicionar opção para extrair dados de serventias judiciais
- [ ] Adicionar opção para extrair dados de servidores
- [ ] Adicionar opção para extrair dados de receitas e despesas do tribunal
