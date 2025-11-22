"""
Exploratory data analysis and visualization module.
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path


def plot_target_distribution(df: pd.DataFrame, target_col: str = 'Churn', 
                             save_path: str = None):
    """
    Plot distribution of target variable.
    
    Args:
        df: Input DataFrame
        target_col: Name of target column
        save_path: Path to save figure
    """
    plt.figure(figsize=(8, 6))
    df[target_col].value_counts().plot(kind='bar')
    plt.title(f'Distribution of {target_col}')
    plt.xlabel(target_col)
    plt.ylabel('Count')
    plt.xticks(rotation=0)
    
    if save_path:
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Plot saved to {save_path}")
    
    plt.close()


def plot_feature_distributions(df: pd.DataFrame, save_dir: str = None):
    """
    Plot distributions of numeric features.
    
    Args:
        df: Input DataFrame
        save_dir: Directory to save figures
    """
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
    
    n_cols = 3
    n_rows = (len(numeric_cols) + n_cols - 1) // n_cols
    
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 5*n_rows))
    axes = axes.flatten()
    
    for idx, col in enumerate(numeric_cols):
        axes[idx].hist(df[col].dropna(), bins=30, edgecolor='black')
        axes[idx].set_title(col)
        axes[idx].set_xlabel(col)
        axes[idx].set_ylabel('Frequency')
    
    # Hide extra subplots
    for idx in range(len(numeric_cols), len(axes)):
        axes[idx].set_visible(False)
    
    plt.tight_layout()
    
    if save_dir:
        save_path = Path(save_dir) / "feature_distributions.png"
        save_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Plot saved to {save_path}")
    
    plt.close()


def plot_correlation_matrix(df: pd.DataFrame, save_path: str = None):
    """
    Plot correlation matrix of numeric features.
    
    Args:
        df: Input DataFrame
        save_path: Path to save figure
    """
    numeric_df = df.select_dtypes(include=['int64', 'float64'])
    
    plt.figure(figsize=(12, 10))
    sns.heatmap(numeric_df.corr(), annot=True, fmt='.2f', 
                cmap='coolwarm', center=0, square=True)
    plt.title('Feature Correlation Matrix')
    
    if save_path:
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Plot saved to {save_path}")
    
    plt.close()


def plot_churn_by_categorical(df: pd.DataFrame, categorical_col: str, 
                              target_col: str = 'Churn', save_path: str = None):
    """
    Plot churn rate by categorical feature.
    
    Args:
        df: Input DataFrame
        categorical_col: Name of categorical column
        target_col: Name of target column
        save_path: Path to save figure
    """
    churn_rate = df.groupby(categorical_col)[target_col].apply(
        lambda x: (x == 'Yes').sum() / len(x) if 'Yes' in x.values else x.mean()
    )
    
    plt.figure(figsize=(10, 6))
    churn_rate.plot(kind='bar')
    plt.title(f'Churn Rate by {categorical_col}')
    plt.xlabel(categorical_col)
    plt.ylabel('Churn Rate')
    plt.xticks(rotation=45)
    
    if save_path:
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Plot saved to {save_path}")
    
    plt.close()


def main():
    """Main function for exploration."""
    pass


if __name__ == "__main__":
    main()


