from backend.configration.create_database import CreateDatabase
from backend.configration.upload_csv import UploadCSV
from backend.logger import logging
from backend.exception import MyException


if __name__ == "__main__":
    try:
        logging.info("Starting database creation and CSV upload process")
        
        # Create database if it doesn't exist
        db_creator = CreateDatabase()
        db_creator.connect_database()
        
        # Upload CSV files to the database
        csv_uploader = UploadCSV()
        csv_uploader.upload_csv_to_db()
        
        logging.info("Database creation and CSV upload process completed successfully")
    except MyException as e:
        logging.error(f"An error occurred: {e}")