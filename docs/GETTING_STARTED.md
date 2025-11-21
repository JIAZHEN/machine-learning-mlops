# Getting Started with Telco Churn MLOps Project

This guide will help you get started with the Telco Churn prediction project.

## Prerequisites

- Python 3.11 or higher
- Git
- Devbox (optional, but recommended)
- Kaggle account (to download the dataset)

## Step 1: Clone the Repository

```bash
git clone <your-repo-url>
cd machine-learning-mlops
```

## Step 2: Set Up Environment

### Option A: Using Devbox (Recommended)

Devbox provides a reproducible development environment.

```bash
# Allow direnv to activate the environment
direnv allow
```

This will automatically:
- Install Python 3.11.10
- Create a virtual environment
- Install all dependencies from requirements.txt

### Option B: Manual Setup

```bash
# Create virtual environment
python3.11 -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # On macOS/Linux
# or
.venv\Scripts\activate  # On Windows

# Install dependencies
pip install -r requirements.txt
```

## Step 3: Download the Dataset

1. Go to Kaggle: https://www.kaggle.com/datasets/denisexpsito/telco-customer-churn-ibm
2. Download the `telco_churn.csv` file
3. Place it in the `data/raw/` directory:

```bash
# Make sure the file is in the right location
ls data/raw/telco_churn.csv
```

## Step 4: Run the Data Pipeline

Process the raw data into train/validation/test sets:

```bash
make data
```

Or run directly:

```bash
python src/pipeline.py
```

This will:
- Load and clean the raw data
- Validate data quality
- Encode the target variable
- Engineer features
- Split into train/val/test sets
- Save processed data to `data/processed/`

## Step 5: Train the Model

```bash
make train
```

Or run directly:

```bash
cd src/models/model1
python train.py
```

This will:
- Load the processed data
- Train a Random Forest model
- Log metrics and artifacts to MLflow
- Save the trained model to `models/`

## Step 6: View Experiment Results

Start the MLflow UI:

```bash
mlflow ui
```

Then open your browser to http://localhost:5000 to view:
- Experiment runs
- Model metrics
- Parameters
- Artifacts

## Step 7: Explore the Data (Optional)

Launch Jupyter:

```bash
jupyter notebook
```

Open `notebooks/01_exploratory_data_analysis.ipynb` to explore the data.

## Project Workflow

```
1. Data Pipeline (src/pipeline.py)
   ↓
2. Model Training (src/models/model1/train.py)
   ↓
3. Model Evaluation (MLflow UI)
   ↓
4. Make Predictions (src/models/model1/predict.py)
```

## Common Commands

### View Available Commands
```bash
make help
```

### Process Data
```bash
make data
```

### Train Model
```bash
make train
```

### Clean Generated Files
```bash
make clean
```

### Run Linters
```bash
make lint
```

### Run Tests
```bash
make test
```

## Configuration

Edit `configs/model1.yaml` to customize:
- Model type (random_forest, gradient_boosting, logistic_regression)
- Hyperparameters
- Data paths
- Training settings

Example:

```yaml
model_params:
  model_type: "random_forest"
  n_estimators: 200
  max_depth: 15
  min_samples_split: 5
```

## Troubleshooting

### Issue: "File not found" when running data pipeline

**Solution**: Make sure you've downloaded the dataset and placed it in `data/raw/telco_churn.csv`

### Issue: "Module not found" errors

**Solution**: Make sure you've activated the virtual environment and installed dependencies:
```bash
source .venv/bin/activate  # or direnv allow
pip install -r requirements.txt
```

### Issue: MLflow UI won't start

**Solution**: Make sure MLflow is installed and port 5000 is not in use:
```bash
pip install mlflow
mlflow ui --port 5001  # Use a different port
```

## Next Steps

1. ✅ Set up environment
2. ✅ Download and process data
3. ✅ Train your first model
4. 🔲 Experiment with different hyperparameters
5. 🔲 Try different model types (gradient boosting, logistic regression)
6. 🔲 Add custom features
7. 🔲 Create a REST API for predictions (FastAPI)
8. 🔲 Containerize with Docker
9. 🔲 Deploy to cloud

## Resources

- [MLflow Documentation](https://mlflow.org/docs/latest/index.html)
- [Scikit-learn Documentation](https://scikit-learn.org/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [MLOps Template](https://github.com/Chim-SO/mlops-template)

## Getting Help

If you encounter issues:
1. Check the documentation in `/docs`
2. Review the code comments
3. Check MLflow logs
4. Open an issue on GitHub

Happy modeling! 🚀

