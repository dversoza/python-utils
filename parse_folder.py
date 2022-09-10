""" This module parses a folder of files and creates either a CSV or JSON file with the results (default is CSV).
    The output file is created in the same folder as the files, using the name of the root folder as it's name.

    Example:
        $ python3 parse_folder.py /path/to/folder --json
    OR:
        $ python3 parse_folder.py /path/to/folder --csv

    Attributes:
        __author__ = "Daniel Versoza Alves"
        __email__ = "daniel@versoza.dev"
        __version__ = "1.0.0"
        __status__ = "Development"
        __date__ = "2022/09/10"
"""

import argparse
import csv
import json
import os


def _walk_dir(path: str = os.getcwd()):
    """Walks through a directory and returns a list of files.

    Args:
        path (str, optional): Path to the directory. Defaults to ´os.getcwd().

    Returns:
        list: List of files.
    """
    files = []

    for root, _, files in os.walk(path, topdown=False):
        for file in files:
            file_path = os.path.join(root, file)

            files.append(
                {
                    "file": os.path.basename(file_path).split(".")[0],
                    "parent_dir": os.path.basename(os.path.dirname(file_path)),
                    "other_parent_dirs": os.path.dirname(file_path)
                    .split(os.sep)[1:-1]
                    .join(", "),
                }
            )

    return files


def _create_csv(files: list, path: str = os.getcwd()):
    """Creates a csv file with the results.

    Args:
        files (list): List of files.
        path (str, optional): Path to the directory. Defaults to os.getcwd().
    """
    csv_file_name = os.path.basename(path) + ".csv"
    with open(
        os.path.join(path, csv_file_name), "w", newline="", encoding="utf-8-sig"
    ) as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=files[0].keys())

        writer.writeheader()
        writer.writerows(files)


def _create_json(files: list, path: str = os.getcwd()):
    """Creates a json file with the results.

    Args:
        files (list): List of files.
        path (str, optional): Path to the directory. Defaults to os.getcwd().
    """
    json_file_name = os.path.basename(path) + ".json"
    with open(
        os.path.join(path, json_file_name), "w", newline="", encoding="utf-8-sig"
    ) as json_file:
        json.dump(files, json_file)


def main(type: str = "csv", path: str = os.getcwd()):
    """Main function"""
    files = _walk_dir(path)

    if type == "json":
        _create_json(files, path)
    else:
        _create_csv(files, path)


def arg_parser():
    """Argument parser"""
    parser = argparse.ArgumentParser(
        description="Parse a folder and create a CSV or JSON with it's sub-folders and files as result."
    )
    parser.add_argument("path", type=str, help="Path to the folder to be parsed.")
    parser.add_argument("--json", action="store_true", help="Outputs to a JSON.")
    parser.add_argument(
        "--csv", action="store_true", help="Outputs to a CSV. (Default)"
    )
    args = parser.parse_args()

    if args.json:
        main(type="json", path=args.path)
    else:
        main(type="csv", path=args.path)


if __name__ == "__main__":
    arg_parser()
