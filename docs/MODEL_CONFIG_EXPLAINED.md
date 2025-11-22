# 📖 Understanding the Model Configuration & Code

## 🎯 Overview

You have a **complete MLOps training system** with:

1. **Configuration file** (`configs/model1.yaml`) - Settings for experiments
2. **Model code** (`src/models/model1/`) - Modular training pipeline
3. **MLflow integration** - Experiment tracking

---

## 📄 Part 1: The Configuration File (`configs/model1.yaml`)

### **What is it?**

A **YAML file** that stores all hyperparameters and settings for your model training. This allows you to:

- ✅ Change model settings without modifying code
- ✅ Track different experiments easily
- ✅ Share configurations with teammates
- ✅ Version control your experiments

### **Structure Breakdown:**

```yaml
# configs/model1.yaml

# ═══════════════════════════════════════════════════════════
# 1. EXPERIMENT TRACKING (for MLflow)
# ═══════════════════════════════════════════════════════════
experiment_name: "telco_churn" # MLflow experiment name
run_name: "churn_model_v1" # Specific run identifier

# ═══════════════════════════════════════════════════════════
# 2. DATA & MODEL PATHS
# ═══════════════════════════════════════════════════════════
data_dir: "data/processed" # Where train/val/test CSVs are
model_dir: "models" # Where to save trained model

# ═══════════════════════════════════════════════════════════
# 3. MODEL HYPERPARAMETERS
# ═══════════════════════════════════════════════════════════
model_params:
  model_type: "random_forest" # Type of model
  n_estimators: 100 # Number of trees
  max_depth: 10 # Max tree depth
  min_samples_split: 2 # Min samples to split node
  random_state: 42 # For reproducibility

# ═══════════════════════════════════════════════════════════
# 4. TRAINING SETTINGS
# ═══════════════════════════════════════════════════════════
training:
  test_size: 0.2 # 20% for test
  val_size: 0.2 # 20% for validation
  random_state: 42

# ═══════════════════════════════════════════════════════════
# 5. FEATURE ENGINEERING FLAGS
# ═══════════════════════════════════════════════════════════
features:
  create_tenure_bins: true # Create tenure categories
  create_revenue_features: true # Create revenue features

# ═══════════════════════════════════════════════════════════
# 6. PREPROCESSING OPTIONS
# ═══════════════════════════════════════════════════════════
preprocessing:
  scale_numeric: true # StandardScaler on numeric
  encode_categorical: "onehot" # One-hot encode categories
  handle_missing: "drop" # Drop missing values
```

### **How It's Used:**

```python
# In train.py (line 14-23)
import yaml

# Load the config file
with open('configs/model1.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Access values like a dictionary
experiment_name = config['experiment_name']  # "telco_churn"
model_type = config['model_params']['model_type']  # "random_forest"
n_estimators = config['model_params']['n_estimators']  # 100
```

---

## 🏗️ Part 2: The Model Code Structure

You have **6 modular files** in `src/models/model1/`:

```
src/models/model1/
├── __init__.py              # Makes it a Python package
├── dataloader.py            # Loads train/val/test data
├── preprocessing.py         # Scales & encodes features
├── model.py                 # Model wrapper class
├── train.py                 # Main training script
├── predict.py               # Prediction script
└── hyperparameters_tuning.py # HPO (hyperparameter optimization)
```

---

### **File 1: `dataloader.py` - Data Loading**

**Purpose:** Load train/val/test splits from processed data

```python
class ChurnDataLoader:
    def __init__(self, data_dir="data/processed"):
        self.data_dir = data_dir

    def load_train_data(self):
        # Loads data/processed/train.csv
        # Returns: X_train, y_train

    def load_val_data(self):
        # Loads data/processed/val.csv
        # Returns: X_val, y_val

    def load_test_data(self):
        # Loads data/processed/test.csv
        # Returns: X_test, y_test
```

**Usage:**

```python
loader = ChurnDataLoader(data_dir="data/processed")
X_train, y_train = loader.load_train_data()
X_val, y_val = loader.load_val_data()
```

---

### **File 2: `preprocessing.py` - Feature Transformation**

**Purpose:** Transform features for model training (scaling, encoding)

```python
class ChurnPreprocessor:
    def __init__(self):
        self.column_transformer = None  # Will hold transformers

    def fit(self, X):
        # Learn transformations from training data
        # - StandardScaler for numeric features
        # - OneHotEncoder for categorical features

    def transform(self, X):
        # Apply learned transformations

    def fit_transform(self, X):
        # Fit and transform in one step
```

**What it does:**

1. **Identifies column types:**

   - Numeric: `tenure`, `MonthlyCharges`, etc. → StandardScaler
   - Categorical: `gender`, `Contract`, etc. → OneHotEncoder

2. **StandardScaler (numeric features):**

   ```python
   # Before: tenure = [1, 12, 36, 72]
   # After:  tenure = [-1.2, -0.5, 0.3, 1.4]  (mean=0, std=1)
   ```

3. **OneHotEncoder (categorical):**
   ```python
   # Already handled by your pipeline!
   # But this can re-encode if needed
   ```

**Usage:**

```python
preprocessor = ChurnPreprocessor()

# Fit on training data only
X_train_scaled = preprocessor.fit_transform(X_train)

# Transform validation/test (using training stats)
X_val_scaled = preprocessor.transform(X_val)
X_test_scaled = preprocessor.transform(X_test)
```

⚠️ **Important:** Always fit on training data, then transform val/test!

---

### **File 3: `model.py` - Model Wrapper**

**Purpose:** Unified interface for different model types

```python
class ChurnModel:
    def __init__(self, model_type='random_forest', **kwargs):
        # Creates model based on type from config
        self.model = self._create_model(model_type, **kwargs)

    def _create_model(self, model_type, **kwargs):
        if model_type == 'random_forest':
            return RandomForestClassifier(
                n_estimators=kwargs.get('n_estimators', 100),
                max_depth=kwargs.get('max_depth', 10),
                ...
            )
        elif model_type == 'gradient_boosting':
            return GradientBoostingClassifier(...)
        elif model_type == 'logistic_regression':
            return LogisticRegression(...)

    def fit(self, X_train, y_train):
        self.model.fit(X_train, y_train)

    def predict(self, X):
        return self.model.predict(X)

    def predict_proba(self, X):
        return self.model.predict_proba(X)

    def save(self, filepath):
        joblib.dump(self, filepath)
```

**Benefits:**

- ✅ Switch between models by changing config only
- ✅ Consistent interface for all model types
- ✅ Easy to save/load models

**Usage:**

```python
# Create model from config
model = ChurnModel(
    model_type='random_forest',
    n_estimators=100,
    max_depth=10
)

# Train
model.fit(X_train_scaled, y_train)

# Predict
predictions = model.predict(X_val_scaled)
probabilities = model.predict_proba(X_val_scaled)

# Save
model.save('models/churn_model.pkl')
```

---

### **File 4: `train.py` - Main Training Script** ⭐

**Purpose:** Orchestrates the entire training pipeline

**Flow:**

```python
def train_model(config_path='configs/model1.yaml'):
    # ────────────────────────────────────────────────────────
    # 1. LOAD CONFIG
    # ────────────────────────────────────────────────────────
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    # ────────────────────────────────────────────────────────
    # 2. LOAD DATA
    # ────────────────────────────────────────────────────────
    loader = ChurnDataLoader(data_dir=config['data_dir'])
    X_train, y_train = loader.load_train_data()
    X_val, y_val = loader.load_val_data()

    # ────────────────────────────────────────────────────────
    # 3. PREPROCESS DATA
    # ────────────────────────────────────────────────────────
    preprocessor = ChurnPreprocessor()
    X_train_scaled = preprocessor.fit_transform(X_train)
    X_val_scaled = preprocessor.transform(X_val)

    # ────────────────────────────────────────────────────────
    # 4. START MLFLOW TRACKING
    # ────────────────────────────────────────────────────────
    mlflow.set_experiment(config['experiment_name'])

    with mlflow.start_run(run_name=config['run_name']):
        # Log config parameters
        mlflow.log_params(config['model_params'])

        # ────────────────────────────────────────────────────
        # 5. TRAIN MODEL
        # ────────────────────────────────────────────────────
        model = ChurnModel(**config['model_params'])
        model.fit(X_train_scaled, y_train)

        # ────────────────────────────────────────────────────
        # 6. EVALUATE MODEL
        # ────────────────────────────────────────────────────
        # Training metrics
        y_train_pred = model.predict(X_train_scaled)
        train_accuracy = accuracy_score(y_train, y_train_pred)
        train_f1 = f1_score(y_train, y_train_pred)
        # ... more metrics

        # Validation metrics
        y_val_pred = model.predict(X_val_scaled)
        val_accuracy = accuracy_score(y_val, y_val_pred)
        val_f1 = f1_score(y_val, y_val_pred)
        # ... more metrics

        # ────────────────────────────────────────────────────
        # 7. LOG TO MLFLOW
        # ────────────────────────────────────────────────────
        mlflow.log_metrics({
            'train_accuracy': train_accuracy,
            'val_accuracy': val_accuracy,
            'train_f1': train_f1,
            'val_f1': val_f1,
            # ... more metrics
        })

        # ────────────────────────────────────────────────────
        # 8. SAVE MODEL & PREPROCESSOR
        # ────────────────────────────────────────────────────
        model.save('models/churn_model.pkl')
        preprocessor.save('models/preprocessor.pkl')

        # Log to MLflow registry
        mlflow.sklearn.log_model(model.model, "model")

    print("Training complete!")
```

---

## 🔄 The Complete Workflow

### **Data Pipeline → Training Pipeline**

```
┌─────────────────────────────────────────────────────────────┐
│ PHASE 1: DATA PIPELINE (src/pipeline.py)                   │
├─────────────────────────────────────────────────────────────┤
│ 1. Load raw data (Excel/CSV)                               │
│ 2. Clean data (missing values, types)                      │
│ 3. Encode target (Churn: Yes/No → 1/0)                     │
│ 4. Engineer features (tenure_bin, revenue)                 │
│ 5. Encode categorical (text → one-hot)                     │
│ 6. Split data (train/val/test)                             │
│                                                             │
│ OUTPUT: data/processed/                                     │
│   ├── train.csv  (all numeric, ready for ML)              │
│   ├── val.csv                                              │
│   └── test.csv                                             │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│ PHASE 2: MODEL TRAINING (src/models/model1/train.py)       │
├─────────────────────────────────────────────────────────────┤
│ 1. Load config (configs/model1.yaml)                       │
│ 2. Load data (ChurnDataLoader)                             │
│ 3. Preprocess (ChurnPreprocessor - scaling)                │
│ 4. Train model (ChurnModel)                                │
│ 5. Evaluate (metrics)                                      │
│ 6. Log to MLflow (experiment tracking)                     │
│ 7. Save model & preprocessor                               │
│                                                             │
│ OUTPUT: models/                                             │
│   ├── churn_model.pkl      (trained model)                │
│   └── preprocessor.pkl     (fitted scaler)                │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 How to Use It

### **Option 1: Default Training**

```bash
# Uses configs/model1.yaml
python src/models/model1/train.py
```

### **Option 2: Custom Config**

```bash
# Create configs/model2.yaml with different settings
python src/models/model1/train.py --config configs/model2.yaml
```

### **Option 3: Experiment with Different Models**

Edit `configs/model1.yaml`:

**Experiment 1: Random Forest (default)**

```yaml
model_params:
  model_type: "random_forest"
  n_estimators: 100
  max_depth: 10
```

**Experiment 2: Gradient Boosting**

```yaml
model_params:
  model_type: "gradient_boosting"
  n_estimators: 100
  max_depth: 5
  learning_rate: 0.1
```

**Experiment 3: Logistic Regression**

```yaml
model_params:
  model_type: "logistic_regression"
  C: 1.0
  max_iter: 1000
```

---

## 🎓 Key Design Principles

### **1. Separation of Concerns**

- **Data Pipeline** (`src/pipeline.py`) → Cleans & prepares data
- **Model Training** (`src/models/model1/`) → Trains models
- **Configuration** (`configs/`) → Hyperparameters

### **2. Configuration-Driven**

- Change model settings → Edit YAML, don't touch code
- Experiment tracking → Each config = one experiment
- Reproducibility → Version control configs

### **3. Modular Components**

- **DataLoader** → Data loading logic
- **Preprocessor** → Feature transformation logic
- **Model** → Model training/prediction logic
- **Train** → Orchestration logic

### **4. MLOps Best Practices**

- ✅ Experiment tracking (MLflow)
- ✅ Model versioning (save/load)
- ✅ Metrics logging (train & val)
- ✅ Configuration management (YAML)

---

## ⚠️ Important Notes

### **Data Pipeline Already Handles:**

- ✅ One-hot encoding (Step 7 in `src/pipeline.py`)
- ✅ Missing values (Step 3)
- ✅ Target encoding (Step 5)

### **Preprocessor (in training) Handles:**

- ✅ Scaling numeric features (StandardScaler)
- ✅ **Re-encoding if needed** (but your pipeline already did it!)

### **Potential Redundancy:**

The `preprocessing.py` has OneHotEncoder, but your data pipeline already one-hot encodes everything. So:

**Option A:** Preprocessor only needs to scale (numeric features already 0/1)
**Option B:** Skip preprocessor entirely if data is already scaled

Let me know if you want me to optimize this! 🔧

---

## 📊 Expected Output

When you run training:

```bash
$ python src/models/model1/train.py

==================================================
Starting model training...
==================================================

Loading data...
Training samples: 4508
Validation samples: 1128

Preprocessing data...

Training model...

==================================================
Training Results:
==================================================
Train Accuracy:  0.9234
Train Precision: 0.8876
Train Recall:    0.7654
Train F1:        0.8213
Train AUC:       0.9456

Validation Results:
Val Accuracy:    0.8123
Val Precision:   0.7543
Val Recall:      0.6987
Val F1:          0.7254
Val AUC:         0.8567
==================================================

Model saved to models/churn_model.pkl
Preprocessor saved to models/preprocessor.pkl

Training complete!
```

---

## 🎉 Summary

**You have a professional MLOps setup:**

1. ✅ **Config file** (`model1.yaml`) controls all settings
2. ✅ **Modular code** (dataloader, preprocessor, model, train)
3. ✅ **MLflow tracking** for experiments
4. ✅ **Easy experimentation** (just edit YAML!)

**To train a model:**

```bash
python src/models/model1/train.py
```

That's it! 🚀
