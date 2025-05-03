# import pandas as pd
# import plotly.express as px
# from plotly.subplots import make_subplots
# color_dict = {
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

# def plot_activity(datafile, color_dict=color_dict):
#     data = pd.read_csv(datafile)
   


#     # data['TIMESLICE'] = data['TIMESLICE'].astype(str)
#     # Create a stacked bar chart using Plotly
#     data['value']= data['value']*277.78
#     data= data[data['TECHNOLOGY'].str.contains('PWR')].sort_values(by='TECHNOLOGY')
#     data = data[~data['TECHNOLOGY'].str.contains('PWRDIST|PWRTRANS')]
#     data = data[round(data['value'],4) != 0]

#     fig = px.bar(data, x="YEAR", y = "value", color="TECHNOLOGY",
#                 color_discrete_map = color_dict,
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
#     fig1 = px.pie(data[data['YEAR']==2019], names='TECHNOLOGY', values='value', hole=0.5, title='Gráfico de Dona 1',color = 'TECHNOLOGY',color_discrete_map = color_dict,
#     opacity=0.7, category_orders={'TECHNOLOGY': data['TECHNOLOGY'].tolist()})
#     fig2 = px.pie(data[data['YEAR']==2030], names='TECHNOLOGY', values='value', hole=0.5, title='Gráfico de Dona 1',color = 'TECHNOLOGY',color_discrete_map = color_dict,
#     opacity=0.7, category_orders={'TECHNOLOGY': data['TECHNOLOGY'].tolist()} )
#     fig3 = px.pie(data[data['YEAR']==2050], names='TECHNOLOGY', values='value', hole=0.5, title='Gráfico de Dona 2',color = 'TECHNOLOGY',color_discrete_map = color_dict,
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

# def create_production_plot(df, color_dict):
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
#         color_discrete_map=color_dict,
#         title='Power Generation by Technology Across Time Slices (Animated by Year)'
#     )
#     return fig


# if __name__ == '__main__':


#     datafile = '../../results/v_ProductionByTechnologyAnnual.csv'
#     plot_activity(datafile)
    
#     data_path = '../../results/v_RateOfProductionByTechnology.csv'
#     production_data = load_and_prepare_data(data_path)
    
 
#     fig = create_production_plot(production_data, color_dict)
#     fig.show()


import os
import sys
import random
root_folder = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
from OSeMOSYS.config import INPUT_FILE_PATH, RESULTS_FOLDER, COLOR_DICT, keyword_colors
# ROOT_FOLDER = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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

# Paletas personalizadas para cada keyword
COLOR_VARIATIONS = {
    # Keyword: [variaciones en orden]
    'crud': ['#2F4F4F','#696969','gray', 'dimgray', 'darkgray', 'silver', 'lightgray', 'gainsboro', 'whitesmoke','black' ],
    'hfo': ['#8B0000', '#6A0000', '#A80000', '#C50000', '#D30000'],
    'ng': ['orange', 'darkorange', '#FF8C00', '#FFA500', '#FFB732'],
    'bio': ['#9ACD32', '#8BB92D', '#7BA428', '#A8D645', '#B6E052'],
    'wnd': ['deepskyblue', '#00BFFF', '#0099CC', '#007399', '#005266'],
    'pv': ['#FFD700', '#CCAC00', '#B38F00', '#FFE55C', '#FFF380'],
    'hydro': ['#0d5c91', '#1f77b4', '#1560BD', '#2E8BFF', '#4AA6FF'],
    'diesel': ['brown', '#8B4513', '#A0522D', '#CD853F', '#DEB887'],
    'csp': ['gray', 'dimgray', 'darkgray']
}

def assign_colors(technologies, keyword_colors):
    """Asigna colores usando paletas predefinidas en orden secuencial."""
    groups = {}
    color_map = {}
    
    # 1. Agrupar tecnologías por keyword
    for tech in technologies:
        tech_lower = tech.lower()
        matched = False
        
        # Buscar coincidencia más específica primero
        for keyword in sorted(keyword_colors.keys(), key=lambda x: (-len(x), x)):
            if keyword in tech_lower:
                groups.setdefault(keyword, []).append(tech)
                matched = True
                break
                
        if not matched:
            groups.setdefault('unmatched', []).append(tech)
    
    # 2. Asignar colores según las paletas
    for keyword, techs in groups.items():
        if keyword == 'unmatched':
            # Paleta especial para no coincidentes (no usada en keywords)
            unused_colors = [c for c in px.colors.qualitative.Plotly 
                            if not any(c in pal for pal in COLOR_VARIATIONS.values())]
            color_cycle = cycle(unused_colors)
            for tech in techs:
                color_map[tech] = next(color_cycle)
        else:
            base_color = keyword_colors[keyword]
            variations = COLOR_VARIATIONS.get(keyword, [base_color])
            color_cycle = cycle(variations)
            
            for tech in techs:
                color_map[tech] = next(color_cycle)
    
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

def plot_activity(datafile, color_dict=COLOR_DICT):
    """
    Create and display energy production plots.

    Args:
        datafile (str): Path to the CSV file containing production data.
        color_dict (dict): Dictionary mapping technologies to colors.
    """
    try:
        data = pd.read_csv(datafile)
        data['value'] = data['value'] * 277.78
        data = data[data['TECHNOLOGY'].str.contains('PWR')].sort_values(by='TECHNOLOGY')
        data = data[~data['TECHNOLOGY'].str.contains('PWRDIST|PWRTRANS')]
        data = data[round(data['value'], 4) != 0]

        # Stacked bar chart
        fig = px.bar(
            data, x="YEAR", y="value", color="TECHNOLOGY",
            color_discrete_map=color_dict, opacity=0.7
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
        years = [2019, 2030, 2050]
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
                color='TECHNOLOGY', color_discrete_map=color_dict, opacity=0.7
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

def create_production_plot(df, color_dict):
    """
    Create an animated bar chart for energy production.

    Args:
        df (pd.DataFrame): DataFrame containing production data.
        color_dict (dict): Dictionary mapping technologies to colors.

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
        color_discrete_map=color_dict,
        title='Power Generation by Technology Across Time Slices (Animated by Year)'
    )
    fig.show()
def plot_accumulated_capacity(results_folder, selected_years=[2020, 2030, 2040, 2050], color_dict = COLOR_DICT):
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
            color_discrete_map=color_dict
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


# if __name__ == '__main__':
#     # Define file paths
#     production_file = os.path.join(RESULTS_FOLDER, 'v_ProductionByTechnologyAnnual.csv')
#     rate_file = os.path.join(RESULTS_FOLDER, 'v_RateOfProductionByTechnology.csv')

#     # Plot activity
#     plot_activity(production_file)

#     # Create production plot
#     production_data = load_and_prepare_data(rate_file)
#     if not production_data.empty:
#         fig = create_production_plot(production_data, COLOR_DICT)
#         fig.show()
if __name__ == '__main__':
    # Definir las rutas de los archivos de resultados
    production_file = os.path.join(RESULTS_FOLDER, 'v_ProductionByTechnologyAnnual.csv')
    rate_file = os.path.join(RESULTS_FOLDER, 'v_RateOfProductionByTechnology.csv')


    production_data = load_and_prepare_data(rate_file)
    data = pd.read_csv(production_file)
    technologies = data['TECHNOLOGY'].unique()
    color_dict = assign_colors(technologies, keyword_colors)
    # print(color_dict)
    # print(color_dict)
    fig = create_production_plot(production_data, color_dict=color_dict)
    # Graficar actividad
    plot_activity(production_file, color_dict=color_dict)


    """ Cumulative Installed Capacity of New Technologies Over the Years"""
    SELECTED_YEARS = [2020, 2024, 2025,2030,  2040, 2050]
    plot_accumulated_capacity(RESULTS_FOLDER, SELECTED_YEARS, color_dict)
    