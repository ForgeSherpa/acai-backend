import os
from dotenv import load_dotenv

ROOT_PATH = os.path.dirname(os.path.dirname(__file__))

ENV_PATH = os.path.join(ROOT_PATH, ".env")

load_dotenv(ENV_PATH, verbose=True)

# Paksa SQLite off karena entah napa masih ada aja yang pake SQLITE.
# Giliran error, malah salahin project error, padahal udah ada tulisan sqlite not tested.
# Maka dari itu saya hapusin aja!
USE_SQLITE = os.getenv("USE_SQLITE", "false").lower() == "true"

if USE_SQLITE:
    print("Warning! Usage of SQLite is disabled... due to some person keep using it")
    print("And complaining once error, therefore I will disable it entirely!")


USE_SQLITE = False

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
