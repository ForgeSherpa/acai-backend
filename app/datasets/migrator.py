from os import path, remove
from enum import Enum
import polars as pl
from sqlalchemy.orm import Session
from typing import Callable, Any
from datetime import datetime
from sqlite3 import connect
from pymysql import connect as mysql_connect, Error as pymysqlError
from ..settings import MYSQL_DB, MYSQL_HOST, MYSQL_PASSWORD, MYSQL_USER

class Datasets(Enum):
    DATA_DOSEN = "Data_Dosen"
    DATA_KEGIATAN_MAHASISWA = "Data_Kegiatan_Mahasiswa_For_Akre"
    DATA_MAHASISWA = "Data_Mahasiswa_For_Akre"
    DATA_PENELITIAN = "Data_Penelitian_Dosen"


current_dir = path.dirname(path.realpath(__file__))

def get_excel_path(dataset: Datasets):
    return f"{current_dir}/{dataset.value}.xlsx"

def migrate(db: Session, dataset: Datasets, model: Callable[[tuple], Any], clean: Callable[[pl.DataFrame], pl.DataFrame] = None):
    df = pl.read_excel(get_excel_path(dataset))

    df = df.drop_nulls()

    if clean:
        df = clean(df)

    for row in df.rows():
        result = model(row)
        db.add(result)


    try:
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Error migrating {dataset.value}. Error: {str(e)}")

    print(f"Migrated: {dataset.value}.")

def handle_datetime(text: str) -> datetime:
    date_only = text.split(' ')[0]

    if date_only == '0000-00-00':
        return None

    return datetime.strptime(date_only, '%Y-%m-%d')

def migrate_sqlite():
    sqlite_path = './data.sqlite'

    if path.isfile(sqlite_path):
        answer = input('Database already exists, proceed to migrate anyway? [Y/n]: ')
        
        if answer != 'Y' and answer != 'y':
            print('Aborting!')
            return
        
        remove(sqlite_path)
        print('Database removed.')

    connection = connect(sqlite_path)

    with open('./schema_sqlite.sql') as f:
        connection.executescript(f.read())
    
    connection.close()

    print('Sqlite Schema Migrated')

def migrate_mysql():
    conn = mysql_connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB
    )

    with open('./schema_mysql.sql') as f:
        sql_script = f.read()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM information_schema.tables WHERE table_schema = %s", (MYSQL_DB,))
            tables = cursor.fetchall()

            if tables:
                answer = input('Database already exists, proceed to migrate anyway? [Y/n]: ')
                
                if answer != 'Y' and answer != 'y':
                    print('Aborting!')
                    return

                for table in tables:
                    cursor.execute(f"DROP TABLE {table[2]}")

            # Execute the SQL script, handling multiple statements
            for statement in sql_script.split(';'):
                statement = statement.strip()
                if statement:
                    try:
                        cursor.execute(statement)
                    except pymysqlError as e:
                        print(f"Error executing statement: {statement}")
                        print(f"Error message: {str(e)}")
                        # Rollback the transaction on error
                        conn.rollback()
                        break

            # Commit the transaction if all statements executed successfully
            conn.commit()

    conn.close()

    print('MySQL Schema Migrated')