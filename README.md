# Customer Churn Prediction — End-to-End ML Pipeline

An end-to-end machine learning project predicting customer churn for a telecommunications company, covering the full lifecycle from data cleaning to (planned) production deployment.

## 📌 Project Overview

Customer churn is one of the most costly problems in subscription-based businesses. This project builds a classification model to predict which customers are likely to abandon the service, enabling proactive retention strategies.

Beyond modeling, the goal of this project is to demonstrate the complete data science workflow: from data cleaning and exploratory analysis, through model training and evaluation, to (in progress) serving the model as a real API, containerized with Docker, and exposed through an interactive dashboard.

## 🗂️ Dataset

[Telco Customer Churn](https://www.kaggle.com/datasets/blastchar/telco-customer-churn) (Kaggle) — 7,043 customer records with demographic, account, and service usage information.

## 🛠️ Tech Stack

**Data & Modeling:** Python · Pandas · NumPy · Scikit-learn · Matplotlib · Seaborn
**Planned (in progress):** FastAPI · Docker · Streamlit

## 📊 Project Structure

The analysis follows a structured pipeline, documented step by step in the notebook:

1. **ETL** — Data cleaning, type correction, and encoding of categorical variables
2. **EDA** — Exploratory analysis of churn distribution, numerical/categorical relationships, and correlation analysis
3. **Model Training & Evaluation** — Baseline Logistic Regression model, evaluated with precision, recall, F1-score, and AUC-ROC (prioritized over accuracy due to class imbalance)
4. **Model Improvement** — Random Forest comparison and hyperparameter tuning via Grid Search
5. **Model Serialization** *(in progress)*
6. **REST API (FastAPI)** *(in progress)*
7. **Containerization (Docker)** *(in progress)*
8. **Deployment** *(in progress)*
9. **Interactive Dashboard (Streamlit)** *(in progress)*

## 📈 Results Summary

| Model | AUC-ROC | Recall (Churn) | Precision (Churn) |
|---|---|---|---|
| Logistic Regression (baseline) | 0.842 | 0.78 | 0.50 |
| Random Forest (default) | 0.829 | 0.49 | 0.63 |
| **Random Forest (tuned)** | **0.844** | **0.78** | 0.55 |

The tuned Random Forest (`max_depth=10`, `min_samples_leaf=5`, `n_estimators=200`) was selected as the final model, matching the baseline's recall while improving precision, F1-score, and AUC — the best trade-off for the business objective of identifying at-risk customers early.

## 📓 Notebook

The full analysis, including data-driven interpretations and business-oriented conclusions at each step, is available in [`customer_churn_prediction.ipynb`](./Predicción_de_Churn_de_Clientes.ipynb).

## 🚧 Status

Actively in development. Sections 1-4 complete; API, containerization, deployment, and dashboard in progress.

## 👤 Author

**Almy Ventura** — Computer Science Engineering Student, PUCMM
[LinkedIn](https://linkedin.com/in/almy-ventura-7b453b383) · [GitHub](https://github.com/aovp-19)
