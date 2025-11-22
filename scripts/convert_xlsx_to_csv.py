#!/usr/bin/env python3
"""
Convert Excel file to CSV for MLOps pipeline.

Simple one-time conversion script. Run once after downloading the data from Kaggle.

Usage:
    python scripts/convert_xlsx_to_csv.py
"""
import pandas as pd
from pathlib import Path


def convert_xlsx_to_csv(
    input_file: str = "data/raw/customer_churn_dataset.xlsx",
    output_file: str = "data/raw/telco_churn.csv",
    drop_customer_id: bool = True
):
    """
    Convert Excel file to CSV with data cleaning.
    
    Args:
        input_file: Path to input Excel file
        output_file: Path to output CSV file
        drop_customer_id: Whether to drop customerID column (default: True)
    """
    print("=" * 60)
    print("Excel → CSV Conversion")
    print("=" * 60)
    
    # Check if input file exists
    input_path = Path(input_file)
    if not input_path.exists():
        print(f"\n❌ Error: {input_file} not found!")
        print("Please download the dataset from Kaggle first.")
        return
    
    # Load Excel file
    print(f"\n[1/4] Loading {input_file}...")
    df = pd.read_excel(input_file)
    print(f"✓ Loaded {len(df)} rows, {len(df.columns)} columns")
    
    # Fix TotalCharges data type (object → numeric)
    print("\n[2/4] Fixing data types...")
    if 'TotalCharges' in df.columns:
        df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
        df['TotalCharges'].fillna(0, inplace=True)
        print("✓ TotalCharges converted to numeric")
    
    # Drop customerID if requested
    if drop_customer_id and 'customerID' in df.columns:
        print("\n[3/4] Dropping customerID column...")
        df = df.drop(columns=['customerID'])
        print("✓ customerID removed")
    else:
        print("\n[3/4] Keeping all columns...")
    
    # Save as CSV
    print(f"\n[4/4] Saving to {output_file}...")
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_file, index=False)
    print(f"✓ Saved {len(df)} rows, {len(df.columns)} columns")
    
    print("\n" + "=" * 60)
    print("Conversion Complete!")
    print("=" * 60)
    print(f"\n✅ CSV file ready: {output_file}")
    print("Now you can run: python src/pipeline.py")
    print("Or use: make data")


if __name__ == "__main__":
    # Simple usage - no arguments needed
    convert_xlsx_to_csv()

