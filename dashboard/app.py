import streamlit as st
import pandas as pd
import joblib
import os

# Carpeta donde vive este mismo archivo (app.py), sin importar el directorio
# de trabajo desde el que Streamlit Cloud ejecute el proceso.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# --- Configuración general de la página ---
st.set_page_config(
    page_title="Dashboard de Churn",
    page_icon="📊",
    layout="wide"
)

# --- Carga de datos y modelo ---
@st.cache_data
def cargar_datos():
    ruta_csv = os.path.join(BASE_DIR, "telco_churn_clean.csv")
    data = pd.read_csv(ruta_csv)

    if data["Churn"].dtype == "object":
        data["Churn"] = data["Churn"].map({"Yes": 1, "No": 0})

    return data

@st.cache_resource
def cargar_modelo():
    model = joblib.load(os.path.join(BASE_DIR, "model", "churn_model.pkl"))
    columns = joblib.load(os.path.join(BASE_DIR, "model", "model_columns.pkl"))
    return model, columns

df = cargar_datos()
model, model_columns = cargar_modelo()

st.title("📊 Dashboard de Predicción de Churn")

# ==========================================================================
# 9.2 SIDEBAR DE FILTROS
# ==========================================================================
st.sidebar.header("Filtros")

contrato_opciones = ["Todos", "Month-to-month", "One year", "Two year"]
contrato_sel = st.sidebar.selectbox("Tipo de contrato", contrato_opciones)

internet_opciones = ["Todos", "DSL", "Fiber optic", "No"]
internet_sel = st.sidebar.selectbox("Servicio de internet", internet_opciones)

tenure_min, tenure_max = st.sidebar.slider(
    "Antigüedad (meses)",
    min_value=int(df["tenure"].min()),
    max_value=int(df["tenure"].max()),
    value=(int(df["tenure"].min()), int(df["tenure"].max()))
)

df_filtrado = df.copy()

if contrato_sel != "Todos":
    if contrato_sel == "Month-to-month":
        df_filtrado = df_filtrado[
            (df_filtrado["Contract_One year"] == False) &
            (df_filtrado["Contract_Two year"] == False)
        ]
    else:
        col_contrato = f"Contract_{contrato_sel}"
        df_filtrado = df_filtrado[df_filtrado[col_contrato] == True]

if internet_sel != "Todos":
    if internet_sel == "DSL":
        df_filtrado = df_filtrado[
            (df_filtrado["InternetService_Fiber optic"] == False) &
            (df_filtrado["InternetService_No"] == False)
        ]
    else:
        col_internet = f"InternetService_{internet_sel}"
        df_filtrado = df_filtrado[df_filtrado[col_internet] == True]

df_filtrado = df_filtrado[
    (df_filtrado["tenure"] >= tenure_min) & (df_filtrado["tenure"] <= tenure_max)
]

# ==========================================================================
# 9.1 KPIs PRINCIPALES
# ==========================================================================
col1, col2, col3 = st.columns(3)

total_clientes = len(df_filtrado)
tasa_churn = df_filtrado["Churn"].mean() * 100
ingreso_en_riesgo = df_filtrado.loc[df_filtrado["Churn"] == 1, "MonthlyCharges"].sum()

col1.metric("Clientes (según filtros)", f"{total_clientes:,}")
col2.metric("Tasa de churn", f"{tasa_churn:.1f}%")
col3.metric("Ingreso mensual en riesgo", f"${ingreso_en_riesgo:,.2f}")