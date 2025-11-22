"""
Hyperparameter tuning module using grid search or random search.
"""
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import make_scorer, f1_score
import numpy as np


def tune_random_forest(X_train, y_train, method='grid'):
    """
    Tune Random Forest hyperparameters.
    
    Args:
        X_train: Training features
        y_train: Training labels
        method: 'grid' for GridSearchCV or 'random' for RandomizedSearchCV
        
    Returns:
        Best estimator and best parameters
    """
    # Define parameter grid
    param_grid = {
        'n_estimators': [50, 100, 200],
        'max_depth': [5, 10, 15, 20],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4]
    }
    
    # Initialize model
    rf = RandomForestClassifier(random_state=42, n_jobs=-1)
    
    # Define scorer
    scorer = make_scorer(f1_score)
    
    if method == 'grid':
        search = GridSearchCV(
            rf, param_grid, cv=5, scoring=scorer, 
            verbose=1, n_jobs=-1
        )
    else:
        search = RandomizedSearchCV(
            rf, param_grid, n_iter=20, cv=5, 
            scoring=scorer, verbose=1, n_jobs=-1, random_state=42
        )
    
    # Fit search
    print("Starting hyperparameter search...")
    search.fit(X_train, y_train)
    
    print(f"\nBest parameters: {search.best_params_}")
    print(f"Best F1 score: {search.best_score_:.4f}")
    
    return search.best_estimator_, search.best_params_


def main():
    """Main function for hyperparameter tuning."""
    pass


if __name__ == "__main__":
    main()


