"""
Complete data processing pipeline for telco churn prediction.
"""
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent))

from data.ingestion import load_raw_data
from data.cleaning import handle_missing_values, handle_data_types
from data.validation import validate_data_schema, validate_target_variable
from data.labeling import encode_target
from data.build_features import create_tenure_bins, create_revenue_features
from data.splitting import split_data, save_splits


def run_data_pipeline(raw_data_path: str = "data/raw/telco_churn.csv",
                     output_dir: str = "data/processed"):
    """
    Run the complete data processing pipeline.
    
    Args:
        raw_data_path: Path to raw data CSV
        output_dir: Directory to save processed data
    """
    print("=" * 60)
    print("Starting Data Processing Pipeline")
    print("=" * 60)
    
    # Step 1: Load raw data
    print("\n[1/7] Loading raw data...")
    df = load_raw_data(raw_data_path)
    print(f"✓ Loaded {len(df)} rows")
    
    # Step 2: Handle data types
    print("\n[2/7] Converting data types...")
    df = handle_data_types(df)
    print("✓ Data types converted")
    
    # Step 3: Clean data
    print("\n[3/7] Cleaning data...")
    df = handle_missing_values(df)
    print(f"✓ Cleaned data: {len(df)} rows remaining")
    
    # Step 4: Validate data
    print("\n[4/7] Validating data...")
    expected_cols = ['customerID', 'gender', 'tenure', 'MonthlyCharges', 
                     'TotalCharges', 'Churn']
    # Note: Add all expected columns based on your dataset
    validate_target_variable(df, target_col='Churn')
    print("✓ Data validated")
    
    # Step 5: Encode target
    print("\n[5/7] Encoding target variable...")
    df = encode_target(df, target_col='Churn')
    print("✓ Target encoded")
    
    # Step 6: Feature engineering
    print("\n[6/7] Engineering features...")
    if 'tenure' in df.columns:
        df = create_tenure_bins(df)
    if 'MonthlyCharges' in df.columns and 'tenure' in df.columns:
        df = create_revenue_features(df)
    print("✓ Features engineered")
    
    # Step 7: Split data
    print("\n[7/7] Splitting data into train/val/test sets...")
    X_train, X_val, X_test, y_train, y_val, y_test = split_data(
        df, target_col='Churn', test_size=0.2, val_size=0.2, random_state=42
    )
    
    # Save splits
    save_splits(X_train, X_val, X_test, y_train, y_val, y_test, 
                output_dir=output_dir)
    
    print("\n" + "=" * 60)
    print("Data Pipeline Complete!")
    print("=" * 60)
    print(f"\nProcessed data saved to: {output_dir}/")
    print(f"  - train.csv: {len(X_train)} samples")
    print(f"  - val.csv: {len(X_val)} samples")
    print(f"  - test.csv: {len(X_test)} samples")
    print("\nReady for model training!")


def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Run telco churn data processing pipeline"
    )
    parser.add_argument(
        "--input", 
        type=str, 
        default="data/raw/telco_churn.csv",
        help="Path to raw data CSV"
    )
    parser.add_argument(
        "--output", 
        type=str, 
        default="data/processed",
        help="Output directory for processed data"
    )
    
    args = parser.parse_args()
    
    try:
        run_data_pipeline(args.input, args.output)
    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        print("\nPlease download the telco churn dataset from Kaggle:")
        print("  https://www.kaggle.com/datasets/denisexpsito/telco-customer-churn-ibm")
        print(f"\nAnd save it as: {args.input}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()


