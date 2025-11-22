#!/usr/bin/env python3
"""
Demo script to show before/after categorical encoding.
Run this after the pipeline completes to see the transformation.
"""
import pandas as pd
from pathlib import Path


def show_before_after_comparison():
    """Compare data before and after encoding."""
    
    print("=" * 80)
    print("CATEGORICAL ENCODING: BEFORE vs AFTER")
    print("=" * 80)
    
    # Check if processed data exists
    train_path = Path("data/processed/train.csv")
    
    if not train_path.exists():
        print("\n❌ Processed data not found!")
        print("Please run the pipeline first:")
        print("  python src/pipeline.py")
        return
    
    # Load processed data
    df = pd.read_csv(train_path)
    
    print("\n📊 AFTER ENCODING (Current State):")
    print(f"  Total columns: {len(df.columns)}")
    print(f"  Total rows: {len(df)}")
    
    # Check data types
    object_cols = df.select_dtypes(include=['object']).columns.tolist()
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    
    print(f"\n  Categorical (text) columns: {len(object_cols)}")
    if object_cols:
        print(f"    {object_cols}")
        print("\n    ⚠️  WARNING: Still have text columns! Run updated pipeline.")
    else:
        print("    ✅ None - All categorical features encoded!")
    
    print(f"\n  Numeric columns: {len(numeric_cols)}")
    
    # Show sample of column names
    print("\n📋 Sample of column names:")
    for i, col in enumerate(df.columns[:20]):
        dtype = df[col].dtype
        unique_vals = df[col].nunique()
        print(f"  {i+1:2d}. {col:30s} | dtype: {str(dtype):8s} | unique: {unique_vals:4d}")
    
    if len(df.columns) > 20:
        print(f"  ... and {len(df.columns) - 20} more columns")
    
    # Show sample row
    print("\n📄 Sample row (first 10 columns):")
    print(df.iloc[0, :10].to_dict())
    
    # Show summary statistics
    print("\n📈 Summary Statistics:")
    print(f"  - All numeric: {'✅ YES' if len(object_cols) == 0 else '❌ NO'}")
    print(f"  - Ready for ML models: {'✅ YES' if len(object_cols) == 0 else '❌ NO'}")
    print(f"  - Binary columns (0/1 only): {sum(df[col].nunique() == 2 for col in numeric_cols)}")
    print(f"  - Continuous columns: {sum(df[col].nunique() > 10 for col in numeric_cols)}")
    
    # Check for one-hot encoded columns
    onehot_cols = [col for col in df.columns if '_' in col and any(
        prefix in col for prefix in ['gender', 'Partner', 'Contract', 'InternetService']
    )]
    
    if onehot_cols:
        print(f"\n✅ One-hot encoded columns detected: {len(onehot_cols)}")
        print("  Examples:")
        for col in onehot_cols[:10]:
            print(f"    - {col}")
        if len(onehot_cols) > 10:
            print(f"    ... and {len(onehot_cols) - 10} more")
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    show_before_after_comparison()

