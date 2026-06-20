import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os
from pymongo import MongoClient

# =========================
# CONFIGURACIÓN DE LA PÁGINA
# =========================

st.set_page_config(
    page_title="Mi App Streamlit con Mongo",
    page_icon="🚀",
    layout="wide"
)

# =========================
# CONEXIÓN A MONGODB ATLAS
# =========================

MONGO_URI = os.getenv("MONGODB_URI")

db = None
coleccion = None

try:
    if MONGO_URI:
        client = MongoClient(MONGO_URI)
        db = client["ejercicio_cloud"]
        coleccion = db["usuarios"]
except Exception as e:
    st.error(f"Error conectando a MongoDB: {e}")

# =========================
# INTERFAZ PRINCIPAL
# =========================

st.title("🚀 Mi Primera App Streamlit con Mongo")
st.markdown("---")

# Sidebar
st.sidebar.header("Configuración")
nombre = st.sidebar.text_input("Tu nombre:", "Usuario")
edad = st.sidebar.slider("Tu edad:", 1, 100, 25)

# Columnas
col1, col2 = st.columns(2)

with col1:
    st.header(f"¡Hola {nombre}!")
    st.write(f"Tienes {edad} años")

    if st.button("Generar datos aleatorios"):
        st.success("¡Datos generados exitosamente!")

with col2:
    st.header("📊 Gráfico de ejemplo")

    data = pd.DataFrame({
        "x": range(10),
        "y": np.random.randn(10).cumsum(),
        "categoria": np.random.choice(["A", "B", "C"], 10)
    })

    fig = px.line(
        data,
        x="x",
        y="y",
        color="categoria",
        title="Datos Aleatorios"
    )

    st.plotly_chart(fig, use_container_width=True)

# =========================
# MÉTRICAS
# =========================

st.markdown("---")
st.header("📈 Métricas")

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.metric("Usuarios", "1,234", "12%")

with m2:
    st.metric("Ventas", "$5,678", "-2%")

with m3:
    st.metric("Conversión", "3.4%", "0.5%")

with m4:
    st.metric("Satisfacción", "4.8/5", "0.2")

# =========================
# TABLA DE DATOS
# =========================

st.markdown("---")
st.header("📋 Tabla de Datos")

st.dataframe(data, use_container_width=True)

# =========================
# MONGODB ATLAS
# =========================

st.markdown("---")
st.header("🍃 MongoDB Atlas")

if coleccion is not None:

    st.write("Guarda información directamente en MongoDB Atlas.")

    nombre_db = st.text_input(
        "Nombre a almacenar",
        value=nombre
    )

    if st.button("Guardar en MongoDB"):

        documento = {
            "nombre": nombre_db,
            "edad": edad
        }

        coleccion.insert_one(documento)

        st.success("Registro guardado correctamente en MongoDB Atlas.")

    st.subheader("Registros almacenados")

    registros = list(
        coleccion.find(
            {},
            {"_id": 0}
        )
    )

    if registros:
        df_registros = pd.DataFrame(registros)
        st.dataframe(df_registros, use_container_width=True)
    else:
        st.info("No existen registros almacenados.")

else:
    st.warning(
        "No se encontró la variable de entorno MONGODB_URI."
    )

# =========================
# FOOTER
# =========================

st.markdown("---")
st.markdown(
    "**Aplicación desplegada con Docker, Azure Web App y MongoDB Atlas** 🚀"
)
