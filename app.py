import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(page_title="Proyecto Cultivos", page_icon="🌱", layout="wide")

st.markdown("<h1 style='text-align: center; color: #000000;'>Dashboard de Análisis de los Factores Determinantes en Ciclos Agrícola </h1>", unsafe_allow_html=True)

st.divider()

opcion = st.sidebar.selectbox(
    "¿Qué deseas ver?",
    ("", "Calculos estadisticos", "Frecuencia de Cultivos", "Fertilizante", "Pesticida", "Rendimiento", "Precipitación", "Fertilizante vs Precipitación", "Precipitación vs Rendimiento")
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

if opcion == "":
    st.markdown("""
    <style>
    .bienvenida {
        font-family: 'Arial black';
        color: #000000; /* Azul Pastel */
        font-size: 14px;
        text-align: center;
        font-weight: bold;
        padding: 18px;
        border-radius: 8px;
        background-color: #91be8c; /* Fondo muy suave */
    }
    </style>
    <p class="bienvenida">
        Bienvenido. Por favor, selecciona una categoría en el menú lateral para comenzar.
    </p>
    """, unsafe_allow_html=True)
    st.write("Bienvenido. Por favor, selecciona una categoría en el menú de lateral para comenzar.")

elif opcion == "Calculos estadisticos":
    st.subheader("Calculos estadisticos de los Factores Determinantes en Ciclos Agrícolas")   
    st.header("Resumen Estadístico")
    st.dataframe(df.describe(), use_container_width=True)

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
    st.subheader("Gráfico de Torta: Rendimiento por Temporada")
    yield_by_season = df.groupby('season')['yield'].mean().reset_index()
    colors = ["#9378E7", "#52A1F7", '#00CC96'] 
    fig5 = px.pie(yield_by_season, values='yield', names='season', color_discrete_sequence=colors) 
    fig5.update_layout(font_color="black",  font_family="Arial Black", font_size=16)
    st.plotly_chart(fig5)

# Scatter plots: Fertilizante vs Rendimiento por Temporada
    st.subheader("Scatter Plot: Fertilizante vs Rendimiento por Temporada")
    colors = ["#9378E7", "#52A1F7", '#00CC96']
    fig6 = px.scatter(df, x='fertilizer', y='yield', color='season',
                  labels={'fertilizer': 'Fertilizante', 'yield': 'Rendimiento', 'season': 'Temporada'}, color_discrete_sequence=colors)
    fig6.update_layout(font_color="black",  font_family="Arial Black", font_size=16)
    st.plotly_chart(fig6)

# Scatter plots: Pesticida vs Rendimiento por Temporada
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



