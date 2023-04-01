import os

import pandas as pd
from tqdm import tqdm


def filter_parquet_file(
    ids_to_be_restored_csv, parquets_dir=os.getcwd(), delete_original_parquets=False
):
    """This function filters the parquet files and only keeps the objects that are in the ids_to_be_restored_csv file.
    IMPORTANT: The CSV file should ONLY have the objects id, with the header "id".
    The parquet files are filtered in place.

    Args:
        ids_to_be_restored_csv (str): path to the csv file containing the ids to be restored.
        parquets_dir (str): path to the parquet files. If None, the current directory is used.
        delete_original_parquets (bool, optional): If True, the original parquet files are deleted. Defaults to False.
    """
    ids_to_be_restored_csv = pd.read_csv(ids_to_be_restored_csv)
    ids_to_be_restored = ids_to_be_restored_csv["id"].values

    files_in_dir = os.listdir(parquets_dir)
    parquet_files = [file for file in files_in_dir if file.endswith(".parquet")]

    final_dfs = []

    for parquet_file in tqdm(parquet_files):
        df = pd.read_parquet(os.path.join(parquets_dir, parquet_file))
        df = df[df["id"].isin(ids_to_be_restored)]
        final_dfs.append(df)

        if delete_original_parquets:
            os.remove(os.path.join(parquets_dir, parquet_file))

    final_df = pd.concat(final_dfs)
    final_df.to_csv(f"filtered_objects.csv", index=False)
    print("Done!\n")

    print('This is the general structure of the filtered parquet files:\n')
    print(final_df.head())
    print("\n")
    print(f"A total of ( {len(final_df)} ) objects were filtered.")
    print(f"The filtered objects are saved in filtered_objects.csv")



def combine_csv_files():
    files_in_dir = os.listdir(os.getcwd())
    csv_files = [
        file for file in files_in_dir if file.endswith(".csv") and "bak" not in file
    ]

    final_df = pd.concat([pd.read_csv(file) for file in csv_files])
    final_df.to_csv("final_df.csv", index=False)


def convert_parquets_to_csv():
    files_in_dir = os.listdir(os.getcwd())
    parquet_files = [file for file in files_in_dir if file.endswith(".parquet")]

    # as we have 1500 parquet files, split them into chunks of 100
    parquet_files_chunks = [
        parquet_files[i : i + 100] for i in range(0, len(parquet_files), 100)
    ]

    for chunk in tqdm(parquet_files_chunks):
        chunk_df = pd.concat([pd.read_parquet(file) for file in chunk])
        chunk_df.to_csv(f"{chunk[0][:-9]}.csv", index=False)


def old_filter_parquet_file():
    objects_df = pd.read_csv("export_202208301448.csv")
    objects_ids = objects_df["id"].values

    csvs_in_dir = os.listdir(os.getcwd())
    csv_files = [
        file
        for file in csvs_in_dir
        if file.endswith(".csv") and file.startswith("part-")
    ]

    # get csv_file row if its id is in objects_ids
    for csv_file in tqdm(csv_files):
        df = pd.read_csv(csv_file)
        df = df[df["id"].isin(objects_ids)]
        df.to_csv(f"{csv_file}_filtered", index=False)


if __name__ == "__main__":
    filter_parquet_file(
        "ids_to_be_restored.csv",
        parquets_dir=os.path.join(os.getcwd(), "trash"),
    )
