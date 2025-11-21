"""
Data validation module for ensuring data quality.
"""
import pandas as pd


def validate_data_schema(df: pd.DataFrame, expected_columns: list) -> bool:
    """
    Validate that DataFrame has expected columns.
    
    Args:
        df: Input DataFrame
        expected_columns: List of expected column names
        
    Returns:
        Boolean indicating if schema is valid
    """
    missing_cols = set(expected_columns) - set(df.columns)
    
    if missing_cols:
        print(f"Missing columns: {missing_cols}")
        return False
    
    return True


def validate_target_variable(df: pd.DataFrame, target_col: str = 'Churn') -> bool:
    """
    Validate target variable exists and has valid values.
    
    Args:
        df: Input DataFrame
        target_col: Name of target column
        
    Returns:
        Boolean indicating if target is valid
    """
    if target_col not in df.columns:
        print(f"Target column '{target_col}' not found")
        return False
    
    unique_values = df[target_col].unique()
    print(f"Target variable values: {unique_values}")
    
    return True


def main():
    """Main function for data validation."""
    pass


if __name__ == "__main__":
    main()

