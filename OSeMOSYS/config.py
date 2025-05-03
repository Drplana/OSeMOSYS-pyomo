import os,sys
# include the main library path (the parent folder) in the path environment variable
root_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_folder)

##### Colors for technologies ###
COLOR_DICT = {
    'PWRCRUD001': 'gray',
    'PWRCRUD002': 'dimgray',
    'PWRCRUD003': 'darkgray',
    'PWRCRUD004': 'silver',
    'PWRCRUD005': 'lightgray',
    'PWRCRUD006': 'gainsboro',
    'PWRCRUD007': 'whitesmoke',
    'PWRCRUD008': 'black',
    'PWRHFO01': '#8B0000',
    'PWRNG01': 'orange',
    'PWRNG02': 'darkorange',
    'PWRGHFO2': '#F19953',
    'PWRBIO': '#9ACD32',
    'PWRWND001': 'deepskyblue',
    'PWRWND002': 'deepskyblue',
    'PWRPV01': '#FFD700',
    'PWRPV02': '#CCAC00',
    'PWRCSP': 'gray',
    'PWRFO': '#FF6961',
    'PWRDSL': 'brown',
    'PWRHYD01': '#0d5c91',
    'PWRHYD02': '#1f77b4'
}
keyword_colors = {
        'pv': '#FFD700',  # Amarillo para fotovoltaica
        'solar': '#FFD700',  # Amarillo para solar
        'wind': 'deepskyblue',  # Azul para eólica
        'wnd': 'deepskyblue',  # Azul para eólica
        'hyd': '#0d5c91',  # Azul oscuro para hidroeléctrica
        'hydro': '#1f77b4',  # Azul oscuro para hidroeléctrica
        'csp': 'yellow',  # Gris para energía solar concentrada
        'bio': '#9ACD32',  # Verde para biomasa
        'coal': 'gray',  # Gris para carbón
        'gas': 'orange',  # Naranja para gas
        'oil': '#8B0000',  # Rojo oscuro para petróleo
        'nuclear': '#FF6961',  # Rojo claro para nuclear
        'crud': 'gray',  # Gris oscuro para crudo
        'hfo': '#F19953',  # Rojo oscuro para fuelóleo pesado
        'lfo': '#FF6961',  # Rojo claro para fuelóleo ligero
        'diesel': 'brown',  # Rojo claro para diésel
        'ng': 'orange',  # Naranja para gas natural
    }






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

INPUT_FILE_PATH = os.path.join(root_folder,'data/SuperSimple.xlsx')


DATA_FILE_PATH = os.path.join(root_folder,'data')

base_results_folder = os.path.join(root_folder, 'results')

# Crear una subcarpeta de resultados basada en el nombre del archivo de entrada
input_file_name = os.path.splitext(os.path.basename(INPUT_FILE_PATH))[0]
RESULTS_FOLDER = os.path.join(base_results_folder, input_file_name)
# print(RESULTS_FOLDER)



try:
    os.makedirs(RESULTS_FOLDER, exist_ok=True)
    print(f"Carpeta de resultados creada: {RESULTS_FOLDER}")
except OSError as e:
    print(f"Error al crear la carpeta de resultados: {e}")
    raise

# Imprimir las rutas para depuración
print(f"Archivo de entrada: {INPUT_FILE_PATH}")
print(f"Carpeta de resultados: {RESULTS_FOLDER}")


# RESULTS_FOLDER = os.path.join(root_folder, 'results/Prueba')
# print(INPUT_FILE_PATH)
# -RESULTS_FOLDER = '../results'

# ROOT_FOLDER = os.path.dirname(os.path.abspath(__file__))

# # Construct the absolute paths
# INPUT_FILE_PATH = os.path.join(ROOT_FOLDER, '../data/OsemosysNew.xlsx')
# RESULTS_FOLDER = os.path.join(ROOT_FOLDER, '../results')