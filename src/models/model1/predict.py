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
            model_path: Path to trained model
            preprocessor_path: Path to fitted preprocessor
        """
        self.model = ChurnModel.load(model_path)
        self.preprocessor = ChurnPreprocessor.load(preprocessor_path)
    
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

