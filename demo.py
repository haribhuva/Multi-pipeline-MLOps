from backend.logger import logging
from backend.exception import MyException
import sys

def main():
    logging.info("Starting the multi-pipeline-mlops demo.")
    try:
        # Simulate some work that could raise an exception
        raise ValueError("This is a demo error for testing MyException.")
    except Exception as e:
        logging.error("An error occurred in main.")
        raise MyException(str(e), sys) from e