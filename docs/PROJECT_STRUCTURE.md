# Project Structure Documentation

This document explains the organization and purpose of each directory and key file in the project.

## Directory Structure

### `/configs`
Configuration files for different models and experiments.
- `model1.yaml`: Hyperparameters and settings for the churn prediction model

### `/data`
All data files (most are gitignored).
- `raw/`: Original, immutable data dump
- `interim/`: Intermediate data that has been transformed
- `processed/`: Final, canonical datasets ready for modeling
- `external/`: Data from third-party sources

### `/docs`
Project documentation and guides.

### `/models`
Trained and serialized models (gitignored).
- Model artifacts (.pkl, .h5, .pt files)
- Preprocessor objects

### `/notebooks`
Jupyter notebooks for exploration and experimentation.
- `01_exploratory_data_analysis.ipynb`: Initial EDA

### `/references`
Data dictionaries, manuals, and other explanatory materials.

### `/reports`
Generated analysis reports.
- `figures/`: Generated graphics and visualizations

### `/src`
Source code for the project.

#### `/src/data`
Data engineering scripts:
- `ingestion.py`: Load raw data from various sources
- `cleaning.py`: Handle missing values and data quality issues
- `validation.py`: Data quality checks and schema validation
- `labeling.py`: Target variable encoding and transformation
- `build_features.py`: Feature engineering and transformation
- `splitting.py`: Split data into train/validation/test sets

#### `/src/models`
Model engineering code, organized by model:

##### `/src/models/model1`
Churn prediction model:
- `dataloader.py`: Load and prepare data for training
- `preprocessing.py`: Feature preprocessing and transformation
- `model.py`: Model architecture and definition
- `train.py`: Training script
- `predict.py`: Inference and prediction
- `hyperparameters_tuning.py`: Hyperparameter optimization

#### `/src/visualization`
Visualization scripts:
- `exploration.py`: Exploratory data analysis plots
- `evaluation.py`: Model evaluation visualizations

## Key Files

### Root Directory

- `README.md`: Project overview and quick start guide
- `requirements.txt`: Python package dependencies
- `Makefile`: Convenient commands for common tasks
- `LICENSE`: MIT License
- `.gitignore`: Specifies files to ignore in version control
- `devbox.json`: Devbox environment configuration
- `devbox.lock`: Locked versions for reproducibility

## Workflow

1. **Data Preparation**: Run scripts in `/src/data` or use `make data`
2. **Model Training**: Run training script or use `make train`
3. **Evaluation**: Generate visualizations and reports
4. **Prediction**: Use trained model for inference

## MLflow Integration

- Experiments are tracked in the `mlruns/` directory (gitignored)
- Run `mlflow ui` to view experiments in browser

## Adding New Models

To add a new model:
1. Create a new directory in `/src/models/` (e.g., `model2/`)
2. Copy the structure from `model1/`
3. Create a corresponding config file in `/configs/`
4. Update the Makefile if needed

## Best Practices

1. Keep raw data immutable
2. Version control code, not data or models
3. Use configuration files for hyperparameters
4. Log experiments with MLflow
5. Write modular, reusable code
6. Document significant decisions in `/docs`


