# Exploratory Data Analysis (EDA) Checklist

## 🎯 High-Level Mindset

**Purpose of EDA:** Understand your data deeply before modeling. EDA is not just checking boxes—it's detective work to uncover insights, issues, and opportunities.

**Key Principles:**

1. **Trust nothing, verify everything** - Assumptions about data are often wrong
2. **Visual first, statistics second** - Plots reveal patterns statistics miss
3. **Question everything** - Why are there outliers? Why missing values? Why this distribution?
4. **Document as you go** - Future you will thank present you
5. **Think like your model** - What will confuse it? What features matter?

**The EDA Journey:**

```
Raw Data → Understanding → Quality Check → Relationships → Decisions → Action Plan
```

**Red Thread:** Every analysis should answer: _"How does this help me build a better model?"_

---

## 📊 Data Understanding

- [ ] **Load data** - Verify file loads correctly
- [ ] **Shape** - Number of rows and columns
- [ ] **Columns** - List all feature names
- [ ] **Data types** - Numeric vs categorical
- [ ] **Sample records** - View first/last rows

## 🔍 Data Quality

- [ ] **Missing values** - Count and percentage per column
- [ ] **Duplicates** - Check for duplicate rows
- [ ] **Data types** - Verify correct types (dates, numeric, categorical)
- [ ] **Value ranges** - Check min/max make sense
- [ ] **Inconsistencies** - Look for data entry errors

## 🎯 Target Variable

- [ ] **Distribution** - Count of each class
- [ ] **Imbalance** - Calculate class balance ratio (majority/minority). Thresholds: 1:1-3:1 (balanced), 3:1-10:1 (moderate, consider treatment), >10:1 (severe, must handle)
- [ ] **Values** - Verify encoding (binary, multiclass, etc.)

## 📈 Numerical Features

- [ ] **Distributions** - Histograms for each feature
- [ ] **Statistics** - Mean, median, std, quartiles
- [ ] **Outliers** - Box plots to detect outliers
- [ ] **Skewness** - Check if transformations needed
- [ ] **Correlation** - Heatmap of feature correlations
- [ ] **Multicollinearity** - Identify highly correlated pairs (|r| > 0.8)

### 📊 Understanding IQR Method for Outlier Detection

**IQR (Interquartile Range) = Q3 - Q1**

```
Q1 (25th percentile) ──┐
                       │ IQR = Q3 - Q1
Q3 (75th percentile) ──┘

Outlier Boundaries:
  Lower: Q1 - 1.5 × IQR
  Upper: Q3 + 1.5 × IQR

Anything outside these bounds = Outlier
```

**When to use IQR:**

- Default method for outlier detection (works for any distribution)
- More robust than mean ± 3σ (not affected by outliers themselves)
- Good for skewed data

**How to interpret:**

- Few outliers (< 5%) → Normal variation, usually keep
- Many outliers (> 10%) → Investigate: data errors? real pattern? different segment?
- All outliers in one direction → Skewed distribution, consider log transform

**What to do with outliers:**

- Keep if: Legitimate values, important for business, small percentage
- Cap if: Extreme values distort model (winsorization at 95th/99th percentile)
- Remove if: Data errors, measurement mistakes
- Transform if: Log/sqrt can normalize distribution

## 🏷️ Categorical Features

- [ ] **Unique values** - Count categories per feature
- [ ] **Frequency** - Value counts for each category
- [ ] **Cardinality** - High cardinality features (>50 categories)
- [ ] **Encoding strategy** - Decide one-hot, label, target encoding

## 🔗 Feature Relationships

- [ ] **Numeric vs Target** - Box plots, violin plots
- [ ] **Categorical vs Target** - Target rate by category
- [ ] **Feature interactions** - Scatter plots for key pairs
- [ ] **Important features** - Identify potential predictors

### 📊 Understanding Chi-Square Test (chi2_contingency)

**What it tests:** Whether two categorical variables are independent or related

**Formula:** χ² = Σ [(Observed - Expected)² / Expected]

**Hypotheses:**

- H₀ (null): Variables are independent (no relationship)
- H₁ (alternative): Variables are related

**When to use:**

- Testing if categorical feature is related to categorical target
- Example: Is "Contract Type" related to "Churn"?
- Both variables must be categorical

**How to interpret p-value:**

- p < 0.05 → **Significant** (feature IS related to target, keep it!)
- p ≥ 0.05 → Not significant (weak/no relationship, consider dropping)
- Lower p-value = stronger relationship

**Example:**

```
Contract Type vs Churn:
  χ² = 1200.5, p-value = 0.0001
  → p < 0.05: Contract type significantly affects churn! ✓

Gender vs Churn:
  χ² = 0.5, p-value = 0.48
  → p ≥ 0.05: Gender doesn't affect churn ✗
```

**Requirements:**

- Sample size: Need at least 5 expected counts in each cell
- If violated → Use Fisher's exact test instead
- Works only for categorical × categorical relationships

**What to do:**

- p < 0.01 → Very strong, definitely keep feature
- 0.01 ≤ p < 0.05 → Significant, keep feature
- p ≥ 0.05 → Not significant, consider dropping or combining categories

**⚠️ CRITICAL WARNING:**

- **Never assume patterns** - Always verify with actual data first
- **Don't use "expected" values** - Calculate real medians/means before interpreting
- **Let data speak** - Your assumptions about "typical" patterns may be wrong
- **Quantify differences** - Use actual numbers, not visual impressions alone

## ⚙️ Data Preparation Decisions

- [ ] **Missing values strategy** - Drop, impute (mean/median/mode/model), or keep as feature
- [ ] **Outliers handling** - Keep, cap (winsorize), transform, or remove
- [ ] **Feature engineering** - New features to create (ratios, bins, interactions, aggregations)
- [ ] **Features to drop** - IDs, constants, redundant, high-cardinality, leakage
- [ ] **Scaling** - StandardScaler, MinMaxScaler, RobustScaler, or none
- [ ] **Encoding** - One-hot, label, target, ordinal, frequency, or embeddings
- [ ] **Class imbalance** - SMOTE, undersampling, oversampling, or class weights

## 📝 Documentation

- [ ] **Key insights** - Top 3-5 findings
- [ ] **Data issues** - Problems found and solutions
- [ ] **Feature importance** - Preliminary ranking
- [ ] **Next steps** - Action items for modeling

## ⚠️ Critical Red Flags

- [ ] **Data leakage** - Features that contain future/target information
- [ ] **Temporal issues** - Time-based data split incorrectly or mixed
- [ ] **Label quality** - Mislabeled, inconsistent, or noisy targets
- [ ] **Sample bias** - Training data not representative of real-world
- [ ] **Severe imbalance** - Extreme class imbalance (>95/5 or worse)
- [ ] **Duplicate records** - Same instance appearing multiple times
- [ ] **Train/test mismatch** - Different distributions or feature ranges

---

## 📚 Statistical Methods Quick Reference

### **IQR Method (Outlier Detection)**

```
Purpose: Find unusual values in numerical data
Method:  Q1 - 1.5×IQR to Q3 + 1.5×IQR
Use for: Any numerical feature
Action:  Investigate outliers, decide keep/cap/remove
```

### **Chi-Square Test (Categorical Relationships)**

```
Purpose: Test if categorical feature relates to target
Method:  chi2_contingency(crosstab(feature, target))
Use for: Categorical × Categorical
Action:  p < 0.05 → Keep feature; p ≥ 0.05 → Consider dropping
```

### **Correlation (Numerical Relationships)**

```
Purpose: Measure linear relationship strength
Method:  df.corr() or corrwith()
Use for: Numerical × Numerical
Range:   -1 (negative) to +1 (positive), 0 = no correlation
```

### **When to Use Which Test:**

| Your Data                 | Target Type                        | Use This Test |
| ------------------------- | ---------------------------------- | ------------- |
| Numerical → Numerical     | Correlation (Pearson/Spearman)     |
| Numerical → Categorical   | T-test, ANOVA, or compare medians  |
| Categorical → Categorical | Chi-Square test                    |
| Any → Any                 | Visual inspection first, then test |

---

## 💡 Final Checks Before Modeling

- [ ] Can explain every preprocessing decision
- [ ] Documented all data quality issues
- [ ] Identified 3-5 most important features (hypothesis)
- [ ] Know baseline performance to beat
- [ ] Have validation strategy that matches production scenario
