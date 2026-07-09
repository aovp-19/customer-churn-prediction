import streamlit as st
import pandas as pd
import joblib

# --- Configuración general de la página ---
st.set_page_config(
    page_title="Dashboard de Churn",
    layout="wide"                  # Usa todo el ancho de la pantalla, mejor para dashboards
)

# --- Carga de datos y modelo ---
@st.cache_data
def cargar_datos():
    data = pd.read_csv("telco_churn_clean.csv")

    # Corrección defensiva: si Churn todavía viene como texto, se convierte.
    if data["Churn"].dtype == "object":
        data["Churn"] = data["Churn"].map({"Yes": 1, "No": 0})

    return data

@st.cache_resource  # cache_resource es para objetos pesados como modelos, no datos
def cargar_modelo():
    model = joblib.load("model/churn_model.pkl")
    columns = joblib.load("model/model_columns.pkl")
    return model, columns

df = cargar_datos()
model, model_columns = cargar_modelo()

st.title("📊 Dashboard de Predicción de Churn")

# ==========================================================================
# 9.2 SIDEBAR DE FILTROS
# ==========================================================================
st.sidebar.header("Filtros")

# Filtro de tipo de contrato: usamos las columnas dummy ya existentes
# (Contract_One year, Contract_Two year) para reconstruir la categoría
contrato_opciones = ["Todos", "Month-to-month", "One year", "Two year"]
contrato_sel = st.sidebar.selectbox("Tipo de contrato", contrato_opciones)

# Filtro de servicio de internet
internet_opciones = ["Todos", "DSL", "Fiber optic", "No"]
internet_sel = st.sidebar.selectbox("Servicio de internet", internet_opciones)

# Filtro de antigüedad (tenure), como rango deslizante
tenure_min, tenure_max = st.sidebar.slider(
    "Antigüedad (meses)",
    min_value=int(df["tenure"].min()),
    max_value=int(df["tenure"].max()),
    value=(int(df["tenure"].min()), int(df["tenure"].max()))  # rango completo por defecto
)

# --- Aplicamos los filtros al DataFrame ---
df_filtrado = df.copy()

if contrato_sel != "Todos":
    if contrato_sel == "Month-to-month":
        # Es la categoría de referencia: ambas dummies de contrato en False
        df_filtrado = df_filtrado[
            (df_filtrado["Contract_One year"] == False) &
            (df_filtrado["Contract_Two year"] == False)
        ]
    else:
        col_contrato = f"Contract_{contrato_sel}"
        df_filtrado = df_filtrado[df_filtrado[col_contrato] == True]

if internet_sel != "Todos":
    if internet_sel == "DSL":
        # Categoría de referencia de internet
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
col1, col2, col3 = st.columns(3)  # 3 tarjetas lado a lado

total_clientes = len(df_filtrado)
tasa_churn = df_filtrado["Churn"].mean() * 100
ingreso_en_riesgo = df_filtrado.loc[df_filtrado["Churn"] == 1, "MonthlyCharges"].sum()

col1.metric("Clientes (según filtros)", f"{total_clientes:,}")
col2.metric("Tasa de churn", f"{tasa_churn:.1f}%")
col3.metric("Ingreso mensual en riesgo", f"${ingreso_en_riesgo:,.2f}")