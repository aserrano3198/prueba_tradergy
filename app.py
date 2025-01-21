import streamlit as st
import pandas as pd
import plotly.express as px

# Cargar datos
@st.cache_data
def load_data(file_path):
    df = pd.read_csv(file_path)
    df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce", utc=True)
    df["datetime"] = df["datetime"].dt.tz_convert("Europe/Madrid")
    return df

# Calcular precios promedio por hora y mes
def calculate_hourly_averages(df):
    df["hour"] = df["datetime"].dt.hour
    df["month"] = df["datetime"].dt.month
    avg_df = df.groupby(["month", "hour"])["value"].mean().reset_index()
    avg_df["month_name"] = avg_df["month"].apply(lambda x: pd.Timestamp(f"2024-{x:02d}-01").strftime("%B"))
    return avg_df

# Cargar datos
st.title("Visualización de Precios Spot del Mercado Eléctrico")
file_path = "precios_spot.csv"  # Archivo generado previamente
data = load_data(file_path)

# Selección de rango de fechas y sesiones
st.sidebar.header("Filtros")
start_date = st.sidebar.date_input("Fecha de inicio", data["datetime"].min().date())
end_date = st.sidebar.date_input("Fecha de fin", data["datetime"].max().date())
sessions = st.sidebar.multiselect(
    "Seleccionar sesiones",
    options=data["session"].unique(),
    default=data["session"].unique(),
)

# Filtrar datos según selección
filtered_data = data[
    (data["datetime"].dt.date >= start_date) &
    (data["datetime"].dt.date <= end_date) &
    (data["session"].isin(sessions))
]

# Gráfica interactiva de precios
st.subheader("Visualización de datos por rango de fechas")
fig = px.line(
    filtered_data,
    x="datetime",
    y="value",
    color="session",
    title="Precios Spot por Fecha y Sesión",
    labels={"value": "Precio (€)", "datetime": "Fecha"},
    hover_data=["session"]
)
fig.update_layout(xaxis_title="Fecha", yaxis_title="Precio (€)")
st.plotly_chart(fig)

# Gráfica de promedios horarios por mes
st.subheader("Promedios horarios por mes (2024)")
hourly_averages = calculate_hourly_averages(data)
fig_avg = px.line(
    hourly_averages,
    x="hour",
    y="value",
    color="month_name",
    title="Precios Spot Promedio por Hora y Mes",
    labels={"value": "Precio promedio (€)", "hour": "Hora del día", "month_name": "Mes"},
    hover_data=["month_name"]
)
fig_avg.update_layout(xaxis_title="Hora del día", yaxis_title="Precio promedio (€)")
st.plotly_chart(fig_avg)
