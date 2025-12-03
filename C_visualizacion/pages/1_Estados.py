from tablas_resumen import TablasResumen
import plotly.express as px
import streamlit as st


def dashboard(tablas):


    st.title("🏥 Análisis de Personal de Salud por Estado")

    psa = tablas.personal_salud_año

    lista_estados = psa.Estado.unique()

    lista_puestos = psa.columns.tolist()[2:13]

    st.sidebar.markdown("---")
    st.sidebar.subheader("📍 Seleccione un Estado")
    estado = st.sidebar.selectbox("Estado", lista_estados)
    st.sidebar.markdown("---")
    
    st.subheader("📊 Evolución de Personal")
    puesto = st.selectbox("👷 Selecciona un puesto para ver su evolución", lista_puestos)

    plot = px.line(psa[psa.Estado == estado], 
                   x="Año", 
                   y=puesto, 
                   title=f"📈 Evolución de {puesto} en {estado}", 
                   color_discrete_sequence=["#11B9AE"]) 
    
    st.plotly_chart(plot)

    st.header("👥 Distribución y Comparativa de Afiliación")

    pa_pie = tablas.pa_pie

    col1, col2 = st.columns([2, 1])
    
    with col1:
        pie = px.pie(
            pa_pie[pa_pie.Estado == estado],
            values='cantidad',
            names="porcentajes",
            title=f' Distribución de Afiliación en {estado} (2020)',
            color_discrete_sequence=px.colors.sequential.Aggrnyl
        )

        pie.update_layout(
            legend=dict(
                x=0.5,
                y=-0.1,
                orientation="h",
                xanchor="center",
                yanchor="top")
        )
        st.plotly_chart(pie, width='stretch')

    with col2:
        promedio = list(pa_pie.cantidad[pa_pie.Estado == "Nacional"])[0]
        valor_estado = list(pa_pie.cantidad[pa_pie.Estado == estado])[0]
        diferencia = round(((valor_estado / promedio) - 1) * 100, 2)
        
        if diferencia > 0:
            color_delta = "normal"
            delta_texto = f"{diferencia}%"
            titulo_metrica = "Por arriba"
        elif diferencia < 0:
            color_delta = "inverse"
            delta_texto = f"{diferencia}%"
            titulo_metrica = "Por debajo"
        else:
            color_delta = "off"
            delta_texto = "0%"
            titulo_metrica = "Igual"

        st.space("large")
        st.space("small")
        
        st.metric(
            label="Afiliación respecto al promedio Nacional",
            value=titulo_metrica, 
            delta=delta_texto,
            delta_color=color_delta
        )
    

    st.header("🌳 Distribución de Personal por Categoría (Treemap)")
    
    with st.container(border=True):
        
        psa_treemap = tablas.psa_treemap
        años = psa_treemap.Año.unique()
        
        año = st.select_slider("📅 Seleccione un año", años)
        
        treemap = px.treemap(psa_treemap[(psa_treemap.Estado == estado) & (psa_treemap.Año == año)],
                             path=["Tipo_personal"],
                             values="Total",
                             color_discrete_sequence=px.colors.sequential.Aggrnyl,
                             title=f"Personal de Salud por Tipo en {estado} ({año})")

        treemap.update_layout(margin=dict(t=50, l=25, r=25, b=25))
        st.plotly_chart(treemap, width='stretch')


if "tablas" not in st.session_state:
    st.session_state.tablas = TablasResumen()
    st.session_state.tablas.Personal_salud_año()
    st.session_state.tablas.Personal_salud_institucion()
    st.session_state.tablas.Poblacion_derechohabiente()
    st.session_state.tablas.Poblacion_afiliada()

dashboard(st.session_state.tablas)