import plotly.graph_objects as go
import plotly.express as px
from itertools import cycle
from OSeMOSYS.utils import assign_colors_to_technologies
from dash import Dash, dcc, html, Input, Output, State, callback, ctx
import pandas as pd



def create_line_chart(data, title, x_column, y_column, color_column, COLOR_VARIATIONS):
    """
    Crea un gráfico de líneas a partir de un DataFrame.
    """
    fig = go.Figure()

    # Asignar colores a las tecnologías
    technology_colors = assign_colors_to_technologies(data, color_column, COLOR_VARIATIONS)

    # Crear una línea para cada categoría en la columna de color
    for category in data[color_column].unique():
        category_data = data[data[color_column] == category]
        fig.add_trace(go.Scatter(
            x=category_data[x_column],
            y=category_data[y_column],
            mode='lines+markers',
            name=category,
            line=dict(color=technology_colors[category])
        ))

    # Configurar el diseño del gráfico
    fig.update_layout(
        title=title,
        xaxis_title=x_column,
        yaxis_title=y_column,
        plot_bgcolor='white',
        font=dict(size=14),
        legend=dict(font=dict(size=12)),
        margin=dict(t=50, b=50, l=50, r=50)
    )

    return fig

def create_stacked_bar_chart(data, title, COLOR_VARIATIONS):
    """
    Crea un gráfico de barras apiladas.
    """
    # Asignar colores a las tecnologías
    all_technologies = data['TECHNOLOGY'].unique()
    technology_colors = assign_colors_to_technologies(pd.DataFrame({'TECHNOLOGY': all_technologies}), 'TECHNOLOGY', COLOR_VARIATIONS)

    # Crear el gráfico de barras apiladas
    fig = px.bar(
        data,
        x='YEAR',
        y='value',
        color='TECHNOLOGY',
        barmode='stack',
        title=title,
        color_discrete_map=technology_colors
    )

    # Configurar el diseño del gráfico
    fig.update_layout(
        xaxis_title="Año",
        yaxis_title="Producción de Energía (GWh)",
        plot_bgcolor='white',
        font=dict(size=14),
        legend=dict(font=dict(size=12)),
        margin=dict(t=50, b=50, l=50, r=50), 
        height=700,
        width=1100,
    )

    return fig


# def create_donut_charts(data, years, COLOR_VARIATIONS):
#     """
#     Crea gráficos de dona para los años seleccionados.

#     Args:
#         data (pd.DataFrame): DataFrame con los datos.
#         years (list): Lista de años para los gráficos de dona.
#         COLOR_VARIATIONS (dict): Diccionario que asigna colores a las tecnologías.

#     Returns:
#         list: Lista de gráficos de dona.
#     """
#     donut_charts = []
#     for year in years:
#         year_data = data[data['YEAR'] == year]
#         technology_colors = assign_colors_to_technologies(year_data, 'TECHNOLOGY', COLOR_VARIATIONS)
#         # total = round(year_data['value'].sum(), 0)
#         if year_data.empty:
#             continue
#         pie_fig = go.Figure(data=[go.Pie(
#             labels=year_data['TECHNOLOGY'],
#             values=year_data['value'],
#             marker=dict(colors=[technology_colors[tech] for tech in year_data['TECHNOLOGY']]),
#             hole=0.5,
#             showlegend=False,
#             textinfo='percent+label',
#             textposition='inside',
#         )])
#         pie_fig.update_layout(
#             margin=dict(t=10, b=10, l=10, r=10),
#             height=300,
#             width=300,
#             annotations=[
#                 dict(
#                     text=f'Total {year}<br>{total} GWh',
#                     x=0.5, y=0.5,
#                     font=dict(size=16, color='black'),
#                     showarrow=False
#                 )
#             ]
#         )
#         donut_charts.append(pie_fig)
#         # donut_charts.append(dcc.Graph(figure=pie_fig, style={'display': 'inline-block', 'width': '300px', 'height': '300px'}))
#     return donut_charts

def create_donut_charts(data, years, COLOR_VARIATIONS, selected_technologies=None, unit="PJ"):
    """
    Crea gráficos de dona para los años seleccionados.

    Args:
        data (pd.DataFrame): DataFrame con los datos.
        years (list): Lista de años para los gráficos de dona.
        COLOR_VARIATIONS (dict): Diccionario que asigna colores a las tecnologías.
        selected_technologies (list): Lista de tecnologías seleccionadas.
        unit (str): Unidad seleccionada (por defecto "PJ").

    Returns:
        list: Lista de gráficos de dona.
    """
    donut_charts = []
    for year in years:
        # Filtrar datos por año
        year_data = data[data['YEAR'] == year]

        # Filtrar por tecnologías seleccionadas si se proporcionan
        if selected_technologies:
            year_data = year_data[year_data['TECHNOLOGY'].isin(selected_technologies)]

        # Calcular el total solo para las tecnologías seleccionadas en el año correspondiente
        total = round(year_data['value'].sum(), 2)
        print(f"Año: {year}, Total calculado: {total}")  # Depuración

        if year_data.empty:
            print(f"Año: {year}, Sin datos después del filtrado.")  # Depuración
            continue

        # Asignar colores a las tecnologías
        technology_colors = assign_colors_to_technologies(year_data, 'TECHNOLOGY', COLOR_VARIATIONS)

        # Crear el gráfico de dona
        pie_fig = go.Figure(data=[go.Pie(
            labels=year_data['TECHNOLOGY'],
            values=year_data['value'],
            marker=dict(colors=[technology_colors[tech] for tech in year_data['TECHNOLOGY']]),
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
                    text=f'Total {year}<br>{total} {unit}',  # Corregir redundancia
                    x=0.5,
                    y=0.5,
                    font=dict(size=16, color='black'),
                    showarrow=False
                )
            ]
        )
        print(f"Año: {year}, Anotación generada: Total {year}<br>{total} {unit}")  # Depuración
        donut_charts.append(pie_fig)
    return donut_charts

def create_heatmap(data, selected_technologies, title, show_colorbar=True):
    """
    Crea un heatmap a partir de un DataFrame.

    Args:
        data (pd.DataFrame): DataFrame con los datos.
        selected_technologies (list): Lista de tecnologías seleccionadas.
        title (str): Título del heatmap.

    Returns:
        go.Figure: Gráfico de heatmap.
    """
    # Filtrar las tecnologías seleccionadas
    if selected_technologies:
        data = data[data['TECHNOLOGY'].isin(selected_technologies)]

    # Agrupar por tecnología y escenario, y sumar los valores
    grouped_data = data.groupby(['TECHNOLOGY', 'SCENARIO'])['value'].sum().reset_index()

    # Pivotar los datos para crear la matriz del heatmap
    heatmap_data = grouped_data.pivot(index='TECHNOLOGY', columns='SCENARIO', values='value').fillna(0)

    # Crear el heatmap
    fig = px.imshow(
        heatmap_data,
        labels=dict(x="Escenarios", y="Tecnologías", color="Valor"),
        x=heatmap_data.columns,
        y=heatmap_data.index,
        color_continuous_scale="Viridis",
        title=title
    )
    if not show_colorbar:
        fig.update_coloraxes(showscale=False)
    fig.update_layout(
        xaxis=dict(
            tickangle=45,  # Rotar etiquetas del eje X
            scaleanchor="y",  # Vincular la escala del eje X con el eje Y
            scaleratio=3  # Hacer que las celdas sean más anchas que altas
        ),
        yaxis=dict(
            automargin=True,  # Ajustar automáticamente los márgenes del eje Y
            scaleanchor="x",  # Vincular la escala del eje X con el eje Y
            scaleratio=10
        ),
        margin=dict(t=50, b=100, l=0, r=50),  # Ajustar márgenes
        height=800,  # Altura del gráfico
        width=800,  # Ancho del gráfico
    )
    return fig

import plotly.express as px

def create_line_chart_app4(data, x_column, y_column, color_column, title, width=800, height=500):
    """
    Crea un gráfico de línea con estilo profesional.

    Args:
        data (pd.DataFrame): DataFrame con los datos.
        x_column (str): Columna para el eje X.
        y_column (str): Columna para el eje Y.
        color_column (str): Columna para agrupar por color.
        title (str): Título del gráfico.
        width (int): Ancho del gráfico.
        height (int): Altura del gráfico.

    Returns:
        go.Figure: Gráfico de línea.
    """
    fig = px.line(
        data,
        x=x_column,
        y=y_column,
        color=color_column,
        title=title,
        markers=True
    )

    # Personalizar el diseño
    fig.update_traces(line=dict(width=3), marker=dict(size=8))  # Líneas más gruesas y marcadores más grandes
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=20, family="Arial, sans-serif"),
            x=0.5,  # Centrar el título
            xanchor="center"
        ),
        xaxis=dict(
            title=x_column,
            title_font=dict(size=16, family="Arial, sans-serif"),
            tickfont=dict(size=14, family="Arial, sans-serif"),
            showgrid=True,  # Mostrar líneas de la cuadrícula
            gridcolor="lightgrey"
        ),
        yaxis=dict(
            title=y_column,
            title_font=dict(size=16, family="Arial, sans-serif"),
            tickfont=dict(size=14, family="Arial, sans-serif"),
            showgrid=True,
            gridcolor="lightgrey"
        ),
        legend=dict(
            title=dict(text=color_column, font=dict(size=14, family="Arial, sans-serif")),
            font=dict(size=12, family="Arial, sans-serif"),
            orientation="h",  # Leyenda horizontal
            x=0.5,
            xanchor="center",
            y=-0.2  # Colocar la leyenda debajo del gráfico
        ),
        plot_bgcolor="white",  # Fondo blanco
        margin=dict(t=60, b=80, l=60, r=40),  # Márgenes ajustados
        width=width,
        height=height
    )
    return fig


def create_combined_line_chart(data, x_column, y_column, color_column, line_group_column, title, width=1500, height=600):
    """
    Crea un gráfico de línea combinado con estilo profesional.

    Args:
        data (pd.DataFrame): DataFrame con los datos.
        x_column (str): Columna para el eje X.
        y_column (str): Columna para el eje Y.
        color_column (str): Columna para agrupar por color.
        line_group_column (str): Columna para agrupar las líneas.
        title (str): Título del gráfico.
        width (int): Ancho del gráfico.
        height (int): Altura del gráfico.

    Returns:
        go.Figure: Gráfico de línea combinado.
    """
    fig = px.line(
        data,
        x=x_column,
        y=y_column,
        color=color_column,
        line_group=line_group_column,
        title=title,
        markers=True,
        color_discrete_sequence=px.colors.qualitative.Set2
    )

    # Personalizar el diseño
    fig.update_traces(line=dict(width=3), marker=dict(size=8))
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=20, family="Arial, sans-serif"),
            x=0.5,
            xanchor="center"
        ),
        xaxis=dict(
            title=x_column,
            title_font=dict(size=16, family="Arial, sans-serif"),
            tickfont=dict(size=16, family="Arial, sans-serif"),
            showgrid=True,
            # gridcolor="lightgrey"
        ),
        yaxis=dict(
            title=y_column,
            title_font=dict(size=16, family="Arial, sans-serif"),
            tickfont=dict(size=16, family="Arial, sans-serif"),
            showgrid=True,
            # gridcolor="lightgrey"
        ),
        legend=dict(
            title=dict(text=color_column, font=dict(size=14, family="Arial, sans-serif")),
            font=dict(size=14, family="Arial, sans-serif"),
            orientation="h",
            x=0.5,
            xanchor="center",
            y=-0.2
        ),
        plot_bgcolor="white",
        margin=dict(t=60, b=80, l=60, r=40),
        width=width,
        height=height,
        template= "presentation",  # Cambia el tema a "presentation"
    )
    return fig

def create_bar_chart(data, x_column, y_column, color_column, title, width=600, height=600):
    """
    Crea un gráfico de barras con estilo profesional.

    Args:
        data (pd.DataFrame): DataFrame con los datos.
        x_column (str): Columna para el eje X.
        y_column (str): Columna para el eje Y.
        color_column (str): Columna para agrupar por color.
        title (str): Título del gráfico.
        width (int): Ancho del gráfico.
        height (int): Altura del gráfico.

    Returns:
        go.Figure: Gráfico de barras.
    """
    fig = px.bar(
        data,
        x=x_column,
        y=y_column,
        color=color_column,
        title=title,
        color_discrete_sequence=px.colors.qualitative.Set2  # Usar la misma paleta de colores
    )

    # Personalizar el diseño
    # fig.update_traces(marker=dict(line=dict(width=1, color='black')))  # Bordes negros en las barras
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=20, family="Arial, sans-serif"),
            x=0.5,
            xanchor="center"
        ),
        xaxis=dict(
            title=x_column,
            title_font=dict(size=16, family="Arial, sans-serif"),
            tickfont=dict(size=16, family="Arial, sans-serif"),
            showgrid=True,
            gridcolor="lightgrey"
        ),
        yaxis=dict(
            title=y_column,
            title_font=dict(size=16, family="Arial, sans-serif"),
            tickfont=dict(size=16, family="Arial, sans-serif"),
            showgrid=True,
            gridcolor="lightgrey"
        ),
        legend=dict(
            title=dict(text=color_column, font=dict(size=14, family="Arial, sans-serif")),
            font=dict(size=14, family="Arial, sans-serif"),
            orientation="h",
            x=0.5,
            xanchor="center",
            y=-0.3
        ),
        showlegend=False,
        plot_bgcolor="white",
        margin=dict(t=60, b=150, l=60, r=40),
        width=width,
        height=height,
        template="presentation"  # Usar el mismo tema
    )
    return fig