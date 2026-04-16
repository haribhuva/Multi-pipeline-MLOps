from backend.components.data_ingestion import DataIngestion
from backend.configration.postgres_client import PostgresClient
from backend.entity.artifact_entity import (DataIngestionArtifact, 
                                            DataValidationArtifact)
from backend.entity.config_entity import (DataIngestionConfig, 
                                          DataValidationConfig)
from backend.components.data_validation import DataValidation
from typing import Optional

import os
import sys

class TrainingPipeline:
    def __init__(self, data_ingestion: Optional[DataIngestion] = None):
        self.data_ingestion = data_ingestion or DataIngestion(
            data_ingestion_config=DataIngestionConfig(),
            postgres_client=PostgresClient(),
            data_artifact=DataIngestionArtifact(trained_data_path="", test_data_path="")
        )

    def start_data_ingestion(self):
        try:
            df = self.data_ingestion.export_data_into_feature_store()
            data_ingestion_artifact = self.data_ingestion.split_data_as_train_test(df)
            return data_ingestion_artifact
        except Exception as e:
            print(f"Error in start_data_ingestion: {e}")
            raise e
        
    def start_validation(self, data_ingestion_artifact: DataIngestionArtifact) -> DataValidationArtifact:
        try:
            data_validation = DataValidation(
                data_validation_config=DataValidationConfig(),
                data_ingestion_artifact=data_ingestion_artifact
            )

            data_validation_artifact = data_validation.initialize_data_validation()
            return data_validation_artifact
        
        except Exception as e:
            print(f"Error in start_validation: {e}")
            raise e