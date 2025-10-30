import streamlit as st
import pandas as pd
import plotly.express as px
import gspread
from google.oauth2.service_account import Credentials
import os

# -------------------------------------------------
# 🔐 CONFIGURACIÓN SEGURA (usa variables de entorno)
# -------------------------------------------------
# En Streamlit Cloud, irás a:
#  Settings → Secrets → Add secrets
# y pegarás tu JSON de credenciales así:
# {
#   "type": "service_account",
#   "project_id": "...",
#   "private_key_id": "...",
#   "private_key": "-----BEGIN PRIVATE KEY-----\\n....\\n-----END PRIVATE KEY-----\\n",
#   "client_email": "...",
#   "client_id": "...",
#   ...
# }

st.set_page_config(
    page_title="Dashboard de Contactos – NexaTech",
    layout="wide",
    page_icon="📊",
)

st.title("📈 Dashboard de Contactos – NexaTech")
st.caption("Análisis profesional e interactivo de la base de datos de networking")

# -------------------------------------------------
# 🔗 Conectar con Google Sheets
# -------------------------------------------------
try:
    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],  # Aquí Streamlit tomará el JSON de tus Secrets
        scopes=[
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ],
    )

    client = gspread.authorize(creds)
    SHEET_ID = "1qqtKqyNqNS7S5fpXenPZTPG5SpcwTmJ1zt9yP2a0coA"  # Tu hoja de NexaTech
    sheet = client.open_by_key(SHEET_ID).sheet1
    data = pd.DataFrame(sheet.get_all_records())

    st.success("✅ Datos cargados correctamente desde Google Sheets")

except Exception as e:
    st.error("❌ Error al conectar con Google Sheets. Verifica tus credenciales.")
    st.exception(e)
    st.stop()

# -------------------------------------------------
# 🧹 Limpieza básica
# -------------------------------------------------
data.columns = [col.strip().replace("\n", " ").replace("  ", " ") for col in data.columns]
for col in data.select_dtypes(include="object"):
    data[col] = data[col].astype(str).str.strip()

# -------------------------------------------------
# 🎨 Estilo profesional (modo oscuro)
# -------------------------------------------------
st.markdown("""
<style>
body {
    background-color: #0e1117;
    color: #fafafa;
}
[data-testid="stAppViewContainer"] {
    background-color: #0e1117;
}
[data-testid="stHeader"] {
    background-color: #0e1117;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# 📊 Dashboard con filtros dinámicos
# -------------------------------------------------
col1, col2, col3 = st.columns(3)

with col1:
    sector = st.selectbox("Filtrar por Sector o Industria:", ["Todos"] + sorted(data["Sector o industria "].unique()))
with col2:
    ciudad = st.selectbox("Filtrar por Ciudad:", ["Todos"] + sorted(data["Ciudad y país"].unique()))
with col3:
    interes = st.selectbox("Filtrar por Nivel de Interés:", ["Todos"] + sorted(data["Nivel de interés en recibir más información "].unique()))

filtered = data.copy()
if sector != "Todos":
    filtered = filtered[filtered["Sector o industria "] == sector]
if ciudad != "Todos":
    filtered = filtered[filtered["Ciudad y país"] == ciudad]
if interes != "Todos":
    filtered = filtered[filtered["Nivel de interés en recibir más información "] == interes]

# -------------------------------------------------
# 📈 Gráficos Neon Interactivos
# -------------------------------------------------
st.subheader("📊 Visualizaciones")

# 1️⃣ Contactos por Sector
fig1 = px.bar(
    filtered,
    x="Sector o industria ",
    title="Contactos por Sector o Industria",
    color="Sector o industria ",
    color_discrete_sequence=px.colors.qualitative.Dark24,
)
fig1.update_layout(template="plotly_dark", xaxis_title=None, yaxis_title="Cantidad de contactos")
st.plotly_chart(fig1, use_container_width=True)

# 2️⃣ Contactos por Ciudad
fig2 = px.pie(
    filtered,
    names="Ciudad y país",
    title="Distribución Geográfica de Contactos",
    color_discrete_sequence=px.colors.sequential.Aggrnyl_r,
)
fig2.update_layout(template="plotly_dark")
st.plotly_chart(fig2, use_container_width=True)

# 3️⃣ Nivel de interés
fig3 = px.histogram(
    filtered,
    x="Nivel de interés en recibir más información ",
    title="Nivel de Interés de los Contactos",
    color="Nivel de interés en recibir más información ",
    color_discrete_sequence=px.colors.sequential.Viridis_r,
)
fig3.update_layout(template="plotly_dark", xaxis_title=None, yaxis_title="Cantidad de contactos")
st.plotly_chart(fig3, use_container_width=True)

# -------------------------------------------------
# 📋 Mostrar tabla
# -------------------------------------------------
with st.expander("📄 Ver datos detallados"):
    st.dataframe(filtered)
