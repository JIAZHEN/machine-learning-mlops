"""
Data ingestion module for loading raw data.
"""
import pandas as pd
from pathlib import Path


def load_raw_data(filepath: str) -> pd.DataFrame:
    """
    Load raw telco churn data from CSV.
    
    Args:
        filepath: Path to the raw CSV file
        
    Returns:
        DataFrame with raw data
    """
    df = pd.read_csv(filepath)
    return df


def main():
    """Main function to run data ingestion."""
    raw_data_path = Path("data/raw/telco_churn.csv")
    
    if not raw_data_path.exists():
        print(f"Error: {raw_data_path} not found.")
        print("Please download the dataset from Kaggle and place it in data/raw/")
        return
    
    df = load_raw_data(raw_data_path)
    print(f"Loaded {len(df)} rows and {len(df.columns)} columns")
    print(f"Columns: {list(df.columns)}")
    

if __name__ == "__main__":
    main()


