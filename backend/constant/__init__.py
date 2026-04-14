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

PIPELINE_NAME: str = ""
ARTIFACT_DIR: str = "artifact"

DATA_INGESTION_COLLECTION_NAME: str = "orders_reviews_nlp"
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_SPLIT_RATIO: float = 0.2

TRAIN_FILE_NAME: str = "train.csv"
TEST_FILE_NAME: str = "test.csv"
FILE_NAME: str = "data.csv"