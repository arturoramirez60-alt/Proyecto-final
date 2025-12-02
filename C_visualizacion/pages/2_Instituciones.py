from tablas_resumen import TablasResumen
import plotly.express as px
import streamlit as st


def dashboard(tablas):
    st.title("Analisis por Institucion")
        
    pd_bar = tablas.pd_bar
    st.header("poblacion afiliada a un institucion en 2020")
    
    bar = px.bar(pd_bar, x = "institucion",y = "Poblacion_afiliada", color = "institucion",color_discrete_sequence=px.colors.sequential.Aggrnyl)
    st.plotly_chart(bar)
    
    tablas.Personal_salud_institucion()
    psi_treemap =  tablas.psi_treemap
    años = psi_treemap.Año.unique()
    st.header("Intituciones con mas personas afiliadas 2020")
    col1,col2,col3 = st.columns(3)
    
    col1.metric("IMSS",f"{pd_bar["Poblacion_afiliada"][pd_bar.institucion == 'IMSS'].values[0]:,}",
                f"{pd_bar["Porcentaje_afiliado"][pd_bar.institucion == 'IMSS'].values[0]*100}%",
                border=True)
                
  
    
    col2.metric("INSABI",f"{pd_bar["Poblacion_afiliada"][pd_bar.institucion == 'INSABI_O_SEGURO_POPULAR'].values[0]:,}",
                f"{pd_bar["Porcentaje_afiliado"][pd_bar.institucion == 'INSABI_O_SEGURO_POPULAR'].values[0]*100}%",
                border=True)
    
    col3.metric("ISSTE",f"{pd_bar["Poblacion_afiliada"][pd_bar.institucion == 'ISSSTE'].values[0]:,}",
                f"{pd_bar["Porcentaje_afiliado"][pd_bar.institucion == 'ISSSTE'].values[0]*100}%",
                border=True)
        
    
    st.header("Personal por institucion") 
    año =  st.select_slider("Seleccione un año", años)
    treemap = px.treemap(psi_treemap[psi_treemap.Año == año],
                         path = ["Institucion"],
                         values= "Personal_total",
                         color_discrete_sequence=px.colors.sequential.Aggrnyl)
    st.plotly_chart(treemap)
    
    st.header("Relacion de la poblacion afiliada con el personal en la institucion")
    
if "tablas" not in st.session_state:
    st.session_state.tablas = TablasResumen()
    st.session_state.tablas.Personal_salud_año()
    st.session_state.tablas.Personal_salud_institucion()
    st.session_state.tablas.Poblacion_derechohabiente()
    st.session_state.tablas.Poblacion_afiliada()

dashboard(st.session_state.tablas)