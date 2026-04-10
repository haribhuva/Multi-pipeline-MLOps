import os
import pandas as pd
import sys

from backend.configration.create_database import CreateDatabase
from backend.logger import logging
from backend.exception import MyException
from backend.constant import csv_folder

class UploadCSV:
    def __init__(self):
        self.db = CreateDatabase()
        self.engine = self.db.create_engine()

    def upload_csv_to_db(self):
        try:
            for filename in os.listdir(csv_folder):
                if filename.endswith(".csv"):
                    file_path = os.path.join(csv_folder, filename)
                    logging.info(f"Processing file: {file_path}")
                    df = pd.read_csv(file_path)
                    table_name = os.path.splitext(filename)[0]
                    df.to_sql(table_name, self.engine, if_exists='replace', index=False)
                    logging.info(f"Uploaded '{filename}' to database as table '{table_name}'")
        except Exception as e:
            logging.error(f"Error uploading CSV to database: {e}")
            raise MyException(e, sys)