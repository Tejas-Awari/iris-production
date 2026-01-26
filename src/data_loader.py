import pandas as pd
from sklearn.datasets import load_iris
import os

def load_and_save_raw_data(output_path: str = "data/raw/iris.csv") -> None:
    """
    Loads the Iris dataset from sklearn and saves it as a CSV.
    This simulates a raw data ingestion process (e.g., from a database).
    
    Args:
        output_path (str): The file path where the raw CSV will be saved.
    """
    # 1. Load data (Simulating extraction)
    print("⏳ Extracting data...")
    data = load_iris()
    
    # 2. Convert to DataFrame
    df = pd.DataFrame(data.data, columns=data.feature_names)
    df['target'] = data.target
    
    # 3. Ensure directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # 4. Save to CSV
    df.to_csv(output_path, index=False)
    print(f"✅ Data saved to {output_path}")

if __name__ == "__main__":
    load_and_save_raw_data()