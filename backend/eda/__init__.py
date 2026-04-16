import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

class EDA:
    def __init__(self, data_path: str):
        self.data_path = data_path
        self.data = None

    def load_data(self) -> pd.DataFrame:
        """Load data from the specified path."""
        try:
            self.data = pd.read_csv(self.data_path)
            return self.data
        except Exception as e:
            print(f"Error loading data: {e}")
            raise

    def plot_correlation_heatmap(self):
        """Plot a correlation heatmap of the features."""
        if self.data is None:
            raise ValueError("Data not loaded. Call load_data() first.")
        
        plt.figure(figsize=(10, 8))
        sns.heatmap(self.data.corr(), annot=True, cmap='coolwarm', linewidths=0.5)
        plt.title('Correlation Heatmap')
        plt.show()