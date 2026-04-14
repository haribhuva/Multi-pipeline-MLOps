from dataclasses import dataclass


@dataclass
class DataIngestionArtifact:
    """Paths to the ingested train and test CSV files."""
    trained_data_path: str
    test_data_path: str