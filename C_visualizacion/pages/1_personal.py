from tablas_resumen import TablasResumen
import plotly.express as px
import pandas as pd
import streamlit as st




def analisis_puestos(tablas):
    st.title("Graficas Ejemplo")
    st.header("hola",divider = True)
    psa = tablas.personal_salud_año
    lista_estados = psa.Estado.unique()
    lista_puestos = psa.columns.tolist()[2:13]
    
    col1, col2 = st.columns(2)   
    
    estado = col1.selectbox("Selecciona un Estado", lista_estados)
    puesto = col2.selectbox("Selecciona un puesto", lista_puestos)
    
   
    plot =  px.line(psa[psa.Estado == estado ], x = "Año", y = puesto, title = f"Evolucion de {puesto} en {estado}")
    st.plotly_chart(plot)
    
    

if __name__ == "__main__":
    if "tablas" not in st.session_state:
        st.session_state.tablas = TablasResumen()
    analisis_puestos(st.session_state.tablas)