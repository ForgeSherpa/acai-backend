import os
from dotenv import load_dotenv

ROOT_PATH = os.path.dirname(os.path.dirname(__file__))

ENV_PATH = os.path.join(ROOT_PATH, ".env")

load_dotenv(ENV_PATH, verbose=True)

USE_SQLITE = os.getenv("USE_SQLITE", "false").lower() == "true"

MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
MYSQL_DB = os.getenv("MYSQL_DB", "acai")

print("Applied Environment Variables:")
print(f"USE_SQLITE={USE_SQLITE}")
print(f"MYSQL_HOST={MYSQL_HOST}")
print(f"MYSQL_USER={MYSQL_USER}")
print(f"MYSQL_PASSWORD={MYSQL_PASSWORD}")
print(f"MYSQL_DB={MYSQL_DB}")

if USE_SQLITE:
    print("Warning! SQLITE is supported but not tested and pritiozed.")
    print("Warning! Expect issues!!!!!")