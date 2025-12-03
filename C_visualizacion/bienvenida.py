import streamlit as st
from tablas_resumen import TablasResumen

st.set_page_config(
    page_title="Dashboard Global",
    layout="wide",
    page_icon="📊"
)


st.markdown("""
<style>

html, body, [class*="css"]  {
    color: white !important;
}

body {
    background-color: #0e1117 !important;
}

/* ENCABEZADO */
.hero {
    text-align: center;
    padding: 40px 0px 10px 0px;
}

.hero-title {
    font-size: 55px;
    font-weight: 900;
    color: white;
    letter-spacing: -1px;
}

.hero-subtitle {
    font-size: 20px;
    color: #d0d0d0;
    margin-top: -10px;
}

/* TARJETAS */
.card {
    background: #f4f6f9;
    padding: 28px;
    border-radius: 18px;
    text-align: center;
    border: 1px solid #cfd4dd;
    box-shadow: 0px 4px 14px rgba(0,0,0,0.15);
    transition: 0.3s;
}

.card:hover {
    transform: translateY(-6px);
    box-shadow: 0px 12px 28px rgba(0,0,0,0.25);
}

.card-title {
    font-size: 18px;
    font-weight: 700;
    color: #000000; 
}

.card p {
    color: #333333 !important;
}

/* FOOTER */
.footer {
    margin-top: 50px;
    text-align: center;
    font-size: 14px;
    color: #cccccc;
}
</style>
""", unsafe_allow_html=True)



st.markdown("""
<div class="hero">
    <div class="hero-title">Análisis de la Salud Pública en México</div>
    <div class="hero-subtitle">Estados · Instituciones · Población · Tendencias · Indicadores</div>
</div>
""", unsafe_allow_html=True)



col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="card">
        <div style="font-size:40px;">🗂️</div>
        <div class="card-title">Datos preparados automáticamente</div>
        <p>Tablas: personal de salud, afiliación, derechohabiencia, población, estados.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card">
        <div style="font-size:40px;">📊</div>
        <div class="card-title">Dashboards interactivos</div>
        <p>Gráficos, KPIs y filtros.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="card">
        <div style="font-size:40px;">📁</div>
        <div class="card-title">Navega desde el menú</div>
        <p>Explora cada módulo desde la barra lateral.</p>
    </div>
    """, unsafe_allow_html=True)



st.markdown("""
<div style='text-align:center; font-size:17px; margin-top:35px;'>
Este proyecto te permitirá visualizar y analizar información clave de salud pública 
en México mediante herramientas interactivas.
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style='text-align:center; font-size:16px; margin-top:25px; color:white;'>
<strong>Integrantes:</strong><br>
Garcia Velazquez Jonathan Magdiel · Gaytan Castellanos Miguel Angel · Ramirez Morales Arturo · Ramos Ramirez Cynthia · Rios Gomez Jesus Dagoberto
</div>
""", unsafe_allow_html=True)



#Inicia todas las tablas de resumen si no estan iniciadas en la sesion de streamlit


if "tablas" not in st.session_state:
    st.session_state.tablas = TablasResumen()
    st.session_state.tablas.Personal_salud_año()
    st.session_state.tablas.Personal_salud_institucion()
    st.session_state.tablas.Poblacion_derechohabiente()
    st.session_state.tablas.Poblacion_afiliada()

st.markdown('<div class="footer">Proyecto Final · Streamlit · Datos Públicos</div>', unsafe_allow_html=True)