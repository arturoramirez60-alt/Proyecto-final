from tablas_resumen import TablasResumen
import plotly.express as px
import streamlit as st


def dashboard(tablas):
    psa_bar = tablas.psa_bar
    
    
    st.title("Analisis de la poblacion")
    lista_años_pob = psa_bar.Año.unique()
    
    col1, col2 = st.columns(2) 
    col2.space(size="large")
    col2.space(size="small")
    año_pob = col2.selectbox("años",lista_años_pob)
    
    personal_medico = list(psa_bar["Total"][(psa_bar.Estado == "Nacional") & (psa_bar.Año == año_pob) & (psa_bar.Poblacion == "Personal_medico")])[0]
    poblacion = list(psa_bar["Total"][(psa_bar.Estado == "Nacional") & (psa_bar.Año == año_pob) & (psa_bar.Poblacion == "Poblacion_total")])[0]
    col2.metric("Hay 1 Personal de la salud por cada", f"{round(poblacion/personal_medico,0)} personas")
    
    bar =  px.bar(psa_bar[(psa_bar.Estado == "Nacional") & (psa_bar.Año == año_pob)], 
                        x = "Poblacion",
                        y = "Total",
                        title='Comparación de personal mmedico vs poblacion total',
                        labels={'Poblacion': 'Categoría', 'Total': 'Número de Personas'},
                        color='Poblacion', 
                        text='Total',
                        color_discrete_sequence=px.colors.sequential.Aggrnyl)
    
    bar.update_layout(showlegend=False)
    col1.plotly_chart(bar)
    
   

    
    psa_scatter =  tablas.psa_scatter
    
    col1, col2 = st.columns([1, 2])
    lista_puestos = psa_scatter.columns.tolist()[2:13]

    with col1:
        st.space("large")
        st.space("small")
        eje_x = st.selectbox("eje x", lista_puestos)
        eje_y = st.selectbox("eje y", lista_puestos)
    
    if eje_x == eje_y:
        st.header("seleccione 2 columnas diferentes")
    else:
        scatter = px.scatter(psa_scatter, x = eje_x, y = eje_y, log_x= True, log_y= True, color = "Estado", animation_frame= "Año")

        with col2:
            st.plotly_chart(scatter, use_container_width=True)

    
        with st.expander("📊 Haz click para ver los Datos del Gráfico"):
            st.dataframe(psa_scatter[["Año","Estado", eje_x, eje_y]])

    psa_histogram =  tablas.psa_histogram
    col1,col2 = st.columns(2)
    
    
    with col2:
        personal_hist = st.selectbox("seleccione un puesto", psa_histogram.Tipo_personal.unique())
        años_hist = list(psa_histogram.Año.unique())
        años_hist.append("Todos los años")
        año_hist =st.selectbox("seleccione un año", años_hist)
    
    if año_hist == "Todos los años":
        
        
        histogram = px.histogram(psa_histogram[psa_histogram.Tipo_personal == personal_hist],x = "Estado", y = "Total")
        col1.plotly_chart(histogram)
        
        st.dataframe(psa_histogram[psa_histogram.Tipo_personal == personal_hist])
    else:
        
        histogram = px.histogram(psa_histogram[(psa_histogram.Año == año_hist)&(psa_histogram.Tipo_personal == personal_hist)],x = "Estado", y = "Total")
        col1.plotly_chart(histogram)
        
        st.dataframe(psa_histogram[(psa_histogram.Año == año_hist)&(psa_histogram.Tipo_personal == personal_hist)])
        
    
    
    
    
if "tablas" not in st.session_state:
    st.session_state.tablas = TablasResumen()
    st.session_state.tablas.Personal_salud_año()
    st.session_state.tablas.Personal_salud_institucion()
    st.session_state.tablas.Poblacion_derechohabiente()
    st.session_state.tablas.Poblacion_afiliada()

dashboard(st.session_state.tablas)