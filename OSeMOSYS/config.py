import os,sys
# include the main library path (the parent folder) in the path environment variable
root_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_folder)
from OSeMOSYS.CalcParam import calculate_yearsplit, calculate_specified_demand_profile, map_daylight_brackets, map_daytypes, map_seasons
import pandas as pd






########################
""" Scenarios created"""
########################
# INPUT_FILE_PATH = os.path.join(root_folder,'data/OsemosysNewDatos.xlsx')

# INPUT_FILE_PATH = os.path.join(root_folder,'data/OsemosysNewDatos1000Recupera.xlsx')

# INPUT_FILE_PATH = os.path.join(root_folder,'data/OsemosysNewDatosNoRecupera.xlsx')

# INPUT_FILE_PATH = os.path.join(root_folder,'data/OsemosysNewDatosBAU37CSP.xlsx')

# INPUT_FILE_PATH = os.path.join(root_folder,'data/OsemosysNewDatosFreeRE.xlsx')
# INPUT_FILE_PATH = os.path.join(root_folder,'data/OsemosysNewDatosNG.xlsx')

"""Scenario with 1000 MW of Biomass due to literature review"""
# INPUT_FILE_PATH = os.path.join(root_folder,'data/OsemosysNewDatosFreeBiomass1000MW.xlsx')

"""Scenario up to 37 % of renewables. Current Policy Scenario. Parameter RE_AtLeast a should be changed to 1 in the Constraint/ReTagTech.py file."""
# INPUT_FILE_PATH = os.path.join(root_folder,'data/OsemosysNewDatosFreeBiomass1000MWUp37.xlsx')

# INPUT_FILE_PATH = os.path.join(root_folder,'data/SuperSimple.xlsx')


# DATA_FILE_PATH = os.path.join(root_folder,'data')

# base_results_folder = os.path.join(root_folder, 'results')

# # Crear una subcarpeta de resultados basada en el nombre del archivo de entrada
# input_file_name = os.path.splitext(os.path.basename(INPUT_FILE_PATH))[0]
# RESULTS_FOLDER = os.path.join(base_results_folder, input_file_name)
# print(RESULTS_FOLDER)



# try:
#     os.makedirs(RESULTS_FOLDER, exist_ok=True)
#     print(f"Carpeta de resultados creada: {RESULTS_FOLDER}")
# except OSError as e:
#     print(f"Error al crear la carpeta de resultados: {e}")
#     raise

# # Imprimir las rutas para depuración
# print(f"Archivo de entrada: {INPUT_FILE_PATH}")
# print(f"Carpeta de resultados: {RESULTS_FOLDER}")
def configure_paths(input_file_path, root_folder):
    """
    Configura las rutas de entrada y resultados basadas en el archivo de entrada.

    Args:
        input_file_path (str): Ruta del archivo de entrada.
        root_folder (str): Carpeta raíz del proyecto.

    Returns:
        dict: Diccionario con las rutas configuradas.
    """
    # Ruta de la carpeta de datos
    data_file_path = os.path.join(root_folder, 'data')

    # Carpeta base de resultados
    base_results_folder = os.path.join(root_folder, 'results')

    # Nombre del archivo de entrada sin extensión
    input_file_name = os.path.splitext(os.path.basename(input_file_path))[0]

    # Carpeta de resultados específica para el archivo de entrada
    results_folder = os.path.join(base_results_folder, input_file_name)
    # root_folder = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

    # Definir la carpeta de salida global
    # output_base_folder = os.path.join(root_folder, "data") # datafile path

    # Obtener el nombre del archivo sin extensión
    file_name = os.path.splitext(os.path.basename(input_file_path))[0]

    # Crear la carpeta de salida basada en el nombre del archivo
    output_folder_data = os.path.join(data_file_path, input_file_name)
    

    # Generar la ruta completa del archivo de datos json de salida
    # output_json_data_path = os.path.join(output_folder_data, f"{file_name}.json")

    # Crear la carpeta de resultados si no existe
    try:
        os.makedirs(results_folder, exist_ok=True)
        print(f"Carpeta de resultados creada: {results_folder}")
        os.makedirs(output_folder_data, exist_ok=True)
        print(f"Carpeta de salida creada: {output_folder_data}")
        output_json_data_path = os.path.join(output_folder_data, f"{file_name}.json")
        print(f"Ruta del archivo JSON de salida: {output_json_data_path}")          
    

    except OSError as e:
        print(f"Error al crear la carpeta de resultados: {e}")
        raise

    # Retornar las rutas configuradas
    return {
        "INPUT_FILE_PATH": input_file_path,
        "DATA_FILE_PATH": data_file_path,
        "BASE_RESULTS_FOLDER": base_results_folder,
        "RESULTS_FOLDER": results_folder,
        "OUTPUT_FOLDER_DATA": output_folder_data,
        "OUTPUT_JSON_DATA_PATH": output_json_data_path

    }

# RESULTS_FOLDER = os.path.join(root_folder, 'results/Prueba')
# print(INPUT_FILE_PATH)
# -RESULTS_FOLDER = '../results'

# ROOT_FOLDER = os.path.dirname(os.path.abspath(__file__))

# # Construct the absolute paths
# INPUT_FILE_PATH = os.path.join(ROOT_FOLDER, '../data/OsemosysNew.xlsx')
# RESULTS_FOLDER = os.path.join(ROOT_FOLDER, '../results')



input_files_simple = [

    # os.path.join(root_folder, 'data/SuperSimpleExpanded.xlsx'),
    # ## Variante para forzar el modelo a producir hasta una cierta cantidad de energía renovable. 
    # # Se cambia el sentido de la desigualdad.
    # os.path.join(root_folder, 'data/SuperSimpleExpandedReTag.xlsx'),

    # ## En esta variante inyecto con tbatt a la red de transmisión 
    # # y recibo la energía de la red de transmisión
    # os.path.join(root_folder, 'data/SuperSimpleExpandedReTagStorage.xlsx'),
    # ## En esta variante inyecto con tbatt directamente a la demanda de electricidad 
    # # y recibo la energía de paneles solares y eólica
    # os.path.join(root_folder, 'data/SuperSimpleExpandedReTagStorage2.xlsx'),


os.path.join(root_folder, 'data/01-BaseScenario.xlsx'),
os.path.join(root_folder, 'data/02-BaseScenarioWind.xlsx'),
os.path.join(root_folder, 'data/03-BaseScenarioWindBiomass.xlsx'),
os.path.join(root_folder, 'data/04-BaseScenarioWindBiomassPV.xlsx'),
os.path.join(root_folder, 'data/05-BaseScenarioWindBiomassPVAnnualInvLimit.xlsx'),
os.path.join(root_folder, 'data/06-MustRunTechBase.xlsx'),
# os.path.join(root_folder, 'data/06-BaseScenarioWind.xlsx'),
# os.path.join(root_folder, 'data/03-BaseScenarioWindBiomass.xlsx'),
# os.path.join(root_folder, 'data/04-BaseScenarioWindBiomassPV.xlsx'),
# os.path.join(root_folder, 'data/05-BaseScenarioWindBiomassPVAnnualInvLimit.xlsx'),

]


season_mapping = {
"1": [12, 1, 2],  # Invierno
"2": [3, 4, 5],   # Primavera
"3": [6, 7, 8],   # Verano
"4": [9, 10, 11]  # Otoño
}

daytype_mapping = {
    "1": [0, 1, 2, 3, 4],  # Workdays (lunes a viernes)
    "2": [5, 6]            # Weekends (sábado y domingo)
}

bracket_mapping = {
    "1": list(range(20, 24)) + list(range(0, 1)),
    "2": list(range(1, 6)),
    "3": list(range(6, 8)),
    "4": list(range(8, 11)),
    "5": list(range(11, 13)),
    "6": list(range(13, 16)),
    "7": list(range(16, 18)),
    "8": list(range(18, 20))
}

year = 2023
data = pd.read_excel('/home/david/Documents/001 - Proyectos/CubaOSeMOSYS/DatosCub.xlsx', sheet_name="DEMAND")
if 'Date' not in data.columns:
        print("La columna 'Date' no existe. Creando un rango de fechas automáticamente...")
        start_date = f'{year}-01-01'
        end_date = f'{year}-12-31 23:00:00'
        date_range = pd.date_range(start=start_date, end=end_date, freq='h')
        data['Date'] = date_range
data['Month'] = data['Date'].dt.month
data['Hour'] = data['Date'].dt.hour

data = map_seasons(data, season_mapping)
data = map_daytypes(data, daytype_mapping)
data = map_daylight_brackets(data, bracket_mapping)

yearsplit = calculate_yearsplit(season_mapping, daytype_mapping, bracket_mapping, year)
yearsplit = yearsplit[['TIMESLICE', 'YearSplit']]

# print(yearsplit)


# Calcular Specified Demand Profile
specified_demand_profile = calculate_specified_demand_profile(data)
specified_demand_profile = specified_demand_profile[['TIMESLICE', 'SpecifiedDemandProfile']]


yearsplit = yearsplit.set_index('TIMESLICE')['YearSplit']
specified_demand_profile = specified_demand_profile.set_index('TIMESLICE')['SpecifiedDemandProfile']
yearsplit.index = yearsplit.index.astype(int)
specified_demand_profile.index = specified_demand_profile.index.astype(int)
print(yearsplit)