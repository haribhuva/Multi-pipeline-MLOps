import pandas as pd

from backend.configration.postgres_client import PostgresClient


def query(postgres_client: PostgresClient, table_name: str) -> pd.DataFrame:
	"""Read a full table from PostgreSQL into a pandas DataFrame."""
	postgres_client.connect()
	try:
		return pd.read_sql_query(f"SELECT * FROM {table_name}", postgres_client.connection)
	finally:
		postgres_client.close()