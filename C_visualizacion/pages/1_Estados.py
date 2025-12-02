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
    
    

    pa_pie = tablas.pa_pie
    
    col1, col2 = st.columns(2) 
    pie = px.pie(
        pa_pie[pa_pie.Estado == estado],
        values='cantidad',  
        names="porcentajes",    
        title=f'Distribución de Afiliación en {estado} para 2020',
        color_discrete_sequence=px.colors.sequential.Aggrnyl
    )

    st.plotly_chart(pie)
    

    
    st.header("Total de personal por estado y año")
    
    psa_treemap = tablas.psa_treemap
    años = psa_treemap.Año.unique()
    año = st.select_slider("seleccione un año", años)
    treemap =  px.treemap(psa_treemap[(psa_treemap.Estado ==  estado) & (psa_treemap.Año == año)],
                          path = ["Tipo_personal"],
                          values= "Total",
                          color_discrete_sequence=px.colors.sequential.Aggrnyl)

    st.plotly_chart(treemap)
 


if "tablas" not in st.session_state:
    st.session_state.tablas = TablasResumen()
    st.session_state.tablas.Personal_salud_año()
    st.session_state.tablas.Personal_salud_institucion()
    st.session_state.tablas.Poblacion_derechohabiente()
    st.session_state.tablas.Poblacion_afiliada()
dashboard(st.session_state.tablas)