"""
Prediction module for making predictions with trained churn model.
"""
import pandas as pd
from pathlib import Path
from model import ChurnModel
from preprocessing import ChurnPreprocessor


class ChurnPredictor:
    """Predictor class for churn prediction."""
    
    def __init__(self, model_path: str = "models/churn_model.pkl",
                 preprocessor_path: str = "models/preprocessor.pkl"):
        """
        Initialize predictor with trained model and preprocessor.
        
        Args:
            model_path: Path to trained model (relative to project root)
            preprocessor_path: Path to fitted preprocessor (relative to project root)
        """
        # Get project root (3 levels up from this file)
        project_root = Path(__file__).resolve().parent.parent.parent.parent
        
        # Resolve paths relative to project root
        model_file = project_root / model_path
        preprocessor_file = project_root / preprocessor_path
        
        if not model_file.exists():
            raise FileNotFoundError(f"Model not found: {model_file}\nPlease train the model first: make train")
        if not preprocessor_file.exists():
            raise FileNotFoundError(f"Preprocessor not found: {preprocessor_file}\nPlease train the model first: make train")
        
        self.model = ChurnModel.load(str(model_file))
        self.preprocessor = ChurnPreprocessor.load(str(preprocessor_file))
    
    def predict(self, X: pd.DataFrame) -> pd.DataFrame:
        """
        Make predictions on new data.
        
        Args:
            X: Features DataFrame
            
        Returns:
            DataFrame with predictions and probabilities
        """
        # Transform features
        X_transformed = self.preprocessor.transform(X)
        
        # Make predictions
        predictions = self.model.predict(X_transformed)
        probabilities = self.model.predict_proba(X_transformed)[:, 1]
        
        # Create results DataFrame
        results = pd.DataFrame({
            'prediction': predictions,
            'churn_probability': probabilities
        })
        
        return results
    
    def predict_single(self, customer_data: dict) -> dict:
        """
        Make prediction for a single customer.
        
        Args:
            customer_data: Dictionary with customer features
            
        Returns:
            Dictionary with prediction and probability
        """
        # Convert to DataFrame
        X = pd.DataFrame([customer_data])
        
        # Get prediction
        results = self.predict(X)
        
        return {
            'will_churn': bool(results['prediction'].iloc[0]),
            'churn_probability': float(results['churn_probability'].iloc[0])
        }


def main():
    """Main function for prediction."""
    pass


if __name__ == "__main__":
    main()


