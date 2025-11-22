"""
Model definition module for churn prediction.
"""
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
import joblib
from pathlib import Path


class ChurnModel:
    """Wrapper class for churn prediction models."""
    
    def __init__(self, model_type: str = 'random_forest', **kwargs):
        """
        Initialize churn model.
        
        Args:
            model_type: Type of model ('random_forest', 'gradient_boosting', 'logistic_regression')
            **kwargs: Additional parameters for the model
        """
        self.model_type = model_type
        self.model = self._create_model(model_type, **kwargs)
    
    def _create_model(self, model_type: str, **kwargs):
        """Create model instance based on type."""
        if model_type == 'random_forest':
            return RandomForestClassifier(
                n_estimators=kwargs.get('n_estimators', 100),
                max_depth=kwargs.get('max_depth', 10),
                min_samples_split=kwargs.get('min_samples_split', 2),
                random_state=kwargs.get('random_state', 42),
                n_jobs=-1
            )
        elif model_type == 'gradient_boosting':
            return GradientBoostingClassifier(
                n_estimators=kwargs.get('n_estimators', 100),
                max_depth=kwargs.get('max_depth', 5),
                learning_rate=kwargs.get('learning_rate', 0.1),
                random_state=kwargs.get('random_state', 42)
            )
        elif model_type == 'logistic_regression':
            return LogisticRegression(
                C=kwargs.get('C', 1.0),
                max_iter=kwargs.get('max_iter', 1000),
                random_state=kwargs.get('random_state', 42)
            )
        else:
            raise ValueError(f"Unknown model type: {model_type}")
    
    def fit(self, X_train, y_train):
        """
        Train the model.
        
        Args:
            X_train: Training features
            y_train: Training labels
        """
        self.model.fit(X_train, y_train)
        return self
    
    def predict(self, X):
        """
        Make predictions.
        
        Args:
            X: Features
            
        Returns:
            Predictions
        """
        return self.model.predict(X)
    
    def predict_proba(self, X):
        """
        Predict probabilities.
        
        Args:
            X: Features
            
        Returns:
            Prediction probabilities
        """
        return self.model.predict_proba(X)
    
    def save(self, filepath: str):
        """Save model to file."""
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(self, filepath)
        print(f"Model saved to {filepath}")
    
    @staticmethod
    def load(filepath: str):
        """Load model from file."""
        return joblib.load(filepath)


def main():
    """Main function for model definition."""
    pass


if __name__ == "__main__":
    main()


