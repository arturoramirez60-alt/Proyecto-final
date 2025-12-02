from tablas_resumen import TablasResumen
import plotly.express as px
import streamlit as st


def dashboard(tablas):

    st.title("🏥 Análisis de Personal y Afiliación por Institución")
        
    pd_bar = tablas.pd_bar
    
    st.header("👥 Población Afiliada a Instituciones de Salud (2020)")

    bar = px.bar(pd_bar, 
                 x = "Institucion",
                 y = "Poblacion_afiliada", 
                 color = "Institucion",
                 color_discrete_sequence=px.colors.sequential.Aggrnyl,
                 title="Distribución de la Población Afiliada")
    
    bar.update_layout(xaxis={'showticklabels': False})
    
    st.plotly_chart(bar, width='stretch')
    
    st.subheader("🔝 Instituciones con Mayor Afiliación (2020)")
    
    tablas.Personal_salud_institucion() 
    psi_treemap = tablas.psi_treemap
    años = psi_treemap.Año.unique()
    
    col1, col2, col3 = st.columns(3)

    def get_metric_data(df, institution_name):
        data = df[df.Institucion == institution_name]
        afiliados = data["Poblacion_afiliada"].values[0]
        porcentaje = data["Porcentaje_afiliado"].values[0]
        return afiliados, porcentaje

    afiliados_imss, porcentaje_imss = get_metric_data(pd_bar, 'IMSS')
    with col1:
        st.metric(
            "⚕️ IMSS",
            f"{afiliados_imss:,.0f}", 
            f"{porcentaje_imss * 100:.1f}% del total" 
        )
            
    afiliados_insabi, porcentaje_insabi = get_metric_data(pd_bar, 'INSABI_O_SEGURO_POPULAR')
    with col2:
        st.metric(
            "🏥 INSABI / Seguro Popular",
            f"{afiliados_insabi:,.0f}",
            f"{porcentaje_insabi * 100:.1f}% del total"
        )
        
    afiliados_issste, porcentaje_issste = get_metric_data(pd_bar, 'ISSSTE')
    with col3:
        st.metric(
            "🩺 ISSSTE",
            f"{afiliados_issste:,.0f}",
            f"{porcentaje_issste * 100:.1f}% del total"
        )
        
    st.header("🧑‍⚕️ Distribución del Personal por Institución y Año")
    with st.container(border=True):
        
        año = st.select_slider("📅 Seleccione un año para ver el personal", años)
        
        treemap = px.treemap(psi_treemap[psi_treemap.Año == año],
                             path = ["Institucion"],
                             values = "Personal_total",
                             color_discrete_sequence=px.colors.sequential.Aggrnyl,
                             title=f"Personal Total por Institución en {año}")
        
        treemap.update_layout(margin=dict(t=50, l=25, r=25, b=25))

        st.plotly_chart(treemap, width='stretch')
        
        with st.expander("ℹ️ Descripción del Gráfico"):
            st.write("Este gráfico muestra cómo se distribuye el personal de salud (en términos de cantidad total) en las diferentes instituciones de salud para el año seleccionado.")
            
            
    st.header("⚖️ Relación entre Población Afiliada y Personal Sanitario")
    
    psi_pd_scatter = tablas.psi_pd_scatter
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        scatter = px.scatter(psi_pd_scatter, 
                             x = "Personal_total", 
                             y = "Poblacion_afiliada", 
                             color = "Institucion",
                             log_y = True, 
                             title="Personal Total (eje X) vs. Población Afiliada (eje Y)")
        
        st.plotly_chart(scatter, width='stretch')
        
    with col2:
        st.markdown("<br>" * 6, unsafe_allow_html=True) 
        with st.expander("🔍 Ver Datos Crudos"):
            st.dataframe(psi_pd_scatter, width='stretch')



if "tablas" not in st.session_state:
    st.session_state.tablas = TablasResumen()
    st.session_state.tablas.Personal_salud_año()
    st.session_state.tablas.Personal_salud_institucion()
    st.session_state.tablas.Poblacion_derechohabiente()
    st.session_state.tablas.Poblacion_afiliada()

dashboard(st.session_state.tablas)