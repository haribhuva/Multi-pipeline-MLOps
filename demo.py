from backend.pipeline.training_pipeline import TrainingPipeline

if __name__ == "__main__":
    try:
        training_pipeline = TrainingPipeline()
        data_ingestion_artifact = training_pipeline.start_data_ingestion()
        print(f"Data Ingestion Artifact: {data_ingestion_artifact}")
    except Exception as e:
        print(f"Error in main: {e}")