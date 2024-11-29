from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .settings import USE_SQLITE, MYSQL_DB, MYSQL_HOST, MYSQL_PASSWORD, MYSQL_USER

if USE_SQLITE:
    SQLALCHEMY_DATABASE_URL = "sqlite:///./data.sqlite"
    connect_args = {"check_same_thread": False}
else:
    SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}"
    connect_args = {}

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args=connect_args
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
