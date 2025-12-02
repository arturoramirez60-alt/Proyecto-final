from tablas_resumen import TablasResumen
import streamlit as st

st.set_page_config(
    page_title="Dashboard Global",
    layout="wide",
)

st.title("🌎 Bienvenido al Proyecto Final")
st.markdown("""
Este proyecto te permitirá crear **dashboards interactivos** usando:

- 📊 Plotly Express  
- 🧩 Contenedores y columnas  
- 🎛️ Filtros dinámicos  
- 🧮 KPIs  
- 📁 Paginación con emojis  

Usa el menú de la izquierda para navegar entre páginas.
""")

if "tablas" not in st.session_state:
    st.session_state.tablas = TablasResumen()
    st.session_state.tablas.Personal_salud_año()
    st.session_state.tablas.Personal_salud_institucion()
    st.session_state.tablas.Poblacion_derechohabiente()
    st.session_state.tablas.Poblacion_afiliada()
    


