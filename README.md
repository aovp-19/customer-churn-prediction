# Customer Churn Prediction — End-to-End ML Pipeline

An end-to-end machine learning project predicting customer churn for a telecommunications company, covering the full lifecycle from data cleaning to a fully deployed, production-style system: a REST API, a customer-facing web app, and an interactive analytics dashboard.

## 🔗 Live Demo

| Component | URL |
|---|---|
| 🌐 Web App (landing + prediction form) | [customer-churn-prediction-frontend.onrender.com](https://customer-churn-prediction-frontend.onrender.com) |
| ⚙️ API (Swagger docs) | [customer-churn-prediction-2h2t.onrender.com/docs](https://customer-churn-prediction-2h2t.onrender.com/docs) |
| 📊 Interactive Dashboard | [dashboard-chrun-clientes.streamlit.app](https://dashboard-chrun-clientes.streamlit.app) |

> **Note:** the API and web app are hosted on Render's free tier, which spins down after periods of inactivity. The first request may take 10–30 seconds to respond while the service wakes up.

## 📌 Project Overview

Customer churn is one of the most costly problems in subscription-based businesses. This project builds a classification model to predict which customers are likely to abandon the service, enabling proactive retention strategies.

Beyond modeling, the goal of this project is to demonstrate the complete data science workflow: from data cleaning and exploratory analysis, through model training and evaluation, to serving the model as a real API, containerizing it with Docker, deploying it to the cloud, and exposing both a customer-facing tool and a business-facing analytics dashboard.

## 🗂️ Dataset

[Telco Customer Churn](https://www.kaggle.com/datasets/blastchar/telco-customer-churn) (Kaggle) — 7,043 customer records with demographic, account, and service usage information.

## 🛠️ Tech Stack

**Data & Modeling:** Python · Pandas · NumPy · Scikit-learn · Matplotlib · Seaborn

**Backend & Deployment:** FastAPI · Docker · Docker Compose · Render

**Dashboard:** Streamlit · Streamlit Community Cloud

**Frontend:** HTML · CSS · JavaScript · Bootstrap 5

## 🏗️ Architecture

The system is composed of three independent, containerized/deployable services, connected through a REST API:

```
├── notebook/       → Full analysis: ETL, EDA, modeling, evaluation
├── api/            → FastAPI service serving the trained model (Dockerized, deployed on Render)
├── frontend/       → Static landing page + prediction form (Dockerized, deployed on Render)
├── dashboard/      → Streamlit analytics dashboard (deployed on Streamlit Community Cloud)
└── docker-compose.yml
```

The **web app** sends a customer's profile to the **API**, which returns a churn probability and prediction; the frontend then generates tailored retention recommendations client-side based on the risk factors identified during the EDA. The **dashboard** independently loads the cleaned dataset and the same trained model to provide aggregate, filterable analysis for business/retention teams.

## 📊 Project Structure (Notebook)

The full analysis follows a structured pipeline, documented step by step with data-driven interpretations at each stage:

1. **ETL** — Data cleaning, type correction, and encoding of categorical variables
2. **EDA** — Exploratory analysis of churn distribution, numerical/categorical relationships, and correlation analysis
3. **Model Training & Evaluation** — Baseline Logistic Regression, evaluated with precision, recall, F1-score, and AUC-ROC (prioritized over accuracy due to class imbalance)
4. **Model Improvement** — Random Forest comparison and hyperparameter tuning via Grid Search
5. **Model Serialization** — Exporting the trained model, encoding columns, and scaler with `joblib`
6. **REST API (FastAPI)** — `/predict` endpoint serving real-time predictions
7. **Containerization (Docker)** — Separate images for the API and frontend, orchestrated with `docker-compose`
8. **Deployment (Render)** — API as a Web Service, frontend as a Static Site
9. **Interactive Dashboard (Streamlit)** — Filterable KPIs and churn analysis for business users

## 📈 Results Summary

| Model                           | AUC-ROC   | Recall (Churn) | Precision (Churn) |
|----------------------------------|:---------:|:---------------:|:-------------------:|
| Logistic Regression (baseline)  | 0.842     | 0.78            | 0.50               |
| Random Forest (default)         | 0.829     | 0.49            | 0.63               |
| **Random Forest (tuned)**       | **0.844** | **0.78**        | 0.55               |

The tuned Random Forest (`max_depth=10`, `min_samples_leaf=5`, `n_estimators=200`) was selected as the final model, matching the baseline's recall while improving precision, F1-score, and AUC — the best trade-off for the business objective of identifying at-risk customers early.

## 📓 Notebook

The full analysis, including data-driven interpretations and business-oriented conclusions at each step, is available in [`Predicción_de_Churn_de_Clientes.ipynb`](./notebook/Predicción_de_Churn_de_Clientes.ipynb).

## 🚀 Running Locally

```bash
git clone https://github.com/aovp-19/customer-churn-prediction.git
cd customer-churn-prediction
docker-compose up --build
```

- Web app: `http://localhost`
- API docs: `http://localhost:8000/docs`

## 👤 Author

**Almy Ventura** — Computer Science Engineering Student, PUCMM
[LinkedIn](https://linkedin.com/in/almy-ventura-7b453b383) · [GitHub](https://github.com/aovp-19)
