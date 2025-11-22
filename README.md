# Telco Churn MLOps Demo

End-to-end **customer churn prediction** project built as a learning playground for **MLOps**:

- Real business dataset (telco customer churn),
- Reproducible data prep & training pipeline,
- Experiment tracking with **MLflow**,
- Online prediction via **FastAPI**,
- **Data drift monitoring** with Evidently AI,
- Containerised with **Docker**,
- Production-ready **Kubernetes** deployment.

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
5. Data drift monitoring
6. Docker containerization
7. Kubernetes deployment to cloud

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
├── k8s/                       # Kubernetes manifests
│   ├── namespace.yaml
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── hpa.yaml
│   └── ingress.yaml
│
├── notebooks/                 # Jupyter notebooks for exploration
│
├── reports/                   # Generated analysis reports
│   ├── figures/              # Generated visualizations
│   └── drift/                # Data drift reports
│
├── references/                # Data dictionaries and documentation
│
├── docs/                      # Project documentation
│   ├── MLFLOW_UI_GUIDE.md
│   ├── CLOUD_DEPLOYMENT.md
│   └── MODEL_CONFIG_EXPLAINED.md
│
└── src/                       # Source code
    ├── __init__.py
    ├── api/                   # FastAPI service
    │   ├── __init__.py
    │   └── app.py             # REST API endpoints
    │
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
    ├── monitoring/            # Production monitoring
    │   ├── __init__.py
    │   └── drift_monitor.py  # Data drift detection
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
make mlflow-ui
```

Then open http://localhost:5000 in your browser.

See the [MLflow UI Guide](docs/MLFLOW_UI_GUIDE.md) for detailed instructions.

---

## 8. FastAPI Service

Start the prediction API:

```bash
make api
```

The API will be available at:

- **Base URL**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

### Test the API

```bash
# Health check
curl http://localhost:8000/health

# Single prediction
curl -X POST http://localhost:8000/predict/single \
  -H "Content-Type: application/json" \
  -d '{
    "gender": "Female",
    "SeniorCitizen": 0,
    "Partner": "Yes",
    "Dependents": "No",
    "tenure": 12,
    "PhoneService": "Yes",
    "MultipleLines": "No",
    "InternetService": "Fiber optic",
    "OnlineSecurity": "No",
    "OnlineBackup": "Yes",
    "DeviceProtection": "No",
    "TechSupport": "No",
    "StreamingTV": "Yes",
    "StreamingMovies": "No",
    "Contract": "Month-to-month",
    "PaperlessBilling": "Yes",
    "PaymentMethod": "Electronic check",
    "MonthlyCharges": 70.35,
    "TotalCharges": 840.20
  }'
```

---

## 9. Data Drift Monitoring

Monitor data quality and drift:

```bash
make drift-monitor
```

This generates:

- HTML drift reports in `reports/drift/`
- JSON metrics for alerting
- Automated drift tests

---

## 10. Docker Deployment

### Build Image

```bash
make docker-build
```

### Run Container

```bash
make docker-run
```

### Stop Container

```bash
make docker-stop
```

---

## 11. Kubernetes Deployment

Deploy to Kubernetes cluster:

```bash
make k8s-deploy
```

This creates:

- Namespace: `ml-production`
- Deployment with 3 replicas
- Service (ClusterIP/LoadBalancer)
- Horizontal Pod Autoscaler
- ConfigMaps and Secrets
- RBAC policies

### Check Deployment

```bash
kubectl get pods -n ml-production
kubectl get svc -n ml-production
kubectl logs -f -n ml-production -l app=churn-prediction
```

### Delete Deployment

```bash
make k8s-delete
```

For detailed cloud deployment instructions (AWS EKS, GCP GKE, Azure AKS), see [Cloud Deployment Guide](docs/CLOUD_DEPLOYMENT.md).

---

## 12. Next Steps

- [x] FastAPI service for online predictions
- [x] Docker containerization
- [x] Kubernetes deployment manifests
- [x] Data drift monitoring
- [x] Cloud deployment guide (AWS/GCP/Azure)
- [ ] Add unit tests
- [ ] Implement CI/CD pipeline (GitHub Actions)
- [ ] Add model A/B testing
- [ ] Set up monitoring alerts (Prometheus/Grafana)
- [ ] Implement automated retraining pipeline

---

## 13. Documentation

- [MLflow UI Guide](docs/MLFLOW_UI_GUIDE.md) - How to use the MLflow interface
- [Cloud Deployment Guide](docs/CLOUD_DEPLOYMENT.md) - Deploy to AWS/GCP/Azure
- [Model Configuration](docs/MODEL_CONFIG_EXPLAINED.md) - Configuration details

---

## 14. Project Template

This project structure is based on the [MLOps Template](https://github.com/Chim-SO/mlops-template) which provides a standardized structure for machine learning projects with MLOps best practices.
