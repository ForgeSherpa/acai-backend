from app.datasets.migrator import migrate, Datasets, handle_datetime, migrate_sqlite, migrate_mysql
from app.database import SessionLocal
from app.settings import USE_SQLITE
from app.models import Lecturer, LecturerResearch, Student, StudentActivity
from app.datasets.schema_reader import preview_all, get_schema
from sqlalchemy.orm import scoped_session
from sqlalchemy import text
import argparse
import polars as pl
import subprocess
import os

parser = argparse.ArgumentParser()

parser.add_argument('command')

args = parser.parse_args()

def performMigration():
    print('Migrating')

    # scoped session here for local threading
    with scoped_session(SessionLocal)() as db:
        if not USE_SQLITE:
            # disable foreign key check for MySQL temporarily
            db.execute(text('SET FOREIGN_KEY_CHECKS=0'))

        migrate(
            db,
            Datasets.DATA_DOSEN,
            lambda data: Lecturer(id=data[0], nidn=data[1], name=data[2], major=data[3]),
        )
        migrate(
            db,
            Datasets.DATA_PENELITIAN,
            model= lambda data: LecturerResearch(
            nidn=data[0],
            title=str(data[1]).encode('utf-8'),
            publication_date=handle_datetime(data[2]),
            publication_type=data[3],
            publication_detail=data[4],
            ),
            clean=lambda df: df.filter(pl.col('tanggal_terbit') != '0000-00-00')
                     .with_columns(pl.col('judul_penelitian').str.replace_all(r'[^\x00-\x7F]+', '', literal=False))
                     .filter(pl.col('nidn_dosen').str.contains(r'^\d+$')),
        )
        migrate(
            db,
            Datasets.DATA_MAHASISWA,
            lambda data: Student(
                id=data[0],
                name=data[1],
                faculty=data[2],
                generation=data[3],
                gpa=data[4],
                status=data[5],
                graduation_year=int(data[6] / 10),
                graduation_semester=data[6] % 10,
            ),
        )
        migrate(
            db,
            Datasets.DATA_KEGIATAN_MAHASISWA,
            lambda data: StudentActivity(
                student_id=data[0],
                bank_id=data[1],
                name=data[2],
                type=data[3],
                date=data[4],
            )
        )

        if not USE_SQLITE:
            # enable foreign key check back
            db.execute(text('SET FOREIGN_KEY_CHECKS=1'))


def version_mismatch():
    print('Version mismatch, please run migrate:sqlite and migrate again.')
    exit(1)

if __name__ == "__main__":
    match args.command:
        case 'migrate:schema':
            print(f"Using {'SQLite' if USE_SQLITE else 'MySQL'}")

            if USE_SQLITE:
                migrate_sqlite()
            else: 
                migrate_mysql()

            with open('./version') as v:
                version = v.read()

                with open('./.your_version', 'w') as f:
                    f.write(version)
        case 'migrate':
            performMigration()
        case 'schema':
            get_schema()
        case 'preview':
            preview_all()
        case 'serve':
            with open('./version') as v:
                version = v.read()

                if not os.path.exists('./.your_version'):
                    version_mismatch()

                with open('./.your_version') as f:
                    user_version = f.read()
                    if user_version != version:
                        version_mismatch()

            subprocess.run(['fastapi', 'dev', 'main.py'])
        case _:
            print("Invalid command: only migrate:schema, migrate, schema, and preview is allowed.")
