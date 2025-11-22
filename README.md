# Telco Churn MLOps Demo

End-to-end **customer churn prediction** project built as a learning playground for **MLOps**:

- Real business dataset (telco customer churn),
- Reproducible data prep & training pipeline,
- Experiment tracking with **MLflow**,
- Online prediction via **FastAPI**,
- Containerised with **Docker**.

We use devbox here. Run `direnv allow` to enable it.

---

## 1. Problem overview

A telecom provider wants to identify **which customers are likely to churn** so they can:

- Target retention offers,
- Prioritise high-risk customers,
- Understand drivers of churn.

This repo implements a simple but realistic MLOps flow around that problem:

1. Data ingestion & preprocessing
2. Model training with experiment tracking
3. Model packaging as reusable artifacts
4. Online serving via REST API
5. (Optional) CI/tests & productionisation ideas

---

## 2. Project Structure

This project follows the MLOps template structure for organized machine learning projects:

```
machine-learning-mlops/
├── README.md                  # This file
├── Makefile                   # Convenient commands for data, training, etc.
├── requirements.txt           # Python package dependencies
├── devbox.json               # Devbox configuration
├── configs/                   # Configuration files
│   └── model1.yaml           # Model hyperparameters and settings
│
├── data/                      # Data directory (gitignored)
│   ├── raw/                  # Original, immutable data
│   ├── interim/              # Intermediate data transformations
│   ├── processed/            # Final data for modeling
│   └── external/             # Data from third-party sources
│
├── models/                    # Trained model artifacts (gitignored)
│
├── notebooks/                 # Jupyter notebooks for exploration
│
├── reports/                   # Generated analysis reports
│   └── figures/              # Generated visualizations
│
├── references/                # Data dictionaries and documentation
│
├── docs/                      # Project documentation
│
└── src/                       # Source code
    ├── __init__.py
    ├── data/                  # Data engineering scripts
    │   ├── ingestion.py      # Load raw data
    │   ├── cleaning.py       # Handle missing values
    │   ├── validation.py     # Data quality checks
    │   ├── labeling.py       # Target variable encoding
    │   ├── splitting.py      # Train/val/test splits
    │   └── build_features.py # Feature engineering
    │
    ├── models/                # Model engineering
    │   └── model1/           # Churn prediction model
    │       ├── dataloader.py
    │       ├── preprocessing.py
    │       ├── model.py
    │       ├── train.py
    │       ├── predict.py
    │       └── hyperparameters_tuning.py
    │
    └── visualization/         # Visualization scripts
        ├── exploration.py    # EDA visualizations
        └── evaluation.py     # Model evaluation plots
```

---

## 3. Setup

### Prerequisites

- Python 3.11+
- Devbox (optional, for reproducible environments)

### Installation

1. **Clone the repository**:

```bash
git clone <your-repo-url>
cd machine-learning-mlops
```

2. **Enable devbox environment** (if using devbox):

```bash
direnv allow
```

This will automatically:

- Set up Python 3.11.10
- Create a virtual environment
- Install all dependencies from `requirements.txt`

3. **Or install manually**:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

## 4. Dataset

The project uses the **IBM Telco Customer Churn** dataset, which contains:

- Customer demographics and service information,
- Contract type, payment method, tenure, charges,
- Binary churn label (`Yes` / `No`).

Example sources:

- Kaggle – IBM Telco Customer Churn:  
  `<https://www.kaggle.com/datasets/denisexpsito/telco-customer-churn-ibm>`
- Alternative Kaggle version:  
  `<https://www.kaggle.com/datasets/nikhilrajubiyyap/ibm-telco-churn-data>`

Download the CSV from Kaggle and save it as:

```bash
data/raw/telco_churn.csv
```

---

## 5. Quick Start

### Process Data

```bash
make data
```

This runs the complete data pipeline:

1. Data ingestion
2. Data cleaning
3. Data validation
4. Label encoding
5. Feature engineering
6. Train/val/test splitting

### Train Model

```bash
make train
```

This will:

- Load processed data
- Train the model with parameters from `configs/model1.yaml`
- Log metrics and artifacts to MLflow
- Save the trained model to `models/`

### Make Predictions

```bash
make predict
```

### Exploratory Data Analysis

```bash
make explore
```

### Clean Generated Files

```bash
make clean
```

---

## 6. Configuration

Edit `configs/model1.yaml` to customize:

- Model hyperparameters (n_estimators, max_depth, etc.)
- Data paths
- Training settings
- Feature engineering options

---

## 7. MLflow Tracking

View experiment results:

```bash
mlflow ui
```

Then open http://localhost:5000 in your browser.

---

## 8. Next Steps

- [ ] Add FastAPI service for online predictions
- [ ] Create Docker container
- [ ] Add unit tests
- [ ] Implement CI/CD pipeline
- [ ] Add data drift monitoring
- [ ] Deploy to cloud platform

---

## 9. Project Template

This project structure is based on the [MLOps Template](https://github.com/Chim-SO/mlops-template) which provides a standardized structure for machine learning projects with MLOps best practices.
