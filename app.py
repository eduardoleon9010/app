import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import gspread
from google.oauth2.service_account import Credentials

# -------------------------------
# CONFIGURACIÓN DE LA PÁGINA
# -------------------------------
st.set_page_config(
    page_title="Dashboard NexaTech",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Dashboard de Contactos – NexaTech")
st.markdown("### Análisis interactivo de base de datos de networking")

# -------------------------------
# CONEXIÓN CON GOOGLE SHEETS
# -------------------------------
SHEET_KEY = "1qqtKqyNqNS7S5fpXenPZTPG5SpcwTmJ1zt9yP2a0coA"
SHEET_NAME = "Base de datos de contactos – NexaTech"

CREDENTIALS_PATH = "nexatech-automation-4aca961fd0d2.json"

scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_file(CREDENTIALS_PATH, scopes=scope)
gc = gspread.authorize(creds)
sheet = gc.open_by_key(SHEET_KEY)
worksheet = sheet.worksheet(SHEET_NAME)
data = pd.DataFrame(worksheet.get_all_records())

# -------------------------------
# LIMPIEZA Y PREPROCESAMIENTO
# -------------------------------
data.columns = [col.strip() for col in data.columns]
data.replace("", pd.NA, inplace=True)

# -------------------------------
# SIDEBAR DE FILTROS
# -------------------------------
st.sidebar.header("🔍 Filtros dinámicos")

sector = st.sidebar.multiselect(
    "Sector o industria",
    options=data["Sector o industria "].dropna().unique()
)

ciudad = st.sidebar.multiselect(
    "Ciudad y país",
    options=data["Ciudad y país"].dropna().unique()
)

contacto = st.sidebar.multiselect(
    "¿Prefieres que te contactemos por...?",
    options=data["¿Prefieres que te contactemos por...? "].dropna().unique()
)

df_filtered = data.copy()
if sector:
    df_filtered = df_filtered[df_filtered["Sector o industria "].isin(sector)]
if ciudad:
    df_filtered = df_filtered[df_filtered["Ciudad y país"].isin(ciudad)]
if contacto:
    df_filtered = df_filtered[df_filtered["¿Prefieres que te contactemos por...? "].isin(contacto)]

# -------------------------------
# DASHBOARD PRINCIPAL
# -------------------------------
st.markdown("## 📈 Análisis general")

col1, col2, col3 = st.columns(3)
col1.metric("Total de contactos", len(df_filtered))
col2.metric("Sectores únicos", df_filtered["Sector o industria "].nunique())
col3.metric("Ciudades", df_filtered["Ciudad y país"].nunique())

# -------------------------------
# GRAFICOS CON ESTILO OSCURO / NEON
# -------------------------------
neon_template = "plotly_dark"

# Gráfico 1: Contactos por sector
fig1 = px.bar(
    df_filtered,
    x="Sector o industria ",
    title="Contactos por Sector o Industria",
    color="Sector o industria ",
    template=neon_template
)
fig1.update_traces(marker=dict(line=dict(width=1, color="cyan")))
st.plotly_chart(fig1, use_container_width=True)

# Gráfico 2: Canales de contacto
fig2 = px.pie(
    df_filtered,
    names="¿Prefieres que te contactemos por...? ",
    title="Preferencia de Canal de Contacto",
    hole=0.5,
    color_discrete_sequence=px.colors.sequential.Plotly3
)
fig2.update_layout(template=neon_template)
st.plotly_chart(fig2, use_container_width=True)

# Gráfico 3: Interés en información
fig3 = px.histogram(
    df_filtered,
    x="Nivel de interés en recibir más información ",
    color="Nivel de interés en recibir más información ",
    title="Nivel de Interés en Información",
    template=neon_template
)
st.plotly_chart(fig3, use_container_width=True)

# Gráfico 4: Tamaño de empresa
fig4 = px.treemap(
    df_filtered,
    path=["Tamaño de tu empresa/proyecto "],
    title="Distribución por Tamaño de Empresa",
    color_discrete_sequence=["#00FFFF"]
)
fig4.update_layout(template=neon_template)
st.plotly_chart(fig4, use_container_width=True)

# -------------------------------
# DATOS EN TABLA
# -------------------------------
st.markdown("## 🗂️ Vista detallada de registros")
st.dataframe(df_filtered, use_container_width=True)

# -------------------------------
# DESCARGA DE DATOS
# -------------------------------
st.download_button(
    label="📥 Descargar datos filtrados (CSV)",
    data=df_filtered.to_csv(index=False).encode("utf-8"),
    file_name="base_contactos_filtrada.csv",
    mime="text/csv"
)
