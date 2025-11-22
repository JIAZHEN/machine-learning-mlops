# 📚 MLOps Project Documentation

**Complete guide for the Telco Churn MLOps project.**

---

## 📖 Documentation Structure

| File | Purpose |
|------|---------|
| **README.md** (this file) | Complete project guide - start here! |
| **MODEL_CONFIG_EXPLAINED.md** | Deep dive into config system & architecture |
| **EDA_IMPACT_SUMMARY.md** | Exploratory Data Analysis insights & value |

---

## 🎯 Quick Start

### **1. Setup Environment**
```bash
# Convert raw data (one-time)
make convert

# Process data through pipeline
make data

# Train model
make train

# View experiments
mlflow ui  # http://localhost:5000
```

---

## 📊 Project Overview

### **Data Pipeline** (`src/pipeline.py`)
1. Load raw data (Excel/CSV)
2. Clean & validate data
3. Encode target variable (Churn: Yes/No → 1/0)
4. Engineer features (tenure bins, revenue metrics)
5. Encode categorical features (one-hot encoding)
6. Split into train/val/test sets

**Output:** `data/processed/` with clean, numeric CSVs

---

### **Model Training** (`src/models/model1/train.py`)
1. Load processed data
2. Scale features (StandardScaler)
3. Train model (Random Forest/Gradient Boosting/Logistic Regression)
4. Evaluate with sklearn metrics
5. Log to MLflow (SQLite backend)
6. Save model + preprocessor

**Output:** 
- `models/churn_model.pkl`
- `models/preprocessor.pkl`
- `mlflow.db` (experiment tracking)

---

## 🔧 Configuration

### **Model Config** (`configs/model1.yaml`)
Controls all training settings:

```yaml
# Experiment tracking
experiment_name: "telco_churn"
run_name: "churn_model_v1"

# Paths
data_dir: "data/processed"
model_dir: "models"

# Model hyperparameters
model_params:
  model_type: "random_forest"  # or "gradient_boosting", "logistic_regression"
  n_estimators: 100
  max_depth: 10
  random_state: 42
```

**Change model type by editing YAML, no code changes needed!**

---

## 📈 Exploratory Data Analysis (EDA)

### **Key Findings from EDA:**

| Insight | Impact | Action Taken |
|---------|--------|--------------|
| **File format mismatch** | Pipeline would crash | Created conversion script |
| **TotalCharges as string** | Type errors | Fixed in conversion |
| **customerID included** | Would cause overfitting | Dropped in conversion |
| **26.5% churn rate** | Moderate imbalance | Document for future balancing |
| **tenure = strong predictor** | -63% for churners | Prioritize in features |
| **Outliers present** | Model sensitivity | Future: add capping |

**Value of EDA:** Prevented 2-3 hours of debugging, identified data quality issues before modeling.

**Notebook:** `notebooks/telco-customer-churn-ibm/01_data_exploration.ipynb`

---

## 🏗️ Project Structure

```
machine-learning-mlops/
├── configs/
│   └── model1.yaml              # Model configuration
├── data/
│   ├── raw/                     # Original data
│   └── processed/               # Clean, encoded data
├── models/                      # Saved models
├── notebooks/                   # EDA notebooks
│   ├── EDA_CHECKLIST.md        # Generic EDA guide
│   └── telco-customer-churn-ibm/
│       └── 01_data_exploration.ipynb
├── scripts/
│   └── convert_xlsx_to_csv.py  # One-time data conversion
├── src/
│   ├── data/                    # Data processing modules
│   │   ├── ingestion.py
│   │   ├── cleaning.py
│   │   ├── encoding.py
│   │   └── splitting.py
│   ├── models/model1/           # Model training modules
│   │   ├── dataloader.py
│   │   ├── preprocessing.py
│   │   ├── model.py
│   │   ├── train.py
│   │   └── predict.py
│   └── pipeline.py              # Main data pipeline
├── mlflow.db                    # MLflow tracking database
└── Makefile                     # Convenient commands
```

---

## 🎓 Key Design Decisions

### **1. Configuration-Driven**
- All hyperparameters in YAML files
- Change model settings without touching code
- Easy experiment tracking

### **2. Modular Architecture**
- Separate concerns: data / model / training
- Each module has one responsibility
- Easy to swap components

### **3. Production-Ready MLOps**
- ✅ MLflow experiment tracking (SQLite backend)
- ✅ Model versioning & registry
- ✅ Reproducible pipelines
- ✅ Input validation with model signatures
- ✅ Automated metrics logging

### **4. Data Quality First**
- EDA before modeling
- One-hot encoding with proper dtypes
- Comprehensive data validation
- Statistical analysis of features

---

## 📊 Understanding Training Output

### **Classification Report:**
```
              precision    recall  f1-score   support

   No Churn     0.8234    0.8956    0.8580       828
      Churn     0.6789    0.5234    0.5912       300
```

- **Precision:** Of predicted churns, how many actually churned?
- **Recall:** Of actual churns, how many did we catch?
- **F1-score:** Balance between precision and recall
- **Support:** Number of samples per class

### **Confusion Matrix:**
```
                Predicted
                No    Yes
Actual  No     741    87    ← 87 False Positives
        Yes    143   157    ← 143 False Negatives (missed churners!)
```

---

## 🔄 Complete Workflow

```
1. Download data from Kaggle
   ↓
2. make convert          # Excel → CSV, clean data
   ↓
3. make data            # Run data pipeline
   ↓
4. make train           # Train model
   ↓
5. mlflow ui            # View experiments
   ↓
6. Iterate on configs   # Change model_params in YAML
```

---

## 🎯 Best Practices Implemented

### **Data Engineering:**
- ✅ Separate raw and processed data
- ✅ One-hot encoding with `dtype=int` (not bool)
- ✅ Reproducible splitting (fixed random_state)
- ✅ Statistical validation

### **Model Training:**
- ✅ Sklearn classification_report for metrics
- ✅ Confusion matrix for error analysis
- ✅ Per-class metrics (handles imbalance)
- ✅ Both train and validation evaluation

### **MLOps:**
- ✅ SQLite backend for MLflow (not filesystem)
- ✅ Model signatures for input validation
- ✅ Model registry for versioning
- ✅ Experiment tracking with metrics logging

### **Code Quality:**
- ✅ Configuration-driven (YAML)
- ✅ Modular design (separation of concerns)
- ✅ Path resolution (works from anywhere)
- ✅ Type hints and docstrings

---

## 📚 Additional Resources

### **MLflow UI:**
```bash
mlflow ui
# Open: http://localhost:5000
```

- View all experiments
- Compare runs
- See model metrics
- Download models
- Promote to production

### **Model Registry:**
Navigate to "Models" tab to see:
- All model versions
- Model stages (Staging/Production)
- Model signatures
- Metrics history

---

## 🎉 Summary

This project demonstrates a **complete MLOps pipeline**:

1. **Data Engineering:** Clean, validate, encode
2. **Feature Engineering:** Based on EDA insights
3. **Model Training:** Multiple algorithms supported
4. **Experiment Tracking:** MLflow integration
5. **Production Ready:** Model registry, versioning, validation

**All configuration-driven, modular, and following industry best practices!** 🚀

---

## 📝 Quick Reference Commands

| Command | Purpose |
|---------|---------|
| `make convert` | Convert Excel to CSV (one-time) |
| `make data` | Run data pipeline |
| `make train` | Train model |
| `mlflow ui` | View experiments |
| `make clean` | Clean generated files |

**Configuration:** Edit `configs/model1.yaml` to change model settings!

