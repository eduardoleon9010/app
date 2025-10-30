# app.py — Dashboard de Contactos NexaTech
# Desarrollado para Streamlit Cloud con integración segura a Google Sheets

import streamlit as st
import pandas as pd
import plotly.express as px
import gspread
from google.oauth2.service_account import Credentials

# ==============================
# 🔐 Conexión segura con Secrets
# ==============================
st.set_page_config(
    page_title="Dashboard de Contactos – NexaTech",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📊 Dashboard de Contactos – NexaTech")
st.markdown("### Análisis interactivo de la base de datos de networking empresarial")

try:
    creds_dict = st.secrets["gcp_service_account"]
    creds = Credentials.from_service_account_info(
        creds_dict,
        scopes=[
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ],
    )
    client = gspread.authorize(creds)

    # ===========================
    # 📂 Cargar datos del Sheet
    # ===========================
    SPREADSHEET_ID = "1qqtKqyNqNS7S5fpXenPZTPG5SpcwTmJ1zt9yP2a0coA"
    sheet = client.open_by_key(SPREADSHEET_ID).sheet1
    data = pd.DataFrame(sheet.get_all_records())

    st.success("✅ Datos cargados correctamente desde Google Sheets")
    st.caption(f"Total de registros: **{data.shape[0]}** filas – **{data.shape[1]}** columnas")

    # ===========================
    # 🎛️ Filtros Interactivos
    # ===========================
    st.sidebar.header("Filtros")
    sector = st.sidebar.multiselect(
        "Seleccionar Sector o Industria",
        options=sorted(data["Sector o industria "].dropna().unique()),
        default=[]
    )
    ciudad = st.sidebar.multiselect(
        "Seleccionar Ciudad o País",
        options=sorted(data["Ciudad y país"].dropna().unique()),
        default=[]
    )

    data_filtered = data.copy()
    if sector:
        data_filtered = data_filtered[data_filtered["Sector o industria "].isin(sector)]
    if ciudad:
        data_filtered = data_filtered[data_filtered["Ciudad y país"].isin(ciudad)]

    # ===========================
    # 📈 Gráficos Interactivos
    # ===========================

    # --- Contactos por Sector ---
    fig1 = px.histogram(
        data_filtered,
        x="Sector o industria ",
        color="Sector o industria ",
        title="Contactos por Sector o Industria",
        template="plotly_dark",
        color_discrete_sequence=px.colors.qualitative.Neon
    )

    # --- Contactos por Ciudad ---
    fig2 = px.histogram(
        data_filtered,
        x="Ciudad y país",
        color="Ciudad y país",
        title="Contactos por Ciudad o País",
        template="plotly_dark",
        color_discrete_sequence=px.colors.qualitative.Neon
    )

    # --- Nivel de interés ---
    fig3 = px.pie(
        data_filtered,
        names="Nivel de interés en recibir más información ",
        title="Distribución por Nivel de Interés",
        template="plotly_dark",
        color_discrete_sequence=px.colors.qualitative.Neon
    )

    # --- Tamaño de empresa ---
    fig4 = px.bar(
        data_filtered,
        x="Tamaño de tu empresa/proyecto ",
        title="Distribución por Tamaño de Empresa o Proyecto",
        template="plotly_dark",
        color_discrete_sequence=px.colors.qualitative.Neon
    )

    # ===========================
    # 🧩 Layout del Dashboard
    # ===========================
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig1, use_container_width=True)
    with col2:
        st.plotly_chart(fig2, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        st.plotly_chart(fig3, use_container_width=True)
    with col4:
        st.plotly_chart(fig4, use_container_width=True)

    # ===========================
    # 🧮 Vista de Datos
    # ===========================
    st.markdown("### 📋 Vista previa de los datos")
    st.dataframe(data_filtered)

except Exception as e:
    st.error("❌ Error al conectar o cargar los datos.")
    st.exception(e)
