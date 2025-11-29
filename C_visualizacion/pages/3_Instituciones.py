from tablas_resumen import TablasResumen
import plotly.express as px
import streamlit as st


def dashboard(tablas):
    st.title("Analisis por Institucion")
    
    tablas.Poblacion_derechohabiente()
    
    pd_bar = tablas.pd_bar
    
    
    bar = px.bar(pd_bar, x = "institucion",y = "Poblacion_afiliada", color = "institucion",color_discrete_sequence=px.colors.sequential.Aggrnyl
           )
    st.plotly_chart(bar)
if __name__ == "__main__":
    if "tablas" not in st.session_state:
        st.session_state.tablas = TablasResumen()

    dashboard(st.session_state.tablas)