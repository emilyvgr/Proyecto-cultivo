import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(page_title="Proyecto Cultivos", page_icon="logo solo.svg", layout="wide")

st.markdown("""
    <style>
    /* 1. CAMBIAR COLOR DE LA BARRA LATERAL */
    section[data-testid="stSidebar"] {
        background-color: #E8F5E9; /* Verde pastel suave */
    }

    /* 2. CAMBIAR COLOR DE LA BARRA SUPERIOR (Header) */
    header[data-testid="stHeader"] {
        background-color: #F1F8E9;/
        color: white;
    }

    /* 3. CAMBIAR COLOR DE LOS WIDGETS (Botones, selectores, etc.) */
    /* Cambia el color de fondo de los inputs y selectores */
    .stSelectbox div[data-baseweb="select"], .stTextInput div[data-baseweb="input"] {
        background-color: #0288D1;
        border-radius: 10px;
    }

    /* Cambia el color de los botones */
    div.stButton > button {
        background-color: #FBC02D;
        color: #444444;
        border-radius: 20px;
        border: none;
        transition: 0.3s;
    }
    
    /* Efecto hover para los botones */
    div.stButton > button:hover {
        background-color: #AEC6CF; /* Cambia a azul pastel al pasar el mouse */
        color: white;
    }

    /* 4. FONDO DE LA PÁGINA PRINCIPAL */
    .stApp {
        background-color: #F1F8E9;/
    }
    </style>
    """, unsafe_allow_html=True)

colA, colB, colC = st.columns([0.2, 3, 0.2])
with colA:
    st.image("logo solo.svg", width=150)
with colB:
   st.markdown("""
    <h1 style='text-align: center; color: #000000; font-size: 30px; font-family: Arial Black;'>
        Análisis de los Factores Determinantes en Ciclos Agrícola
    </h1>
    """, unsafe_allow_html=True)
st.divider()

col1, col2, col3 = st.sidebar.columns([1, 2, 1])
with col2:
    st.image("logo solo.svg", width=100)
opcion = st.sidebar.selectbox(
    "Selecciona una opción",
    ("Calculos Estadisticos", "Tabla de Datos", "Frecuencia de Cultivos", "Fertilizante", "Pesticida", "Rendimiento", "Precipitación", "Fertilizante vs Precipitación", "Precipitación vs Rendimiento")
)

df = pd.read_csv("./27. Agricultura.csv")

df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

df = df.drop_duplicates()

# Convertir tipos según tus columnas
for col in df.select_dtypes(include=["object", "string"]).columns:
    df[col] = df[col].str.strip()

df = df.infer_objects()

q1_production = df["production"].quantile(0.25)
q3_production = df["production"].quantile(0.75)
iqr_production = q3_production - q1_production
lower_bound_production = q1_production - 1.5 * iqr_production
upper_bound_production = q3_production + 1.5 * iqr_production
df = df.query("production >= @lower_bound_production and production <= @upper_bound_production")

q1_fertilizer = df["fertilizer"].quantile(0.25)
q3_fertilizer = df["fertilizer"].quantile(0.75)
iqr_fertilizer = q3_fertilizer - q1_fertilizer
lower_bound_fertilizer = q1_fertilizer - 1.5 * iqr_fertilizer
upper_bound_fertilizer = q3_fertilizer + 1.5 * iqr_fertilizer
df = df.query("fertilizer >= @lower_bound_fertilizer and fertilizer <= @upper_bound_fertilizer")

q1_area = df["area"].quantile(0.25)
q3_area = df["area"].quantile(0.75)
iqr_area = q3_area - q1_area
lower_bound_area = q1_area - 1.5 * iqr_area
upper_bound_area = q3_area + 1.5 * iqr_area
df = df.query("area >= @lower_bound_area and area <= @upper_bound_area")
 
df = df.query("crop_year >= 2010 and crop_year <= 2020")

df = df[df['season'] != 'Whole Year']
df['season'] = df['season'].replace('Summer', 'Zaid')
df['season'] = df['season'].replace('Winter', 'Rabi')
df['season'] = df['season'].replace('Autumn', 'Kharif')



if opcion == "Calculos Estadisticos":
    col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
    with col1:
        st.markdown("""
        <h1 style='text-align: center; color: #444444; font-size: 18px; font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;'>
        Influencia de los Factores Determinantes en Ciclos Agrícolas
        </h1>
        """, unsafe_allow_html=True)
        st.markdown("""
<style>
    .metric-card {
        background-color: #FFFFFF; /* Fondo blanco */
        border: 2px solid #E0E0E0; /* Borde gris suave */
        padding: 20px;
        border-radius: 15px; /* Esquinas redondeadas */
        text-align: center;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.05); /* Sombra sutil */
        margin-bottom: 10px;
    }
    .metric-label {
        color: #555555;
        font-size: 10px;
        font-weight: bold;
        margin-bottom: 5px;
    }
    .metric-value {
        color: #AEC6CF; /* Color pastel (puedes cambiarlo por cada col) */
        font-size: 10px
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)
        promedios = df[['fertilizer', 'pesticide', 'yield']].mean()
        col11, col12, col13 = st.columns(3)
        with col11:
            st.markdown(f"""
         <div class="metric-card" style="border-color: #AEC6CF;">
            <div class="metric-label">Promedio Fertilizante</div>
            <div class="metric-value" style="color: #AEC6CF;">{promedios['fertilizer']:.2f} kg</div>
            </div>
            """, unsafe_allow_html=True)
        with col12:
            st.markdown(f"""
            <div class="metric-card" style="border-color: #FFD1DC;">
            <div class="metric-label">Promedio Pesticida</div>
            <div class="metric-value" style="color: #FFD1DC;">{promedios['pesticide']:.2f} L</div>
            </div>
            """, unsafe_allow_html=True)
        with col13:
            st.markdown(f"""
            <div class="metric-card" style="border-color: #B3E5BE;">
            <div class="metric-label">Rendimiento Promedio</div>
            <div class="metric-value" style="color: #B3E5BE;">{promedios['yield']:.2f} Ton</div>
            </div>
            """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <h1 style='text-align: center; color: #444444; font-size: 18px; font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;'>
        Necesidad de Agroquímicos en la Temporada
        </h1>
        """, unsafe_allow_html=True)
        st.markdown("""
        <style>
        /* Buscamos el contenedor donde Streamlit mete los dataframes */
        [data-testid="stDataFrame"] {
            background-color: #FFFFFF;
            border-radius: 20px;
            padding: 20px;
            border: 2px solid #E0E0E0;
            box-shadow: 2px 2px 15px rgba(0,0,0,0.05);
        }
        </style>
        """, unsafe_allow_html=True)
        matriz_corr = df[['fertilizer', 'pesticide', 'yield']].corr()
        st.dataframe(
        matriz_corr.style.background_gradient().format("{:.2f}"),
        use_container_width=True
        )


    with col3:
        pass
    with col4:
        pass

elif opcion == "Tabla de Datos":
   st.markdown("""
        <h1 style='text-align: center; color: #444444; font-size: 18px; font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;'>
        Tabla de Calculos estadisticos para los Factores Determinantes en Ciclos Agrícola
        </h1>
        """, unsafe_allow_html=True)   
   st.markdown("""
        <style>
        /* Aplicamos el diseño a los contenedores de tablas */
        [data-testid="stDataFrame"] {
        background-color: #FFFFFF;
        border-radius: 20px;
        padding: 20px;
        border: 2px solid #E0E0E0;
        box-shadow: 2px 2px 15px rgba(0,0,0,0.05);
        }
        </style>
        """, unsafe_allow_html=True)
   st.dataframe(
        df.describe().style.format("{:.2f}"), 
        use_container_width=True )

elif opcion == "Frecuencia de Cultivos":
    st.subheader("Frecuencia de los Cultivos por Temporada")
    freq_by_season_crop = df.groupby(['season', 'crop']).size().reset_index(name='count')
    colors = ["#9378E7", "#52A1F7", '#00CC96']
    top_crops = (freq_by_season_crop.groupby('crop')['count']
      .sum()
      .nlargest(10)
      .index)
    freq_top = freq_by_season_crop[freq_by_season_crop['crop'].isin(top_crops)]
    fig2 = px.bar(freq_top, x='crop', y='count',color='season', barmode='group',color_discrete_sequence=colors)
    fig2.update_layout(font_color="black",  font_family="Arial Black", font_size=16)
    st.plotly_chart(fig2)

elif opcion == ("Fertilizante"):
    st.subheader("Fertilizante por Temporada de Cultivo")
    fertilizer_by_season = df.groupby('season')['fertilizer'].mean().reset_index()
    colors = ["#9378E7", "#52A1F7", '#00CC96']
    fig3 = px.pie(fertilizer_by_season, values='fertilizer', names='season', color_discrete_sequence=colors)
    fig3.update_layout(font_color="black",  font_family="Arial Black", font_size=16)
    st.plotly_chart(fig3)

elif opcion == ("Pesticida"):
    st.subheader("Pesticida por Temporada de Cultivo")
    pesticide_by_season = df.groupby('season')['pesticide'].mean().reset_index()
    colors = ["#9378E7", "#52A1F7", '#00CC96']
    fig4 = px.pie(pesticide_by_season, values='pesticide', names='season', color_discrete_sequence=colors)
    fig4.update_layout(font_color="black",  font_family="Arial Black", font_size=16)
    st.plotly_chart(fig4)

elif opcion == ("Rendimiento"):
   col1, col2, col3 = st.columns([2, 2, 2])
   with col1:
        st.subheader("Gráfico de Torta: Rendimiento por Temporada")
        yield_by_season = df.groupby('season')['yield'].mean().reset_index()
        colors = ["#9378E7", "#52A1F7", '#00CC96'] 
        fig5 = px.pie(yield_by_season, values='yield', names='season', color_discrete_sequence=colors) 
        fig5.update_layout(font_color="black",  font_family="Arial Black", font_size=16)
        st.plotly_chart(fig5)
   with col2:
        st.subheader("Scatter Plot: Fertilizante vs Rendimiento por Temporada")
        colors = ["#9378E7", "#52A1F7", '#00CC96']
        fig6 = px.scatter(df, x='fertilizer', y='yield', color='season',
                  labels={'fertilizer': 'Fertilizante', 'yield': 'Rendimiento', 'season': 'Temporada'}, color_discrete_sequence=colors)
        fig6.update_layout(font_color="black",  font_family="Arial Black", font_size=16)
        st.plotly_chart(fig6)
   with col3:
        st.subheader("Scatter Plot: Pesticida vs Rendimiento por Temporada")
        colors = ["#9378E7", "#52A1F7", '#00CC96']
        fig7 = px.scatter(df, x='pesticide', y='yield', color='season',
                  labels={'pesticide': 'Pesticida', 'yield': 'Rendimiento', 'season': 'Temporada'}, color_discrete_sequence=colors)
        fig7.update_layout(font_color="black",  font_family="Arial Black", font_size=16)
        st.plotly_chart(fig7)

elif opcion == ("Precipitación"):
    st.subheader("Precipitación por Temporada y por Años")
    rain_by_year_season = df.groupby(['crop_year', 'season'])['annual_rainfall'].mean().reset_index()
    colors = ["#9378E7", "#52A1F7", '#00CC96']
    fig8 = px.line(rain_by_year_season, x='crop_year', y='annual_rainfall', color='season',
                  labels={'crop_year': 'Año', 'annual_rainfall': 'Precipitación Anual Promedio (mm)'}, color_discrete_sequence=colors)
    fig8.update_layout(font_color="black",  font_family="Arial Black", font_size=16)
    st.plotly_chart(fig8)

elif opcion == ("Fertilizante vs Precipitación"):
    st.subheader("Scatter Plot: Fertilizante vs Precipitación por Temporada")
    colors = ["#9378E7", "#52A1F7", '#00CC96']
    fig9 = px.scatter(df, x='annual_rainfall', y='fertilizer', color='season',
                   labels={'annual_rainfall': 'Precipitación Anual (mm)', 'fertilizer': 'Fertilizante'}, color_discrete_sequence=colors)
    fig9.update_layout(font_color="black",  font_family="Arial Black", font_size=16)
    st.plotly_chart(fig9)

elif opcion == ("Precipitación vs Rendimiento"):
    st.subheader("Precipitación vs Rendimiento por Temporada")
    colors = ["#9378E7", "#52A1F7", '#00CC96']
    fig10 = px.scatter(df, x='annual_rainfall', y='yield', color='season',
                       labels={'annual_rainfall': 'Precipitación Anual (mm)', 'yield': 'Rendimiento', 'season': 'Temporada'}, color_discrete_sequence=colors)
    fig10.update_layout(font_color="black",  font_family="Arial Black", font_size=16)
    st.plotly_chart(fig10)



