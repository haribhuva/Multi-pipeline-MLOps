import os
import sys
import psycopg2
import sqlite3

from backend.constant import POSTGRE_SQL_PASSWORD, DATABASE_NAME, USER, HOST, DB_PORT
from backend.exception import MyException
from backend.logger import logging

class PostgresClient:
    def __init__(self):
        self.connection = None

    def connect(self):
        try:
            db_name = (DATABASE_NAME or "").lower()
            self.connection = psycopg2.connect(
                host=HOST,
                user=USER,
                password=POSTGRE_SQL_PASSWORD,
                port=DB_PORT,
                dbname=db_name
            )
            logging.info("Connected to PostgreSQL database successfully.")
        except Exception as e:
            logging.error(f"Failed to connect to PostgreSQL database: {e}")
            raise MyException(e, sys)

    def close(self):
        if self.connection:
            self.connection.close()
            logging.info("PostgreSQL database connection closed.")