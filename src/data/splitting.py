"""
Data splitting module for train/validation/test splits.
"""
import pandas as pd
from sklearn.model_selection import train_test_split
from pathlib import Path


def split_data(df: pd.DataFrame, target_col: str = 'Churn', 
               test_size: float = 0.2, val_size: float = 0.2,
               random_state: int = 42):
    """
    Split data into train, validation, and test sets.
    
    Args:
        df: Input DataFrame
        target_col: Name of target column
        test_size: Proportion for test set
        val_size: Proportion of training data for validation
        random_state: Random seed for reproducibility
        
    Returns:
        Tuple of (X_train, X_val, X_test, y_train, y_val, y_test)
    """
    # Separate features and target
    X = df.drop(columns=[target_col])
    y = df[target_col]
    
    # First split: train+val vs test
    X_temp, X_test, y_temp, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    
    # Second split: train vs val
    X_train, X_val, y_train, y_val = train_test_split(
        X_temp, y_temp, test_size=val_size, random_state=random_state, stratify=y_temp
    )
    
    print(f"Train size: {len(X_train)}")
    print(f"Validation size: {len(X_val)}")
    print(f"Test size: {len(X_test)}")
    
    return X_train, X_val, X_test, y_train, y_val, y_test


def save_splits(X_train, X_val, X_test, y_train, y_val, y_test, 
                output_dir: str = "data/processed"):
    """
    Save data splits to CSV files.
    
    Args:
        X_train, X_val, X_test: Feature DataFrames
        y_train, y_val, y_test: Target Series
        output_dir: Directory to save splits
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Combine features and target
    train_df = X_train.copy()
    train_df['Churn'] = y_train.values
    
    val_df = X_val.copy()
    val_df['Churn'] = y_val.values
    
    test_df = X_test.copy()
    test_df['Churn'] = y_test.values
    
    # Save to CSV
    train_df.to_csv(output_path / "train.csv", index=False)
    val_df.to_csv(output_path / "val.csv", index=False)
    test_df.to_csv(output_path / "test.csv", index=False)
    
    print(f"Saved splits to {output_dir}")


def main():
    """Main function for data splitting."""
    pass


if __name__ == "__main__":
    main()

