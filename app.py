import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="Proyecto Cultivos", page_icon="logo solo.svg", layout="wide")
#limpieza
@st.cache_data 
def datos_a_trabajar():
    df = pd.read_csv("agricultura.csv")
    columnas_es = {
    'Crop': 'cultivo', 'Crop_Year': 'año', 'Season': 'temporada',
    'State': 'estado', 'Area': 'area', 'Production': 'produccion',
    'Annual_Rainfall': 'precipitacion_anual', 'Fertilizer': 'fertilizante',
    'Pesticide': 'pesticida', 'Yield': 'rendimiento'}
    df.rename(columns=columnas_es, inplace=True)

    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    df = df.drop_duplicates()
    
    for col in df.select_dtypes(include=["object", "string"]).columns:
        df[col] = df[col].str.strip()

    # Filtro Outliers (Simplificado para el ejemplo)
    for col in ["produccion", "fertilizante", "area"]:
        q1, q3 = df[col].quantile([0.25, 0.75])
        iqr = q3 - q1
        df = df.query(f"{col} >= {q1 - 1.5*iqr} and {col} <= {q3 + 1.5*iqr}")

    df = df.query("año >= 2010 and año <= 2020")
    df = df[df['temporada'] != 'Whole Year']
    df['temporada'] = df['temporada'].replace({'Summer': 'Zaid', 'Winter': 'Rabi', 'Autumn': 'Kharif'})
    return df

df_estudio = datos_a_trabajar()

st.markdown("<h1>Análisis de los Factores Determinantes en Ciclos Agrícolas</h1>", unsafe_allow_html=True)

tab_media, tab_investigacion, tab_datos = st.tabs(["Cálculos Estadísticos", "Análisis de Investigación", "Base de Datos Limpia"])
#tabla datos
with tab_datos:
    st.subheader("Base de Datos Limpia")
    st.write(f"Total registros: **{len(df_estudio)}**")
    st.dataframe(df_estudio, use_container_width=True, hide_index=True)

#tabla calculos
with tab_media:
    st.subheader("Cálculos Estadísticos Globales")
    estadisticas = df_estudio.describe().rename(index={
        'count': 'Total (N)', 'mean': 'Promedio', 'std': 'Des. Típica',
        'min': 'Mínimo', '25%': '25%', '50%': 'Mediana', '75%': '75%', 'max': 'Máximo'
    })
    st.dataframe(estadisticas.style.format("{:.2f}"))

with tab_investigacion:
    st.subheader("Preguntas de Investigación")
    col_p1, col_p2 = st.columns(2)
    # PREGUNTA 1
    with col_p1:
        st.subheader("¿De qué manera influyen la cantidad de agroquímicos en los ciclos de cultivos?")
        df_q1 = df_estudio.groupby('temporada')[['fertilizante', 'pesticida']].mean().reset_index()
        fig1 = px.bar(df_q1, x='temporada', y=['fertilizante', 'pesticida'], 
                        barmode='group', title="Promedio de Agroquímicos por Temporada",
                        color_discrete_sequence=['#2e7d32', '#81c784'])
        st.plotly_chart(fig1, use_container_width=True)
    # PREGUNTA 2
    with col_p2:
        st.subheader("¿Por que son necesario los fertilizantes y los pesticidas en una temporada de cultivo?")
        df_estudio['uso_insumos'] = df_estudio['fertilizante'] + df_estudio['pesticida']
        umbral = df_estudio['uso_insumos'].median()
        df_alto = df_estudio[df_estudio['uso_insumos'] > umbral]
        df_bajo = df_estudio[df_estudio['uso_insumos'] <= umbral]

        col_g1, col_g2 = st.columns(2)
        with col_g1:
            fig2_1 = px.histogram(df_alto, x='rendimiento', title="Rendimiento (Uso Alto de Agroquímicos)",
                                 color_discrete_sequence=['#1b5e20'])
            st.plotly_chart(fig2_1, use_container_width=True)
        with col_g2:
            fig2_2 = px.histogram(df_bajo, x='rendimiento', title="Rendimiento (Uso Bajo de Agroquímicos)",
                                 color_discrete_sequence=['#a5d6a7'])
            st.plotly_chart(fig2_2, use_container_width=True)
    
    col_p3, col_p4 = st.columns(2)
    # PREGUNTA 3
    with col_p3:
        st.subheader("¿Que temporada de cultivo se favorece de las precipitaciones anuales?")
        df_q3 = df_estudio.groupby('temporada')['precipitacion_anual'].mean().reset_index()
        fig3 = px.bar(df_q3, x='temporada', y='precipitacion_anual', 
                        title="Precipitación Promedio por Temporada",
                        color_discrete_sequence=['#388e3c'])
        st.plotly_chart(fig3, use_container_width=True)
    
    #pregunta 4
    with col_p4:
        st.subheader("¿La cantidad de agroquímicos varía según los niveles de precipitación?")
        df_estudio['total_agroquimicos'] = df_estudio['fertilizante'] + df_estudio['pesticida']
        fig4 = px.scatter(df_estudio, x='total_agroquimicos', y='precipitacion_anual',
            color='temporada', title="Dispersión: Agroquímicos vs Precipitación",
            color_discrete_sequence=['#00441b', '#238b45', '#74c476'])
        st.plotly_chart(fig4, use_container_width=True)