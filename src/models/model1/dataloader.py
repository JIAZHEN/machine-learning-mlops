"""
DataLoader module for loading and preparing data for model training.
"""
import pandas as pd
from pathlib import Path
from typing import Tuple


class ChurnDataLoader:
    """DataLoader for telco churn dataset."""
    
    def __init__(self, data_dir: str = "data/processed"):
        self.data_dir = Path(data_dir)
    
    def load_train_data(self) -> Tuple[pd.DataFrame, pd.Series]:
        """
        Load training data.
        
        Returns:
            Tuple of (X_train, y_train)
        """
        train_path = self.data_dir / "train.csv"
        
        if not train_path.exists():
            raise FileNotFoundError(f"Training data not found at {train_path}")
        
        df = pd.read_csv(train_path)
        X = df.drop(columns=['Churn'])
        y = df['Churn']
        
        return X, y
    
    def load_val_data(self) -> Tuple[pd.DataFrame, pd.Series]:
        """
        Load validation data.
        
        Returns:
            Tuple of (X_val, y_val)
        """
        val_path = self.data_dir / "val.csv"
        
        if not val_path.exists():
            raise FileNotFoundError(f"Validation data not found at {val_path}")
        
        df = pd.read_csv(val_path)
        X = df.drop(columns=['Churn'])
        y = df['Churn']
        
        return X, y
    
    def load_test_data(self) -> Tuple[pd.DataFrame, pd.Series]:
        """
        Load test data.
        
        Returns:
            Tuple of (X_test, y_test)
        """
        test_path = self.data_dir / "test.csv"
        
        if not test_path.exists():
            raise FileNotFoundError(f"Test data not found at {test_path}")
        
        df = pd.read_csv(test_path)
        X = df.drop(columns=['Churn'])
        y = df['Churn']
        
        return X, y
    
    def load_raw_data(self, filepath: str = "data/raw/telco_churn.csv") -> pd.DataFrame:
        """
        Load raw data.
        
        Args:
            filepath: Path to raw data file
            
        Returns:
            Raw data DataFrame
        """
        raw_path = Path(filepath)
        
        if not raw_path.exists():
            raise FileNotFoundError(f"Raw data not found at {raw_path}")
        
        return pd.read_csv(raw_path)


def main():
    """Main function for data loading."""
    pass


if __name__ == "__main__":
    main()


