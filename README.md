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

## 2. Dataset

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
