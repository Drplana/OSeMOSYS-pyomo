import os
import sys
import random
root_folder = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
# from OSeMOSYS.config import INPUT_FILE_PATH, RESULTS_FOLDER, configure_paths
from OSeMOSYS.postprocessing.charts import create_line_chart, create_stacked_bar_chart, create_donut_charts, create_line_chart_app4, create_combined_line_chart, create_heatmap, create_bar_chart
from OSeMOSYS.utils import COLOR_VARIATIONS, DEPENDENCIES_VAR_DICT, assign_colors_to_technologies, dependency_key_app1, dependency_key_app2, dependency_key_app4, dependency_key_app5
# ROOT_FOLDER = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dash import Dash, dcc, html, Input, Output, State, callback, ctx
import webbrowser
from threading import Thread
from itertools import cycle
import itertools
import colorsys
from collections import defaultdict
from OSeMOSYS.config import season_mapping, daytype_mapping, bracket_mapping, yearsplit, specified_demand_profile, input_files_simple
from concurrent.futures import ProcessPoolExecutor
# from OSeMOSYS.CalcParam import transform_to_hourly

from OSeMOSYS.CalcParam import transform_to_hourly

def transform_to_hourly_extra(dependency_files, bracket_mapping, daytype_mapping, season_mapping):
    """
    Transforma los datos agregados por TIMESLICE en datos horarios para múltiples escenarios y archivos.

    Args:
        dependency_files (dict): Diccionario con los archivos organizados por escenario.
        bracket_mapping (dict): Mapeo de bloques horarios.
        daytype_mapping (dict): Mapeo de tipos de día.
        season_mapping (dict): Mapeo de estaciones.

    Returns:
        dict: Diccionario con los datos transformados por escenario y archivo.
    """
    print("Iniciando transformación a formato horario para múltiples escenarios...")
    hourly_data = {}

    for scenario, files in dependency_files.items():
        scenario_data = {}
        print(f"Procesando escenario: {scenario}")
        for file_name, file_path in files.items():
            print(f"Procesando archivo: {file_name} en {file_path}")
            try:
                # Leer el archivo como DataFrame
                results = pd.read_csv(file_path)
                print(f"Columnas en el archivo {file_name}: {results.columns.tolist()}")

                if results.empty:
                    print(f"El archivo {file_name} está vacío.")
                    continue

                # Transformar los datos a formato horario
                hourly_results = transform_to_hourly(results, bracket_mapping, daytype_mapping, season_mapping)
                scenario_data[file_name] = hourly_results
            except Exception as e:
                print(f"Error al procesar el archivo {file_name}: {e}")

        if scenario_data:
            hourly_data[scenario] = scenario_data
        else:
            print(f"No se generaron datos para el escenario {scenario}.")

    return hourly_data

# def transform_to_hourly(results, bracket_mapping, daytype_mapping, season_mapping):
#     """
#     Transforma los datos agregados por TIMESLICE en datos horarios.

#     Args:
#         results (DataFrame): Datos agregados por TIMESLICE.
#         bracket_mapping (dict): Mapeo de bloques horarios.
#         daytype_mapping (dict): Mapeo de tipos de día.
#         season_mapping (dict): Mapeo de estaciones.

#     Returns:
#         DataFrame: Datos transformados a formato horario.
#     """
#     print("Iniciando transformación a formato horario...")
#     print(f"Datos recibidos: {results.head()}")

#     hourly_results = []

#     for _, row in results.iterrows():
#         try:
#             region = row['REGION']
#             timeslice = str(row['TIMESLICE'])  # Convertir a string para descomponer
#             technology = row['TECHNOLOGY']
#             fuel = row['FUEL']
#             year = row['YEAR']
#             value = row['value']

#             # Descomponer el TIMESLICE en Season, DayType y DaylyTimeBracket
#             if len(timeslice) != 3:
#                 print(f"Advertencia: TIMESLICE {timeslice} no tiene el formato esperado (tres dígitos).")
#                 continue

#             season = timeslice[0]  # Primer dígito: Season
#             daytype = timeslice[1]  # Segundo dígito: DayType
#             bracket = timeslice[2]  # Tercer dígito: DaylyTimeBracket

#             # Verificar si los componentes existen en los mapeos
#             if season not in season_mapping:
#                 print(f"Advertencia: Season {season} no encontrado en season_mapping.")
#                 continue
#             if daytype not in daytype_mapping:
#                 print(f"Advertencia: DayType {daytype} no encontrado en daytype_mapping.")
#                 continue
#             if bracket not in bracket_mapping:
#                 print(f"Advertencia: Bracket {bracket} no encontrado en bracket_mapping.")
#                 continue

#             months = season_mapping[season]
#             days = daytype_mapping[daytype]
#             hours = bracket_mapping[bracket]

#             # Distribuir el valor entre las horas
#             hourly_value = value

#             # Generar combinaciones de MONTH, DAY y HOUR
#             for month in months:
#                 for day in days:
#                     for hour in hours:
#                         hourly_results.append({
#                             'REGION': region,
#                             'TECHNOLOGY': technology,
#                             'TIMESLICE': timeslice,
#                             'FUEL': fuel,
#                             'YEAR': year,
#                             'MONTH': month,
#                             'DAY': day,
#                             'HOUR': hour,
#                             'VALUE': hourly_value
#                         })
#         except KeyError as e:
#             print(f"Error: Falta la columna {e} en los datos.")
#             continue
#         except Exception as e:
#             print(f"Error inesperado al procesar la fila: {e}")
#             continue

#     if not hourly_results:
#         print("No se generaron resultados horarios.")
#     else:
#         print(f"Se generaron {len(hourly_results)} filas de datos horarios.")

#     hourly_results_df = pd.DataFrame(hourly_results)
#     print(f"Transformación completada. Datos horarios: {hourly_results_df.head()}")
#     return hourly_results_df

def transform_to_hourly(results, bracket_mapping, daytype_mapping, season_mapping):
    """
    Transforma los datos agregados por TIMESLICE en datos horarios.

    Args:
        results (DataFrame): Datos agregados por TIMESLICE.
        bracket_mapping (dict): Mapeo de bloques horarios.
        daytype_mapping (dict): Mapeo de tipos de día.
        season_mapping (dict): Mapeo de estaciones.

    Returns:
        DataFrame: Datos transformados a formato horario.
    """
    hourly_results = []

    for _, row in results.iterrows():
        try:
            region = row['REGION']
            timeslice = str(row['TIMESLICE'])  # Convertir a string para descomponer
            technology = row['TECHNOLOGY']
            fuel = row['FUEL']
            year = row['YEAR']
            value = row['value']


            # Descomponer el TIMESLICE
            season = timeslice[0]
            daytype = timeslice[1]
            bracket = timeslice[2]

            months = season_mapping[season]
            days = daytype_mapping[daytype]
            hours = bracket_mapping[bracket]

            # Distribuir el valor entre las horas
            hourly_value = value
            # Generar combinaciones de MONTH, DAY y HOUR
            # for month in months:
            #     for day in days:

            ### solo tengo que iterar sobre las horas, 
            ### pero si se quiere tener todas las combinaciones se puede iterar en los meses y en los días(no hace falta)
            for hour in hours:
                hourly_results.append({
                    'REGION': region,
                    'TECHNOLOGY': technology,
                    'TIMESLICE': timeslice,
                    'FUEL': fuel,
                    'YEAR': year,
                    # 'MONTH': month,
                    # 'DAY': day,
                    'HOUR': hour,
                    # 'YearSplit': yearsplit,
                    'VALUE': hourly_value
                })
        except Exception as e:
            print(f"Error al procesar TIMESLICE {timeslice}: {e}")

    hourly_results_df = pd.DataFrame(hourly_results)
    print(f"Transformación completada. Datos horarios: {hourly_results_df.head()}")
    return hourly_results_df


# def transform_to_hourly(results, bracket_mapping, daytype_mapping, season_mapping):
#     print("Iniciando transformación a formato horario...")
#     print(f"Datos recibidos: {results.head()}")

#     hourly_results = []

#     for _, row in results.iterrows():
#         try:
#             region = row['REGION']
#             timeslice = row['TIMESLICE']
#             fuel = row['FUEL']
#             year = row['YEAR']
#             value = row['value']

#             # Verificar si el timeslice está en el bracket_mapping
#             if timeslice not in bracket_mapping:
#                 print(f"Advertencia: TIMESLICE {timeslice} no encontrado en bracket_mapping.")
#                 continue

#             hours = bracket_mapping[timeslice]
#             hourly_value = value

#             for hour in hours:
#                 hourly_results.append({
#                     'REGION': region,
#                     'FUEL': fuel,
#                     'YEAR': year,
#                     'HOUR': hour,
#                     'VALUE': hourly_value
#                 })
#         except KeyError as e:
#             print(f"Error: Falta la columna {e} en los datos.")
#             continue
#         except Exception as e:
#             print(f"Error inesperado al procesar la fila: {e}")
#             continue

#     if not hourly_results:
#         print("No se generaron resultados horarios.")
#     else:
#         print(f"Se generaron {len(hourly_results)} filas de datos horarios.")

#     hourly_results_df = pd.DataFrame(hourly_results)
#     print(f"Transformación completada. Datos horarios: {hourly_results_df.head()}")
#     return hourly_results_df


def get_hourly_files(base_folder="results"):
    """
    Busca archivos con el sufijo 'hourly' en las carpetas de resultados.

    Args:
        base_folder (str): Carpeta base donde se encuentran los resultados.

    Returns:
        dict: Diccionario con los nombres de los escenarios como claves y los archivos correspondientes como valores.
    """
    hourly_files = {}

    # Recorrer las carpetas de resultados
    for scenario_folder in os.listdir(base_folder):
        scenario_path = os.path.join(base_folder, scenario_folder)
        if os.path.isdir(scenario_path):
            # Buscar archivos con el sufijo 'hourly'
            files = [
                file for file in os.listdir(scenario_path)
                if file.endswith("_hourly.csv")
            ]
            if files:
                hourly_files[scenario_folder] = {
                    file: os.path.join(scenario_path, file) for file in files
                }

    return hourly_files





# def process_and_save_hourly_data(dependency_files, yearsplit, specified_demand_profile, bracket_mapping, daytype_mapping, season_mapping):
#     """
#     Procesa los archivos de dependencia y transforma los datos a formato horario.

#     Args:
#         dependency_files (dict): Diccionario con los archivos organizados por escenario.
#         bracket_mapping (dict): Mapeo de bloques horarios.
#         daytype_mapping (dict): Mapeo de tipos de día.
#         season_mapping (dict): Mapeo de estaciones.

#     Returns:
#         dict: Diccionario con los datos transformados por escenario y archivo.
#     """
#     hourly_data = {}

#     for scenario, files in dependency_files.items():
#         scenario_data = {}
#         print(f"Procesando escenario: {scenario}")
#         for file_name, file_path in files.items():
#             results_folder = os.path.dirname(file_path)
#             output_file = os.path.join(results_folder, f"{file_name}_hourly.csv")
#             print(f"Procesando archivo: {file_name} en {file_path}")
#             try:
#                 # Leer el archivo como DataFrame
#                 results = pd.read_csv(file_path)
#                 print(f"Columnas en el archivo {file_name}: {results.columns.tolist()}")

#                 if results.empty:
#                     print(f"El archivo {file_name} está vacío.")
#                     continue
#                 # Mapear YearSplit y SpecifiedDemandProfile a la columna TIMESLICE
#                 # la funcion map me permite aplicar una funcion a cada elemento de la columna 
#                 results['YearSplit'] = results['TIMESLICE'].map(yearsplit)
#                 results['SpecifiedDemandProfile'] = results['TIMESLICE'].map(specified_demand_profile)
#                 results['value'] = results['value'] * results['SpecifiedDemandProfile'] / (results['YearSplit'] * 8760)
#                 # Transformar los datos a formato horario
#                 hourly_results = transform_to_hourly(results, bracket_mapping, daytype_mapping, season_mapping)
#                 hourly_results.to_csv(output_file, index=False)
#                 scenario_data[file_name] = pd.read_csv(output_file)
#             except Exception as e:
#                 print(f"Error al procesar el archivo {file_name}: {e}")

#         if scenario_data:
#             hourly_data[scenario] = scenario_data
#         else:
#             print(f"No se generaron datos para el escenario {scenario}.")

#     return hourly_data

def process_and_save_hourly_data(dependency_files, yearsplit, specified_demand_profile, bracket_mapping, daytype_mapping, season_mapping):
    """
    Procesa los archivos de dependencia, agrega columnas, realiza operaciones matemáticas,
    transforma los datos a formato horario y exporta los resultados.

    Args:
        dependency_files (dict): Diccionario con los archivos organizados por escenario.
        yearsplit (pd.Series): Serie con los valores de YearSplit indexados por TIMESLICE.
        specified_demand_profile (pd.Series): Serie con los valores de SpecifiedDemandProfile indexados por TIMESLICE.
        bracket_mapping (dict): Mapeo de bloques horarios.
        daytype_mapping (dict): Mapeo de tipos de día.
        season_mapping (dict): Mapeo de estaciones.

    Returns:
        None
    """
    for scenario, files in dependency_files.items():
        print(f"Procesando escenario: {scenario}")
        for file_name, file_path in files.items():
            if file_name != "ProductionByTechnology":
                continue
            df = os.path.dirname(file_path)
            output_file = os.path.join(df, f"{file_name}_hourly.csv")
            print(f"Procesando archivo: {file_name} en {file_path}")
            try:
                # Leer el archivo como DataFrame

                df = pd.read_csv(file_path)
                # print(df)
                # df = 
                print(f"Columnas en el archivo {file_name}: {df.columns.tolist()}")

                if df.empty:
                    print(f"El archivo {file_name} está vacío.")
                    continue

                # Agregar columnas YearSplit y SpecifiedDemandProfile
                df['YearSplit'] = df['TIMESLICE'].map(yearsplit)
                df['SpecifiedDemandProfile'] = df['TIMESLICE'].map(specified_demand_profile)
                # print(df)
                # Verificar si hay valores faltantes
                if df[['YearSplit', 'SpecifiedDemandProfile']].isnull().any().any():
                    print(f"Advertencia: Valores faltantes en YearSplit o SpecifiedDemandProfile para {file_name}.")
                    continue
############## Esto es para calcular la demanda horaria 
                df['value'] = df['value'] / (df['YearSplit'] * 8760)
                print(df)
                # Esto es para calcular la demanda horaria 
                # df['value'] = df['value'] * df['TIMESLICE'].map(specified_demand_profile)/(df['TIMESLICE'].map(yearsplit)*8760)  #['SpecifiedDemandProfile'] / (df['YearSplit'] * 8760)
                # print(df)
################ Luego exporto a hourly results el valor de la demanda horaria
                hourly_results = transform_to_hourly(df, bracket_mapping, daytype_mapping, season_mapping)

                # Exportar los resultados a CSV
                output_file = os.path.join(os.path.dirname(file_path), f"{file_name}_hourly.csv")
                hourly_results.to_csv(output_file, index=False)
                print(f"Archivo procesado y guardado en: {output_file}")

            except Exception as e:
                print(f"Error al procesar el archivo {file_name}: {e}")


def get_dependency_files(input_files, dependency_key, base_folder="results"):
    """
    Obtiene los archivos que coinciden con una dependencia específica para cada escenario.

    Args:
        input_files (list): Lista de rutas de archivos de entrada.
        dependency_key (str): Clave de dependencia en DEPENDENCIES_VAR_DICT.
        base_folder (str): Nombre de la carpeta donde se encuentran los resultados.

    Returns:
        dict: Diccionario con los nombres de los escenarios como claves y los archivos correspondientes como valores.
    """
    dependency_files = {}

    for input_file in input_files:
        # Obtener el nombre base del archivo de entrada (sin extensión)
        file_name = os.path.splitext(os.path.basename(input_file))[0]

        # Ruta de la carpeta de resultados para este archivo
        results_folder = os.path.join(root_folder, base_folder, file_name)

        # Verificar si la carpeta de resultados existe
        if not os.path.exists(results_folder):
            print(f"Warning: La carpeta de resultados no existe: {results_folder}")
            continue

        # Buscar los archivos que coincidan con la dependencia
        matching_files = {}
        for dependency_file in DEPENDENCIES_VAR_DICT.get(dependency_key, []):
            file_path = os.path.join(results_folder, f"{dependency_file}.csv")
            if os.path.exists(file_path):
                matching_files[dependency_file] = file_path

        # Agregar los archivos encontrados al diccionario
        if matching_files:
            dependency_files[file_name] = matching_files

    return dependency_files



def process_single_file(file_name, file_path, yearsplit, specified_demand_profile, bracket_mapping, daytype_mapping, season_mapping):
    """
    Procesa un único archivo y lo transforma a formato horario.

    Args:
        file_name (str): Nombre del archivo.
        file_path (str): Ruta del archivo.
        yearsplit (pd.Series): Serie con los valores de YearSplit indexados por TIMESLICE.
        specified_demand_profile (pd.Series): Serie con los valores de SpecifiedDemandProfile indexados por TIMESLICE.
        bracket_mapping (dict): Mapeo de bloques horarios.
        daytype_mapping (dict): Mapeo de tipos de día.
        season_mapping (dict): Mapeo de estaciones.

    Returns:
        str: Mensaje indicando el resultado del procesamiento.
    """
    try:
        if file_name != "ProductionByTechnology":
            return f"Archivo {file_name} no procesado (no es 'ProductionByTechnology')."

        df = pd.read_csv(file_path)
        if df.empty:
            return f"El archivo {file_name} está vacío."

        # Agregar columnas YearSplit y SpecifiedDemandProfile
        df['YearSplit'] = df['TIMESLICE'].map(yearsplit)
        df['SpecifiedDemandProfile'] = df['TIMESLICE'].map(specified_demand_profile)

        if df[['YearSplit', 'SpecifiedDemandProfile']].isnull().any().any():
            return f"Advertencia: Valores faltantes en YearSplit o SpecifiedDemandProfile para {file_name}."

        # Calcular la demanda horaria
        df['value'] = df['value'] / (df['YearSplit'] * 8760)

        # Transformar los datos a formato horario
        hourly_results = transform_to_hourly(df, bracket_mapping, daytype_mapping, season_mapping)

        # Exportar los resultados a CSV
        output_file = os.path.join(os.path.dirname(file_path), f"{file_name}_hourly.csv")
        hourly_results.to_csv(output_file, index=False)
        return f"Archivo procesado y guardado en: {output_file}"

    except Exception as e:
        return f"Error al procesar el archivo {file_name}: {e}"


def process_and_save_hourly_data_parallel(dependency_files, yearsplit, specified_demand_profile, bracket_mapping, daytype_mapping, season_mapping):
    """
    Procesa los archivos de dependencia en paralelo y los transforma a formato horario.

    Args:
        dependency_files (dict): Diccionario con los archivos organizados por escenario.
        yearsplit (pd.Series): Serie con los valores de YearSplit indexados por TIMESLICE.
        specified_demand_profile (pd.Series): Serie con los valores de SpecifiedDemandProfile indexados por TIMESLICE.
        bracket_mapping (dict): Mapeo de bloques horarios.
        daytype_mapping (dict): Mapeo de tipos de día.
        season_mapping (dict): Mapeo de estaciones.

    Returns:
        None
    """
    tasks = []

    # Crear tareas para cada archivo
    for scenario, files in dependency_files.items():
        for file_name, file_path in files.items():
            tasks.append((file_name, file_path, yearsplit, specified_demand_profile, bracket_mapping, daytype_mapping, season_mapping))

    # Ejecutar las tareas en paralelo
    with ProcessPoolExecutor() as executor:
        results = executor.map(process_single_file_wrapper, tasks)
        for result in results:
            print(result)


def process_single_file_wrapper(args):
    """
    Wrapper para desempaquetar argumentos y llamar a process_single_file.

    Args:
        args (tuple): Argumentos para process_single_file.

    Returns:
        str: Resultado de process_single_file.
    """
    return process_single_file(*args)


# def create_stacked_bar_chart(data, title, COLOR_VARIATIONS):
#     """
#     Crea un gráfico de barras apiladas.

#     Args:
#         data (pd.DataFrame): DataFrame con los datos.
#         title (str): Título del gráfico.
#         COLOR_VARIATIONS (dict): Diccionario que asigna colores a las tecnologías.

#     Returns:
#         go.Figure: Gráfico de barras apiladas.
#     """
#     # Crear una lista de colores por defecto para tecnologías no definidas
#     default_colors = cycle(px.colors.qualitative.Plotly)

#     # Crear un mapeo entre tecnologías y colores
#     technology_colors =  assign_colors_to_technologies(data, 'TECHNOLOGY', COLOR_VARIATIONS)


#     # Crear el gráfico de barras apiladas
#     fig = px.bar(
#         data,
#         x='YEAR',
#         y='value',
#         color='TECHNOLOGY',
#         barmode='stack',
#         title=title,
#         color_discrete_map=technology_colors  # Usar el mapeo de colores
#     )

#     # Configurar el diseño del gráfico
#     fig.update_layout(
#         xaxis_title="Año",
#         yaxis_title="Producción de Energía (GWh)",
#         plot_bgcolor='white',
#         font=dict(size=14),
#         legend=dict(font=dict(size=12)),
#         margin=dict(t=50, b=50, l=50, r=50)
#     )

#     return fig

def generate_colored_options(technologies, COLOR_VARIATIONS):
    """
    Genera las opciones del checklist con los colores correspondientes.

    Args:
        technologies (list): Lista de tecnologías.
        COLOR_VARIATIONS (dict): Diccionario que asigna colores a las categorías.

    Returns:
        list: Lista de opciones para el checklist.
    """
    options = []
    used_colors = {key: itertools.cycle(colors) for key, colors in COLOR_VARIATIONS.items()}  # Ciclos de colores por clave

    # Ordenar tecnologías alfabéticamente
    for tech in sorted(technologies):
        color = 'gray'  # Color por defecto
        for key, color_cycle in used_colors.items():
            if key.lower() in tech.lower():  # Coincidencia parcial (ignorando mayúsculas)
                color = next(color_cycle)  # Tomar el siguiente color disponible
                break

        # Crear la opción con el color correspondiente
        options.append({
            'label': html.Div([
                html.Div(
                    style={
                        'width': '20px',
                        'height': '20px',
                        'background-color': color,
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
        })

    return options


# files = {
#     "BaseScenario": "/home/david/OSeMOSYS-pyomo/results/BaseScenario/ProductionByTechnologyAnnual.csv",
#     "BaseScenarioWind": "/home/david/OSeMOSYS-pyomo/results/BaseScenarioWind/ProductionByTechnologyAnnual.csv",
#     "BaseScenarioWindBiomass": "/home/david/OSeMOSYS-pyomo/results/BaseScenarioWindBiomass/ProductionByTechnologyAnnual.csv",
#     "BaseScenarioAnualCapLim": "/home/david/OSeMOSYS-pyomo/results/BaseScenarioAnualCapLim/ProductionByTechnologyAnnual.csv",
#     "RecapitalizarUnidades": "/home/david/OSeMOSYS-pyomo/results/RecapitalizarUnidades/ProductionByTechnologyAnnual.csv",
#     "RecapitalizarUnidades600": "/home/david/OSeMOSYS-pyomo/results/RecapitalizarUnidades600/ProductionByTechnologyAnnual.csv",
#     "RecapitalizarUnidades700": "/home/david/OSeMOSYS-pyomo/results/RecapitalizarUnidades700/ProductionByTechnologyAnnual.csv",
#     "RecapitalizarUnidades800": "/home/david/OSeMOSYS-pyomo/results/RecapitalizarUnidades800/ProductionByTechnologyAnnual.csv",


#     "RecapMustRun": "/home/david/OSeMOSYS-pyomo/results/RecapMustRun/ProductionByTechnologyAnnual.csv",

# }

def create_first_app(files_by_scenario, COLOR_VARIATIONS, scenarios):
    """
    Crea la primera aplicación Dash para comparar resultados entre dos escenarios.

    Args:
        files_by_scenario (dict): Diccionario con los archivos organizados por escenario.
        COLOR_VARIATIONS (dict): Diccionario que asigna colores a las tecnologías.
        scenarios (list): Lista de escenarios disponibles.

    Returns:
        Dash: Aplicación Dash configurada.
    """
    # Crear la aplicación Dash
    app = Dash(__name__)
    app.layout = html.Div([
        html.H1("Scenario Comparison Dashboard", style={'textAlign': 'center'}),
        html.Div([
            html.Label("Tecnologías a mostrar:", style={'font-size': '20px'}),
            dcc.Checklist(
                id='technology-filter',  # Mantén un único id para este checklist
                options=[],
                value=[],
                inline=False,
                style={'font-size': '16px', 'display': 'flex', 'flex-wrap': 'wrap', 'gap': '10px'},
            ),
            html.Button(
                "Seleccionar/Deseleccionar todas",
                id='toggle-all-button',
                n_clicks=0,
                style={'margin-top': '10px', 'font-size': '16px'}
            )
        ], style={'margin-bottom': '20px'}),
    
        # Dropdowns para seleccionar escenarios
        html.Div([
            html.Div([
                html.Label("Selecciona el primer escenario:", style={'font-size': '16px'}),
                dcc.Dropdown(
                    id='scenario-dropdown-1',
                    options=[{'label': scenario, 'value': scenario} for scenario in scenarios],
                    value=scenarios[0],
                    style={'width': '80%'}
                ),
                html.Label("Selecciona el archivo:", style={'font-size': '16px', 'margin-top': '10px'}),
                dcc.Dropdown(
                    id='file-dropdown-1',
                    options=[],
                    value=None,
                    style={'width': '80%'}
                )
            ], style={'width': '48%', 'display': 'inline-block'}),
            
            html.Div([
                html.Label("Selecciona el segundo escenario:", style={'font-size': '16px'}),
                dcc.Dropdown(
                    id='scenario-dropdown-2',
                    options=[{'label': scenario, 'value': scenario} for scenario in scenarios],
                    value=scenarios[1] if len(scenarios) > 1 else scenarios[0],
                    style={'width': '80%'}
                ),
                html.Label("Selecciona el archivo:", style={'font-size': '16px', 'margin-top': '10px'}),
                dcc.Dropdown(
                    id='file-dropdown-2',
                    options=[],
                    value=None,
                    style={'width': '80%'}
                )
            ], style={'width': '48%', 'display': 'inline-block'})
        ]),
        
        # Gráficos de líneas
        html.Div([
            dcc.Graph(id='line-chart-1', style={'width': '48%', 'display': 'inline-block'}),
            dcc.Graph(id='line-chart-2', style={'width': '48%', 'display': 'inline-block'})
        ]),
        html.Div([dcc.Graph(id='stacked-bar-chart-1', style={'width': '48%', 'display': 'inline-block'}),
                dcc.Graph(id='stacked-bar-chart-2', style={'width': '48%', 'display': 'inline-block'})
        ]),
    ])
    # Cargar todos los datos al inicio
#     def load_all_data(files_by_scenario):
#         data_cache = {}
#         for scenario, files in files_by_scenario.items():
#             data_cache[scenario] = {}
#             for file_name, file_path in files.items():
#                 data = pd.read_csv(file_path)
#                 data['TECHNOLOGY'] = data['TECHNOLOGY'].str.strip()  # Eliminar espacios en blanco
#                 data_cache[scenario][file_name] = data
#         return data_cache

# # Almacenar los datos en memoria
#     data_cache = load_all_data(files_by_scenario)    

    # @app.callback(
    #     Output('technology-filter', 'value'),
    #     [Input('toggle-all-button', 'n_clicks')],
    #     [State('technology-filter', 'options'),
    #      State('technology-filter', 'value')]
    # )
    # def toggle_all_technologies(n_clicks, options, current_selection):
    #     # Si el número de clics es impar, seleccionar todas las tecnologías
    #     if n_clicks % 2 == 1:
    #         return [option['value'] for option in options]
    #     # Si el número de clics es par, deseleccionar todas las tecnologías
    #     return []

    # Callback para actualizar los archivos disponibles según el escenario seleccionado
    # Callbacks para los dropdowns
    @app.callback(
        [Output('file-dropdown-1', 'options'),
        Output('file-dropdown-1', 'value')],
        [Input('scenario-dropdown-1', 'value')],
        [State('file-dropdown-1', 'value')]
    )
    def update_file_dropdown_1(scenario1, current_file):
        # Obtener los archivos disponibles para el escenario seleccionado
        options1 = [{'label': file, 'value': file} for file in files_by_scenario[scenario1].keys()]
        
        # Verificar si el archivo actualmente seleccionado está disponible
        if current_file in files_by_scenario[scenario1].keys():
            selected_file = current_file
        else:
            # Si no está disponible, seleccionar el primer archivo
            selected_file = options1[0]['value']
        
        return options1, selected_file


    @app.callback(
        [Output('file-dropdown-2', 'options'),
        Output('file-dropdown-2', 'value')],
        [Input('scenario-dropdown-2', 'value')],
        [State('file-dropdown-2', 'value')]
    )
    def update_file_dropdown_2(scenario2, current_file):
        # Obtener los archivos disponibles para el escenario seleccionado
        options2 = [{'label': file, 'value': file} for file in files_by_scenario[scenario2].keys()]
        
        # Verificar si el archivo actualmente seleccionado está disponible
        if current_file in files_by_scenario[scenario2].keys():
            selected_file = current_file
        else:
            # Si no está disponible, seleccionar el primer archivo
            selected_file = options2[0]['value']
        
        return options2, selected_file

    # Callback para actualizar el checklist de tecnologías
    @app.callback(
        [Output('technology-filter', 'options'),
        Output('technology-filter', 'value')],
        [Input('scenario-dropdown-1', 'value'),
        Input('file-dropdown-1', 'value'),
        Input('scenario-dropdown-2', 'value'),
        Input('file-dropdown-2', 'value'),
        Input('toggle-all-button', 'n_clicks')],
        [State('technology-filter', 'value'),
        State('technology-filter', 'options')]
    )
    def update_technology_filter(scenario1, file1, scenario2, file2, n_clicks, current_selection, current_options):
        # Obtener tecnologías de los archivos seleccionados
        techs1 = pd.read_csv(files_by_scenario[scenario1][file1])['TECHNOLOGY'].unique()
        techs2 = pd.read_csv(files_by_scenario[scenario2][file2])['TECHNOLOGY'].unique()
        all_techs = sorted(set(techs1).union(set(techs2)), reverse=True)

        # Generar opciones con colores
        options = generate_colored_options(all_techs, COLOR_VARIATIONS)

        # Determinar las tecnologías seleccionadas
        # ctx = Dash.callback_context  # Obtener el contexto del callback
        if not ctx.triggered:
            # Si no hay interacción, mantener la selección actual
            selected_techs = current_selection if current_selection else all_techs
        else:
            # Verificar qué Input activó el callback
            triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
            if triggered_id == 'toggle-all-button':
                # Alternar entre seleccionar y deseleccionar todas
                if n_clicks % 2 == 1:
                    selected_techs = all_techs  # Seleccionar todas
                else:
                    selected_techs = []  # Deseleccionar todas
            else:
                # Si se cambian los archivos o escenarios, mantener solo las tecnologías válidas
                selected_techs = [tech for tech in current_selection if tech in all_techs] if current_selection else all_techs

        return options, selected_techs

    # Callback para actualizar los gráficos de líneas
    @app.callback(
        [Output('line-chart-1', 'figure'),
        Output('line-chart-2', 'figure')],
        [Input('scenario-dropdown-1', 'value'),
        Input('file-dropdown-1', 'value'),
        Input('scenario-dropdown-2', 'value'),
        Input('file-dropdown-2', 'value'),
        Input('technology-filter', 'value')]
    )
    def update_line_charts(scenario1, file1, scenario2, file2, selected_techs):
        # Leer datos del primer archivo
        data1 = pd.read_csv(files_by_scenario[scenario1][file1])
        data1 = data1[data1['TECHNOLOGY'].isin(selected_techs)]
        chart1 = create_line_chart(
            data=data1,
            title=f"Gráfico de {file1} - {scenario1}",
            x_column="YEAR",
            y_column="value",
            color_column="TECHNOLOGY",
            COLOR_VARIATIONS=COLOR_VARIATIONS
        )
        
        # Leer datos del segundo archivo
        data2 = pd.read_csv(files_by_scenario[scenario2][file2])
        data2 = data2[data2['TECHNOLOGY'].isin(selected_techs)]
        chart2 = create_line_chart(
            data=data2,
            title=f"Gráfico de {file2} - {scenario2}",
            x_column="YEAR",
            y_column="value",
            color_column="TECHNOLOGY",
            COLOR_VARIATIONS=COLOR_VARIATIONS
        )
        
        return chart1, chart2
    @app.callback(
    [Output('stacked-bar-chart-1', 'figure'),
     Output('stacked-bar-chart-2', 'figure')],
    [Input('scenario-dropdown-1', 'value'),
     Input('file-dropdown-1', 'value'),
     Input('scenario-dropdown-2', 'value'),
     Input('file-dropdown-2', 'value'),
     Input('technology-filter', 'value')]
        )
    def update_stacked_bar_charts(scenario1, file1, scenario2, file2, selected_techs):
        # Leer datos del primer archivo
        data1 = pd.read_csv(files_by_scenario[scenario1][file1])
        data1 = data1[data1['TECHNOLOGY'].isin(selected_techs)]

        # Leer datos del segundo archivo
        data2 = pd.read_csv(files_by_scenario[scenario2][file2])
        data2 = data2[data2['TECHNOLOGY'].isin(selected_techs)]

        # Crear los gráficos de barras apiladas
        bar_chart_1 = create_stacked_bar_chart(
            data=data1,
            title=f"Barras Apiladas - {scenario1}",
            COLOR_VARIATIONS=COLOR_VARIATIONS
        )

        bar_chart_2 = create_stacked_bar_chart(
            data=data2,
            title=f"Barras Apiladas - {scenario2}",
            COLOR_VARIATIONS=COLOR_VARIATIONS
        )

        return bar_chart_1, bar_chart_2
    return app


def create_comparison_dashboard_with_options(files_by_scenario, COLOR_VARIATIONS, years, scenarios):
    """
    Crea un dashboard para comparar resultados entre dos escenarios con opciones de gráficos.

    Args:
        files_by_scenario (dict): Diccionario con los archivos organizados por escenario.
        COLOR_VARIATIONS (dict): Diccionario que asigna colores a las tecnologías.
        years (list): Lista de años para los gráficos de dona.
        scenarios (list): Lista de escenarios disponibles.

    Returns:
        Dash: Aplicación Dash configurada.
    """
    app = Dash(__name__)

    # Layout de la aplicación
    app.layout = html.Div([
        html.H1("Scenario Comparison Dashboard", style={'textAlign': 'center'}),
        html.Div([
            html.Label("Tecnologías a mostrar:", style={'font-size': '20px'}),
            dcc.Checklist(
                id='technology-filter',
                options=[],
                value=[],
                inline=False,
                style={'font-size': '16px', 'display': 'flex', 'flex-wrap': 'wrap', 'gap': '10px'},
            ),
            html.Button(
                "Seleccionar/Deseleccionar todas",
                id='toggle-all-button',
                n_clicks=0,
                style={'margin-top': '10px', 'font-size': '16px'}
            )
        ], style={'margin-bottom': '20px'}),
        html.Div([
        html.Label("Selecciona la unidad:", style={'font-size': '20px'}),
        dcc.RadioItems(
            id='unit-selector',
            options=[
                {'label': 'PJ', 'value': 'PJ'},
                {'label': 'GWh', 'value': 'GWh'},
                {'label': 'TWh', 'value': 'TWh'},
                {'label': 'MWh', 'value': 'MWh'}
            ],
        value='PJ',  # Unidad predeterminada
            inline=True,
            style={'font-size': '16px'}
        )
        ], style={'margin-bottom': '20px'}),
        
        # Dropdowns para seleccionar escenarios y archivos
        html.Div([
            html.Div([
                html.Label("Selecciona el primer escenario:", style={'font-size': '16px'}),
                dcc.Dropdown(
                    id='scenario-dropdown-1',
                    options=[{'label': scenario, 'value': scenario} for scenario in scenarios],
                    value=scenarios[0],
                    style={'width': '80%'}
                ),
                html.Label("Selecciona el archivo:", style={'font-size': '16px', 'margin-top': '10px'}),
                dcc.Dropdown(
                    id='file-dropdown-1',
                    options=[],
                    value=None,
                    style={'width': '80%'}
                )
            ], style={'width': '48%', 'display': 'inline-block'}),
            
            html.Div([
                html.Label("Selecciona el segundo escenario:", style={'font-size': '16px'}),
                dcc.Dropdown(
                    id='scenario-dropdown-2',
                    options=[{'label': scenario, 'value': scenario} for scenario in scenarios],
                    value=scenarios[1] if len(scenarios) > 1 else scenarios[0],
                    style={'width': '80%'}
                ),
                html.Label("Selecciona el archivo:", style={'font-size': '16px', 'margin-top': '10px'}),
                dcc.Dropdown(
                    id='file-dropdown-2',
                    options=[],
                    value=None,
                    style={'width': '80%'}
                )
            ], style={'width': '48%', 'display': 'inline-block'})
        ]),
        
        # Gráficos de barras apiladas y donas
        html.Div([
            html.Div([
                dcc.Graph(id='stacked-bar-chart-1', style={'width': '100%', 'display': 'inline-block'}),
                html.Div(id='donut-charts-1', style={'display': 'flex', 'justify-content': 'left', 'gap': '10px'})
            ], style={'width': '48%', 'display': 'inline-block'}),
            html.Div([
                dcc.Graph(id='stacked-bar-chart-2', style={'width': '100%', 'display': 'inline-block'}),
                html.Div(id='donut-charts-2', style={'display': 'flex', 'justify-content': 'left', 'gap': '10px'})
            ], style={'width': '48%', 'display': 'inline-block'})
        ])
    ])
    # Cargar todos los datos al inicio
    def load_all_data(files_by_scenario):
        data_cache = {}
        for scenario, files in files_by_scenario.items():
            data_cache[scenario] = {}
            for file_name, file_path in files.items():
                data = pd.read_csv(file_path)
                data['TECHNOLOGY'] = data['TECHNOLOGY'].str.strip()  # Eliminar espacios en blanco
                #data['value'] = data['value']*277.8  # Asegurarse de que los valores sean numéricos
                data_cache[scenario][file_name] = data
        return data_cache

    # Almacenar los datos en memoria
    data_cache = load_all_data(files_by_scenario)

    # Callbacks para actualizar los dropdowns de archivos
    @app.callback(
        [Output('file-dropdown-1', 'options'),
         Output('file-dropdown-1', 'value')],
        [Input('scenario-dropdown-1', 'value')],
        [State('file-dropdown-1', 'value')]
    )
    def update_file_dropdown_1(scenario1, current_file):
        options1 = [{'label': file, 'value': file} for file in files_by_scenario[scenario1].keys()]
        selected_file = current_file if current_file in files_by_scenario[scenario1].keys() else options1[0]['value']
        return options1, selected_file

    @app.callback(
        [Output('file-dropdown-2', 'options'),
         Output('file-dropdown-2', 'value')],
        [Input('scenario-dropdown-2', 'value')],
        [State('file-dropdown-2', 'value')]
    )
    def update_file_dropdown_2(scenario2, current_file):
        options2 = [{'label': file, 'value': file} for file in files_by_scenario[scenario2].keys()]
        selected_file = current_file if current_file in files_by_scenario[scenario2].keys() else options2[0]['value']
        return options2, selected_file

    # Callback para actualizar el checklist de tecnologías
    @app.callback(
        [Output('technology-filter', 'options'),
         Output('technology-filter', 'value')],
        [Input('scenario-dropdown-1', 'value'),
         Input('file-dropdown-1', 'value'),
         Input('scenario-dropdown-2', 'value'),
         Input('file-dropdown-2', 'value'),
         Input('toggle-all-button', 'n_clicks')],
        [State('technology-filter', 'value'),
         State('technology-filter', 'options')]
    )
    def update_technology_filter(scenario1, file1, scenario2, file2, n_clicks, current_selection, current_options):
        # Obtener tecnologías de los archivos seleccionados
        techs1 = pd.read_csv(files_by_scenario[scenario1][file1])['TECHNOLOGY'].unique()
        techs2 = pd.read_csv(files_by_scenario[scenario2][file2])['TECHNOLOGY'].unique()
        all_techs = sorted(set(techs1).union(set(techs2)), reverse=True)

        # Generar opciones con colores
        options = generate_colored_options(all_techs, COLOR_VARIATIONS)

        # Determinar las tecnologías seleccionadas
        # ctx = Dash.callback_context  # Obtener el contexto del callback
        if not ctx.triggered:
            # Si no hay interacción, mantener la selección actual
            selected_techs = current_selection if current_selection else all_techs
        else:
            # Verificar qué Input activó el callback
            triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
            if triggered_id == 'toggle-all-button':
                # Alternar entre seleccionar y deseleccionar todas
                if n_clicks % 2 == 1:
                    selected_techs = all_techs  # Seleccionar todas
                else:
                    selected_techs = []  # Deseleccionar todas
            else:
                # Si se cambian los archivos o escenarios, mantener solo las tecnologías válidas
                selected_techs = [tech for tech in current_selection if tech in all_techs] if current_selection else all_techs

        return options, selected_techs

    # Callback para actualizar los gráficos
    @app.callback(
        [Output('stacked-bar-chart-1', 'figure'),
        Output('donut-charts-1', 'children'),
        Output('stacked-bar-chart-2', 'figure'),
        Output('donut-charts-2', 'children')],
        [Input('scenario-dropdown-1', 'value'),
        Input('file-dropdown-1', 'value'),
        Input('scenario-dropdown-2', 'value'),
        Input('file-dropdown-2', 'value'),
        Input('technology-filter', 'value'),
        Input('unit-selector', 'value')]
    )
    def update_graphs(scenario1, file1, scenario2, file2, selected_techs, unit):
        # Leer datos
        data1 = data_cache[scenario1][file1].copy()
        data2 = data_cache[scenario2][file2].copy()


        data1 = data1[data1['TECHNOLOGY'].isin(selected_techs)]
        data2 = data2[data2['TECHNOLOGY'].isin(selected_techs)]
        conversion_factors = {
            'PJ': 1,
            'GWh': 277.8,
            'TWh': 0.2778,
            'MWh': 277.8*1000
        }

        factor = conversion_factors.get(unit, 1)
        data1['value'] = data1['value'] * factor
        data2['value'] = data2['value'] * factor # Asegurarse de que los valores sean numéricos
        # Crear gráficos de barras apiladas
        bar_chart_1 = create_stacked_bar_chart(data1, f"Barras Apiladas - {scenario1}", COLOR_VARIATIONS)
        bar_chart_2 = create_stacked_bar_chart(data2, f"Barras Apiladas - {scenario2}", COLOR_VARIATIONS)
        bar_chart_1.update_layout(yaxis_title=f"Energy Production ({unit})")
        bar_chart_2.update_layout(yaxis_title=f"Energy Production ({unit})")

        # Crear gráficos de dona
        donut_charts_1 = create_donut_charts(data1, years, COLOR_VARIATIONS, selected_techs, unit)
        donut_charts_2 = create_donut_charts(data2, years, COLOR_VARIATIONS, selected_techs, unit)
        
        print("Donut Charts 1:")
        for chart in donut_charts_1:
            print(chart.layout.annotations)

        print("Donut Charts 2:")
        for chart in donut_charts_2:
            print(chart.layout.annotations)

        # Envolver los gráficos de dona en dcc.Graph
        donut_charts_1 = [dcc.Graph(figure=chart) for chart in donut_charts_1]
        donut_charts_2 = [dcc.Graph(figure=chart) for chart in donut_charts_2]


        return bar_chart_1, donut_charts_1, bar_chart_2, donut_charts_2

    return app


def create_heatmap_app(dependency_files, scenarios):
    """
    Crea una aplicación Dash para visualizar heatmaps basados en los archivos de dependencia.

    Args:
        dependency_files (dict): Diccionario con los archivos de dependencia organizados por escenario.
        scenarios (list): Lista de escenarios disponibles.

    Returns:
        Dash: Aplicación Dash configurada.
    """
    app = Dash(__name__)

    # Layout de la aplicación
    app.layout = html.Div([
        html.H1("Heatmap Dashboard", style={'textAlign': 'center'}),
        html.Div([
            html.Label("Selecciona las tecnologías:", style={'font-size': '16px'}),
            dcc.Checklist(
                id='technology-checklist',
                options=[],  # Se llenará dinámicamente
                value=[],  # Selección inicial vacía
                inline=False,
                style={'font-size': '16px', 'display': 'flex', 'flex-wrap': 'wrap', 'gap': '10px'}
            )
        ], style={'margin-bottom': '20px'}),
        html.Div([
            html.Div([
                html.Label("Selecciona el archivo de dependencia 1:", style={'font-size': '16px'}),
                dcc.Dropdown(
                    id='dependency-file-dropdown-1',
                    options=[{'label': file, 'value': file} for file in list(dependency_files[scenarios[0]].keys())],
                    value=list(dependency_files[scenarios[0]].keys())[0],  # Seleccionar el primer archivo por defecto
                    style={'width': '80%'}
                ),
                dcc.Graph(id='heatmap-1', style={'width': '100%', 'display': 'inline-block'})
            ], style={'width': '48%', 'display': 'inline-block'}),
            html.Div([
                html.Label("Selecciona el archivo de dependencia 2:", style={'font-size': '16px'}),
                dcc.Dropdown(
                    id='dependency-file-dropdown-2',
                    options=[{'label': file, 'value': file} for file in list(dependency_files[scenarios[0]].keys())],
                    value=list(dependency_files[scenarios[0]].keys())[0],  # Seleccionar el primer archivo por defecto
                    style={'width': '80%'}
                ),
                dcc.Graph(id='heatmap-2', style={'width': '100%', 'display': 'inline-block'})
            ], style={'width': '48%', 'display': 'inline-block'})
        ])
    ])

    # Cargar todos los datos al inicio
    def load_all_data(dependency_files):
        data_cache = {}
        for scenario, files in dependency_files.items():
            data_cache[scenario] = {}
            for file_name, file_path in files.items():
                data = pd.read_csv(file_path)
                data['TECHNOLOGY'] = data['TECHNOLOGY'].str.strip()  # Eliminar espacios en blanco
                data_cache[scenario][file_name] = data
        return data_cache

    # Almacenar los datos en memoria
    data_cache = load_all_data(dependency_files)

    # Callback para llenar el checklist de tecnologías
    @app.callback(
        Output('technology-checklist', 'options'),
        [Input('dependency-file-dropdown-1', 'value'),
         Input('dependency-file-dropdown-2', 'value')]
    )
    def update_technology_checklist(file1, file2):
        techs = set()
        for scenario, files in data_cache.items():
            if file1 in files:
                techs.update(files[file1]['TECHNOLOGY'].unique())
            if file2 in files:
                techs.update(files[file2]['TECHNOLOGY'].unique())
        return [{'label': tech, 'value': tech} for tech in sorted(techs)]

    # Callback para actualizar los heatmaps
    @app.callback(
        [Output('heatmap-1', 'figure'),
        Output('heatmap-2', 'figure')],
        [Input('dependency-file-dropdown-1', 'value'),
        Input('dependency-file-dropdown-2', 'value'),
        Input('technology-checklist', 'value')]
    )
    def update_heatmaps(file1, file2, selected_technologies):
        # Preparar datos para el primer heatmap
        data1 = []
        for scenario, files in data_cache.items():
            if file1 in files:
                df = files[file1].copy()
                df['SCENARIO'] = scenario  # Añadir la columna 'SCENARIO'
                data1.append(df)
        data1 = pd.concat(data1)

        # Preparar datos para el segundo heatmap
        data2 = []
        for scenario, files in data_cache.items():
            if file2 in files:
                df = files[file2].copy()
                df['SCENARIO'] = scenario  # Añadir la columna 'SCENARIO'
                data2.append(df)
        data2 = pd.concat(data2)

        # Crear los heatmaps
        heatmap1 = create_heatmap(data1, selected_technologies, f"Heatmap para {file1}", show_colorbar=False)
        heatmap2 = create_heatmap(data2, selected_technologies, f"Heatmap para {file2}", show_colorbar=True)

        return heatmap1, heatmap2

    return app


def create_app_4(dependency_files):
    """
    Crea una aplicación Dash para comparar escenarios con gráficos de línea basados en la dependencia ['REGION','YEAR'].

    Args:
        dependency_files (dict): Diccionario con los archivos de dependencia organizados por escenario.

    Returns:
        Dash: Aplicación Dash configurada.
    """
    app = Dash(__name__)

    # Layout de la aplicación
    app.layout = html.Div([
        html.H1("App 4: Comparación de Escenarios", style={'textAlign': 'center'}),
        html.Div([
            html.Div([
                html.Label("Selecciona el primer escenario:", style={'font-size': '16px'}),
                dcc.Dropdown(
                    id='scenario-dropdown-1',
                    options=[{'label': scenario, 'value': scenario} for scenario in dependency_files.keys()],
                    value=list(dependency_files.keys())[0],  # Seleccionar el primer escenario por defecto
                    style={'width': '80%'}
                ),
                html.Label("Selecciona el archivo del primer escenario:", style={'font-size': '16px', 'margin-top': '10px'}),
                dcc.Dropdown(
                    id='file-dropdown-1',
                    options=[],  # Se llenará dinámicamente
                    value=None,
                    style={'width': '80%'}
                )
            ], style={'width': '48%', 'display': 'inline-block'}),
            html.Div([
                html.Label("Selecciona el segundo escenario:", style={'font-size': '16px'}),
                dcc.Dropdown(
                    id='scenario-dropdown-2',
                    options=[{'label': scenario, 'value': scenario} for scenario in dependency_files.keys()],
                    value=list(dependency_files.keys())[1] if len(dependency_files) > 1 else list(dependency_files.keys())[0],
                    style={'width': '80%'}
                ),
                html.Label("Selecciona el archivo del segundo escenario:", style={'font-size': '16px', 'margin-top': '10px'}),
                dcc.Dropdown(
                    id='file-dropdown-2',
                    options=[],  # Se llenará dinámicamente
                    value=None,
                    style={'width': '80%'}
                )
            ], style={'width': '48%', 'display': 'inline-block'})
        ], style={'margin-bottom': '20px'}),
        html.Div([
            html.Label("Selecciona las regiones:", style={'font-size': '16px'}),
            dcc.Checklist(
                id='region-checklist',
                options=[],  # Se llenará dinámicamente
                value=[],  # Selección inicial vacía
                inline=False,
                style={'font-size': '16px', 'display': 'flex', 'flex-wrap': 'wrap', 'gap': '10px'}
            )
        ], style={'margin-bottom': '20px'}),
        html.Div([
            dcc.Graph(id='line-chart-1', style={'width': '48%', 'display': 'inline-block'}),
            dcc.Graph(id='line-chart-2', style={'width': '48%', 'display': 'inline-block'})
        ]),
            html.Div([
        html.Label("Selecciona los escenarios a mostrar:", style={'font-size': '16px'}),
        dcc.Checklist(
            id='scenario-checklist',
            options=[{'label': scenario, 'value': scenario} for scenario in dependency_files.keys()],
            value=list(dependency_files.keys()),  # Seleccionar todos los escenarios por defecto
            inline=False,
            style={'font-size': '16px', 'display': 'flex', 'flex-wrap': 'wrap', 'gap': '10px'}
        )
    ], style={'margin-top': '20px'}),
    html.Div([
        html.Div([
            dcc.Graph(id='combined-line-chart', style={'width': '48%', 'display': 'inline-block'}),
        ]),
        html.Div([
            dcc.Graph(id='bar-chart', style={'width': '48%', 'display': 'inline-block'})
        ])
    ], style={'display': 'flex', 'align-items': 'center'})
])


    # Cargar todos los datos al inicio
    def load_all_data(dependency_files):
        data_cache = {}
        for scenario, files in dependency_files.items():
            data_cache[scenario] = {}
            for file_name, file_path in files.items():
                data = pd.read_csv(file_path)
                data['REGION'] = data['REGION'].str.strip()  # Eliminar espacios en blanco
                data_cache[scenario][file_name] = data
        return data_cache

    # Almacenar los datos en memoria
    data_cache = load_all_data(dependency_files)
    @app.callback(
        [Output('file-dropdown-1', 'options'),
        Output('file-dropdown-1', 'value')],
        [Input('scenario-dropdown-1', 'value')]
    )
    def update_file_dropdown_1(selected_scenario):
        if selected_scenario in data_cache:
            files = data_cache[selected_scenario].keys()
            options = [{'label': file, 'value': file} for file in files]
            return options, options[0]['value'] if options else None
        return [], None


    @app.callback(
        [Output('file-dropdown-2', 'options'),
        Output('file-dropdown-2', 'value')],
        [Input('scenario-dropdown-2', 'value')]
    )
    def update_file_dropdown_2(selected_scenario):
        if selected_scenario in data_cache:
            files = data_cache[selected_scenario].keys()
            options = [{'label': file, 'value': file} for file in files]
            return options, options[0]['value'] if options else None
        return [], None

    # Callback para llenar el checklist de regiones
    @app.callback(
        Output('region-checklist', 'options'),
        [Input('file-dropdown-1', 'value'),
        Input('file-dropdown-2', 'value')]
    )
    def update_region_checklist(file1, file2):
        regions = set()
        for file in [file1, file2]:
            if file:
                for scenario, files in data_cache.items():
                    if file in files:
                        regions.update(files[file]['REGION'].unique())
        return [{'label': region, 'value': region} for region in sorted(regions)]
        # Callback para actualizar los gráficos de línea
    @app.callback(
    [Output('line-chart-1', 'figure'),
     Output('line-chart-2', 'figure')],
    [Input('scenario-dropdown-1', 'value'),
     Input('file-dropdown-1', 'value'),
     Input('scenario-dropdown-2', 'value'),
     Input('file-dropdown-2', 'value'),
     Input('region-checklist', 'value')]
    )
    def update_line_charts(scenario1, file1, scenario2, file2, selected_regions):
        # Leer datos del primer archivo
        if scenario1 in data_cache and file1 in data_cache[scenario1]:
            data1 = data_cache[scenario1][file1]
            if selected_regions:
                data1 = data1[data1['REGION'].isin(selected_regions)]
            line_chart_1 = create_line_chart_app4(
                data = data1,
                x_column='YEAR',
                y_column='value',
                color_column='REGION',
                title=f"Escenario: {scenario1}, Archivo: {file1}",
            )
        else:
            line_chart_1 = px.line(title="No se encontraron datos para el primer archivo")

        # Leer datos del segundo archivo
        if scenario2 in data_cache and file2 in data_cache[scenario2]:
            data2 = data_cache[scenario2][file2]
            if selected_regions:
                data2 = data2[data2['REGION'].isin(selected_regions)]
            line_chart_2 = create_line_chart_app4(
                data = data2,
                x_column='YEAR',
                y_column='value',
                color_column='REGION',
                title=f"Escenario: {scenario2}, Archivo: {file2}",
            )
        else:
            line_chart_2 = px.line(title="No se encontraron datos para el segundo archivo")

        return line_chart_1, line_chart_2
    
    @app.callback(
    Output('combined-line-chart', 'figure'),
    [Input('scenario-checklist', 'value'),
     Input('file-dropdown-1', 'value'),
     Input('region-checklist', 'value')]
)
    def update_combined_line_chart(selected_scenarios, selected_file, selected_regions):
        if not selected_scenarios or not selected_file:
            return px.line(title="Selecciona al menos un escenario y un archivo para visualizar los datos")

        combined_data = []
        for scenario in selected_scenarios:
            if scenario in data_cache and selected_file in data_cache[scenario]:
                data = data_cache[scenario][selected_file]
                if selected_regions:
                    data = data[data['REGION'].isin(selected_regions)]
                data['SCENARIO'] = scenario  # Añadir la columna de escenario
                combined_data.append(data)

        if not combined_data:
            return px.line(title="No se encontraron datos para los escenarios seleccionados")

        combined_data = pd.concat(combined_data)

        # Crear el gráfico combinado
        combined_chart = create_combined_line_chart(
            data = combined_data,
            x_column='YEAR',
            y_column='value',
            color_column='SCENARIO',
            line_group_column='REGION',
            title=f"{selected_file} For all Scenarios",
        )
        return combined_chart
    @app.callback(
        Output('bar-chart', 'figure'),
        [Input('scenario-checklist', 'value')]
    )
    def update_bar_chart(selected_scenarios):
        total_costs = []
        for scenario, files in dependency_files.items():
            for file_name, file_path in files.items():
                if 'TotalDiscountedCost' in file_name:
                    try:
                        data = pd.read_csv(file_path)
                        if not data.empty and 'value' in data.columns:
                            total_cost = data['value'].sum()
                            total_costs.append({'Scenario': scenario, 'TotalDiscountedCost': total_cost})
                    except Exception as e:
                        print(f"Error al leer el archivo {file_path}: {e}")

        if not total_costs:
            return create_bar_chart(pd.DataFrame(), "Scenario", "TotalDiscountedCost", "Scenario", "No se encontraron datos")

        total_costs_df = pd.DataFrame(total_costs)

        # Crear el gráfico de barras con el nuevo estilo
        return create_bar_chart(
            data=total_costs_df,
            x_column='Scenario',
            y_column='TotalDiscountedCost',
            color_column='Scenario',
            title="Comparación de TotalDiscountedCost entre todos los escenarios"
        )






    return app


def create_app_5(hourly_data, color_variations):
    """
    Crea una aplicación Dash para visualizar datos transformados a formato horario.

    Args:
        hourly_data (dict): Diccionario con los datos transformados por escenario.
        color_variations (dict): Diccionario con los colores asignados a las tecnologías.

    Returns:
        Dash: Aplicación Dash configurada.
    """
    app = Dash(__name__)

    # Layout de la aplicación
    app = Dash(__name__, suppress_callback_exceptions=True)  # Permitir excepciones de callbacks

    # Layout de la aplicación
    app.layout = html.Div([
        html.H1("App 5: Visualización de Datos Horarios", style={'textAlign': 'center'}),
        html.Div([
            html.Label("Selecciona la unidad:", style={'font-size': '16px'}),
            dcc.RadioItems(
                id='unit-selector',
                options=[
                    {'label': 'PJ', 'value': 'PJ'},
                    {'label': 'TWh', 'value': 'TWh'},
                    {'label': 'GWh', 'value': 'GWh'},
                    {'label': 'MWh', 'value': 'MWh'}
                ],
                value='PJ',  # Unidad predeterminada
                inline=True,
                style={'font-size': '16px'}
            )
        ], style={'margin-bottom': '20px'}),
        html.Div([
            html.Div([
                html.Label("Selecciona el escenario:", style={'font-size': '16px'}),
                dcc.Dropdown(
                    id='scenario-dropdown-1',
                    options=[{'label': scenario, 'value': scenario} for scenario in hourly_data.keys()],
                    value=list(hourly_data.keys())[0],
                    style={'width': '80%'}
                ),
                html.Label("Selecciona el archivo:", style={'font-size': '16px', 'margin-top': '10px'}),
                dcc.Dropdown(
                    id='file-dropdown-1',
                    options=[],
                    value=None,
                    style={'width': '80%'}
                ),
                html.Div([
                    html.Label("Selecciona los TIMESLICE:", style={'font-size': '16px'}),
                    html.Div([
                        html.Button(
                            "Abrir/Cerrar Dropdown",
                            id='toggle-dropdown-button-1',
                            n_clicks=0,
                            style={'margin-bottom': '10px'}
                        ),
                        html.Div(
                            id='dropdown-menu-1',
                            style={
                                'display': 'none',  # Oculto por defecto
                                'border': '1px solid #ccc',
                                'padding': '10px',
                                'background-color': 'white',
                                'position': 'absolute',
                                'zIndex': 1000,
                                'width': '300px'
                            },
                            children=[
                                dcc.Input(
                                    id='timeslice-search-1',
                                    type='text',
                                    placeholder="Escribe para filtrar TIMESLICE...",
                                    style={'width': '100%', 'margin-bottom': '10px'}
                                ),
                                dcc.Checklist(
                                    id='timeslice-checklist-1',
                                    options=[],  # Se llenará dinámicamente
                                    value=[],  # Selección inicial vacía
                                    inline=False,
                                    style={'font-size': '16px', 'display': 'flex', 'flex-wrap': 'wrap', 'gap': '10px'}
                                ),
                                html.Button(
                                    "Seleccionar/Deseleccionar todas",
                                    id='checkall-button-1',
                                    n_clicks=0,
                                    style={'margin-top': '10px'}
                                )
                            ]
                        )
                    ], style={'position': 'relative'})
                ], style={'margin-bottom': '20px'}),
                html.Label("Selecciona el año:", style={'font-size': '16px', 'margin-top': '10px'}),
                dcc.Dropdown(
                    id='year-dropdown-1',
                    options=[],  # Se llenará dinámicamente
                    value=None,
                    style={'width': '80%'}
                ),
                html.Label("Selecciona las tecnologías:", style={'font-size': '16px', 'margin-top': '10px'}),
                dcc.Checklist(
                    id='technology-checklist-1',
                    options=[],
                    value=[],
                    inline=False,
                    style={'font-size': '16px', 'display': 'flex', 'flex-wrap': 'wrap', 'gap': '10px'}
                )
            ], style={'width': '48%', 'display': 'inline-block'}),
            html.Div([
                html.Label("Selecciona el escenario:", style={'font-size': '16px'}),
                dcc.Dropdown(
                    id='scenario-dropdown-2',
                    options=[{'label': scenario, 'value': scenario} for scenario in hourly_data.keys()],
                    value=list(hourly_data.keys())[0],
                    style={'width': '80%'}
                ),
                html.Label("Selecciona el archivo:", style={'font-size': '16px', 'margin-top': '10px'}),
                dcc.Dropdown(
                    id='file-dropdown-2',
                    options=[],
                    value=None,
                    style={'width': '80%'}
                ),
                html.Div([
                    html.Label("Selecciona los TIMESLICE:", style={'font-size': '16px'}),
                    html.Div([
                        html.Button(
                            "Abrir/Cerrar Dropdown",
                            id='toggle-dropdown-button-2',
                            n_clicks=0,
                            style={'margin-bottom': '10px'}
                        ),
                        html.Div(
                            id='dropdown-menu-2',
                            style={
                                'display': 'none',  # Oculto por defecto
                                'border': '1px solid #ccc',
                                'padding': '10px',
                                'background-color': 'white',
                                'position': 'absolute',
                                'zIndex': 1000,
                                'width': '300px'
                            },
                            children=[
                                dcc.Input(
                                    id='timeslice-search-2',
                                    type='text',
                                    placeholder="Escribe para filtrar TIMESLICE...",
                                    style={'width': '100%', 'margin-bottom': '10px'}
                                ),
                                dcc.Checklist(
                                    id='timeslice-checklist-2',
                                    options=[],  # Se llenará dinámicamente
                                    value=[],  # Selección inicial vacía
                                    inline=False,
                                    style={'font-size': '16px', 'display': 'flex', 'flex-wrap': 'wrap', 'gap': '10px'}
                                ),
                                html.Button(
                                    "Seleccionar/Deseleccionar todas",
                                    id='checkall-button-2',
                                    n_clicks=0,
                                    style={'margin-top': '10px'}
                                )
                            ]
                        )
                    ], style={'position': 'relative'})
                ], style={'margin-bottom': '20px'}),
                html.Label("Selecciona el año:", style={'font-size': '16px', 'margin-top': '10px'}),
                dcc.Dropdown(
                    id='year-dropdown-2',
                    options=[],  # Se llenará dinámicamente
                    value=None,
                    style={'width': '80%'}
                ),
                html.Label("Selecciona las tecnologías:", style={'font-size': '16px', 'margin-top': '10px'}),
                dcc.Checklist(
                    id='technology-checklist-2',
                    options=[],
                    value=[],
                    inline=False,
                    style={'font-size': '16px', 'display': 'flex', 'flex-wrap': 'wrap', 'gap': '10px'}
                )
            ], style={'width': '48%', 'display': 'inline-block'})
        ]),
        html.Div([
            dcc.Graph(id='hourly-stacked-area-chart-1', style={'width': '48%', 'display': 'inline-block'}),
            dcc.Graph(id='hourly-stacked-area-chart-2', style={'width': '48%', 'display': 'inline-block'})
        ])
    ])
    @app.callback(
        Output('dropdown-menu-1', 'style'),
        [Input('toggle-dropdown-button-1', 'n_clicks')],
        [State('dropdown-menu-1', 'style')]
    )
    def toggle_dropdown_1(n_clicks, current_style):
        if n_clicks % 2 == 1:
            # Mostrar el menú
            return {**current_style, 'display': 'block'}
        # Ocultar el menú
        return {**current_style, 'display': 'none'}
    @app.callback(
        Output('dropdown-menu-2', 'style'),
        [Input('toggle-dropdown-button-2', 'n_clicks')],
        [State('dropdown-menu-2', 'style')]
    )
    def toggle_dropdown_2(n_clicks, current_style):
        if n_clicks % 2 == 1:
            # Mostrar el menú
            return {**current_style, 'display': 'block'}
        # Ocultar el menú
        return {**current_style, 'display': 'none'}



    @app.callback(
            [Output('timeslice-checklist-1', 'options'),
            Output('timeslice-checklist-1', 'value')],
            [Input('scenario-dropdown-1', 'value'),
            Input('file-dropdown-1', 'value'),
            Input('timeslice-search-1', 'value'),
            Input('checkall-button-1', 'n_clicks')],
            [State('timeslice-checklist-1', 'value')]
        )
    def update_timeslice_checklist_1(selected_scenario, selected_file, search_value, n_clicks, current_selection):
            if selected_scenario and selected_file:
                data = hourly_data[selected_scenario][selected_file]
                timeslices = sorted(data['TIMESLICE'].unique())

                # Filtrar opciones según el texto ingresado
                if search_value:
                    filtered_timeslices = [ts for ts in timeslices if search_value.lower() in str(ts).lower()]
                else:
                    filtered_timeslices = timeslices

                options = [{'label': ts, 'value': ts} for ts in filtered_timeslices]

                # Alternar selección/deselección de todas las opciones visibles
                # ctx = dash.callback_context
                if ctx.triggered and 'checkall-button-1' in ctx.triggered[0]['prop_id']:
                    if set(current_selection) == set(filtered_timeslices):
                        # Si todas las opciones visibles están seleccionadas, deseleccionarlas
                        return options, []
                    else:
                        # Si no todas están seleccionadas, seleccionarlas todas
                        return options, filtered_timeslices

                # Mantener selecciones válidas
                selected_timeslices = [ts for ts in current_selection if ts in filtered_timeslices]

                return options, selected_timeslices
            return [], []

    @app.callback(
            [Output('timeslice-checklist-2', 'options'),
            Output('timeslice-checklist-2', 'value')],
            [Input('scenario-dropdown-2', 'value'),
            Input('file-dropdown-2', 'value'),
            Input('timeslice-search-2', 'value'),
            Input('checkall-button-2', 'n_clicks')],
            [State('timeslice-checklist-2', 'value')]
        )
    def update_timeslice_checklist_2(selected_scenario, selected_file, search_value, n_clicks, current_selection):
            if selected_scenario and selected_file:
                data = hourly_data[selected_scenario][selected_file]
                timeslices = sorted(data['TIMESLICE'].unique())

                # Filtrar opciones según el texto ingresado
                if search_value:
                    filtered_timeslices = [ts for ts in timeslices if search_value.lower() in str(ts).lower()]
                else:
                    filtered_timeslices = timeslices

                options = [{'label': ts, 'value': ts} for ts in filtered_timeslices]

                # Alternar selección/deselección de todas las opciones visibles
                # ctx = dash.callback_context
                if ctx.triggered and 'checkall-button-1' in ctx.triggered[0]['prop_id']:
                    if set(current_selection) == set(filtered_timeslices):
                        # Si todas las opciones visibles están seleccionadas, deseleccionarlas
                        return options, []
                    else:
                        # Si no todas están seleccionadas, seleccionarlas todas
                        return options, filtered_timeslices

                # Mantener selecciones válidas
                selected_timeslices = [ts for ts in current_selection if ts in filtered_timeslices]

                return options, selected_timeslices
            return [], []

    # Callback para actualizar los dropdowns y checklists dinámicamente
    @app.callback(
        [Output('file-dropdown-1', 'options'),
        Output('file-dropdown-1', 'value'),
        Output('year-dropdown-1', 'options'),
        Output('year-dropdown-1', 'value'),
        Output('technology-checklist-1', 'options'),
        Output('technology-checklist-1', 'value')],
        [Input('scenario-dropdown-1', 'value')],
        [State('file-dropdown-1', 'value'),
        State('year-dropdown-1', 'value'),
        State('technology-checklist-1', 'value')]
    )
    def update_dropdowns_1(selected_scenario, current_file, current_year, current_technologies):
        if selected_scenario:
            files = hourly_data[selected_scenario].keys()
            data = hourly_data[selected_scenario][list(files)[0]]
            years = data['YEAR'].unique()
            technologies = data['TECHNOLOGY'].unique()

            file_options = [{'label': file, 'value': file} for file in files]
            year_options = [{'label': year, 'value': year} for year in sorted(years)]
            technology_options = [{'label': tech, 'value': tech} for tech in sorted(technologies)]

            # Mantener selecciones si son válidas
            selected_file = current_file if current_file in files else list(files)[0]
            selected_year = current_year if current_year in years else years[0]
            selected_technologies = [tech for tech in current_technologies if tech in technologies] if current_technologies else list(technologies)

            return file_options, selected_file, year_options, selected_year, technology_options, selected_technologies
        return [], None, [], None, [], None

    # Repetir el callback para el segundo conjunto de dropdowns y checklists
    @app.callback(
        [Output('file-dropdown-2', 'options'),
        Output('file-dropdown-2', 'value'),
        Output('year-dropdown-2', 'options'),
        Output('year-dropdown-2', 'value'),
        Output('technology-checklist-2', 'options'),
        Output('technology-checklist-2', 'value')],
        [Input('scenario-dropdown-2', 'value')],
        [State('file-dropdown-2', 'value'),
        State('year-dropdown-2', 'value'),
        State('technology-checklist-2', 'value')]
    )
    def update_dropdowns_2(selected_scenario, current_file, current_year, current_technologies):
        if selected_scenario:
            files = hourly_data[selected_scenario].keys()
            data = hourly_data[selected_scenario][list(files)[0]]
            years = data['YEAR'].unique()
            technologies = data['TECHNOLOGY'].unique()

            file_options = [{'label': file, 'value': file} for file in files]
            year_options = [{'label': year, 'value': year} for year in sorted(years)]
            technology_options = [{'label': tech, 'value': tech} for tech in sorted(technologies)]

            # Mantener selecciones si son válidas
            selected_file = current_file if current_file in files else list(files)[0]
            selected_year = current_year if current_year in years else years[0]
            selected_technologies = [tech for tech in current_technologies if tech in technologies] if current_technologies else list(technologies)

            return file_options, selected_file, year_options, selected_year, technology_options, selected_technologies
        return [], None, [], None, [], None

    # Callback para actualizar los gráficos
    @app.callback(
        [Output('hourly-stacked-area-chart-1', 'figure'),
        Output('hourly-stacked-area-chart-2', 'figure')],
        [Input('scenario-dropdown-1', 'value'),
        Input('file-dropdown-1', 'value'),
        Input('timeslice-checklist-1', 'value'),  # Cambiado de timeslice-dropdown-1 a timeslice-checklist
        Input('year-dropdown-1', 'value'),
        Input('technology-checklist-1', 'value'),
        Input('scenario-dropdown-2', 'value'),
        Input('file-dropdown-2', 'value'),
        Input('timeslice-checklist-2', 'value'),
        Input('year-dropdown-2', 'value'),
        Input('technology-checklist-2', 'value'),
        Input('unit-selector', 'value')]
    )
    def update_area_charts(scenario1, file1, timeslices1, year1, technologies1,
                        scenario2, file2, timeslices2, year2, technologies2, unit):
        # Factores de conversión
        conversion_factors = {
            'PJ': 1,
            'TWh': 0.2778,
            'GWh': 277.8,
            'MWh': 277800
        }
        factor = conversion_factors.get(unit, 1)

        def create_area_chart(scenario, file, timeslices, year, technologies):
            if scenario and file:
                data = hourly_data[scenario][file]
                filtered_data = data[
                    (data['TIMESLICE'].isin(timeslices)) &
                    (data['YEAR'] == year) &
                    (data['TECHNOLOGY'].isin(technologies))
                ]
                filtered_data['VALUE'] *= factor  # Aplicar conversión de unidades

                # Asignar colores a las tecnologías presentes en los datos
                technology_colors = assign_colors_to_technologies(
                    filtered_data, 'TECHNOLOGY', color_variations
                )

                # Crear el gráfico de áreas apiladas
                hourly_data_by_tech = filtered_data.groupby(['HOUR', 'TECHNOLOGY'])['VALUE'].sum().reset_index()
                return px.area(
                    hourly_data_by_tech,
                    x='HOUR',
                    y='VALUE',
                    color='TECHNOLOGY',
                    title=f"Producción Total por Tecnología - {file} ({scenario})",
                    labels={'HOUR': 'Hora', 'VALUE': f'Producción Total ({unit})'},
                    color_discrete_map=technology_colors  # Usar colores asignados dinámicamente
                )
            
            return px.area(title="No se encontraron datos")

        chart1 = create_area_chart(scenario1, file1, timeslices1, year1, technologies1)
        chart1.update_layout(
            title={
                # 'text': title,
                'y': 0.95,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'font': {'size': 15, 'family': 'Arial'}
            },
            # xaxis=dict(
            #     # title=labels.get(x, x),
            #     showgrid=False,
            #     gridcolor='lightgrey',
            #     zeroline=False,
            #     showline=True,
            #     linecolor='black',
            #     tickfont=dict(size=12, family='Arial')
            # ),
            yaxis=dict(
                # title=labels.get(y, y),
                showgrid=False,
                gridcolor='lightgrey',
                zeroline=False,
                showline=True,
                linecolor='black',
                # tickfont=dict(size=12, family='Arial')
            ),
            legend=dict(
                title=dict(text=""), 
                font=dict(size=12, family='Arial'),
                orientation="h",
                yanchor="bottom",
                y=-0.4,
                xanchor="center",
                x=0.5,
                
            ),
            plot_bgcolor='white',
            margin=dict(l=50, r=50, t=50, b=50),
            font=dict(size=14, family='Arial'),
            width=1000,
            height=750,
            template = 'presentation'
        )
        chart1.update_traces(
        line=dict(width=2),
        opacity=0.8
    )   

        chart2 = create_area_chart(scenario2, file2, timeslices2, year2, technologies2)
        chart2.update_layout(
            title={
                # 'text': title,
                'y': 0.95,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'font': {'size': 15, 'family': 'Arial'}
            },
            # xaxis=dict(
            #     # title=labels.get(x, x),
            #     showgrid=False,
            #     gridcolor='lightgrey',
            #     zeroline=False,
            #     showline=True,
            #     linecolor='black',
            #     tickfont=dict(size=12, family='Arial')
            # ),
            yaxis=dict(
                # title=labels.get(y, y),
                showgrid=False,
                gridcolor='lightgrey',
                zeroline=False,
                showline=True,
                linecolor='black',
                # tickfont=dict(size=12, family='Arial')
            ),
            legend=dict(
                title=dict(text=""), 
                font=dict(size=12, family='Arial'),
                orientation="h",
                yanchor="bottom",
                y=-0.4,
                xanchor="center",
                x=0.5,
                
            ),
            plot_bgcolor='white',
            margin=dict(l=50, r=50, t=50, b=50),
            font=dict(size=14, family='Arial'),
            width=1000,
            height=750,
            template = 'presentation'
        )
        chart2.update_traces(
        line=dict(width=2),
        opacity=0.8
    )      
        return chart1, chart2
    return app

# def run_app_1():
#     print("Ejecutando la App 1 en el puerto 8050...")
#     app1 = create_first_app(dependency_files_app1, COLOR_VARIATIONS, scenarios)
#     webbrowser.open("http://127.0.0.1:8050/")
#     app1.run(debug=False, port=8050)

# # Función para ejecutar la App 2
# def run_app_2():
#     print("Ejecutando la App 2 en el puerto 8051...")
#     years = [2019, 2030, 2050]
#     app2 = create_comparison_dashboard_with_options(dependency_files_app2, COLOR_VARIATIONS, years, scenarios)
#     webbrowser.open("http://127.0.0.1:8051/")
#     app2.run(debug=False, port=8051)

# def run_app_3():
#     print("Ejecutando la App 3 en el puerto 8052...")
#     app3 = create_heatmap_app(dependency_files_app1, scenarios)
#     webbrowser.open("http://127.0.0.1:8052/")
#     app3.run(debug=False, port=8052)
# def run_app_4():
#     print("Ejecutando la App 4 en el puerto 8053...")
#     dependency_key = "['REGION','YEAR']"
#     dependency_files_app4 = get_dependency_files(input_files, dependency_key, base_folder="results")
#     webbrowser.open("http://127.0.0.1:8053/")
#     app4 = create_app_4(dependency_files_app4)
#     app4.run(debug=False, port=8053)


def run_app_1(dependency_files_app1, color_variations, scenarios):
    print("Ejecutando la App 1 en el puerto 8050...")
    app1 = create_first_app(dependency_files_app1, color_variations, scenarios)
    webbrowser.open("http://127.0.0.1:8050/")
    app1.run(debug=False, port=8050)

def run_app_2(dependency_files_app2, color_variations, years, scenarios):
    print("Ejecutando la App 2 en el puerto 8051...")
    app2 = create_comparison_dashboard_with_options(dependency_files_app2, color_variations, years, scenarios)
    webbrowser.open("http://127.0.0.1:8051/")
    app2.run(debug=False, port=8051)

def run_app_3(dependency_files_app1, scenarios):
    print("Ejecutando la App 3 en el puerto 8052...")
    app3 = create_heatmap_app(dependency_files_app1, scenarios)
    webbrowser.open("http://127.0.0.1:8052/")
    app3.run(debug=False, port=8052)

def run_app_4(dependency_files_app4):
    print("Ejecutando la App 4 en el puerto 8053...")
    app4 = create_app_4(dependency_files_app4)
    webbrowser.open("http://127.0.0.1:8053/")
    app4.run(debug=False, port=8053)
def run_app_5(base_folder="results", color_variations=COLOR_VARIATIONS):
    """
    Ejecuta la App 5 para visualizar datos horarios.

    Args:
        base_folder (str): Carpeta base donde se encuentran los resultados.
    """
    print("Buscando archivos 'hourly' en las carpetas de resultados...")
    hourly_files = get_hourly_files(base_folder)

    if not hourly_files:
        print("No se encontraron archivos 'hourly'. Verifica las carpetas de resultados.")
        return

    print(f"Archivos encontrados: {hourly_files.keys()}")

    # Cargar los datos desde los archivos encontrados
    hourly_data = {}
    for scenario, files in hourly_files.items():
        scenario_data = {}
        for file_name, file_path in files.items():
            try:
                scenario_data[file_name] = pd.read_csv(file_path)
            except Exception as e:
                print(f"Error al cargar el archivo {file_path}: {e}")
        if scenario_data:
            hourly_data[scenario] = scenario_data

    if not hourly_data:
        print("No se pudieron cargar los datos desde los archivos 'hourly'.")
        return

    # Crear y ejecutar la aplicación Dash
    app5 = create_app_5(hourly_data, COLOR_VARIATIONS)
    print("Ejecutando la App 5 en el puerto 8055...")
    webbrowser.open("http://127.0.0.1:8055/")
    app5.run(debug=False, port=8055, use_reloader=False)

# def run_app_5(dependency_files, bracket_mapping, daytype_mapping, season_mapping):
#     print("Ejecutando la App 5 en el puerto 8055...")

#     # Procesar y guardar los datos horarios
#     hourly_data = process_and_save_hourly_data(dependency_files, bracket_mapping, daytype_mapping, season_mapping)

#     if not hourly_data:
#         print("No se generaron datos horarios. Verifica los archivos de entrada.")
#         return

#     # Crear y ejecutar la aplicación Dash
#     app5 = create_app_5(hourly_data)
#     webbrowser.open("http://127.0.0.1:8055/")
#     app5.run(debug=True, port=8055)

# Ejecutar la aplicación
if __name__ == '__main__':

    # input_files_simple = [

    #     os.path.join(root_folder, 'data/SuperSimpleExpandedReTagStorage.xlsx'),

    #    ]

    dependency_files_app1 = get_dependency_files(input_files_simple, dependency_key_app1, base_folder="results")
    dependency_files_app2 = get_dependency_files(input_files_simple, dependency_key_app2, base_folder="results")
    dependency_files_app4 = get_dependency_files(input_files_simple, dependency_key_app4, base_folder="results")
    # dependency_files_app5 = get_dependency_files(input_files_simple, dependency_key_app5, base_folder="results")
    # run_app_5(dependency_files_app5, bracket_mapping, daytype_mapping, season_mapping)
    


################################################################################################  
################################################################################################
    """
    Aquí es donde calculo el parámetro Production by technology de forma horaria para mostrar despacho. 
    Tengo que pensar para donde moverlo, para no tener que comentarlo cuando ejecute los gráficos.
    """
    dependency_files = get_dependency_files(
        input_files=input_files_simple,  # Lista de archivos de entrada
        dependency_key="['REGION','TIMESLICE','TECHNOLOGY','FUEL','YEAR']",  # Clave de dependencia
        base_folder="results"  # Carpeta donde están los resultados
    )
    
    # process_and_save_hourly_data(
    # dependency_files=dependency_files,
    # yearsplit=yearsplit,
    # specified_demand_profile=specified_demand_profile,
    # bracket_mapping=bracket_mapping,
    # daytype_mapping=daytype_mapping,
    # season_mapping=season_mapping
    # )
    print(dependency_files)

    # process_and_save_hourly_data_parallel(
    #     dependency_files=dependency_files,
    #     yearsplit=yearsplit,
    #     specified_demand_profile=specified_demand_profile,
    #     bracket_mapping=bracket_mapping,
    #     daytype_mapping=daytype_mapping,
    #     season_mapping=season_mapping
    # )
###############################################################################################
###############################################################################################

    # print(dependency_files)
    # hourly_data = transform_to_hourly_extra(dependency_files, bracket_mapping, daytype_mapping, season_mapping)
    # run_app_5(base_folder="results", color_variations=COLOR_VARIATIONS)

# print(dependency_files)

    # scenario = "BaseScenario"  # Cambia esto para probar con otros escenarios
    # line_charts = generate_line_charts_from_dependency(dependency_files, scenario, COLOR_VARIATIONS)

# Mostrar los gráficos generados
# for chart in line_charts:
#     chart.show()
    scenarios = list(dependency_files_app1.keys()) # Solo depende de laos input files, no hay que crear uno para uno pero se podría hacer
    
    ## definir para los gráficos de pastel. Permite ver el porcentaje de cada tecnología en cada año
    years = [2020, 2025, 2030]
    from multiprocessing import Process
    threads = []
    threads.append(Thread(target=run_app_1, args=(dependency_files_app1, COLOR_VARIATIONS, scenarios)))
    threads.append(Thread(target=run_app_2, args=(dependency_files_app2, COLOR_VARIATIONS, years, scenarios)))
    threads.append(Thread(target=run_app_3, args=(dependency_files_app1, scenarios)))
    threads.append(Thread(target=run_app_4, args=(dependency_files_app4,)))
    # threads.append(Thread(target=run_app_5, args=(dependency_files_app5, COLOR_VARIATIONS)))
    # Ejecutar App 5 en un proceso separado
    app5_process = Process(target=run_app_5, args=("results", COLOR_VARIATIONS))
    for thread in threads:
        thread.start()
    app5_process.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()
    # run_app_2(dependency_files_app2, COLOR_VARIATIONS, [2019, 2030, 2050], scenarios)
    # run_app_5(base_folder="results", color_variations=COLOR_VARIATIONS)
    app5_process.join()



    

    # app2keys = "['REGION','TECHNOLOGY', 'FUEL','YEAR']"
    # dependency_files1 = get_dependency_files(input_files, app2keys, base_folder="results")
    # print(dependency_files)

    # scenario = "BaseScenario"  # Cambia esto para probar con otros escenarios
    # line_charts = generate_line_charts_from_dependency(dependency_files1, scenario, COLOR_VARIATIONS)

    # Mostrar los gráficos generados
    # for chart in line_charts:
    #     chart.show()
    # scenarios = list(dependency_files.keys())
    # print(scenarios)
    # files_by_scenario = dependency_files

    # years= [2019, 2030,2055]
    # create_comparison_dashboard_with_options(files_by_scenario, COLOR_VARIATIONS, years, scenarios, files_by_scenario).run(debug=True, port = 8051)