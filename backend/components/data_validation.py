import os
import sys
import pandas as pd

from backend.constant import SCHEMA_FILE_PATH
from backend.entity.artifact_entity import DataValidationArtifact, DataIngestionArtifact
from backend.entity.config_entity import DataValidationConfig
from backend.exception import MyException
from backend.logger import logging
from backend.utils import read_yaml_file, write_yaml_file, read_csv

class DataValidation:
    def __init__ (self, data_validation_config: DataValidationConfig,
                  data_ingestion_artifact: DataIngestionArtifact) -> None:
        
        try:
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
            logging.info("DataValidation initialized.")
        except Exception as e:
            logging.error(f"Error initializing DataValidation: {e}")
            raise MyException(e, sys) from e
    
    def _get_schema_details(self) -> dict:
        try:
            return self._schema_config.get("columns", {})
        except Exception as e:
            logging.error(f"Error reading schema details: {e}")
            raise MyException(e, sys) from e
    
    def _validate_number_of_columns(self, df: pd.DataFrame) -> bool:
        try:
            expected_columns = self._get_schema_details()
            if len(df.columns) != len(expected_columns):
                logging.warning(f"Expected {len(expected_columns)} columns, but got {len(df.columns)}")
                return False
            return True
        except Exception as e:
            logging.error(f"Error validating number of columns: {e}")
            raise MyException(e, sys) from e
        
    def _validate_if_columns_exist(self, df: pd.DataFrame) -> bool:
        try:
            expected_columns = self._get_schema_details()
            missing_columns = [col for col in expected_columns if col not in df.columns]
            if missing_columns:
                self.validation_messages.append(f"Missing columns: {missing_columns}")
                logging.warning(f"Missing columns: {missing_columns}")
                return False
            return True
        except Exception as e:
            logging.error(f"Error validating column existence: {e}")
            raise MyException(e, sys) from e


    def initialize_data_validation(self) -> DataValidationArtifact:
        try:
            logging.info("Starting data validation process.")

            train_df = read_csv(self.data_ingestion_artifact.trained_data_path)

            validation_status = True
            validation_messages = [] or ["Data validation passed successfully."]

            if not self._validate_number_of_columns(train_df):
                validation_status = False
                validation_messages.append("Number of columns does not match schema.")

            if not self._validate_if_columns_exist(train_df):
                validation_status = False
                validation_messages.append("Some expected columns are missing.")

            validation_report = {
                "validation_status": validation_status,
                "messages": validation_messages
            }

            write_yaml_file(self.data_validation_config.validation_report_file_path, validation_report)
            logging.info("Data validation completed.")

            return DataValidationArtifact(
                validation_status=validation_status,
                message="\n".join(validation_messages),
                validation_report_file_path=self.data_validation_config.validation_report_file_path
            )

        except Exception as e:
            logging.error(f"Error during data validation: {e}")
            raise MyException(e, sys) from e