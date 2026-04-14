import os
import sys
import pandas as pd

from sklearn.model_selection import train_test_split

from backend.configration.postgres_client import PostgresClient
from backend.entity.artifact_entity import DataIngestionArtifact
from backend.entity.config_entity import DataIngestionConfig
from backend.exception import MyException
from backend.logger import logging
from backend.utils import query
from backend.constant import (DATA_INGESTION_DIR_NAME, 
                              DATA_INGESTION_FEATURE_STORE_DIR, 
                              DATA_INGESTION_INGESTED_DIR, 
                              DATA_SPLIT_RATIO, 
                              TRAIN_FILE_NAME, 
                              TEST_FILE_NAME)

class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig, 
                 postgres_client: PostgresClient, 
                 data_artifact: DataIngestionArtifact):
        
        self.data_ingestion_config = data_ingestion_config
        self.postgres_client = postgres_client
        self.data_artifact = data_artifact

    def export_data_into_feature_store(self) -> pd.DataFrame:
        try:
            logging.info("Exporting data from MongoDB to feature store")
            df = query(self.postgres_client, self.data_ingestion_config.data_collection_name)
            feature_store_dir = os.path.dirname(self.data_ingestion_config.feature_store_file_path)
            os.makedirs(feature_store_dir, exist_ok=True)
            df.to_csv(self.data_ingestion_config.feature_store_file_path, index=False)
            return df
        except Exception as e:
            logging.error(f"Error exporting data to feature store: {e}")
            raise MyException(e, sys) from e
        
    def split_data_as_train_test(self, df: pd.DataFrame) -> DataIngestionArtifact:
        try:
            logging.info("Splitting data into train and test sets")
            train_df, test_df = train_test_split(df, test_size=DATA_SPLIT_RATIO, random_state=42)
            ingested_dir = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(ingested_dir, exist_ok=True)
            train_df.to_csv(self.data_ingestion_config.training_file_path, index=False)
            test_df.to_csv(self.data_ingestion_config.testing_file_path, index=False)
            return DataIngestionArtifact(
                trained_data_path=self.data_ingestion_config.training_file_path,
                test_data_path=self.data_ingestion_config.testing_file_path
            )
        except Exception as e:
            logging.error(f"Error splitting data into train and test sets: {e}")
            raise MyException(e, sys) from e