import streamlit as st
import pandas as pd
import os, sys
import plotly.express as px
import altair as alt

root_folder = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from OSeMOSYS.utils import assign_colors_to_technologies, COLOR_VARIATIONS

# Configuración inicial de Streamlit
st.set_page_config(
    page_title="OSeMOSYS Streamlit",
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Título de la aplicación
st.title("OSeMOSYS Streamlit")

# Cargar datos
# datos = pd.read_csv('/home/david/OSeMOSYS-pyomo/results/SuperSimpleExpandedReTagStorage/RateOfActivity.csv')
datos = pd.read_csv('/home/david/OSeMOSYS-pyomo/results/RetroffUnits700-24RE-NoBio/RateOfActivity.csv')


# Mostrar los primeros datos
st.sidebar.title("Configuración")
st.sidebar.write("Vista previa de los datos:")
st.sidebar.dataframe(datos.head())

# Combine YEAR and TIMESLICE into a new column
datos["YEAR_TIMESLICE"] = datos["YEAR"].astype(str) + "_" + datos["TIMESLICE"].astype(str)

# Crear mapeo plano de tecnologías → color
def get_tech_color(tech):
    tech_lower = tech.lower()
    for key in COLOR_VARIATIONS:
        if key in tech_lower:
            return COLOR_VARIATIONS[key][0]
    return 'gray'

# Widgets de filtro interactivo
selected_techs = st.multiselect("Selecciona tecnologías", options=sorted(datos["TECHNOLOGY"].unique()), default=list(datos["TECHNOLOGY"].unique()))
# selected_years = st.multiselect("Selecciona años", options=sorted(datos["YEAR"].unique()), default=list(datos["YEAR"].unique()))
selected_slices = st.multiselect("Selecciona timeslices", options=sorted(datos["TIMESLICE"].unique()), default=list(datos["TIMESLICE"].unique()))
min_year = int(datos["YEAR"].min())
max_year = int(datos["YEAR"].max())

selected_year_range = st.slider(
    "Selecciona rango de años",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year),
    step=1
)


# Filtrar datos según selección
filtered_data = datos[
    (datos["TECHNOLOGY"].isin(selected_techs)) &
    (datos["YEAR"] >= selected_year_range[0]) &
    (datos["YEAR"] <= selected_year_range[1]) &
    (datos["TIMESLICE"].isin(selected_slices))
]
# Si no hay datos, muestra aviso
if filtered_data.empty:
    st.warning("No hay datos para la combinación seleccionada.")
else:
    # Crear mapeo de color actualizado solo con datos filtrados
    tech_color_map = {tech: get_tech_color(tech) for tech in filtered_data["TECHNOLOGY"].unique()}

    # Crear gráfico
    chart = alt.Chart(filtered_data).mark_bar().encode(
        x=alt.X("YEAR_TIMESLICE:N", title="Año / Timeslice"),
        y=alt.Y("value:Q", title="Valor"),
        color=alt.Color("TECHNOLOGY:N", scale=alt.Scale(domain=list(tech_color_map.keys()), range=list(tech_color_map.values()))),
        tooltip=["YEAR", "TIMESLICE", "TECHNOLOGY", "value"]
    )

    st.altair_chart(chart, use_container_width=True)