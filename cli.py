from app.datasets.migrator import migrate, Datasets, handle_datetime, migrate_sqlite
from app.database import SessionLocal
from app.models import Lecturer, LecturerResearch, Student, StudentActivity
from app.datasets.schema_reader import preview_all, get_schema
from sqlalchemy.orm import scoped_session
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('command')

args = parser.parse_args()

def performMigration():
    print('Migrating')

    # scoped session here for local threading
    with scoped_session(SessionLocal)() as db:
        migrate(
            db,
            Datasets.DATA_DOSEN,
            lambda data: Lecturer(id=data[0], nidn=data[1], name=data[2]),
        )
        migrate(
            db,
            Datasets.DATA_PENELITIAN,
            lambda data: LecturerResearch(
                nidn=data[0],
                title=data[1],
                publication_date=handle_datetime(data[2]),
                publication_type=data[3],
                publication_detail=data[4],
            ),
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
                graduation_year=data[6] % 10 if data[6] is not None else None,
                graduation_semester=int(data[6] / 10) if data[6] is not None else None,
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


if __name__ == "__main__":
    match args.command:
        case 'migrate:sqlite':
            migrate_sqlite()
        case 'migrate':
            performMigration()
        case 'schema':
            get_schema()
        case 'preview':
            preview_all()
        case _:
            print("Invalid command")