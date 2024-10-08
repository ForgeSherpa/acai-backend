from .migrator import Datasets, get_excel_path
import polars as pl

all_datasets = [dataset.value for dataset in Datasets]

# Get the schema of all datasets
def get_schema():
    for dataset in all_datasets:
        print("="*5 + f" {dataset} " + "="*5)
        df = pl.read_excel(get_excel_path(Datasets(dataset)))

        # print columns names with it types, also check if there is any missing value if so mark is as ?
        # next to the type
        for column in df.columns:
            missing = '?' if df[column].null_count() > 0 else ''
            print(f"{column}: {df[column].dtype}{missing}")

def preview_all():
    for dataset in all_datasets:
        print("="*5 + f" {dataset} " + "="*5)
        df = pl.read_excel(get_excel_path(Datasets(dataset)))
        print(df.head())