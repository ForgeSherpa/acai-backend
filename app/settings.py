from dotenv import load_dotenv
import os

load_dotenv()

USE_SQLITE = os.getenv("USE_SQLITE", "false").lower() == "true"

MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
MYSQL_DB = os.getenv("MYSQL_DB", "acai")