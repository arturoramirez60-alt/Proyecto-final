from tablas_resumen import TablasResumen
import plotly.express as px
import streamlit as st


def dashboard(tablas):
    
    st.title("Analisis de personal por Estado")

    psa = tablas.personal_salud_año
    
    lista_estados = psa.Estado.unique()
    lista_puestos = psa.columns.tolist()[2:13]
    
    col1, col2 = st.columns(2)   
    
    
    st.sidebar.subheader("Seleccione un Estado")
    estado = st.sidebar.selectbox("Estado",lista_estados)
    puesto = st.selectbox("Selecciona un puesto", lista_puestos)
    
   
    plot =  px.line(psa[psa.Estado == estado ], x = "Año", y = puesto, title = f"Evolucion de {puesto} en {estado}", color_discrete_sequence= ["#11B9AE"])
    st.plotly_chart(plot)
    
    
    tablas.Poblacion_afiliada()
    pa_pie = tablas.pa_pie #poblacion afiliada ajustada para grafica de pastel
    
    col1, col2 = st.columns(2) 
    pie = px.pie(
        pa_pie[pa_pie.Estado == estado],
        values='cantidad',  
        names="porcentajes",    
        title=f'Distribución de Afiliación en {estado}',
        color_discrete_sequence=px.colors.sequential.Aggrnyl
    )

    st.plotly_chart(pie)
    
 
    
    
  

if __name__ == "__main__":
    if "tablas" not in st.session_state:
        st.session_state.tablas = TablasResumen()

    dashboard(st.session_state.tablas)