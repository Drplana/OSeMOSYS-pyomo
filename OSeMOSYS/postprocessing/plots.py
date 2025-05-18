# import pandas as pd
# import plotly.express as px
# from plotly.subplots import make_subplots
# COLOR_VARIATIONS = {
#     'PWRCRUD001': 'gray',
#     'PWRCRUD002': 'dimgray',
#     'PWRCRUD003': 'darkgray',
#     'PWRCRUD004': 'silver',
#     'PWRCRUD005': 'lightgray',
#     'PWRCRUD006': 'gainsboro',
#     'PWRCRUD007': 'whitesmoke',
#     'PWRCRUD008': 'black',
#     'PWRHFO01': '#8B0000',
#     'PWRNG01': 'orange',
#     'PWRNG02': 'darkorange',
#     'PWRGHFO2': '#F19953',
#     'PWRBIO': '#9ACD32',
#     'PWRWND001': 'deepskyblue',#4169E1
#     'PWRWND002': 'deepskyblue',
#     'PWRPV01': '#FFD700',
#     'PWRPV02': '#CCAC00',
#     'PWRCSP': 'gray',
#     'PWRFO': '#FF6961',
#     'PWRDSL': 'brown',
#     'PWRHYD01': '#0d5c91',
#     'PWRHYD02': '#1f77b4'
# }

# def load_and_prepare_data(filepath):
#     df = pd.read_csv(filepath)
#     df['TIMESLICE'] = df['TIMESLICE'].astype(str)
    
#     # Filter for power technologies (PWR) excluding distribution/transmission
#     df = df[df['TECHNOLOGY'].str.contains('PWR') & 
#             ~df['TECHNOLOGY'].str.contains('PWRDIST|PWRTRANS')]
    
#     # Optional: Filter out near-zero values (uncomment if needed)
#     # df = df[round(df['value'], 4) != 0]
    
#     return df

# def plot_activity(datafile, COLOR_VARIATIONS=COLOR_VARIATIONS):
#     data = pd.read_csv(datafile)
   


#     # data['TIMESLICE'] = data['TIMESLICE'].astype(str)
#     # Create a stacked bar chart using Plotly
#     data['value']= data['value']*277.78
#     data= data[data['TECHNOLOGY'].str.contains('PWR')].sort_values(by='TECHNOLOGY')
#     data = data[~data['TECHNOLOGY'].str.contains('PWRDIST|PWRTRANS')]
#     data = data[round(data['value'],4) != 0]

#     fig = px.bar(data, x="YEAR", y = "value", color="TECHNOLOGY",
#                 color_discrete_map = COLOR_VARIATIONS,
#                 opacity = 0.7,
#                 )

#     fig.update_layout(hovermode='x unified', 
#                     autosize=False,
#                     width= 1000,
#                     height= 600, 
#                     yaxis_title="Energy Production in GWh",
#                     plot_bgcolor='white',
#                     #   paper_bgcolor='lightgrey',
#                     xaxis=dict(
#             tickfont=dict(size=14),  # Tamaño de la fuente de las etiquetas del eje x
#             titlefont=dict(size=16)
#                     ),
#                     yaxis=dict(
#             showgrid=False,
#             tickfont=dict(size=14),      
#             gridwidth=0.5,        #
#             gridcolor='lightgrey',
#             tickformat='.0f' 
#             ),
#     legend=dict(font=dict(size=16)),
#     title={'text': 'Energy production base scenario by technology', 'x': 0.5},
#     font=dict( size=16,color='black')
#     )

#     # Show the interactive plot
#     fig.show()
#     fig1 = px.pie(data[data['YEAR']==2019], names='TECHNOLOGY', values='value', hole=0.5, title='Gráfico de Dona 1',color = 'TECHNOLOGY',color_discrete_map = COLOR_VARIATIONS,
#     opacity=0.7, category_orders={'TECHNOLOGY': data['TECHNOLOGY'].tolist()})
#     fig2 = px.pie(data[data['YEAR']==2030], names='TECHNOLOGY', values='value', hole=0.5, title='Gráfico de Dona 1',color = 'TECHNOLOGY',color_discrete_map = COLOR_VARIATIONS,
#     opacity=0.7, category_orders={'TECHNOLOGY': data['TECHNOLOGY'].tolist()} )
#     fig3 = px.pie(data[data['YEAR']==2050], names='TECHNOLOGY', values='value', hole=0.5, title='Gráfico de Dona 2',color = 'TECHNOLOGY',color_discrete_map = COLOR_VARIATIONS,
#     opacity=0.7, category_orders={'TECHNOLOGY': data['TECHNOLOGY'].tolist()})
    

#     fig = make_subplots(
#         rows=1, cols=3, 
#         specs=[[{'type': 'domain'}, {'type': 'domain'}, {'type': 'domain'}]],
#         subplot_titles=('2019','2030', '2050')
#     )
#     total_2019 = round(data[data['YEAR'] == 2019]['value'].sum(),0)
#     total_2030 = round(data[data['YEAR'] == 2030]['value'].sum(),0)
#     total_2050 = round(data[data['YEAR'] == 2050]['value'].sum(),0)

#     for trace in fig1.data:
#         fig.add_trace(trace, row=1, col=1)

#     for trace in fig2.data:
#         fig.add_trace(trace, row=1, col=2)
#     for trace in fig3.data:
#         fig.add_trace(trace, row=1, col=3)
#     annotations = [
#     dict(text=f'Total 2019<br> {total_2019} GWh', x=0.145, y=0.45,  font=dict(size=20, color='#2f4f4f'), showarrow=False),
#     dict(text=f'Total 2030<br> {total_2030} GWh', x=0.50, y=0.45, font=dict(size=20, color='#2f4f4f'), showarrow=False),
#     dict(text=f'Total 2050<br> {total_2050} GWh', x=0.855, y=0.45, font=dict(size=20, color='#2f4f4f'), showarrow=False)
#     ]
    

#     fig.update_layout(height=700, width=1200, title={'text': 'Energy Production by technology REN37 scenario(%)', 'x': 0.5, 'y':0.85, 'font':{'size': 28}} , font=dict( size=16,color='black'),annotations=annotations)

#     fig.show()

# def create_production_plot(df, COLOR_VARIATIONS):
#     # Calculate total production per timeslice for ordering
#     timeslice_order = df.groupby('TIMESLICE')['value'].sum().index
    
#     fig = px.bar(
#         df,
#         x='TIMESLICE', 
#         y='value', 
#         color='TECHNOLOGY', 
#         animation_frame='YEAR',
#         labels={
#             'value': 'Energy Production (PJ)',
#             'TIMESLICE': 'Time Slice',
#             'TECHNOLOGY': 'Power Technology'
#         },
#         width=900,  # Slightly wider for better display
#         height=700,  # Taller to accommodate legend
#         category_orders={
#             'TIMESLICE': timeslice_order,
#             'YEAR': sorted(df['YEAR'].unique())
#         },
#         color_discrete_map=COLOR_VARIATIONS,
#         title='Power Generation by Technology Across Time Slices (Animated by Year)'
#     )
#     return fig


# if __name__ == '__main__':


#     datafile = '../../results/v_ProductionByTechnologyAnnual.csv'
#     plot_activity(datafile)
    
#     data_path = '../../results/v_RateOfProductionByTechnology.csv'
#     production_data = load_and_prepare_data(data_path)
    
 
#     fig = create_production_plot(production_data, COLOR_VARIATIONS)
#     fig.show()


import os
import sys
import random
root_folder = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
from OSeMOSYS.config import configure_paths
# ROOT_FOLDER = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import matplotlib.colors as mcolors
import colorsys
import plotly.express as px
import itertools
import colorsys
import random
from collections import defaultdict

import matplotlib.colors as mcolors
import itertools

import matplotlib.colors as mcolors
from itertools import cycle
from OSeMOSYS.utils import COLOR_VARIATIONS, DEPENDENCIES_VAR_DICT
from dash import Dash, dcc, html, Input, Output
import webbrowser
# Paletas personalizadas para cada keyword


# def assign_colors(technologies, keyword_colors):
#     """Asigna colores usando paletas predefinidas en orden secuencial."""
#     groups = {}
#     color_map = {}
    
#     # 1. Agrupar tecnologías por keyword
#     for tech in technologies:
#         tech_lower = tech.lower()
#         matched = False
        
#         # Buscar coincidencia más específica primero
#         for keyword in sorted(keyword_colors.keys(), key=lambda x: (-len(x), x)):
#             if keyword in tech_lower:
#                 groups.setdefault(keyword, []).append(tech)
#                 matched = True
#                 break
                
#         if not matched:
#             groups.setdefault('unmatched', []).append(tech)
    
#     # 2. Asignar colores según las paletas
#     for keyword, techs in groups.items():
#         if keyword == 'unmatched':
#             # Paleta especial para no coincidentes (no usada en keywords)
#             unused_colors = [c for c in px.colors.qualitative.Plotly 
#                             if not any(c in pal for pal in COLOR_VARIATIONS.values())]
#             color_cycle = cycle(unused_colors)
#             for tech in techs:
#                 color_map[tech] = next(color_cycle)
#         else:
#             base_color = keyword_colors[keyword]
#             variations = COLOR_VARIATIONS.get(keyword, [base_color])
#             color_cycle = cycle(variations)
            
#             for tech in techs:
#                 color_map[tech] = next(color_cycle)
    
#     return color_map
def assign_colors(technologies, color_variations):
    """
    Asigna colores a las tecnologías usando COLOR_VARIATIONS. Si no hay coincidencia, usa un color por defecto.

    Args:
        technologies (list): Lista de tecnologías.
        color_variations (dict): Diccionario con keywords y sus paletas de colores.

    Returns:
        dict: Diccionario que asigna un color a cada tecnología.
    """
    color_map = {}
    unused_colors = cycle(px.colors.qualitative.Plotly)  # Paleta genérica para tecnologías no coincidentes

    # Convertir las claves de COLOR_VARIATIONS a minúsculas
    color_variations_lower = {k.lower(): cycle(v) for k, v in color_variations.items()}

    for tech in technologies:
        tech_lower = tech.lower()
        matched = False

        # Buscar coincidencia en COLOR_VARIATIONS (convertido a minúsculas)
        for keyword, variations in color_variations_lower.items():
            if keyword in tech_lower:
                color_map[tech] = next(variations)
                matched = True
                break

        # Si no hay coincidencia, asignar un color por defecto
        if not matched:
            color_map[tech] = next(unused_colors)

    return color_map
# Define a color dictionary for technologies


def load_and_prepare_data(filepath):
    """
    Load and prepare data from a CSV file.

    Args:
        filepath (str): Path to the CSV file.

    Returns:
        pd.DataFrame: Processed DataFrame.
    """
    try:
        df = pd.read_csv(filepath)
        df['TIMESLICE'] = df['TIMESLICE'].astype(str)
        df = df[df['TECHNOLOGY'].str.contains('PWR') & 
                ~df['TECHNOLOGY'].str.contains('PWRDIST|PWRTRANS')]
        return df
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        return pd.DataFrame()

def plot_activity(datafile, COLOR_VARIATIONS=COLOR_VARIATIONS, years=[2019, 2030, 2050]):
    """
    Create and display energy production plots.

    Args:
        datafile (str): Path to the CSV file containing production data.
        COLOR_VARIATIONS (dict): Dictionary mapping technologies to colors.
    """
    try:
        data = pd.read_csv(datafile)
        # data['value'] = data['value'] * 277.78
        # data = data[data['TECHNOLOGY'].str.contains('PWR')].sort_values(by='TECHNOLOGY')
        # data = data[~data['TECHNOLOGY'].str.contains('PWRDIST|PWRTRANS')]
        # data = data[round(data['value'], 4) != 0]

        # Stacked bar chart
        fig = px.bar(
            data, x="YEAR", y="value", color="TECHNOLOGY",
            color_discrete_map=COLOR_VARIATIONS, opacity=0.7
        )
        fig.update_layout(
            hovermode='x unified',
            autosize=False,
            width=1000,
            height=600,
            yaxis_title="Energy Production in GWh",
            plot_bgcolor='white',
            xaxis=dict(tickfont=dict(size=14), titlefont=dict(size=16)),
            yaxis=dict(showgrid=False, tickfont=dict(size=14), gridcolor='lightgrey'),
            legend=dict(font=dict(size=16)),
            title={'text': 'Energy production base scenario by technology', 'x': 0.5},
            font=dict(size=16, color='black')
        )
        fig.show()

        # Pie charts for specific years
        # years = [2019, 2030, 2050]
        fig = make_subplots(
            rows=1, cols=3, specs=[[{'type': 'domain'}] * 3],
            subplot_titles=[str(year) for year in years]
        )
        annotations = []
        for i, year in enumerate(years):
            year_data = data[data['YEAR'] == year]
            total = round(year_data['value'].sum(), 0)
            pie = px.pie(
                year_data, names='TECHNOLOGY', values='value', hole=0.5,
                color='TECHNOLOGY', color_discrete_map=COLOR_VARIATIONS, opacity=0.7
            )
            for trace in pie.data:
                fig.add_trace(trace, row=1, col=i + 1)
            annotations.append(
                dict(
                    text=f'Total {year}<br>{total} GWh',
                    x=0.145 + i * 0.355, y=0.45,
                    font=dict(size=20, color='#2f4f4f'), showarrow=False
                )
            )
        fig.update_layout(
            height=700, width=1200,
            title={'text': 'Energy Production by Technology (%)', 'x': 0.5, 'y': 0.85},
            font=dict(size=16, color='black'),
            annotations=annotations
        )
        fig.show()
    except FileNotFoundError:
        print(f"Error: File not found at {datafile}")


def dashboard(datafile, COLOR_VARIATIONS, years=[2019, 2030, 2050]):
    """
    Create and display energy production plots in a single dashboard.

    Args:
        datafile (str): Path to the CSV file containing production data.
        COLOR_VARIATIONS (dict): Dictionary mapping technologies to colors.
        years (list): List of years for the pie charts.
    """
    try:
        # Leer los datos
        data = pd.read_csv(datafile)

        # Obtener los años únicos del DataFrame
        years_in_data = sorted(data['YEAR'].unique())
        # print(f"Años en los datos: {years_in_data}")

        # Gráfico de barras apiladas
        bar_fig = px.bar(
            data, x="YEAR", y="value", color="TECHNOLOGY",
            color_discrete_map=COLOR_VARIATIONS, opacity=0.7
        )
        bar_fig.update_traces(showlegend=True)  # Asegurar que la leyenda esté habilitada
        bar_fig.update_layout(
            barmode='stack',  # Apilar las barras
            hovermode='x unified',
            yaxis_title="Energy Production in GWh",
            plot_bgcolor='white',
            title={'text': 'Energy Production by Technology', 'x': 0.5},
            font=dict(size=16, color='black'),
            xaxis=dict(tickfont=dict(size=14), titlefont=dict(size=16), range=[min(years_in_data), max(years_in_data)]),
            yaxis=dict(showgrid=False, tickfont=dict(size=14), gridcolor='lightgrey'),
            legend=dict(font=dict(size=16), bgcolor='rgba(255, 255, 255, 0.5)')  # Fondo semitransparente
        )

        # Crear un layout combinado para ambos gráficos
        dashboard = make_subplots(
            rows=2, cols=3,  # Cambiar a 2 filas y 3 columnas
            specs=[[{'type': 'xy', 'colspan': 3}, None, None],  # Primera fila: gráfico de barras ocupa las 3 columnas
                   [{'type': 'domain'}, {'type': 'domain'}, {'type': 'domain'}]],  # Segunda fila: gráficos de dona
            subplot_titles=["Energy Production by Technology", "2019", "2030", "2050"],
            vertical_spacing=0.15,  # Reducir el espacio vertical entre filas
            column_widths=[0.33, 0.33, 0.33],  # Asegurar que las columnas tengan el mismo ancho
            row_heights=[0.6, 0.4]  # Ajustar la altura de las filas
        )

        # Agregar el gráfico de barras al dashboard
        for trace in bar_fig.data:
            dashboard.add_trace(trace, row=1, col=1)  # Agregar el gráfico de barras a la primera celda

        # Configurar explícitamente barmode='stack' en el dashboard
        dashboard.update_layout(barmode='stack')

        # Gráficos de dona para años específicos
        annotations = []
        for i, year in enumerate(years):
            year_data = data[data['YEAR'] == year]
            total = round(year_data['value'].sum(), 0)
            pie = px.pie(
                year_data, names='TECHNOLOGY', values='value', hole=0.5,
                color='TECHNOLOGY', color_discrete_map=COLOR_VARIATIONS, opacity=0.7
            )
            pie.update_traces(showlegend=False)  # Ocultar la leyenda en los gráficos de dona
            for trace in pie.data:
                dashboard.add_trace(trace, row=2, col=i + 1)  # Agregar cada gráfico de dona a su columna
            annotations.append(
                dict(
                    text=f'Total {year}<br>{total} GWh',
                    x=0.145 + i * 0.355, y=0.15,  # Ajustar posición de las anotaciones
                    font=dict(size=16, color='#2f4f4f'), showarrow=False
                )
            )
        # pie.update_layout(title = ["Energy Production by Technology", "2019", "2030", "2050"])
        # Configurar el diseño del dashboard
        dashboard.update_layout(
            height=800,  # Ajustar el alto total del dashboard
            width=1000,  # Ajustar el ancho total del dashboard
            title={'text': 'Energy Production Dashboard', 'x': 0.5},
            font=dict(size=16, color='black'),
            annotations=annotations,
            plot_bgcolor='white',
            legend=dict(font=dict(size=14), x=1, y=1, bgcolor='rgba(255, 255, 255, 0.5)'),  # Fondo semitransparente
            xaxis_title="Year",  # Título del eje X
            yaxis_title="Energy Production (GWh)"  # Título del eje Y
        )

        # Mostrar el dashboard
        dashboard.show()

    except FileNotFoundError:
        print(f"Error: File not found at {datafile}")

def create_production_plot(df, COLOR_VARIATIONS):
    """
    Create an animated bar chart for energy production.

    Args:
        df (pd.DataFrame): DataFrame containing production data.
        COLOR_VARIATIONS (dict): Dictionary mapping technologies to colors.

    Returns:
        plotly.graph_objects.Figure: Plotly figure object.
    """
    timeslice_order = df.groupby('TIMESLICE')['value'].sum().index
    fig = px.bar(
        df, x='TIMESLICE', y='value', color='TECHNOLOGY', animation_frame='YEAR',
        labels={
            'value': 'Energy Production (PJ)',
            'TIMESLICE': 'Time Slice',
            'TECHNOLOGY': 'Power Technology'
        },
        width=900, height=700,
        category_orders={'TIMESLICE': timeslice_order, 'YEAR': sorted(df['YEAR'].unique())},
        color_discrete_map=COLOR_VARIATIONS,
        title='Power Generation by Technology Across Time Slices (Animated by Year)'
    )
    fig.show()
def plot_accumulated_capacity(results_folder, selected_years=[2020, 2030, 2040, 2050], COLOR_VARIATIONS = COLOR_VARIATIONS):
    """
    Generate a scatter plot for accumulated installed capacity.

    Args:
        results_folder (str): Path to the folder containing results.
    """
    total_capacity_path = os.path.join(results_folder, 'v_TotalCapacityAnnual.csv')
    new_capacity_path = os.path.join(results_folder, 'v_NewCapacity.csv')

    try:
        TotalCapacityAnnual = pd.read_csv(total_capacity_path)
        NewCapacity = pd.read_csv(new_capacity_path)

        # Filter data
        NewCapacity = NewCapacity[NewCapacity['value'] != 0]
        NewCapacity = NewCapacity[NewCapacity['TECHNOLOGY'].str.contains('PWR')]
        NewCapacity = NewCapacity[~NewCapacity['TECHNOLOGY'].str.contains('PWRDIST|PWRTRANS')]

        TotalCapacityAnnual = TotalCapacityAnnual.sort_values(by=['TECHNOLOGY', 'YEAR'])
        TotalCapacityAnnual = TotalCapacityAnnual[TotalCapacityAnnual['TECHNOLOGY'].isin(NewCapacity.TECHNOLOGY.unique())]
        TotalCapacityAnnual = TotalCapacityAnnual[~TotalCapacityAnnual['TECHNOLOGY'].isin(['PWRFO'])]

        # User input for years
        TotalCapacityFiltered = TotalCapacityAnnual[TotalCapacityAnnual['YEAR'].isin(selected_years)]

        # Filter by selected years
        TotalCapacityFiltered = TotalCapacityAnnual[TotalCapacityAnnual['YEAR'].isin(selected_years)]

        # Create scatter plot
        fig = px.scatter(
            TotalCapacityFiltered, y='value', x='YEAR', color='TECHNOLOGY',
            color_discrete_map=COLOR_VARIATIONS
        )
        fig.update_layout(
            hovermode='x unified',
            width=800,
            height=600,
            yaxis_title="Capacity GW",
            plot_bgcolor='white',
            font=dict(size=20, color='black'),
            yaxis=dict(showgrid=True, tickfont=dict(size=16), gridcolor='lightgrey'),
            title={'text': 'Cumulative Installed Capacity of New Technologies Over the Years', 'x': 0.5}
        )
        fig.update_traces(mode='lines+markers', line=dict(width=4), marker=dict(size=10))
        fig.update_xaxes(tickvals=selected_years)
        fig.show()
    except FileNotFoundError as e:
        print(f"Error: {e}")
# Función para cargar datos
def load_data(file_path):
    """
    Carga los datos desde un archivo CSV.

    Args:
        file_path (str): Ruta al archivo CSV.

    Returns:
        pd.DataFrame: DataFrame con los datos cargados.
    """
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return pd.DataFrame()
def generate_dashboard(data, COLOR_VARIATIONS, years):
    """
    Genera un dashboard con gráficos de barras apiladas y gráficos de dona.

    Args:
        data (pd.DataFrame): DataFrame con los datos.
        COLOR_VARIATIONS (dict): Diccionario que asigna colores a las tecnologías.
        years (list): Lista de años para los gráficos de dona.

    Returns:
        plotly.graph_objects.Figure: Figura del dashboard.
    """
    if 'YEAR' in data.columns and not data['YEAR'].isnull().any():
        years_in_data = sorted(data['YEAR'].unique())
        xaxis_range = [min(years_in_data), max(years_in_data)]
    else:
        years_in_data = years  # Usar los años proporcionados si no hay datos válidos
        xaxis_range = [min(years), max(years)]
    

    dashboard = make_subplots(
    rows=2, cols=3,
    specs=[[{'type': 'xy', 'colspan': 3}, None, None],
           [{'type': 'domain'}, {'type': 'domain'}, {'type': 'domain'}]],
    vertical_spacing=0.15,
    column_widths=[0.33, 0.33, 0.33],
    row_heights=[0.6, 0.4]
)

    # Gráfico de barras apiladas
    technologies = []
    for tech in data['TECHNOLOGY'].unique():
        technologies.append(tech)
        tech_data = data[data['TECHNOLOGY'] == tech]
        bar_trace = go.Bar(
            x=tech_data['YEAR'],
            y=tech_data['value'],
            name=tech,  # Nombre de la tecnología
            marker=dict(color=COLOR_VARIATIONS[tech]),
            # legendgroup=tech,  # Vincular la leyenda por tecnología
            # legendgrouptitle=dict(text="Technologies"),
            showlegend=True  # Mostrar la leyenda solo en el gráfico de barras
        )
        dashboard.add_trace(bar_trace, row=1, col=1)
    dashboard.update_layout(
            barmode='stack',  # Apilar las barras
        )
    # dashboard['layout']['legend'] = dict(
    #     orientation="v",  # Leyenda vertical
    #     x=1.05,  # Posición a la derecha del gráfico
    #     y=1,  # Alineada en la parte superior
    #     xanchor="left",
    #     yanchor="top",
    #     font=dict(size=12)
    # )
    
    # Gráficos de dona para años específicos
    for i, year in enumerate(years):
        year_data = data[data['YEAR'] == year]
        pie_trace = go.Pie(
            labels=year_data['TECHNOLOGY'],
            values=year_data['value'],
            name=f"Year {year}",
            marker=dict(colors=[COLOR_VARIATIONS[tech] for tech in year_data['TECHNOLOGY']]),
            # legendgroup=year_data['TECHNOLOGY'],  # Vincular la leyenda por tecnología
            # legendgrouptitle=dict(text="Technologies"),  # Título del grupo en la leyenda
            # showlegend=True,  # Ocultar la leyenda en los gráficos de dona
            hole=0.5,
            textinfo='label+text+percent'
        )
        dashboard.add_trace(pie_trace, row=2, col=i + 1)
#     dashboard['layout']['legend2'] = dict(
#         orientation="h",  # Leyenda horizontal
#         x=0.5,  # Centrada debajo del gráfico
#         y=-0.2,  # Debajo del gráfico
#         xanchor="center",
#         yanchor="top",
#         font=dict(size=12)
# )


    # Configurar el diseño del dashboard
    dashboard.update_layout(
        height=800,
        width=1000,
        title={'text': 'Energy Production Dashboard', 'x': 0.5},
        font=dict(size=16, color='black'),
        showlegend = False,
        # annotations=annotations,
        plot_bgcolor='white',
        xaxis_title="Year",
        yaxis_title="Energy Production (GWh)"
    )


    return dashboard
# Función para crear el dashboard
def create_dash_app_1(files, COLOR_VARIATIONS, years):
    """
    Crea y configura la aplicación Dash.

    Args:
        files (dict): Diccionario con los nombres y rutas de los archivos.
        COLOR_VARIATIONS (dict): Diccionario que asigna colores a las tecnologías.
        years (list): Lista de años para los gráficos de dona.

    Returns:
        Dash: Aplicación Dash configurada.
    """
    app = Dash(__name__)

    # Layout de la aplicación
    app.layout = html.Div([
        html.H1("Energy Production/Consumption Dashboard", style={'textAlign': 'center'}),
        dcc.Dropdown(
            id='file-dropdown',
            options=[{'label': key, 'value': value} for key, value in files.items()],
            value=list(files.values())[0],  # Archivo seleccionado por defecto
            style={'width': '50%', 'margin': 'auto'}
        ),
        dcc.Checklist(
            id='technology-filter',
            options=[{'label': tech, 'value': tech} for tech in technologies],
            value=technologies,  # Seleccionar todas las tecnologías por defecto
            inline=True,
            style={'margin': '20px'}
        ),
        dcc.Graph(id='dashboard-graph')
        ])



    # Callback para actualizar el gráfico
    @app.callback(
        Output('dashboard-graph', 'figure'),
        [Input('file-dropdown', 'value'),
         Input('technology-filter', 'value')]
    )
    # def update_dashboard(selected_file, selected_technologies):
    #     # Filtrar los datos según las tecnologías seleccionadas
        
    #     data = load_data(selected_file)
    #     filtered_data = data[data['TECHNOLOGY'].isin(selected_technologies)]
    #     if data.empty:
    #         return {}
    #     return generate_dashboard(data, COLOR_VARIATIONS, years)
    def update_dashboard_1(selected_file, selected_technologies):
        # Cargar datos
        data = pd.read_csv(selected_file)
        data['value'] = data['value'] * 277.78 

        # Filtrar datos según las tecnologías seleccionadas
        filtered_data = data[data['TECHNOLOGY'].isin(selected_technologies)]
        

        # Crear el dashboard
        dashboard = make_subplots(
            rows=2, cols=3,
            specs=[[{'type': 'xy', 'colspan': 3}, None, None],
                   [{'type': 'domain'}, {'type': 'domain'}, {'type': 'domain'}]],
            vertical_spacing=0.15,
            column_widths=[0.33, 0.33, 0.33],
            row_heights=[0.6, 0.4]
        )

        # Gráfico de barras apiladas
        for tech in filtered_data['TECHNOLOGY'].unique():
            tech_data = filtered_data[filtered_data['TECHNOLOGY'] == tech]
            bar_trace = go.Bar(
                x=tech_data['YEAR'],
                y=tech_data['value'],
                name=tech,
                marker=dict(color=COLOR_VARIATIONS.get(tech, 'gray')),
                showlegend=True
            )
            dashboard.add_trace(bar_trace, row=1, col=1)
        dashboard.update_layout(
            barmode='stack',  # Apilar las barras
        )

        # Gráficos de dona para años específicos
        for i, year in enumerate(years):
            year_data = filtered_data[filtered_data['YEAR'] == year]
            pie_trace = go.Pie(
                labels=year_data['TECHNOLOGY'],
                values=year_data['value'],
                name=f"Year {year}",
                marker=dict(colors=[COLOR_VARIATIONS.get(tech, 'gray') for tech in year_data['TECHNOLOGY']]),
                showlegend=False,
                hole=0.5
            )
            dashboard.add_trace(pie_trace, row=2, col=i + 1)

        # Configurar el diseño del dashboard
        dashboard.update_layout(
            height=800,
            width=1000,
            title={'text': 'Energy Production Dashboard', 'x': 0.5},
            font=dict(size=16, color='black'),
            plot_bgcolor='white',
            xaxis_title="Year",
            yaxis_title="Energy Production (GWh)",
            legend=dict(
            font=dict(size=14),
            x=1, y=1,  # Posición de la leyenda (esquina superior derecha)
            bgcolor='rgba(255, 255, 255, 0.5)',  # Fondo semitransparente
            bordercolor='black',
            borderwidth=1
    ),
        )

        return dashboard
def create_dash_app(files, COLOR_VARIATIONS, years):
    """
    Crea y configura la aplicación Dash.

    Args:
        files (dict): Diccionario con los nombres y rutas de los archivos.
        COLOR_VARIATIONS (dict): Diccionario que asigna colores a las tecnologías.
        years (list): Lista de años para los gráficos de dona.

    Returns:
        Dash: Aplicación Dash configurada.
    """
    app = Dash(__name__)

    # Cargar datos iniciales
    data = pd.read_csv(list(files.values())[0])
    technologies = data['TECHNOLOGY'].unique()
    fuels = data['FUEL'].unique() if 'FUEL' in data.columns else []

    # Layout de la aplicación
    app.layout = html.Div([
        html.H1("Energy Production/Consumption Dashboard", style={'textAlign': 'center'}),
        dcc.Dropdown(
            id='file-dropdown',
            options=[{'label': key, 'value': value} for key, value in files.items()],
            value=list(files.values())[0],  # Archivo seleccionado por defecto
            style={'width': '50%', 'margin': 'auto'}
        ),
        dcc.RadioItems(
            id='grouping-filter',
            options=[
                {'label': 'Tecnologías', 'value': 'TECHNOLOGY'},
                {'label': 'Fuels', 'value': 'FUEL'}
            ],
            value='TECHNOLOGY',  # Valor por defecto
            inline=True,
            style={'margin': '20px'}
        ),
        dcc.Checklist(
            id='item-filter',
            options=[{'label': tech, 'value': tech} for tech in technologies],
            value=technologies,  # Seleccionar todas las tecnologías por defecto
            inline=True,
            style={'margin': '20px'}
        ),
        dcc.Graph(id='dashboard-graph')
    ])

    # Callback para actualizar el gráfico
    @app.callback(
        [Output('dashboard-graph', 'figure'),
        Output('item-filter', 'options'),
        Output('item-filter', 'value')],
        [Input('file-dropdown', 'value'),
        Input('grouping-filter', 'value'),
        Input('item-filter', 'value')]
    )
    def update_dashboard(selected_file, grouping, selected_items):
        # Cargar datos
        data = pd.read_csv(selected_file)
        data['value'] = data['value'] * 277.78
        data= data.sort_values(by='TECHNOLOGY')
        # data = data[~data['TECHNOLOGY'].str.contains('PWRDIST|PWRTRANS')]
        data = data[round(data['value']) != 0]


        # Actualizar las opciones del filtro según el agrupamiento
        if grouping == 'TECHNOLOGY':
            items = data['TECHNOLOGY'].unique()
        elif grouping == 'FUEL' and 'FUEL' in data.columns:
            items = data['FUEL'].unique()
        else:
            items = []

        # Si los valores seleccionados no están en las opciones actuales, resetearlos
        if not set(selected_items).issubset(set(items)):
            selected_items = list(items)  # Seleccionar todos los elementos por defecto

        # Filtrar datos según los elementos seleccionados
        filtered_data = data[data[grouping].isin(selected_items)]

        # Crear el dashboard
        dashboard = make_subplots(
            rows=2, cols=3,
            specs=[[{'type': 'xy', 'colspan': 3}, None, None],
                [{'type': 'domain'}, {'type': 'domain'}, {'type': 'domain'}]],
            vertical_spacing=0,
            column_widths=[0.33, 0.33, 0.33],
            row_heights=[0.6, 0.5]
        )

        # Gráfico de barras apiladas
        for item in filtered_data[grouping].unique():
            item_data = filtered_data[filtered_data[grouping] == item]
            bar_trace = go.Bar(
                x=item_data['YEAR'],
                y=item_data['value'],
                name=item,
                marker=dict(color=COLOR_VARIATIONS.get(item, 'gray')),
                showlegend=True,
                opacity=0.8
            )
            dashboard.add_trace(bar_trace, row=1, col=1)
        dashboard.update_layout(
            barmode='stack',  # Apilar las barras
        )
        donut_charts = []
        # Gráficos de dona para años específicos
        for i, year in enumerate(years):
            year_data = filtered_data[(filtered_data['YEAR'] == year)]
            pie_trace = go.Pie(
                labels=year_data[grouping],
                values=year_data['value'],
                name=f"Year {year}",
                marker=dict(colors=[COLOR_VARIATIONS.get(item, 'gray') for item in year_data[grouping]]),
                showlegend=False,
                hole=0.35,
                textinfo='percent+label',
                textposition='inside',
                opacity=0.8,
                text = ['2030']


            )
            dashboard.add_trace(pie_trace, row=2, col=i + 1)
            x_position = 0.145 + i * 0.355  # Ajustar dinámicamente según la columna
            y_position = 0.15  # Posición fija debajo de los gráficos de dona

            # Agregar anotación para el año debajo del gráfico


        # Configurar el diseño del dashboard
        dashboard.update_layout(
            height=1000,
            width=1000,
            title={'text': 'Energy Production/Consumption Dashboard', 'x': 0.5},
            font=dict(size=16, color='black'),
            plot_bgcolor='white',
            xaxis_title="Year",
            yaxis_title="Energy Production (GWh)",
            # annotations=annotations,
        )

        # Actualizar las opciones del filtro
        options = [{'label': item, 'value': item} for item in items]
        return dashboard, options, selected_items

    return app

def create_dash_app_new(files, COLOR_VARIATIONS, years):
    """
    Crea y configura la aplicación Dash.

    Args:
        files (dict): Diccionario con los nombres y rutas de los archivos.
        COLOR_VARIATIONS (dict): Diccionario que asigna colores a las tecnologías.
        years (list): Lista de años para los gráficos de dona.

    Returns:
        Dash: Aplicación Dash configurada.
    """
    app = Dash(__name__)

    # Layout de la aplicación
    app.layout = html.Div([
        html.H1("Energy Production/Consumption Dashboard", style={'textAlign': 'center'}),
        dcc.Dropdown(
            id='file-dropdown',
            options=[{'label': key, 'value': value} for key, value in files.items()],
            value=list(files.values())[0],  # Archivo seleccionado por defecto
            style={'width': '50%', 'margin': 'auto'}
        ),
        dcc.RadioItems(
            id='grouping-filter',
            options=[
                {'label': 'Tecnologías', 'value': 'TECHNOLOGY'},
                {'label': 'Fuels', 'value': 'FUEL'}
            ],
            value='TECHNOLOGY',  # Valor por defecto
            inline=True,
            style={'margin': '20px'}
        ),
        dcc.Checklist(
            id='item-filter',
            options=[],  # Opciones dinámicas basadas en los datos
            value=[],  # Valores seleccionados dinámicamente
            inline=True,
            style={'margin': '20px'}
        ),
        html.Div([
            dcc.Graph(id='bar-chart', style={'display': 'inline-block', 'width': '100%'}),
            html.Div(id='donut-charts', style={'display': 'flex', 'justifyContent': 'left','gap': '1px', 'margin': '1px'}),
        ])
    ])

    # Callback para actualizar los gráficos
    @app.callback(
        [Output('bar-chart', 'figure'),
         Output('donut-charts', 'children'),
         Output('item-filter', 'options'),
         Output('item-filter', 'value')],
        [Input('file-dropdown', 'value'),
         Input('grouping-filter', 'value'),
         Input('item-filter', 'value')]
    )
    def update_dashboard(selected_file, grouping, selected_items):
        # Cargar datos
        data = pd.read_csv(selected_file)
        data = data[data['value']> 0]  # Excluir valores 0.0
        data['value'] = data['value']*277.78

        # Actualizar las opciones del filtro según el agrupamiento
        if grouping == 'TECHNOLOGY':
            items = data['TECHNOLOGY'].unique()
        elif grouping == 'FUEL' and 'FUEL' in data.columns:
            items = data['FUEL'].unique()
        else:
            items = []

        # Si los valores seleccionados no están en las opciones actuales, resetearlos
        # if not set(selected_items).issubset(set(items)):
        #     selected_items = list(items)  # Seleccionar todos los elementos por defecto
        if not selected_items or not set(selected_items).issubset(set(items)):
            selected_items = list(items) 

        # Filtrar datos según los elementos seleccionados
        filtered_data = data[data[grouping].isin(selected_items)].sort_values(by='TECHNOLOGY')
        

        # Crear el gráfico de barras
        bar_fig = go.Figure()
        for item in filtered_data[grouping].unique():
            item_data = filtered_data[filtered_data[grouping] == item]
            bar_fig.add_trace(go.Bar(
                x=item_data['YEAR'],
                y=item_data['value'],
                name=item,
                marker=dict(color=COLOR_VARIATIONS.get(item, 'gray')),
                opacity=0.8
            ))
        bar_fig.update_layout(
            barmode='stack',
            # title="Energy Production by Year",
            title_x=0.5,
            xaxis_title="Year",
            yaxis_title="Energy Production (GWh)",
            plot_bgcolor='white',
            font=dict(size=16, color='black'),
            width=1100,
            height=800,
        )

        # Crear los gráficos de dona
        donut_charts = []
        for year in years:
            year_data = filtered_data[filtered_data['YEAR'] == year].sort_values(by='TECHNOLOGY')
            total = round(year_data['value'].sum(), 0)
            if year_data.empty:
                continue
            pie_fig = go.Figure(data=[go.Pie(
                labels=year_data[grouping],
                values=year_data['value'],
                marker=dict(colors=[COLOR_VARIATIONS.get(item, 'gray') for item in year_data[grouping]]),
                hole=0.5,
                showlegend=False,
                textinfo='percent+label',
                textposition='inside',
            )])
            pie_fig.update_layout(
                margin=dict(t=10, b=50, l=50, r=10),
                height=300,
                width=300,
                annotations=[
                    dict(
                        text=f'Total {year}<br>{total} GWh',
                        x=0.5, y=0.5,  # Centrado dentro del gráfico
                        font=dict(size=16, color='black'),
                        showarrow=False
                    )
                ]
            )
            donut_charts.append(html.Div([
                dcc.Graph(figure=pie_fig, style={'display': 'inline-block', 'width': '300px', 'height': '300px'}),  
                # html.P(f"Year: {year}", style={'textAlign': 'center', 'marginTop': '-20px'})
            ], style={'display': 'inline-block', 'margin': '1px'}))

        return bar_fig, donut_charts, [{'label': item, 'value': item} for item in items], selected_items

    return app

def create_comparison_dashboard(files, COLOR_VARIATIONS, years):
    """
    Crea un dashboard para comparar resultados entre dos escenarios.

    Args:
        files (dict): Diccionario con los nombres y rutas de los archivos.
        COLOR_VARIATIONS (dict): Diccionario que asigna colores a las tecnologías.
        years (list): Lista de años para los gráficos de dona.

    Returns:
        Dash: Aplicación Dash configurada.
    """
    app = Dash(__name__)
    def generate_colored_options(tech_list=None):
        if tech_list is None:
            tech_list = COLOR_VARIATIONS.keys()
        return [{
            'label': html.Div([
                html.Div(
                    style={
                        'width': '20px',
                        'height': '20px',
                        'background-color': COLOR_VARIATIONS.get(tech, '#cccccc'),
                        'border-radius': '2px',
                        'display': 'inline-block',
                        'margin-right': '8px',
                        'position': 'relative',
                        'top': '1px'
                    }
                ),
                tech
            ], style={'display': 'flex', 'align-items': 'center'}),
            'value': tech
        } for tech in tech_list]
    
    # Layout de la aplicación
    app.layout = html.Div([
    html.H1("Scenario Comparison Dashboard", style={'textAlign': 'center'}),
    html.Div([
        html.Label("Tecnologies to be shown:", style={'display': 'block', 'textAlign': 'center', 'margin-bottom': '5px', 'font-size': '25px'}),
        dcc.Checklist(
            id='technology-filter',
            options=generate_colored_options(),
            value=[],
            inline=False,
            style={
                'margin': '0',
                'padding': '0',
                'font-size': '20px'
            },
            labelStyle={ ##### estilo de la etiqueta
                'margin': '10px 0 0 0',
                'padding': '0',
                'display': 'inline-block',
                'gap': '0px',
            },
            inputStyle={    ##### caja de verificacion
                'margin': '0 10px 0 0',
                'height': '12px',
                'width': '12px'
            }
        )
    ], style={'width': '1500px', 'margin': '0 auto', 'padding': '20px', 'border': '1px solid #eee', 'border-radius': '10px', 'border': '1px solid #ccc', 'box-sizing': 'border-box'}),
    html.Div([
        html.Div([
            html.Label("Selecciona el primer escenario:", style={'display': 'block', 'textAlign': 'center', 'margin-bottom': ' 50 px'}),
            dcc.Dropdown(
                id='file-dropdown-1',
                options=[{'label': key, 'value': value} for key, value in files.items()],
                value=list(files.values())[0],  # Archivo seleccionado por defecto
                style={'width': '80%', 'margin': 'auto'}
            )
        ], style={'width': '48%', 'display': 'inline-block', 'vertical-align': 'top'}),
        html.Div([
            html.Label("Selecciona el segundo escenario:", style={'display': 'block', 'textAlign': 'center'}),
            dcc.Dropdown(
                id='file-dropdown-2',
                options=[{'label': key, 'value': value} for key, value in files.items()],
                value=list(files.values())[1],  # Segundo archivo seleccionado por defecto
                style={'width': '80%', 'margin': 'auto'}
            )
        ], style={'width': '48%', 'display': 'inline-block', 'vertical-align': 'top'})
    ]),
    html.Div([
        html.Div([
            dcc.Graph(id='bar-chart-1', style={'display': 'inline-block', 'width': '100%', 'margin': '0 5%'}),
            html.Div(id='donut-charts-1', style={'display': 'flex', 'justifyContent': 'left', 'gap': '10px', 'margin': '0 8%'})
        ], style={'width': '48%', 'display': 'inline-block', 'vertical-align': 'top'}),
        html.Div([
            dcc.Graph(id='bar-chart-2', style={'display': 'inline-block', 'width': '100%'}),
            html.Div(id='donut-charts-2', style={'display': 'flex', 'justifyContent': 'left', 'gap': '10px'})
        ], style={'width': '48%', 'display': 'inline-block', 'vertical-align': 'top'})
    ]),
])
    # Callback para actualizar los gráficos
    @app.callback(
        [Output('bar-chart-1', 'figure'),
        Output('donut-charts-1', 'children'),
        Output('bar-chart-2', 'figure'),
        Output('donut-charts-2', 'children'),
        Output('technology-filter', 'options'),
        Output('technology-filter', 'value')],
        [Input('file-dropdown-1', 'value'),
        Input('file-dropdown-2', 'value'),
        Input('technology-filter', 'value')],
        # prevent_initial_call=True
    )
    def update_comparison_graphs(file1, file2, selected_techs):
        
        data1 = pd.read_csv(file1)
        data1['value'] = data1['value']*277.78
        # print(data1)
        data1 = data1[data1['value'] > 0]  # Excluir valores 0.0
        techs1 = data1['TECHNOLOGY'].unique()

        # Cargar datos del segundo archivo
        data2 = pd.read_csv(file2)
        data2['value'] = data2['value']*277.78
        data2 = data2[data2['value'] > 0]  # Excluir valores 0.0
        techs2 = data2['TECHNOLOGY'].unique()



        # Opciones para el checklist
        all_techs = sorted(set(techs1).union(set(techs2)))
        options = generate_colored_options(all_techs)
        if not selected_techs:
            selected_techs = all_techs

        # Filtrar datos según las tecnologías seleccionadas
        data1 = data1[data1['TECHNOLOGY'].isin(selected_techs)].sort_values(by='TECHNOLOGY')
        data2 = data2[data2['TECHNOLOGY'].isin(selected_techs)].sort_values(by='TECHNOLOGY')
        
        
        # Crear el gráfico de barras para el primer archivo
        bar_fig1 = go.Figure()
        for tech in data1['TECHNOLOGY'].unique():
            tech_data = data1[data1['TECHNOLOGY'] == tech]
            bar_fig1.add_trace(go.Bar(
                x=tech_data['YEAR'],
                y=tech_data['value'],
                name=tech,
                marker=dict(color=COLOR_VARIATIONS.get(tech, 'gray')),
                opacity=0.8
            ))
        bar_fig1.update_layout(
            barmode='stack',
            title="Escenario 1: Producción de Energía",
            xaxis_title="Year",
            yaxis_title="Energy Production (GWh)",
            plot_bgcolor='white',
            font=dict(size=16, color='black'),
            width=1000,
            height=700,
            showlegend = False,
            
        )

        # Crear gráficos de dona para el primer archivo
        donut_charts1 = []
        for year in years:
            year_data = data1[data1['YEAR'] == year]
            total = round(year_data['value'].sum(), 0)
            if year_data.empty:
                continue
            pie_fig = go.Figure(data=[go.Pie(
                labels=year_data['TECHNOLOGY'],
                values=year_data['value'],
                marker=dict(colors=[COLOR_VARIATIONS.get(tech, 'gray') for tech in year_data['TECHNOLOGY']]),
                hole=0.5,
                showlegend=False,
                textinfo='percent+label',
                textposition='inside',
            )])
            pie_fig.update_layout(
                margin=dict(t=10, b=10, l=10, r=10),
                height=300,
                width=300,
                annotations=[
                    dict(
                        text=f'Total {year}<br>{total} GWh',
                        x=0.5, y=0.5,
                        font=dict(size=16, color='black'),
                        showarrow=False
                    )
                ]
            )
            donut_charts1.append(dcc.Graph(figure=pie_fig, style={'display': 'inline-block', 'width': '300px', 'height': '300px'}))

        # Repetir para el segundo archivo
        data2 = pd.read_csv(file2)
        data2 = data2[data2['value'] > 0]
        techs2 = data2['TECHNOLOGY'].unique()

        if selected_techs:
            data2 = data2[data2['TECHNOLOGY'].isin(selected_techs)].sort_values(by='TECHNOLOGY')

        bar_fig2 = go.Figure()
        for tech in data2['TECHNOLOGY'].unique():
            tech_data = data2[data2['TECHNOLOGY'] == tech]
            bar_fig2.add_trace(go.Bar(
                x=tech_data['YEAR'],
                y=tech_data['value'],
                name=tech,
                marker=dict(color=COLOR_VARIATIONS.get(tech, 'gray')),
                opacity=0.8
            ))
        bar_fig2.update_layout(
            barmode='stack',
            title="Escenario 2: Producción de Energía",
            xaxis_title="Year",
            yaxis_title="Energy Production (GWh)",
            plot_bgcolor='white',
            font=dict(size=16, color='black'),
            width=1000,
            height=700,
            showlegend = False

        )

        donut_charts2 = []
        for year in years:
            year_data = data2[data2['YEAR'] == year].sort_values(by='TECHNOLOGY')
            total = round(year_data['value'].sum(), 0)
            if year_data.empty:
                continue
            pie_fig = go.Figure(data=[go.Pie(
                labels=year_data['TECHNOLOGY'],
                values=year_data['value'],
                marker=dict(colors=[COLOR_VARIATIONS.get(tech, 'gray') for tech in year_data['TECHNOLOGY']]),
                hole=0.5,
                showlegend=False,
                textinfo='percent+label',
                textposition='inside',
            )])
            pie_fig.update_layout(
                margin=dict(t=10, b=10, l=10, r=10),
                height=300,
                width=300,
                annotations=[
                    dict(
                        text=f'Total {year}<br>{total} GWh',
                        x=0.5, y=0.5,
                        font=dict(size=16, color='black'),
                        showarrow=False
                    )
                ]
            )
            donut_charts2.append(dcc.Graph(figure=pie_fig, style={'display': 'inline-block', 'width': '300px', 'height': '300px'}))

        return  bar_fig1, donut_charts1, bar_fig2, donut_charts2, generate_colored_options(all_techs), selected_techs

    return app

def create_simple_dash_app(data, COLOR_VARIATIONS):
    """
    Crea una aplicación Dash simple con un gráfico de barras y un checkbox para tecnologías.

    Args:
        data (pd.DataFrame): DataFrame con los datos.
        COLOR_VARIATIONS (dict): Diccionario que asigna colores a las tecnologías.

    Returns:
        Dash: Aplicación Dash configurada.
    """
    app = Dash(__name__)

    # Obtener las tecnologías únicas
    technologies = data['TECHNOLOGY'].unique()

    # Layout de la aplicación
    app.layout = html.Div([
        html.H1("Energy Production Dashboard", style={'textAlign': 'center'}),
        html.Div([
            html.Label("Selecciona tecnologías para mostrar:", style={'display': 'block', 'textAlign': 'center'}),
            html.Div(
                id='technology-checkboxes',
                children=[
                    html.Div(
                        children=[
                            dcc.Checklist(
                                id={'type': 'tech-checkbox', 'index': tech},
                                options=[{'label': '', 'value': tech}],
                                value=[tech],
                                style={
                                    'position': 'relative',
                                    'width': '30px',
                                    'height': '30px',
                                    'cursor': 'pointer'
                                }
                            ),
                            html.Div(style={
                                'width': '30px',
                                'height': '30px',
                                'backgroundColor': COLOR_VARIATIONS.get(tech, 'gray'),
                                'margin': '0 px',
                                'marginTop': '0px'
                            }),
                            html.Span(tech, style={'fontSize': '14px', 'textAlign': 'left', 'marginTop': '5px'})
                        ],
                        style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center', 'margin': '10px'}
                    ) for tech in technologies
                ],
                style={'display': 'flex', 'justifyContent': 'center', 'flexWrap': 'wrap'}
            )
        ]),
        dcc.Graph(id='bar-chart', style={'width': '80%', 'margin': 'auto'})
    ])

    # Callback para actualizar el gráfico
    @app.callback(
        Output('bar-chart', 'figure'),
        [Input({'type': 'tech-checkbox', 'index': tech}, 'value') for tech in technologies]
    )
    def update_bar_chart(*selected_techs):
        # Obtener las tecnologías seleccionadas
        selected_techs = [tech for tech, selected in zip(technologies, selected_techs) if selected]

        # Filtrar los datos según las tecnologías seleccionadas
        filtered_data = data[data['TECHNOLOGY'].isin(selected_techs)].sort_values(by='TECHNOLOGY')

        # Crear el gráfico de barras
        bar_fig = go.Figure()
        for tech in filtered_data['TECHNOLOGY'].unique():
            tech_data = filtered_data[filtered_data['TECHNOLOGY'] == tech]
            bar_fig.add_trace(go.Bar(
                x=tech_data['YEAR'],
                y=tech_data['value'],
                name=tech,
                marker=dict(color=COLOR_VARIATIONS.get(tech, 'gray')),
                opacity=0.8
            ))
        bar_fig.update_layout(
            barmode='stack',
            title="Energy Production by Year",
            xaxis_title="Year",
            yaxis_title="Energy Production (GWh)",
            plot_bgcolor='white',
            font=dict(size=16, color='black'),
            width=1100,
            height=800, showlegend=False
        )
        return bar_fig

    return app

def run_app_1(files):
    app = create_dash_app_new(files, COLOR_VARIATIONS, years)
    webbrowser.open("http://127.0.0.1:8053/")
    app.run(debug=False, port=8053) #### el debug lo uso solo para el desarrollo, no para la produccion

def run_app_2(files):
    app1 = create_comparison_dashboard(files, COLOR_VARIATIONS, years)
    webbrowser.open("http://127.0.0.1:8052/")
    app1.run(debug=False, port=8052)


# if __name__ == '__main__':
#     # Define file paths
#     production_file = os.path.join(RESULTS_FOLDER, 'v_ProductionByTechnologyAnnual.csv')
#     rate_file = os.path.join(RESULTS_FOLDER, 'v_RateOfProductionByTechnology.csv')

#     # Plot activity
#     plot_activity(production_file)

#     # Create production plot
#     production_data = load_and_prepare_data(rate_file)
#     if not production_data.empty:
#         fig = create_production_plot(production_data, COLOR_VARIATIONS)
#         fig.show()
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from dash import Dash
from flask import Flask
server = Flask(__name__)
if __name__ == '__main__':
    # Definir las rutas de los archivos de resultados
    root_folder = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    print(f"Root folder: {root_folder}")
    input_files = [
        os.path.join(root_folder, 'data/SuperSimple.xlsx'),
        os.path.join(root_folder, 'data/OsemosysNewDatosFreeBiomass1000MWUp37.xlsx'),
        os.path.join(root_folder, 'data/OsemosysNewDatosFreeBiomass1000MW.xlsx'),
        # os.path.join(root_folder, 'data/OsemosysNewDatosFreeBiomass1000MWUp37.xlsx'),
    ]

    results_folders={}
    for input_file in input_files:
        paths = configure_paths(input_file, root_folder)
        results_folders[input_file] = paths['RESULTS_FOLDER']
        print(f"Archivo: {paths['INPUT_FILE_PATH']}")
        print(f"Carpeta de resultados: {paths['RESULTS_FOLDER']}")
    files1 = {
        "Production by Technology Annual": os.path.join(results_folders[input_files[2]], "ProductionByTechnologyAnnual.csv"),
        "Use by Technology Annual": os.path.join(results_folders[input_files[2]], "UseByTechnologyAnnual.csv")
    }
    # print(files)
    production_file = files1["Production by Technology Annual"]
    try:
        data = pd.read_csv(production_file)
        print("Datos cargados correctamente:")
        print(data.head())
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo en {production_file}")
        exit() 
    # print(f"Production file: {production_file}")
    # data = pd.read_csv(production_file)
    technologies = data['TECHNOLOGY'].unique()
    # print(f"Technologies: {technologies}")
    fuels = data['FUEL'].unique() if 'FUEL' in data.columns else []
    items = list(technologies) + list(fuels)
    COLOR_VARIATIONS = assign_colors(items, COLOR_VARIATIONS)
    years = [2020, 2030, 2050]
    file4444 = pd.read_csv( '/home/david/OSeMOSYS-pyomo/results/OsemosysNewDatosFreeBiomass1000MWUp37NG/ProductionByTechnologyAnnual.csv')

    # app = create_dash_app(files, COLOR_VARIATIONS, years)
    app = create_simple_dash_app(file4444, COLOR_VARIATIONS)
    # app.run(debug=True, port=8053)


    files = {
    "BaseScenario": "/home/david/OSeMOSYS-pyomo/results/BaseScenario/ProductionByTechnologyAnnual.csv",
    "BaseScenarioWind": "/home/david/OSeMOSYS-pyomo/results/BaseScenarioWind/ProductionByTechnologyAnnual.csv",
    "BaseScenarioWindBiomass": "/home/david/OSeMOSYS-pyomo/results/BaseScenarioWindBiomass/ProductionByTechnologyAnnual.csv",
    "BaseScenarioAnualCapLim": "/home/david/OSeMOSYS-pyomo/results/BaseScenarioAnualCapLim/ProductionByTechnologyAnnual.csv",
    "RecapitalizarUnidades": "/home/david/OSeMOSYS-pyomo/results/RecapitalizarUnidades/ProductionByTechnologyAnnual.csv",
    "RecapitalizarUnidades600": "/home/david/OSeMOSYS-pyomo/results/RecapitalizarUnidades600/ProductionByTechnologyAnnual.csv",
    "RecapitalizarUnidades700": "/home/david/OSeMOSYS-pyomo/results/RecapitalizarUnidades700/ProductionByTechnologyAnnual.csv",
    "RecapitalizarUnidades800": "/home/david/OSeMOSYS-pyomo/results/RecapitalizarUnidades800/ProductionByTechnologyAnnual.csv",


    "RecapMustRun": "/home/david/OSeMOSYS-pyomo/results/RecapMustRun/ProductionByTechnologyAnnual.csv",

}
    BASE_FOLDER = "/home/david/OSeMOSYS-pyomo/results"
    dependency_files = {
    file: os.path.join(BASE_FOLDER, f"{file}.csv")
    for file in DEPENDENCIES_VAR_DICT["['REGION','TECHNOLOGY','YEAR']"]
    if os.path.exists(os.path.join(BASE_FOLDER, f"{file}.csv"))
}
    


    region_tech_year_files = DEPENDENCIES_VAR_DICT["['REGION','TECHNOLOGY','YEAR']"]




    # app.run(debug=True)
#     from threading import Thread
#     app1 = create_dash_app_new(files1, COLOR_VARIATIONS, years)
#     app2 = create_comparison_dashboard(files, COLOR_VARIATIONS, years)
#     app2.run(debug=True, port=8052)
#     server.wsgi_app = DispatcherMiddleware(
#     server,
#     {
#         '/app1': app1.server,
#         '/app2': app2.server
#     }
# )
#     server.run(debug=True, port=8050)
    # run_app_1(files1)
    # run_app_2(files)
    from threading import Thread
    t1 = Thread(target=run_app_1, args=(files1,))
    t2 = Thread(target=run_app_2, args=(files,))

    t1.start()
    t2.start()

    t1.join()
    t2.join()
