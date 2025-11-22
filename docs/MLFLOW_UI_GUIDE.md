# MLflow UI Guide

## Starting the UI

```bash
make mlflow-ui
# Or directly: mlflow ui --backend-store-uri sqlite:///mlflow.db
```

Access at: **http://localhost:5000**

---

## 🎯 Main Views

### 1. **Experiments Page** (Home)

Shows all your ML experiments in one place.

**Key Information:**
- **Experiment Name**: `telco_churn` (your current experiment)
- **Number of Runs**: How many training runs you've executed
- **Click on experiment** → See all runs inside it

---

### 2. **Runs Table**

Displays all training runs within an experiment.

**Columns to Watch:**

| Column | What It Shows | Use Case |
|--------|---------------|----------|
| **Run Name** | `churn_model_v1` | Identify specific training sessions |
| **Created** | Timestamp | When the model was trained |
| **Duration** | Time elapsed | How long training took |
| **User** | Your username | Who ran the experiment |
| **Source** | Script path | Which code was executed |
| **Version** | Git commit | Code version tracking |

**Metrics Columns** (customizable):
- `val_accuracy`, `val_auc`, `val_f1`, `val_precision`, `val_recall`
- `train_accuracy`, `train_auc`, etc.

**💡 Tip:** Click column headers to sort (e.g., sort by `val_auc` to find best model)

---

### 3. **Individual Run Page**

Click any run name to see detailed information.

#### **📊 Overview Tab**
- **Run ID**: Unique identifier
- **Status**: Finished/Failed/Running
- **Start/End Time**: Duration details
- **Git Info**: Commit hash for reproducibility

#### **⚙️ Parameters Tab**
Shows all hyperparameters used:
```yaml
model_type: random_forest
n_estimators: 100
max_depth: 10
min_samples_split: 2
random_state: 42
```

#### **📈 Metrics Tab**
All logged metrics with values:
- Training metrics: `train_accuracy`, `train_auc`, `train_f1`, etc.
- Validation metrics: `val_accuracy`, `val_auc`, `val_f1`, etc.

**💡 Tip:** Metrics can be plotted over time if logged at multiple steps

#### **🗂️ Artifacts Tab**
Stored files and models:
- **Model artifacts** (the trained model)
- **Plots** (confusion matrices, ROC curves - if logged)
- **Feature importance** (if logged)
- **Any custom files** you saved

**Actions:**
- 📥 **Download** artifacts
- 🔍 **Preview** some file types

---

### 4. **Model Registry**

Navigate to: **Models** (top menu) → `telco_churn_model`

**Shows:**
- **Model Versions**: Version 1, 2, 3, etc.
- **Stage**: None/Staging/Production/Archived
- **Source Run**: Which training run created this version
- **Registered Time**: When it was added to registry

**Key Actions:**
- **Transition to Staging**: Mark for testing
- **Transition to Production**: Deploy this version
- **Compare Versions**: See differences in metrics
- **Download Model**: Get the .pkl file

---

## 🔄 Common Workflows

### **Finding Your Best Model**

1. Go to **Experiments** → `telco_churn`
2. Click **Add Column** → Select `val_auc` (or your key metric)
3. Click column header to **sort descending**
4. Top row = best model
5. Click run name → See details
6. Go to **Artifacts** → Download or register model

### **Comparing Multiple Runs**

1. Select checkboxes for 2+ runs
2. Click **Compare** button
3. View side-by-side:
   - Parameter differences
   - Metric differences
   - Visual charts

### **Promoting a Model to Production**

1. Go to **Models** → `telco_churn_model`
2. Find the version you want
3. Click **Stage** dropdown → **Transition to Production**
4. Add description/notes
5. ✅ Now marked as production model

---

## 📊 Key Metrics to Monitor

For your churn prediction project, focus on:

| Metric | What It Means | Good Value |
|--------|---------------|------------|
| **val_auc** | Overall model performance | > 0.80 |
| **val_recall** | How many churners caught | > 0.70 (catch most churners) |
| **val_precision** | Accuracy of churn predictions | > 0.60 (limit false alarms) |
| **val_f1** | Balance of precision/recall | > 0.65 |

**⚠️ Watch for overfitting:**
- `train_accuracy` much higher than `val_accuracy` → Model memorizing training data

---

## 🎨 Customizing the View

### **Add/Remove Columns**
- Click **Columns** button
- Check/uncheck metrics and parameters
- Saves your preferences

### **Filter Runs**
- Click **Add Filter**
- Example: `params.n_estimators = 100`
- Example: `metrics.val_auc > 0.85`

### **Search Runs**
- Use search bar for run names
- Filter by tags or parameters

---

## 🚀 Pro Tips

1. **Tag Important Runs**: Add tags like "best_model", "production_candidate"
2. **Use Descriptive Run Names**: Not just "run_1", but "rf_tuned_v2"
3. **Download Before Deleting**: Always download artifacts before cleaning old runs
4. **Compare Baselines**: Keep a baseline run to compare against
5. **Check Git Commits**: Ensure reproducibility by checking source version

---

## 🐛 Troubleshooting

**Issue**: UI shows no experiments
- ✅ Check: Is `mlflow.db` in the project root?
- ✅ Run: `make train` to create a run first

**Issue**: Metrics not showing
- ✅ Check: Did training complete successfully?
- ✅ Check: Look for errors in training logs

**Issue**: Model not in registry
- ✅ Check: `registered_model_name` parameter in `log_model()`
- ✅ Re-run training if missing

---

## 📚 Quick Reference

```bash
# Start UI
make mlflow-ui

# Train and create new run
make train

# Access UI
http://localhost:5000

# Stop UI
Ctrl+C in terminal
```

**Navigation:**
- 🏠 Experiments → All experiments
- 🏃 Runs → Training runs
- 📦 Models → Model registry
- ⚙️ Settings → Configuration

---

**Need more?** See [MLflow Documentation](https://mlflow.org/docs/latest/tracking.html)

