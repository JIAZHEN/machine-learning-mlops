"""
Training module for churn prediction model.
"""
import yaml
import os
import sys
from pathlib import Path
from dataloader import ChurnDataLoader
from preprocessing import ChurnPreprocessor
from model import ChurnModel
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, roc_auc_score,
    classification_report, confusion_matrix
)
import mlflow
import mlflow.sklearn
import numpy as np


def train_model(config_path: str = "configs/model1.yaml"):
    """
    Train churn prediction model.
    
    Args:
        config_path: Path to configuration file (relative to project root)
    """
    # Get project root (3 levels up from this file: model1 -> models -> src -> root)
    project_root = Path(__file__).resolve().parent.parent.parent.parent
    
    # Resolve config path relative to project root
    config_file = project_root / config_path
    
    if not config_file.exists():
        raise FileNotFoundError(f"Config file not found: {config_file}\nProject root: {project_root}")
    
    # Load configuration
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)
    
    # Update paths to be relative to project root
    config['data_dir'] = str(project_root / config.get('data_dir', 'data/processed'))
    config['model_dir'] = str(project_root / config.get('model_dir', 'models'))
    
    print("=" * 50)
    print("Starting model training...")
    print("=" * 50)
    
    # Initialize data loader
    data_loader = ChurnDataLoader(data_dir=config.get('data_dir', 'data/processed'))
    
    # Load data
    print("\nLoading data...")
    X_train, y_train = data_loader.load_train_data()
    X_val, y_val = data_loader.load_val_data()
    
    print(f"Training samples: {len(X_train)}")
    print(f"Validation samples: {len(X_val)}")
    
    # Preprocess data
    print("\nPreprocessing data...")
    preprocessor = ChurnPreprocessor()
    X_train_transformed = preprocessor.fit_transform(X_train)
    X_val_transformed = preprocessor.transform(X_val)
    
    # Set MLflow tracking to use SQLite backend (avoids filesystem deprecation warning)
    project_root = Path(__file__).resolve().parent.parent.parent.parent
    mlflow_db = project_root / "mlflow.db"
    mlflow.set_tracking_uri(f"sqlite:///{mlflow_db}")
    
    # Start MLflow run
    mlflow.set_experiment(config.get('experiment_name', 'telco_churn'))
    
    with mlflow.start_run(run_name=config.get('run_name', 'churn_model_v1')):
        # Log parameters
        mlflow.log_params(config.get('model_params', {}))
        
        # Initialize and train model
        print("\nTraining model...")
        model = ChurnModel(**config.get('model_params', {}))
        model.fit(X_train_transformed, y_train)
        
        # Evaluate on training set
        y_train_pred = model.predict(X_train_transformed)
        y_train_proba = model.predict_proba(X_train_transformed)[:, 1]
        
        train_accuracy = accuracy_score(y_train, y_train_pred)
        train_precision = precision_score(y_train, y_train_pred)
        train_recall = recall_score(y_train, y_train_pred)
        train_f1 = f1_score(y_train, y_train_pred)
        train_auc = roc_auc_score(y_train, y_train_proba)
        
        # Evaluate on validation set
        y_val_pred = model.predict(X_val_transformed)
        y_val_proba = model.predict_proba(X_val_transformed)[:, 1]
        
        val_accuracy = accuracy_score(y_val, y_val_pred)
        val_precision = precision_score(y_val, y_val_pred)
        val_recall = recall_score(y_val, y_val_pred)
        val_f1 = f1_score(y_val, y_val_pred)
        val_auc = roc_auc_score(y_val, y_val_proba)
        
        # Log metrics
        mlflow.log_metrics({
            'train_accuracy': train_accuracy,
            'train_precision': train_precision,
            'train_recall': train_recall,
            'train_f1': train_f1,
            'train_auc': train_auc,
            'val_accuracy': val_accuracy,
            'val_precision': val_precision,
            'val_recall': val_recall,
            'val_f1': val_f1,
            'val_auc': val_auc
        })
        
        # Print metrics using sklearn's classification_report
        print("\n" + "=" * 70)
        print("TRAINING SET RESULTS:")
        print("=" * 70)
        print(f"\nAccuracy: {train_accuracy:.4f}")
        print(f"AUC-ROC:  {train_auc:.4f}\n")
        print("Classification Report:")
        print(classification_report(y_train, y_train_pred, 
                                    target_names=['No Churn', 'Churn'],
                                    digits=4))
        
        print("\n" + "=" * 70)
        print("VALIDATION SET RESULTS:")
        print("=" * 70)
        print(f"\nAccuracy: {val_accuracy:.4f}")
        print(f"AUC-ROC:  {val_auc:.4f}\n")
        print("Classification Report:")
        print(classification_report(y_val, y_val_pred, 
                                    target_names=['No Churn', 'Churn'],
                                    digits=4))
        
        print("\nConfusion Matrix (Validation):")
        cm = confusion_matrix(y_val, y_val_pred)
        print(f"                Predicted")
        print(f"                No    Yes")
        print(f"Actual  No    {cm[0,0]:5d} {cm[0,1]:5d}")
        print(f"        Yes   {cm[1,0]:5d} {cm[1,1]:5d}")
        print("=" * 70)
        
        # Save model and preprocessor
        model_dir = Path(config.get('model_dir', 'models'))
        model_dir.mkdir(parents=True, exist_ok=True)
        
        model.save(model_dir / "churn_model.pkl")
        preprocessor.save(model_dir / "preprocessor.pkl")
        
        # Create input example for model signature
        input_example = X_train_transformed[:5]  # First 5 rows as example
        
        # Log model to MLflow with signature
        # Using signature inference to avoid artifact_path deprecation warning
        from mlflow.models.signature import infer_signature
        signature = infer_signature(X_train_transformed, y_train_pred)
        
        mlflow.sklearn.log_model(
            sk_model=model.model,
            signature=signature,
            input_example=input_example,
            registered_model_name="telco_churn_model"
        )
        
    print("\nTraining complete!")


def main():
    """Main function for training."""
    train_model()


if __name__ == "__main__":
    main()


