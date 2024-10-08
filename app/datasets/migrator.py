from os import path
from enum import Enum
import polars as pl
from sqlalchemy.orm import Session
from typing import Callable, Any
from datetime import datetime
from sqlite3 import connect

class Datasets(Enum):
    DATA_DOSEN = "Data_Dosen"
    DATA_KEGIATAN_MAHASISWA = "Data_Kegiatan_Mahasiswa_For_Akre"
    DATA_MAHASISWA = "Data_Mahasiswa_For_Akre"
    DATA_PENELITIAN = "Data_Penelitian_Dosen"


current_dir = path.dirname(path.realpath(__file__))

def get_excel_path(dataset: Datasets):
    return f"{current_dir}/{dataset.value}.xlsx"

def migrate(db: Session, dataset: Datasets, model: Callable[[tuple], Any]):
    df = pl.read_excel(get_excel_path(dataset))

    for row in df.rows():
        result = model(row)
        db.add(result)

    db.commit()
    print(f"Migrated: {dataset.value}.")

def handle_datetime(text: str) -> datetime:
    date_only = text.split(' ')[0]

    if date_only == '0000-00-00':
        return None

    return datetime.strptime(date_only, '%Y-%m-%d')

def migrate_sqlite():
    connection = connect('./data.sqlite')

    with open('./schema.sql') as f:
        connection.executescript(f.read())

    print('Sqlite Schema Migrated')
