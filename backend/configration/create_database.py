import psycopg2
import pandas as pd
import os
import sys
from pathlib import Path
from sqlalchemy import create_engine
from psycopg2 import sql

from backend.logger import logging
from backend.exception import MyException
from backend.constant import (
    POSTGRE_SQL_PASSWORD,
    DATABASE_NAME,
    USER,
    HOST,
    DB_PORT
)


class CreateDatabase:
    def __init__(self):
        pass

    @staticmethod
    def _normalized_db_name() -> str:
        # Postgres folds unquoted identifiers to lowercase; keep one canonical form.
        return DATABASE_NAME.lower()

    def connect_database(self):
        try:
            db_name = self._normalized_db_name()
            conn = psycopg2.connect(
                host=HOST,
                user=USER,
                password=POSTGRE_SQL_PASSWORD,
                port=DB_PORT
            )
            conn.autocommit = True
            cur = conn.cursor()

            cur.execute("SELECT 1 FROM pg_database WHERE datname=%s", (db_name,))
            exists = cur.fetchone()

            if not exists:
                cur.execute(sql.SQL("CREATE DATABASE {} ").format(sql.Identifier(db_name)))
                logging.info(f"Database '{db_name}' created")
            else:
                logging.info(f"Database '{db_name}' already exists")

        except Exception as e:
            logging.error(f"Database connection error: {e}")
            raise MyException(e, sys)

    def create_engine(self):
        try:
            db_name = self._normalized_db_name()
            engine = create_engine(
                f"postgresql://{USER}:{POSTGRE_SQL_PASSWORD}@{HOST}:{DB_PORT}/{db_name}"
            )
            return engine

        except Exception as e:
            logging.error(f"Engine creation error: {e}")
            raise MyException(e, sys)