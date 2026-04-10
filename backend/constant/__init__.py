import dotenv
import os
from pathlib import Path

# Always load backend/.env regardless of current working directory.
dotenv.load_dotenv(Path(__file__).resolve().parents[1] / ".env")

POSTGRE_SQL_PASSWORD = os.getenv('POSTGRE_SQL_PASSWORD')
DATABASE_NAME = (os.getenv('DATABASE_NAME') or '').strip().strip('"').strip("'")
USER = (os.getenv('USER') or '').strip().strip('"').strip("'")
HOST = (os.getenv('HOST') or '').strip().strip('"').strip("'")
DB_PORT = (os.getenv('DB_PORT') or '').strip().strip('"').strip("'")

csv_folder = "D:\\New folder\\archive"
