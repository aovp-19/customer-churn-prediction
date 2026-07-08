from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

model = joblib.load("model/churn_model.pkl")
model_columns = joblib.load("model/model_columns.pkl")
scaler = joblib.load("model/scaler.pkl")

app = FastAPI(title="Churn Prediction API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ClienteInput(BaseModel):
    gender: str
    SeniorCitizen: int
    Partner: str
    Dependents: str
    tenure: int
    PhoneService: str
    MultipleLines: str
    InternetService: str
    OnlineSecurity: str
    OnlineBackup: str
    DeviceProtection: str
    TechSupport: str
    StreamingTV: str
    StreamingMovies: str
    Contract: str
    PaperlessBilling: str
    PaymentMethod: str
    MonthlyCharges: float
    TotalCharges: float

@app.get("/")
def read_root():
    return RedirectResponse(url="/index.html")

@app.post("/predict")
def predict_churn(cliente: ClienteInput):
    input_df = pd.DataFrame([cliente.dict()])

    binary_map = {'Yes': 1, 'No': 0}
    binary_cols = ['Partner', 'Dependents', 'PhoneService', 'PaperlessBilling']
    for col in binary_cols:
        input_df[col] = input_df[col].map(binary_map)

    input_df['gender'] = input_df['gender'].map({'Male': 1, 'Female': 0})

    multi_cat_cols = [
        'MultipleLines', 'InternetService', 'OnlineSecurity', 'OnlineBackup',
        'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies',
        'Contract', 'PaymentMethod'
    ]
    input_df = pd.get_dummies(input_df, columns=multi_cat_cols)
    input_df = input_df.reindex(columns=model_columns, fill_value=0)

    probabilidad_churn = model.predict_proba(input_df)[0][1]
    prediccion = model.predict(input_df)[0]

    return {
        "prediccion": "Churn" if prediccion == 1 else "No Churn",
        "probabilidad_churn": round(float(probabilidad_churn), 4)
    }

# Se monta al final para no tapar las rutas de arriba (/predict, /docs, etc.)
app.mount("/", StaticFiles(directory="../frontend", html=True), name="frontend")