"""
Categorical encoding module for converting text features to numeric.
"""
import pandas as pd
from typing import List, Optional


def encode_categorical_features(df: pd.DataFrame, 
                                encoding_type: str = 'onehot',
                                exclude_cols: Optional[List[str]] = None) -> pd.DataFrame:
    """
    Encode categorical features to numeric format.
    
    Args:
        df: Input DataFrame
        encoding_type: Type of encoding ('onehot' or 'label')
        exclude_cols: Columns to exclude from encoding (e.g., target, already numeric)
        
    Returns:
        DataFrame with encoded categorical features
    """
    df_encoded = df.copy()
    
    # Default columns to exclude
    if exclude_cols is None:
        exclude_cols = ['Churn']  # Target variable already encoded
    
    # Identify categorical columns (object/string dtype)
    categorical_cols = df_encoded.select_dtypes(include=['object']).columns.tolist()
    categorical_cols = [col for col in categorical_cols if col not in exclude_cols]
    
    if len(categorical_cols) == 0:
        print("  No categorical columns to encode")
        return df_encoded
    
    print(f"  Encoding {len(categorical_cols)} categorical columns...")
    
    if encoding_type == 'onehot':
        # One-hot encoding (creates binary columns for each category)
        df_encoded = pd.get_dummies(df_encoded, columns=categorical_cols, drop_first=False, dtype=int)
        print(f"  ✓ One-hot encoding complete: {len(df_encoded.columns)} total columns")
        
    elif encoding_type == 'label':
        # Label encoding (converts to integers 0, 1, 2, ...)
        from sklearn.preprocessing import LabelEncoder
        
        for col in categorical_cols:
            le = LabelEncoder()
            df_encoded[col] = le.fit_transform(df_encoded[col].astype(str))
        
        print(f"  ✓ Label encoding complete: {len(categorical_cols)} columns encoded")
    
    else:
        raise ValueError(f"Unknown encoding_type: {encoding_type}. Use 'onehot' or 'label'")
    
    return df_encoded


def encode_binary_features(df: pd.DataFrame, 
                           binary_cols: Optional[List[str]] = None) -> pd.DataFrame:
    """
    Encode binary Yes/No features to 1/0.
    
    Args:
        df: Input DataFrame
        binary_cols: List of binary columns to encode. If None, auto-detect.
        
    Returns:
        DataFrame with encoded binary features
    """
    df_encoded = df.copy()
    
    if binary_cols is None:
        # Auto-detect columns with only Yes/No values
        binary_cols = []
        for col in df_encoded.select_dtypes(include=['object']).columns:
            unique_vals = df_encoded[col].dropna().unique()
            if set(unique_vals).issubset({'Yes', 'No'}):
                binary_cols.append(col)
    
    if len(binary_cols) == 0:
        return df_encoded
    
    print(f"  Encoding {len(binary_cols)} binary Yes/No columns to 1/0...")
    
    for col in binary_cols:
        if col in df_encoded.columns:
            df_encoded[col] = df_encoded[col].map({'Yes': 1, 'No': 0})
    
    return df_encoded


def get_categorical_columns(df: pd.DataFrame, exclude_cols: Optional[List[str]] = None) -> List[str]:
    """
    Get list of categorical columns in DataFrame.
    
    Args:
        df: Input DataFrame
        exclude_cols: Columns to exclude
        
    Returns:
        List of categorical column names
    """
    if exclude_cols is None:
        exclude_cols = []
    
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
    categorical_cols = [col for col in categorical_cols if col not in exclude_cols]
    
    return categorical_cols


def main():
    """Main function for encoding."""
    pass


if __name__ == "__main__":
    main()

