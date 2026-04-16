from backend.pipeline.training_pipeline import TrainingPipeline

if __name__ == "__main__":
    training_pipeline = TrainingPipeline()
    data_ingestion_artifact = training_pipeline.start_data_ingestion()
    data_validation_artifact = training_pipeline.start_validation(data_ingestion_artifact)
    print(f"Data Validation Artifact: {data_validation_artifact}")