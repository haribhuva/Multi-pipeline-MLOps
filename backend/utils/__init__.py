from __future__ import annotations

import sys
import dill
import yaml
import logging
import numpy as np
import pandas as pd

from pathlib import Path
from typing import Any

from backend.exception import MyException
from backend.configration.postgres_client import PostgresClient

def query(postgres_client: PostgresClient, table_name: str) -> pd.DataFrame:
    """
    Read a full table from PostgreSQL into a pandas DataFrame.

    NOTE:
    This assumes PostgresClient internally manages a SQLAlchemy engine
    or a correctly scoped connection.
    """
    try:
        postgres_client.connect()
        return pd.read_sql(f"SELECT * FROM {table_name}", postgres_client.connection)
    except Exception as e:
        raise MyException(e, sys) from e
    finally:
        postgres_client.close()

def read_yaml_file(file_path: Path) -> dict[str, Any]:
    """
    Load a YAML file and return its contents.

    Contract:
    - Caller must pass a resolved or resolvable Path
    - No assumptions about CWD
    """
    try:
        file_path = Path(file_path).resolve()
        logging.info(f"Reading YAML file: {file_path}")

        if not file_path.exists():
            raise FileNotFoundError(f"YAML file not found: {file_path}")

        with file_path.open("r", encoding="utf-8") as yaml_file:
            return yaml.safe_load(yaml_file)

    except Exception as e:
        raise MyException(e, sys) from e


def write_yaml_file(
    file_path: Path,
    content: Any,
    replace: bool = False
) -> None:
    """
    Write a Python object to a YAML file.
    """
    try:
        file_path = Path(file_path).resolve()
        logging.info(f"Writing YAML file: {file_path}")

        file_path.parent.mkdir(parents=True, exist_ok=True)

        if replace and file_path.exists():
            file_path.unlink()

        with file_path.open("w", encoding="utf-8") as file:
            yaml.safe_dump(content, file)

    except Exception as e:
        raise MyException(e, sys) from e

def save_object(file_path: Path, obj: Any) -> None:
    """
    Serialize an object to disk using dill.
    """
    try:
        file_path = Path(file_path).resolve()
        logging.info(f"Saving object to: {file_path}")

        file_path.parent.mkdir(parents=True, exist_ok=True)

        with file_path.open("wb") as file_obj:
            dill.dump(obj, file_obj)

    except Exception as e:
        raise MyException(e, sys) from e


def load_object(file_path: Path) -> Any:
    """
    Deserialize a dill-pickled object from disk.
    """
    try:
        file_path = Path(file_path).resolve()
        logging.info(f"Loading object from: {file_path}")

        if not file_path.exists():
            raise FileNotFoundError(f"Object file not found: {file_path}")

        with file_path.open("rb") as file_obj:
            return dill.load(file_obj)

    except Exception as e:
        raise MyException(e, sys) from e

def save_numpy_array_data(file_path: Path, array: np.ndarray) -> None:
    """
    Save a NumPy array to a .npy file.
    """
    try:
        file_path = Path(file_path).resolve()
        file_path.parent.mkdir(parents=True, exist_ok=True)

        with file_path.open("wb") as file_obj:
            np.save(file_obj, array)

    except Exception as e:
        raise MyException(e, sys) from e


def load_numpy_array_data(file_path: Path) -> np.ndarray:
    """
    Load a NumPy array from a .npy file.
    """
    try:
        file_path = Path(file_path).resolve()

        if not file_path.exists():
            raise FileNotFoundError(f"Numpy file not found: {file_path}")

        with file_path.open("rb") as file_obj:
            return np.load(file_obj)

    except Exception as e:
        raise MyException(e, sys) from e

def read_csv(file_path: Path) -> pd.DataFrame:
    """
    Read a CSV file into a pandas DataFrame.
    """
    try:
        file_path = Path(file_path).resolve()
        logging.info(f"Reading CSV file: {file_path}")

        if not file_path.exists():
            raise FileNotFoundError(f"CSV file not found: {file_path}")

        return pd.read_csv(file_path)

    except Exception as e:
        raise MyException(e, sys) from e


def resolve_target_column(df: pd.DataFrame, configured: str) -> str:
    """
    Resolve the target column name using a priority order.
    """
    for col in (configured, "life_ratio"):
        if col and col in df.columns:
            logging.info(f"Resolved target column: {col}")
            return col

    raise ValueError(
        f"Target column not found. "
        f"Configured='{configured}', Available={list(df.columns)}"
    )


def split_features_target(
    df: pd.DataFrame,
    target_col: str
) -> tuple[pd.DataFrame, pd.Series]:
    """
    Split DataFrame into features (X) and target (y).
    """
    return df.drop(columns=[target_col]), df[target_col]

def get_latest_test_data_path(artifact_root: Path) -> Path | None:
    """
    Find the most recent test.csv under an artifact root.

    NOTE:
    - No assumptions about directory layout outside artifact_root
    - Caller controls artifact_root
    """
    try:
        artifact_root = Path(artifact_root).resolve()

        if not artifact_root.exists():
            return None

        run_dirs = [
            d for d in artifact_root.iterdir()
            if d.is_dir() and "_" in d.name
        ]

        for run_dir in sorted(
            run_dirs,
            key=lambda d: d.stat().st_mtime,
            reverse=True
        ):
            test_path = run_dir / "data_ingestion" / "ingested" / "test.csv"
            if test_path.exists():
                return test_path

        return None

    except Exception as e:
        logging.warning(f"Failed to locate latest test data: {e}")
        return None