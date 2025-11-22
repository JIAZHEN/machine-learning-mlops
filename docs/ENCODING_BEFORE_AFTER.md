# Before vs After: Categorical Encoding

## 🔍 Why This Matters

Machine learning models require **numeric input**. Text categories like "Male", "Female", "DSL" cannot be processed by algorithms.

---

## 📊 Before Encoding (Current State)

### Sample Row from `data/processed/train.csv`:
```csv
gender,SeniorCitizen,Partner,Dependents,tenure,PhoneService,MultipleLines,InternetService,...,Churn
Male,0,No,No,26,Yes,No,DSL,...,0
```

### Data Types:
- **Text/Categorical** 🔴: `gender`, `Partner`, `Dependents`, `PhoneService`, `MultipleLines`, `InternetService`, `OnlineSecurity`, `OnlineBackup`, `DeviceProtection`, `TechSupport`, `StreamingTV`, `StreamingMovies`, `Contract`, `PaperlessBilling`, `PaymentMethod`, `tenure_bin`
- **Numeric** ✅: `SeniorCitizen`, `tenure`, `MonthlyCharges`, `TotalCharges`, `numAdminTickets`, `numTechTickets`, `avg_monthly_charges`
- **Target** ✅: `Churn` (0/1)

### Problem:
❌ Models like Random Forest, XGBoost, Neural Networks **cannot** process text  
❌ Will throw errors or silently fail  
❌ Need to convert "Male" → numeric representation

---

## 🎯 After Encoding (With One-Hot Encoding)

### What One-Hot Encoding Does:

**Original Column:**
```
gender
------
Male
Female
Male
```

**After One-Hot Encoding:**
```
gender_Female  gender_Male
-----------    -----------
0              1
1              0
0              1
```

Each category becomes a **binary column** (0 or 1).

---

## 🔢 Expected Output After Encoding

### From ~24 columns → ~60-70 columns

#### Original Categories → One-Hot Columns:

1. **gender** (2 values) → `gender_Female`, `gender_Male`
2. **Partner** (2 values) → `Partner_No`, `Partner_Yes`
3. **Dependents** (2 values) → `Dependents_No`, `Dependents_Yes`
4. **PhoneService** (2 values) → `PhoneService_No`, `PhoneService_Yes`
5. **MultipleLines** (3 values) → `MultipleLines_No`, `MultipleLines_No phone service`, `MultipleLines_Yes`
6. **InternetService** (3 values) → `InternetService_DSL`, `InternetService_Fiber optic`, `InternetService_No`
7. **OnlineSecurity** (3 values) → `OnlineSecurity_No`, `OnlineSecurity_No internet service`, `OnlineSecurity_Yes`
8. **OnlineBackup** (3 values) → `OnlineBackup_No`, `OnlineBackup_No internet service`, `OnlineBackup_Yes`
9. **DeviceProtection** (3 values) → Similar to above
10. **TechSupport** (3 values) → Similar to above
11. **StreamingTV** (3 values) → Similar to above
12. **StreamingMovies** (3 values) → Similar to above
13. **Contract** (3 values) → `Contract_Month-to-month`, `Contract_One year`, `Contract_Two year`
14. **PaperlessBilling** (2 values) → `PaperlessBilling_No`, `PaperlessBilling_Yes`
15. **PaymentMethod** (4 values) → `PaymentMethod_Bank transfer (automatic)`, `PaymentMethod_Credit card (automatic)`, `PaymentMethod_Electronic check`, `PaymentMethod_Mailed check`
16. **tenure_bin** (4 values) → `tenure_bin_0-1yr`, `tenure_bin_1-2yr`, `tenure_bin_2-4yr`, `tenure_bin_4+yr`

**Numeric columns remain unchanged:**
- `SeniorCitizen`, `tenure`, `MonthlyCharges`, `TotalCharges`, `numAdminTickets`, `numTechTickets`, `avg_monthly_charges`

**Target remains:**
- `Churn` (0/1)

---

## 🆚 Side-by-Side Comparison

### Before (24 columns):
```
gender | SeniorCitizen | Partner | tenure | Contract      | MonthlyCharges | Churn
Male   | 0             | No      | 26     | One year      | 59.45          | 0
Male   | 1             | Yes     | 72     | Two year      | 116.05         | 0
Female | 0             | No      | 1      | Month-to-month| 29.85          | 1
```
❌ Models cannot use "Male", "No", "One year" directly

### After (~60-70 columns):
```
gender_Male | gender_Female | SeniorCitizen | Partner_Yes | Partner_No | tenure | Contract_One year | Contract_Two year | Contract_Month-to-month | MonthlyCharges | Churn
1           | 0             | 0             | 0           | 1          | 26     | 1                 | 0                 | 0                       | 59.45          | 0
1           | 0             | 1             | 1           | 0          | 72     | 0                 | 1                 | 0                       | 116.05         | 0
0           | 1             | 0             | 0           | 1          | 1      | 0                 | 0                 | 1                       | 29.85          | 1
```
✅ All columns are now numeric (0s and 1s, plus continuous values)

---

## 🛠️ What We Added to the Pipeline

### 1. Created `src/data/encoding.py`

**Main Function:**
```python
def encode_categorical_features(df, encoding_type='onehot'):
    """
    Encode categorical features to numeric format.
    
    - encoding_type='onehot': Creates binary columns (recommended)
    - encoding_type='label': Converts to integers (0,1,2,...)
    """
    # Automatically detects columns with text/object dtype
    # Uses pd.get_dummies() for one-hot encoding
    # Returns DataFrame with all numeric columns
```

### 2. Updated `src/pipeline.py`

**Added Step 7 (between feature engineering and splitting):**
```python
# Step 7: Encode categorical features
print("\n[7/8] Encoding categorical features...")
df = encode_categorical_features(df, encoding_type='onehot')
print("✓ Categorical features encoded")
```

**Pipeline Flow (8 steps now):**
1. Load raw data
2. Convert data types (TotalCharges string → numeric)
3. Clean data (missing values)
4. Validate data
5. Encode target (Churn: Yes/No → 1/0)
6. Engineer features (tenure_bin, avg_monthly_charges)
7. **🆕 Encode categorical features (text → numeric)** ← NEW!
8. Split data (train/val/test)

---

## 📈 Benefits of One-Hot Encoding

### ✅ Advantages:
1. **No ordinal assumption**: "Male" vs "Female" are not ordered (0 vs 1 implies order)
2. **Works with all algorithms**: Random Forest, XGBoost, Neural Networks, etc.
3. **Interpretable**: Each binary column has clear meaning
4. **Captures all information**: No information loss

### ⚠️ Considerations:
1. **Increases dimensionality**: 24 columns → 60-70 columns
2. **Sparse data**: Many 0s, only one 1 per category
3. **Memory usage**: More columns = more memory

### Alternative: Label Encoding
If you prefer fewer columns, change to `encoding_type='label'`:
```python
# This would convert:
# "Male" → 0, "Female" → 1
# "Month-to-month" → 0, "One year" → 1, "Two year" → 2
```
**Downside**: Implies ordering (Month-to-month < One year < Two year), which may not be meaningful.

---

## 🚀 Running the Updated Pipeline

```bash
# Clean old processed data
rm -rf data/processed/*.csv

# Run updated pipeline with encoding
python src/pipeline.py

# Or use Makefile
make data
```

### Expected Output:
```
Starting Data Processing Pipeline
============================================================

[1/8] Loading raw data...
✓ Loaded 7043 rows

[2/8] Converting data types...
✓ Data types converted

[3/8] Cleaning data...
✓ Cleaned data: 7032 rows remaining

[4/8] Validating data...
✓ Data validated

[5/8] Encoding target variable...
✓ Target encoded

[6/8] Engineering features...
✓ Features engineered

[7/8] Encoding categorical features...
  Encoding 16 categorical columns...
  ✓ One-hot encoding complete: 67 total columns
✓ Categorical features encoded

[8/8] Splitting data into train/val/test sets...
Train size: 4508
Validation size: 1128
Test size: 1410
Saved splits to data/processed

============================================================
Data Pipeline Complete!
============================================================

Processed data saved to: data/processed/
  - train.csv: 4508 samples
  - val.csv: 1128 samples
  - test.csv: 1410 samples

Ready for model training!
```

---

## ✅ Verification

After running, check the processed data:

```bash
# Check number of columns (should be ~60-70)
head -1 data/processed/train.csv | awk -F',' '{print NF}'

# Check first few column names
head -1 data/processed/train.csv | tr ',' '\n' | head -20

# Verify all values are numeric (no text)
head -5 data/processed/train.csv
```

**All values should now be numbers!** 🎉

---

## 🎓 Key Takeaway

**Before**: Text categories → ❌ Models fail  
**After**: All numeric → ✅ Models work  

One-hot encoding is the **bridge** between raw data and machine learning models!

