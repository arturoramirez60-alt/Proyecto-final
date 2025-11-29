from tablas_resumen import TablasResumen
import plotly.express as px
import streamlit as st


def dashboard(tablas):
    tablas.Personal_salud_año()
    psa_bar = tablas.psa_bar
    
    
    st.title("Analisis de la poblacion")
    lista_años = psa_bar.Año.unique()
    año = st.select_slider("años",lista_años)
    col1, col2 = st.columns(2) 
   
    
    bar =  px.bar(psa_bar[(psa_bar.Estado == "Nacional") & (psa_bar.Año == año)], 
                        x = "Poblacion",
                        y = "Total",
                        title='Comparación de personal mmedico vs poblacion total',
                        labels={'Poblacion': 'Categoría', 'Total': 'Número de Personas'},
                        color='Poblacion', 
                        text='Total',
                        color_discrete_sequence=px.colors.sequential.Aggrnyl)
    
    bar.update_layout(showlegend=False)
    col1.plotly_chart(bar)
    
    
    
  

if __name__ == "__main__":
    if "tablas" not in st.session_state:
        st.session_state.tablas = TablasResumen()

    dashboard(st.session_state.tablas)