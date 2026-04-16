from dataclasses import dataclass


@dataclass
class DataIngestionArtifact:
    """Paths to the ingested train and test CSV files."""
    trained_data_path: str
    test_data_path: str

@dataclass
class DataValidationArtifact:
    """Path to the data validation report YAML file."""
    validation_status: bool
    message: str
    validation_report_file_path: str