"""
Preprocessing module for feature transformation before model training.
"""
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
import joblib
from pathlib import Path


class ChurnPreprocessor:
    """Preprocessor for telco churn data."""
    
    def __init__(self):
        self.column_transformer = None
        self.label_encoders = {}
        self.feature_names = None
        
    def fit(self, X: pd.DataFrame):
        """
        Fit the preprocessor on training data.
        
        Args:
            X: Training features DataFrame
        """
        # Identify numeric and categorical columns
        numeric_features = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
        categorical_features = X.select_dtypes(include=['object']).columns.tolist()
        
        # Remove customer ID if present
        if 'customerID' in numeric_features:
            numeric_features.remove('customerID')
        if 'customerID' in categorical_features:
            categorical_features.remove('customerID')
        
        # Create column transformer
        self.column_transformer = ColumnTransformer(
            transformers=[
                ('num', StandardScaler(), numeric_features),
                ('cat', OneHotEncoder(drop='first', sparse_output=False, handle_unknown='ignore'), 
                 categorical_features)
            ],
            remainder='drop'
        )
        
        # Fit the transformer
        self.column_transformer.fit(X)
        
        # Store feature names
        self.feature_names = self._get_feature_names()
        
        return self
    
    def transform(self, X: pd.DataFrame) -> np.ndarray:
        """
        Transform features using fitted preprocessor.
        
        Args:
            X: Features DataFrame
            
        Returns:
            Transformed features array
        """
        if self.column_transformer is None:
            raise ValueError("Preprocessor must be fitted before transform")
        
        return self.column_transformer.transform(X)
    
    def fit_transform(self, X: pd.DataFrame) -> np.ndarray:
        """
        Fit and transform features.
        
        Args:
            X: Features DataFrame
            
        Returns:
            Transformed features array
        """
        self.fit(X)
        return self.transform(X)
    
    def _get_feature_names(self):
        """Get feature names after transformation."""
        feature_names = []
        
        for name, transformer, features in self.column_transformer.transformers_:
            if name == 'num':
                feature_names.extend(features)
            elif name == 'cat':
                if hasattr(transformer, 'get_feature_names_out'):
                    cat_features = transformer.get_feature_names_out(features)
                    feature_names.extend(cat_features)
        
        return feature_names
    
    def save(self, filepath: str):
        """Save preprocessor to file."""
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(self, filepath)
        print(f"Preprocessor saved to {filepath}")
    
    @staticmethod
    def load(filepath: str):
        """Load preprocessor from file."""
        return joblib.load(filepath)


def main():
    """Main function for preprocessing."""
    pass


if __name__ == "__main__":
    main()

