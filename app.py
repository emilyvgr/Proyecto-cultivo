import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(page_title="Proyecto Cultivos", page_icon="logo solo.svg", layout="wide")

st.markdown("""
    <style>
    [data-testid="stDataFrame"], .stPlotlyChart {
        background-color: #FFFFFF !important;
        border-radius: 20px !important;
        padding: 15px !important;
        border: 2px solid #E0E0E0 !important;
        box-shadow: 2px 2px 15px rgba(0,0,0,0.05) !important;
        margin-bottom: 20px !important;
    }
    .contenedor-horizontal {
        display: flex !important;
        flex-direction: row;
        justify-content: space-around;
        background-color: #F0F2F6;
        padding: 20px;
        border-radius: 20px;
        gap: 15px;
        margin-bottom: 30px;
    }
    .tarjeta-temporada {
        background-color: white !important;
        padding: 15px;
        border-radius: 15px;
        border: 1px solid #E0E0E0;
        flex: 1; 
        min-width: 180px; 
    }
    .tarjeta-temporada h4 { margin-top: 0; text-align: center; color: #31333F; }
    .label-dato { color: #666; font-size: 0.75em; display: block; }
    .valor-dato { font-size: 1em; display: block; font-family: monospace; font-weight: bold; }
    .dato-lluvia .valor-dato { color: #007BFF; }
    .dato-rendimiento .valor-dato { color: #28A745; }
    .dato-fertilizante .valor-dato { color: #FD7E14; }
    .dato-pesticida .valor-dato { color: #DC3545; }
    </style>
    """, unsafe_allow_html=True)


col_logo, col_titulo = st.columns([1, 4])
with col_logo:
    st.image("logo solo.svg", width=80)
with col_titulo:
    st.markdown("<h1 style='text-align: left; color: #000000; font-size: 28px; font-family: Arial Black;'>Análisis de los Factores Determinantes en Ciclos Agrícola</h1>", unsafe_allow_html=True)

st.divider()

@st.cache_data 
def cargar_datos():
    df = pd.read_csv("agricultura.csv")

    columnas_es = {
    'Crop': 'cultivo',
    'Crop_Year': 'año',
    'Season': 'temporada',
    'State': 'estado',
    'Area': 'area',
    'Production': 'produccion',
    'Annual_Rainfall': 'precipitacion_anual',
    'Fertilizer': 'fertilizante',
    'Pesticide': 'pesticida',
    'Yield': 'rendimiento'
}
    df.rename(columns=columnas_es, inplace=True)

    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    df = df.drop_duplicates()

    for col in df.select_dtypes(include=["object", "string"]).columns:
        df[col] = df[col].str.strip()

    df = df.infer_objects()

    q1_produccion = df["produccion"].quantile(0.25)
    q3_produccion = df["produccion"].quantile(0.75)
    iqr_produccion = q3_produccion - q1_produccion
    lower_bound_produccion = q1_produccion - 1.5 * iqr_produccion
    upper_bound_produccion = q3_produccion + 1.5 * iqr_produccion
    df = df.query("produccion >= @lower_bound_produccion and produccion <= @upper_bound_produccion")

    q1_fertilizante = df["fertilizante"].quantile(0.25)
    q3_fertilizante = df["fertilizante"].quantile(0.75)
    iqr_fertilizante = q3_fertilizante - q1_fertilizante
    lower_bound_fertilizante = q1_fertilizante - 1.5 * iqr_fertilizante
    upper_bound_fertilizante = q3_fertilizante + 1.5 * iqr_fertilizante
    df = df.query("fertilizante >= @lower_bound_fertilizante and fertilizante <= @upper_bound_fertilizante")

    q1_area = df["area"].quantile(0.25)
    q3_area = df["area"].quantile(0.75)
    iqr_area = q3_area - q1_area
    lower_bound_area = q1_area - 1.5 * iqr_area
    upper_bound_area = q3_area + 1.5 * iqr_area
    df = df.query("area >= @lower_bound_area and area <= @upper_bound_area")
 
    df = df.query("año >= 2010 and año <= 2020")

    df = df[df['temporada'] != 'Whole Year']
    df['temporada'] = df['temporada'].replace('Summer', 'Zaid')
    df['temporada'] = df['temporada'].replace('Winter', 'Rabi')
    df['temporada'] = df['temporada'].replace('Autumn', 'Kharif')

    estadisticas = df.describe()
    estadisticas = estadisticas.rename(index={
    'count': 'Total (N)',
    'mean': 'Promedio',
    'std': 'Des. Tipica',
    'min': 'Mínimo',
    '25%': '25%',
    '50%': 'Mediana',
    '75%': '75%',
    'max': 'Máximo'
})
    return df

df_estudio = cargar_datos()

# 4. MENÚ DE NAVEGACIÓN
with st.sidebar:
    st.title("Navegación")
    opcion = st.selectbox(
        "Seleccione una sección:",
        ["Resumen Estadístico", "Preguntas de Investigación", "Objetivos del Proyecto"]
    )


if opcion == "Resumen Estadístico":
    st.subheader("Tabla de Cálculos Estadísticos")
    estadisticas = df_estudio.describe().rename(index={'count': 'Total (N)', 'mean': 'Promedio', 'std': 'Des. Tipica', '50%': 'Mediana'})
    st.dataframe(estadisticas.style.format("{:.2f}"), use_container_width=True)

elif opcion == "Preguntas de Investigación":
    tab1, tab2, tab3, tab4 = st.tabs(["Fertilizante vs Rendimiento", "Nivel de Fertilizante", "Precipitaciones", "Correlación"])
    
    with tab1:
        st.markdown("### Influencia del Fertilizante en el Rendimiento")
        fig_a = px.scatter(df_estudio, x='fertilizante', y='rendimiento', color='temporada', opacity=0.6)
        st.plotly_chart(fig_a, use_container_width=True)
        
    with tab2:
        st.markdown("### Rendimiento según Nivel de Fertilizante")
        mediana_fert = df_estudio['fertilizante'].median()
        df_estudio['nivel_fertilizante'] = df_estudio['fertilizante'].apply(lambda x: 'Alto' if x > mediana_fert else 'Bajo')
        fig_b = px.box(df_estudio, x='nivel_fertilizante', y='rendimiento', color='temporada')
        st.plotly_chart(fig_b, use_container_width=True)

    with tab3:
        st.markdown("### Distribución de Precipitaciones (Alto Rendimiento)")
        alto_r = df_estudio[df_estudio['rendimiento'] >= df_estudio['rendimiento'].quantile(0.75)]
        fig_c = px.histogram(alto_r, x='precipitacion_anual', color='temporada', barmode='overlay')
        st.plotly_chart(fig_c, use_container_width=True)

    with tab4:
        st.markdown("### Correlación entre Precipitaciones y Agroquímicos")
        matriz_corr = df_estudio[['precipitacion_anual', 'fertilizante', 'pesticida']].corr()
        fig_d = px.imshow(matriz_corr, text_auto=True, color_continuous_scale='Blues')
        st.plotly_chart(fig_d, use_container_width=True)

elif opcion == "Objetivos del Proyecto":
    # Objetivo 1
    st.markdown("### Variabilidad Pluviométrica por Temporada")
    fig_obj1 = px.box(df_estudio, x="temporada", y="precipitacion_anual", color="temporada")
    st.plotly_chart(fig_obj1, use_container_width=True)
    
    # Objetivo 2
    st.markdown("### Comparación de Factores Críticos")
    factores = df_estudio.groupby('temporada')[['precipitacion_anual','rendimiento', 'fertilizante', 'pesticida']].mean().reset_index()
    html_cards = '<div class="contenedor-horizontal">'
    for _, fila in factores.iterrows():
        html_cards += f"""
        <div class="tarjeta-temporada">
            <h4>{fila['temporada']}</h4>
            <div class="dato-lluvia"><span class="label-dato">Lluvia</span><span class="valor-dato">{fila['precipitacion_anual']:.2f} mm</span></div>
            <div class="dato-rendimiento"><span class="label-dato">Rendimiento</span><span class="valor-dato">{fila['rendimiento']:.3f}</span></div>
            <div class="dato-fertilizante"><span class="label-dato">Fertilizante</span><span class="valor-dato">{fila['fertilizante']:.2f} kg</span></div>
            <div class="dato-pesticida"><span class="label-dato">Pesticida</span><span class="valor-dato">{fila['pesticida']:.2f} kg</span></div>
        </div>
        """.replace("\n", "").replace("    ", "")
    html_cards += '</div>'
    st.markdown(html_cards, unsafe_allow_html=True)

    # Objetivo 3
    st.markdown("### Demanda Total de Agroquímicos")
    demanda = df_estudio.groupby('temporada')[['fertilizante', 'pesticida']].sum().reset_index()
    fig_obj3 = px.bar(demanda, x='temporada', y=['fertilizante', 'pesticida'], barmode='group')
    st.plotly_chart(fig_obj3, use_container_width=True)