"""
Feature engineering module for creating and transforming features.
"""
import pandas as pd
import numpy as np


def create_tenure_bins(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create binned tenure features.
    
    Args:
        df: Input DataFrame
        
    Returns:
        DataFrame with tenure bins
    """
    df_feat = df.copy()
    
    if 'tenure' in df_feat.columns:
        df_feat['tenure_bin'] = pd.cut(df_feat['tenure'], 
                                        bins=[0, 12, 24, 48, 72],
                                        labels=['0-1yr', '1-2yr', '2-4yr', '4+yr'])
    
    return df_feat


def create_revenue_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create revenue-related features.
    
    Args:
        df: Input DataFrame
        
    Returns:
        DataFrame with revenue features
    """
    df_feat = df.copy()
    
    if 'MonthlyCharges' in df_feat.columns and 'tenure' in df_feat.columns:
        # Average monthly charges over tenure
        df_feat['avg_monthly_charges'] = df_feat['TotalCharges'] / (df_feat['tenure'] + 1)
    
    return df_feat


def main():
    """Main function for feature engineering."""
    pass


if __name__ == "__main__":
    main()

