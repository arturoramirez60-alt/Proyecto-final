from tablas_resumen import TablasResumen
import plotly.express as px
import streamlit as st


def dashboard(tablas):
    psa_bar = tablas.psa_bar
    
    
    st.title("🌎 Análisis de la Población y el Personal Sanitario")
    
    st.header("⚖️ Relación Personal Médico / Población Total Nacional")
    
    lista_años_pob = psa_bar.Año.unique()
    
    col1, col2 = st.columns([2, 1]) 
    
    with col2:

        st.markdown("<br>" * 2, unsafe_allow_html=True) 
        año_pob = st.selectbox("📅 Seleccione un año", lista_años_pob)
        
        personal_medico = list(psa_bar["Total"][(psa_bar.Estado == "Nacional") & (psa_bar.Año == año_pob) & (psa_bar.Poblacion == "Personal_medico")])[0]
        poblacion = list(psa_bar["Total"][(psa_bar.Estado == "Nacional") & (psa_bar.Año == año_pob) & (psa_bar.Poblacion == "Poblacion_total")])[0]
        
        ratio = round(poblacion / personal_medico, 0)
        
        st.subheader("Ratio Nacional:")
        st.caption("Hay **1** Personal de la salud por cada...")
        st.metric(
            label="Personas",
            value=f"{ratio:,.0f}" 
        )
        
    
    with col1:
        
        bar = px.bar(psa_bar[(psa_bar.Estado == "Nacional") & (psa_bar.Año == año_pob)], 
                     x = "Poblacion",
                     y = "Total",
                     title=f'Comparación de Personal Médico vs. Población Total ({año_pob})',
                     labels={'Poblacion': 'Categoría', 'Total': 'Número de Personas'},
                     color='Poblacion', 
                     text='Total',
                     color_discrete_sequence=px.colors.sequential.Aggrnyl)
        
        bar.update_layout(showlegend=False)
        st.plotly_chart(bar, width='stretch')
        
  
    st.header("📈 Correlación Histórica entre Puestos de Personal (por Estado)")
    
    psa_scatter = tablas.psa_scatter
    
    col1, col2 = st.columns([1, 2])
    lista_puestos = psa_scatter.columns.tolist()[2:13]

    with col1:
        st.subheader("Selección de Ejes")
        eje_x = st.selectbox("Eje X", lista_puestos)
        eje_y = st.selectbox("Eje Y", lista_puestos)
    
    with col2:
        if eje_x == eje_y:
            st.markdown("<br>" * 4, unsafe_allow_html=True) 
            st.error("⚠️ **Seleccione dos puestos diferentes** para visualizar la correlación.")
        else:
      
            scatter = px.scatter(psa_scatter, 
                                 x = eje_x, 
                                 y = eje_y, 
                                 log_x= True, 
                                 log_y= True, 
                                 color = "Estado", 
                                 animation_frame= "Año",
                                 title=f"Correlación entre {eje_x} y {eje_y}")

            st.plotly_chart(scatter, width='stretch')


    if eje_x != eje_y:
        with st.expander("📊 Haz click para ver los Datos Crudos del Gráfico"):
 
            st.dataframe(psa_scatter[["Año","Estado", eje_x, eje_y]], use_container_width=True)


    st.header("📦 Distribución del Personal de la Salud en los Estados")
    
    psa_histogram = tablas.psa_histogram
    
    opc_distribucion = st.selectbox("Ver distribución por:", ["Personal","Estado"]) 
    col1, col2 = st.columns([2, 1])


    with col2:
        st.markdown("<br>" * 2, unsafe_allow_html=True) 
        personal_hist = st.selectbox("Seleccione un puesto", psa_histogram.Tipo_personal.unique())
        años_hist = list(psa_histogram.Año.unique())
        años_hist.append("Todos los años")
        año_hist =st.selectbox("Seleccione un año", años_hist)
    
    with col1:
        if opc_distribucion == "Personal":

            if año_hist == "Todos los años":
                df_filtrado = psa_histogram[psa_histogram.Tipo_personal == personal_hist]
                title = f"Frecuencia de {personal_hist} (Todos los Años)"
            else:
                df_filtrado = psa_histogram[(psa_histogram.Año == año_hist) & (psa_histogram.Tipo_personal == personal_hist)]
                title = f"Frecuencia de {personal_hist} en el Año {año_hist}"

            histogram = px.histogram(df_filtrado, x = "Total", title=title)
            st.plotly_chart(histogram, width='stretch')
            
        elif opc_distribucion == "Estado":

            if año_hist == "Todos los años":
                df_filtrado = psa_histogram[psa_histogram.Tipo_personal == personal_hist].groupby('Estado')['Total'].sum().reset_index()
                title = f"Distribución Total de {personal_hist} por Estado (Todos los Años)"
            else:
                df_filtrado = psa_histogram[(psa_histogram.Año == año_hist) & (psa_histogram.Tipo_personal == personal_hist)]
                title = f"Distribución de {personal_hist} por Estado en {año_hist}"
            
            histogram = px.bar(df_filtrado, x = "Estado", y = "Total", title=title)
            st.plotly_chart(histogram, width='stretch')



if "tablas" not in st.session_state:
    st.session_state.tablas = TablasResumen()
    st.session_state.tablas.Personal_salud_año()
    st.session_state.tablas.Personal_salud_institucion()
    st.session_state.tablas.Poblacion_derechohabiente()
    st.session_state.tablas.Poblacion_afiliada()

dashboard(st.session_state.tablas)