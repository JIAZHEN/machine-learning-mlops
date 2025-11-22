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
- [ ] **Imbalance** - Calculate class balance ratio
- [ ] **Values** - Verify encoding (binary, multiclass, etc.)

## 📈 Numerical Features

- [ ] **Distributions** - Histograms for each feature
- [ ] **Statistics** - Mean, median, std, quartiles
- [ ] **Outliers** - Box plots to detect outliers
- [ ] **Skewness** - Check if transformations needed
- [ ] **Correlation** - Heatmap of feature correlations
- [ ] **Multicollinearity** - Identify highly correlated pairs (|r| > 0.8)

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

## 💡 Final Checks Before Modeling

- [ ] Can explain every preprocessing decision
- [ ] Documented all data quality issues
- [ ] Identified 3-5 most important features (hypothesis)
- [ ] Know baseline performance to beat
- [ ] Have validation strategy that matches production scenario
