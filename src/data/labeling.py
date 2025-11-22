"""
Data labeling module for target variable transformations.
"""
import pandas as pd


def encode_target(df: pd.DataFrame, target_col: str = 'Churn') -> pd.DataFrame:
    """
    Encode target variable to binary (0/1).
    
    Args:
        df: Input DataFrame
        target_col: Name of target column
        
    Returns:
        DataFrame with encoded target
    """
    df_labeled = df.copy()
    
    if target_col in df_labeled.columns:
        # Convert Yes/No to 1/0
        df_labeled[target_col] = df_labeled[target_col].map({'Yes': 1, 'No': 0})
    
    return df_labeled


def main():
    """Main function for data labeling."""
    pass


if __name__ == "__main__":
    main()


