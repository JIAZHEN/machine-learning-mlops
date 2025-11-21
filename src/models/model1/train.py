"""
Training module for churn prediction model.
"""
import yaml
from pathlib import Path
from dataloader import ChurnDataLoader
from preprocessing import ChurnPreprocessor
from model import ChurnModel
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
import mlflow
import mlflow.sklearn


def train_model(config_path: str = "configs/model1.yaml"):
    """
    Train churn prediction model.
    
    Args:
        config_path: Path to configuration file
    """
    # Load configuration
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
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
        
        # Print metrics
        print("\n" + "=" * 50)
        print("Training Results:")
        print("=" * 50)
        print(f"Train Accuracy:  {train_accuracy:.4f}")
        print(f"Train Precision: {train_precision:.4f}")
        print(f"Train Recall:    {train_recall:.4f}")
        print(f"Train F1:        {train_f1:.4f}")
        print(f"Train AUC:       {train_auc:.4f}")
        print("\nValidation Results:")
        print(f"Val Accuracy:    {val_accuracy:.4f}")
        print(f"Val Precision:   {val_precision:.4f}")
        print(f"Val Recall:      {val_recall:.4f}")
        print(f"Val F1:          {val_f1:.4f}")
        print(f"Val AUC:         {val_auc:.4f}")
        print("=" * 50)
        
        # Save model and preprocessor
        model_dir = Path(config.get('model_dir', 'models'))
        model_dir.mkdir(parents=True, exist_ok=True)
        
        model.save(model_dir / "churn_model.pkl")
        preprocessor.save(model_dir / "preprocessor.pkl")
        
        # Log model to MLflow
        mlflow.sklearn.log_model(model.model, "model")
        
    print("\nTraining complete!")


def main():
    """Main function for training."""
    train_model()


if __name__ == "__main__":
    main()

