import streamlit as st
import pandas as pd
import plotly.express as px
from google.oauth2.service_account import Credentials
import gspread

# ==============================
# ⚙️ CONFIGURACIÓN INICIAL
# ==============================
st.set_page_config(
    page_title="Dashboard de Contactos – NexaTech",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📊 Dashboard de Contactos – NexaTech")
st.markdown("#### Análisis interactivo de base de datos de networking")

# ==============================
# 🔐 CONEXIÓN SEGURA CON GOOGLE SHEETS
# ==============================
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

# Usa las credenciales seguras desde Streamlit Secrets
creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)
client = gspread.authorize(creds)

# ID del Sheet (solo cambia este si usas otro documento)
SHEET_ID = "1qqtKqyNqNS7S5fpXenPZTPG5SpcwTmJ1zt9yP2a0coA"
sheet = client.open_by_key(SHEET_ID)
worksheet = sheet.sheet1

# Cargar los datos
data = pd.DataFrame(worksheet.get_all_records())

# Limpiar los nombres de columnas
data.columns = data.columns.str.strip()

# ==============================
# 🎨 CONFIGURACIÓN VISUAL GENERAL
# ==============================
st.markdown("""
<style>
body {background-color: #0e1117; color: white;}
[data-testid="stSidebar"] {background-color: #111418;}
.block-container {padding-top: 2rem; padding-bottom: 2rem;}
h1, h2, h3, h4 {color: #0ef;}
</style>
""", unsafe_allow_html=True)

# ==============================
# 🎛️ FILTROS INTERACTIVOS
# ==============================
st.sidebar.header("🎚️ Filtros de datos")

ciudad = st.sidebar.multiselect("Ciudad o país", options=data["Ciudad y país"].unique())
sector = st.sidebar.multiselect("Sector o industria", options=data["Sector o industria"].unique())

filtered_data = data.copy()
if ciudad:
    filtered_data = filtered_data[filtered_data["Ciudad y país"].isin(ciudad)]
if sector:
    filtered_data = filtered_data[filtered_data["Sector o industria"].isin(sector)]

st.sidebar.markdown("---")
st.sidebar.write(f"**Total de registros filtrados:** {len(filtered_data)}")

# ==============================
# 📊 DASHBOARD PRINCIPAL
# ==============================

col1, col2 = st.columns(2)

# --- Gráfico 1: Contactos por Sector ---
with col1:
    if "Sector o industria" in filtered_data.columns:
        fig1 = px.bar(
            filtered_data,
            x="Sector o industria",
            color="Sector o industria",
            title="Contactos por Sector o Industria",
            color_discrete_sequence=px.colors.sequential.Viridis_r
        )
        fig1.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white"),
            title_font=dict(size=18),
        )
        st.plotly_chart(fig1, use_container_width=True)

# --- Gráfico 2: Nivel de interés ---
with col2:
    if "Nivel de interés en recibir más información" in filtered_data.columns:
        fig2 = px.pie(
            filtered_data,
            names="Nivel de interés en recibir más información",
            title="Distribución de Nivel de Interés",
            color_discrete_sequence=px.colors.qualitative.Dark2
        )
        fig2.update_traces(textinfo="percent+label", textfont_size=14)
        fig2.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white"),
        )
        st.plotly_chart(fig2, use_container_width=True)

# --- Gráfico 3: Preferencia de contacto ---
col3, col4 = st.columns(2)

with col3:
    if "¿Prefieres que te contactemos por...?" in filtered_data.columns:
        fig3 = px.histogram(
            filtered_data,
            x="¿Prefieres que te contactemos por...?",
            title="Preferencia de Canal de Contacto",
            color_discrete_sequence=["#00f5d4"]
        )
        fig3.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white"),
        )
        st.plotly_chart(fig3, use_container_width=True)

# --- Gráfico 4: Tamaño de empresa ---
with col4:
    if "Tamaño de tu empresa/proyecto" in filtered_data.columns:
        fig4 = px.bar(
            filtered_data,
            x="Tamaño de tu empresa/proyecto",
            title="Tamaño de Empresa o Proyecto",
            color_discrete_sequence=["#ff6ec7"]
        )
        fig4.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white"),
        )
        st.plotly_chart(fig4, use_container_width=True)

# ==============================
# 📋 TABLA DETALLADA
# ==============================
st.markdown("### 📄 Detalle de contactos filtrados")
st.dataframe(filtered_data, use_container_width=True)
