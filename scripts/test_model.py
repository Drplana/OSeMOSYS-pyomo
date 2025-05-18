'''
This file illustrates the use of the osemodsys-pyomo library to run a test case

It loads the main function from the library and provides as parameters the input excel file and the folder where
the results should be written
'''
import os,sys
# include the main library path (the parent folder) in the path environment variable
root_folder = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(root_folder)
import time


#Two solution to import the library
# (1) as a package (defined in __init__.py) => function calls are done through the lpackage (eg om.solve_model)
import OSeMOSYS as om

# (2) as separate functions:
from OSeMOSYS.readXlsData import load_dataframes, transform_all_dataframes, save_dataframes_to_csv, dict_to_json, adjust_json_for_pyomo, export_to_json
from OSeMOSYS.SolveSolutions import solve_model, export_results
from OSeMOSYS.postprocessing.plots import plot_activity, assign_colors
from OSeMOSYS.config import configure_paths
from OSeMOSYS.utils import COLOR_VARIATIONS, modify_parameter, dataframe_metadata
from pyomo.environ import DataPortal
from concurrent.futures import ProcessPoolExecutor
from OSeMOSYS.ReadSets import load_sets
from multiprocessing import Pool
import traceback

from OSeMOSYS.ScenariosManager import ScenarioManager
class DimensionManager:
    def __init__(self, sets):
        """
        Inicializa el gestor de dimensiones con los sets cargados.

        Args:
            sets (dict): Diccionario con los sets del modelo.
        """
        self.dimensions = sets

    def get_all_dimensions(self):
        """
        Devuelve todas las dimensiones disponibles.

        Returns:
            dict: Diccionario con todas las dimensiones.
        """
        return self.dimensions

    def get_filtered_dimensions(self, regions=None, technologies=None, years=None, fuels=None, seasons=None, daytypes=None, dailytimebrackets=None, timeslices=None, modes_of_operation=None, storages=None, emissions=None):
        """
        Filtra las dimensiones según los criterios especificados.

        Args:
            regions (list, opcional): Lista de regiones a incluir.
            technologies (list, opcional): Lista de tecnologías a incluir.
            years (list, opcional): Lista de años a incluir.
            fuels (list, opcional): Lista de combustibles a incluir.
            seasons (list, opcional): Lista de estaciones a incluir.
            daytypes (list, opcional): Lista de tipos de día a incluir.
            dailytimebrackets (list, opcional): Lista de brackets de tiempo diario a incluir.
            timeslices (list, opcional): Lista de timeslices a incluir.
            modes_of_operation (list, opcional): Lista de modos de operación a incluir.
            storages (list, opcional): Lista de almacenamientos a incluir.
            emissions (list, opcional): Lista de emisiones a incluir.

        Returns:
            dict: Diccionario con las dimensiones filtradas.
        """
        return {
            "REGION": regions if regions else self.dimensions["REGION"],
            "TECHNOLOGY": technologies if technologies else self.dimensions["TECHNOLOGY"],
            "YEAR": years if years else self.dimensions["YEAR"],
            "FUEL": fuels if fuels else self.dimensions["FUEL"],
            "SEASON": seasons if seasons else self.dimensions["SEASON"],
            "DAYTYPE": daytypes if daytypes else self.dimensions["DAYTYPE"],
            "DAILYTIMEBRACKET": dailytimebrackets if dailytimebrackets else self.dimensions["DAILYTIMEBRACKET"],
            "TIMESLICE": timeslices if timeslices else self.dimensions["TIMESLICE"],
            "MODE_OF_OPERATION": modes_of_operation if modes_of_operation else self.dimensions["MODE_OF_OPERATION"],
            "STORAGE": storages if storages else self.dimensions["STORAGE"],
            "EMISSION": emissions if emissions else self.dimensions["EMISSION"]
        }

# print(f"Root folder: {root_folder}")

#############################################################################################################
""" Defining multiple input files for running in parallel in the function at the bottom ```process_file``"""
#############################################################################################################

input_files_simple = [

    os.path.join(root_folder, 'data/SuperSimpleExpanded.xlsx'),
    ## Variante para forzar el modelo a producir hasta una cierta cantidad de energía renovable. 
    # Se cambia el sentido de la desigualdad.
    os.path.join(root_folder, 'data/SuperSimpleExpandedReTag.xlsx'),

    ## En esta variante inyecto con tbatt a la red de transmisión 
    # y recibo la energía de la red de transmisión
    os.path.join(root_folder, 'data/SuperSimpleExpandedReTagStorage.xlsx'),
    ## En esta variante inyecto con tbatt directamente a la demanda de electricidad 
    # y recibo la energía de paneles solares solamente. No puede invertir en nada que no sea solar
    os.path.join(root_folder, 'data/SuperSimpleExpandedReTagStorage2.xlsx'),
    ### En esta variante inyecto con tbatt directamente a la demanda de electricidad
    # y recibo la energía de paneles solares y eólica 
    os.path.join(root_folder, 'data/SuperSimpleExpandedReTagStorage2a.xlsx'),

    ### Recibo la energía de paneles solares y eólica pero puede bypasear el almacenamiento.
    os.path.join(root_folder, 'data/SuperSimpleExpandedReTagStorage3.xlsx'),
    ### Recibo la energía de paneles solares y eólica limitada a 50 MW.
    os.path.join(root_folder, 'data/SuperSimpleExpandedReTagStorage4.xlsx'),



    #### Discusión con manuel de resultados de almacenamiento
    os.path.join(root_folder, 'data/SuperSimpleExpandedReTagStorageDiscussion.xlsx'), # Capital Cost del panel solar a 300 $/kW
    os.path.join(root_folder, 'data/SuperSimpleExpandedReTagStorageDiscussionNoStg.xlsx'), # No puede almacenar
    os.path.join(root_folder, 'data/SuperSimpleExpandedReTagStorageDiscussion400.xlsx'), # Capital Cost del panel solar a 400 $/kW
    os.path.join(root_folder, 'data/SuperSimpleExpandedReTagStorageDiscussionBatt10.xlsx') # Bajar el precio de la batería conectada a la linea de PV a 10 $/kWh


]


#############################################################################################################
""" Defining multiple input files for running in parallel in the function at the bottom ```process_file``"""
#############################################################################################################

# input_files_base_scenarios = [
#     os.path.join(root_folder, 'data/01-BaseScenario.xlsx'),
#     os.path.join(root_folder, 'data/02-BaseScenarioWind.xlsx'),
#     os.path.join(root_folder, 'data/03-BaseScenarioWindBiomass.xlsx'),
#     os.path.join(root_folder, 'data/04-BaseScenarioWindBiomassPV.xlsx'),
#     os.path.join(root_folder, 'data/05-BaseScenarioWindBiomassPVAnnualInvLimit.xlsx'),


# ]

input_files_base_scenarios = [
    # os.path.join(root_folder, 'data/01-BaseScenario.xlsx'),
    # os.path.join(root_folder, 'data/02-BaseScenarioWind.xlsx'),
    # os.path.join(root_folder, 'data/03-BaseScenarioWindBiomass.xlsx'),
    # os.path.join(root_folder, 'data/04-BaseScenarioWindBiomassPV.xlsx'),
    # os.path.join(root_folder, 'data/05-BaseScenarioWindBiomassPVAnnualInvLimit.xlsx'),

    os.path.join(root_folder, 'data/06-MustRunTechBase.xlsx'),
]




###################################################################### 
"""Recapitalización de unidades y uso de la restriccion de MustRun"""
#######################################################################
input_files2 = [
    os.path.join(root_folder, 'data/RecapMustRun.xlsx'),
    os.path.join(root_folder, 'data/RecapitalizarUnidades.xlsx'),
]

input_files3 = [os.path.join(root_folder, 'data/RecapitalizarUnidades600.xlsx'),
                os.path.join(root_folder, 'data/RecapitalizarUnidades700.xlsx'),
                os.path.join(root_folder, 'data/RecapitalizarUnidades800.xlsx'),
                
                
                ]



input_files4 = [os.path.join(root_folder, 'data/RecapitalizarUnidades500.xlsx'),
                os.path.join(root_folder, 'data/RecapitalizarUnidadesAll2025.xlsx'),
                ] 
input_files5 = [os.path.join(root_folder, 'data/RetroffUnits700-24RE-NoBio.xlsx'),
                os.path.join(root_folder, 'data/RetroffUnits700-24REBio2030.xlsx'),
                os.path.join(root_folder, 'data/RetroffUnits700-24REBio2025.xlsx'),

                ]       


########################
"""paper"""
#########################
input_files_paper = [
    os.path.join(root_folder, 'data/BaseScenario.xlsx'),
    os.path.join(root_folder, 'data/BaseScenarioWind.xlsx'),
    os.path.join(root_folder, 'data/BaseScenarioWindBiomass.xlsx'),
    os.path.join(root_folder, 'data/BaseScenarioAnualCapLim.xlsx'),
    os.path.join(root_folder, 'data/RecapitalizarUnidades500.xlsx'),
    os.path.join(root_folder, 'data/RecapitalizarUnidades600.xlsx'),
                os.path.join(root_folder, 'data/RecapitalizarUnidades700.xlsx'),
                os.path.join(root_folder, 'data/RecapitalizarUnidades800.xlsx'),
    
    
    


]


#####################################################################
"""Storage options"""
#####################################################################







# results_folders={}
# data_folder = {}
# json_file_path = {}
# for input_file in input_files:
#     paths = configure_paths(input_file, root_folder)
#     results_folders[input_file] = paths['RESULTS_FOLDER']
#     data_folder[input_file] = paths['OUTPUT_FOLDER_DATA']
#     json_file_path[input_file]  = paths['OUTPUT_JSON_DATA_PATH']

#     # print(f"Archivo: {paths['INPUT_FILE_PATH']}")
#     # print(f"Carpeta de resultados: {paths['RESULTS_FOLDER']}")
# # print(json_file_path)
# # print(input_files[0])

# plot_files_1 = {
#     "Production by Technology Annual": os.path.join(results_folders[input_files[0]], "ProductionByTechnologyAnnual.csv"),
#     "Use by Technology Annual": os.path.join(results_folders[input_files[0]], "UseByTechnologyAnnual.csv")
# }
# # print(plot_files_1)






# ###############################################################
# """ Exporting the dataframes to CSV files and JSON files """
# ###############################################################
# json_file_path = json_file_path[input_files[0]]
# file1 = (str(input_files[0]))
# dataframe = load_dataframes(file1)
# transf_data = transform_all_dataframes(dataframe)
# dict_to_be_adjusted = dict_to_json(transf_data, file1)
# pyomo_dict =adjust_json_for_pyomo(dict_to_be_adjusted)
# export_to_json(pyomo_dict, json_file_path)

### ############################################################################
"""This change the RETag equation sign to be able to investigate what
are the share of renewables in the system 
1 is used to force the model to produce a certain amount of renewable energy
0 is used to force the model to produce up to a certain amount of renewable energy 
"""
# RE_AtLeast = 1 # Ned to put this in the REtag equation
##################################################################################


"""Exporting the dataframes to CSV files
save_dataframes_to_csv(transf_data, file1)
Pudiera ser útil para algo más adelante
"""

###############################################################
""" Running the model for the first file """
###############################################################
solver_name = "gurobi"  # Cambia esto al nombre del solver que estés usando

"""
solver_options = {"TimeLimit": 600, "MIPGap": 0.01} 

instance = solve_model(
    input_file=file1,
    solver_name=solver_name,
    json_file_path_or_dict=json_file_path, ###dictionaries have to be adjusted in another way 
    solver_options=solver_options,
    tee=True
)
"""


###############################################################
""" Working in parallel """
###############################################################
# import hashlib
# def process_file(input_file, parameter_name=None, parameter_value=None, dataframe_metadata=None, dimension_manager=None, filters=None, additional_parameters=None, subscenario_name=None):
#     # from OSeMOSYS.utils import dataframe_metadata
#     """
#     function for processing several input files using the format below:
#     input_files = [
#     os.path.join(root_folder, 'data/file1.xlsx'),
#     os.path.join(root_folder, 'data/file2.xlsx')
# ]
#     """
#     try:
#         print(f"Iniciando procesamiento para: {input_file}, subescenario: {subscenario_name}")
#         # Configurar rutas para cada archivo
#         paths = configure_paths(input_file, root_folder)

#         # Usar el nombre del subescenario proporcionado o generar uno automáticamente
#         if not subscenario_name:
#             if isinstance(parameter_value, dict):
#                 value_hash = hashlib.md5(str(parameter_value).encode()).hexdigest()[:8]
#                 subscenario_name = f"{parameter_name}_{value_hash}"
#             else:
#                 subscenario_name = f"{parameter_name}_{parameter_value}"

#         results_folder = os.path.join(paths['RESULTS_FOLDER'], subscenario_name)
#         os.makedirs(results_folder, exist_ok=True)

#         json_file_path = os.path.join(
#             paths['OUTPUT_FOLDER_DATA'], 
#             f"{os.path.basename(input_file).replace('.xlsx', '')}_{subscenario_name}.json"
#         )


#         print(f"Procesando archivo de entrada: {input_file}")
#         print(f"Resultados se guardarán en: {results_folder}")

#         start_time = time.time()
#         # Cargar y transformar los datos
#         dataframe = load_dataframes(input_file)
#         transf_data = transform_all_dataframes(dataframe)
#         dict_to_be_adjusted = dict_to_json(transf_data, input_file)
#         pyomo_dict = adjust_json_for_pyomo(dict_to_be_adjusted)


#         if parameter_name and parameter_value is not None:
#             modify_parameter(pyomo_dict, parameter_name, dataframe_metadata, parameter_value, filters, dimension_manager=dimension_manager, use_existing_keys=True)

#         # Modificar parámetros adicionales
#         if additional_parameters:
#             for param in additional_parameters:
#                 param_name_with_prefix = f"p_{param['name']}"
#                 # print(f"Antes de modificar: {pyomo_dict.get(param_name_with_prefix, [])}")
#                 modify_parameter(pyomo_dict, param["name"], dataframe_metadata, param["values"], param["filters"], dimension_manager=dimension_manager, use_existing_keys=False)
#                 # print(f"Después de modificar: {pyomo_dict.get(param_name_with_prefix, [])}")
#         # if additional_parameters:
#         #     for param in additional_parameters:
#         #         modify_parameter(pyomo_dict, param["name"], dataframe_metadata, param["values"], param["filters"], dimension_manager=dimension_manager)
#         # modify_parameter(pyomo_dict, parameter_name, dataframe_metadata, parameter_value, filters, dimension_manager=dimension_manager)
#         # if filters:
#         #     filtered_dimensions = dimension_manager.get_filtered_dimensions(
#         #         regions=filters.get("REGION"),
#         #         technologies=filters.get("TECHNOLOGY"),
#         #         years=filters.get("YEAR"),
#         #         fuels=filters.get("FUEL"),
#         #         seasons=filters.get("SEASON"),
#         #         daytypes=filters.get("DAYTYPE"),
#         #         dailytimebrackets=filters.get("DAILYTIMEBRACKET"),
#         #         timeslices=filters.get("TIMESLICE"),
#         #         modes_of_operation=filters.get("MODE_OF_OPERATION"),
#         #         storages=filters.get("STORAGE"),
#         #         emissions=filters.get("EMISSION")
#         #     )
#         #     # Crear un diccionario de valores basado en los filtros
#         #     values = {
#         #         tuple(filtered_dimensions): parameter_value
#         #     }
#         # else:
#         #     values = parameter_value


#         # print(f"Contenido de pyomo_dict[f'p_{parameter_name}']: {pyomo_dict[f'p_{parameter_name}']}")
#         # modify_parameter(pyomo_dict, parameter_name, dataframe_metadata, parameter_value, dimension_manager)


#         # Exportar los datos a JSON
#         export_to_json(pyomo_dict, json_file_path)
#         end_time = time.time()
#         print(f"Loading data time: {end_time - start_time:.2f} segundos")
#         # Ejecutar el modelo
#         start_time = time.time()
#         instance = solve_model(
#             input_file=input_file,
#             solver_name=solver_name,
#             json_file_path_or_dict=json_file_path,
#             solver_options=None,
#             tee=True
#         )
#         end_time = time.time()
#         print(f"Model solving time: {end_time - start_time:.2f} segundos")

#         # Exportar resultados
#         export_results(instance, results_folder)
#         print(f"Modelo ejecutado exitosamente para: {input_file}")

#     except Exception as e:
#         print(f"Error al procesar el archivo {input_file} con parámetro {parameter_name}={parameter_value}: {e}")
#         import traceback
#         traceback.print_exc()


###########################################################################
"""Ejecutar en paralelo usando ProcessPoolExecutor"""
""" 
Aquí es donde se introduce el archivod de entrada definido arriba:
(input_filesXX) 
"""
############################################################################

# with ProcessPoolExecutor() as executor:
#     # executor.map(process_file, input_files)
#     executor.map(process_file, input_files_base_scenarios) ##archivos de entrada 




# Crear combinaciones de archivos de entrada y valores del parámetro
# tasks = [(input_file, parameter_name, value, dataframe_metadata) for input_file in input_files_base_scenarios for value in parameter_values]
# for task in tasks:
#     process_file(*task)



# def modify_parameter(pyomo_dict, parameter_name, dataframe_metadata, parameter_value, dimension_manager):
#     """
#     Modifica un parámetro del modelo Pyomo para todas las combinaciones de dimensiones.

#     Args:
#         pyomo_dict (dict): Diccionario del modelo Pyomo.
#         parameter_name (str): Nombre del parámetro a modificar.
#         dataframe_metadata (dict): Metadatos del dataframe.
#         parameter_value (float): Valor a asignar.
#         dimension_manager (DimensionManager): Gestor de dimensiones.

#     Returns:
#         None
#     """
#     # Verificar si el parámetro está definido en dataframe_metadata
#     if parameter_name not in dataframe_metadata:
#         print(f"El parámetro '{parameter_name}' no está definido en dataframe_metadata.")
#         return

#     # Obtener las dimensiones del parámetro desde dataframe_metadata
#     dimensions = dataframe_metadata[parameter_name]["indices"]

#     # Obtener todas las combinaciones de dimensiones
#     # all_dimensions = dimension_manager.get_all_dimensions()
#     # try:
#     #     all_combinations = [
#     #         tuple(all_dimensions[dim]) for dim in dimensions if dim in all_dimensions
#     #     ]
#     # except KeyError as e:
#     #     print(f"Error: La dimensión {e} no está definida en los sets del modelo.")
#     #     return

#     # Crear un diccionario de valores para todas las combinaciones
#     # values = {
#     #     combination: parameter_value
#     #     for combination in zip(*all_combinations)
#     # }
#     # print(f"Combinaciones generadas: {list(values.keys())}")
#     # Modificar los valores en pyomo_dict
#     # parameter_name_with_prefix = f"p_{parameter_name}"
#     # if parameter_name_with_prefix in pyomo_dict:

#     #     print(f"Claves existentes: {[tuple(entry['index']) for entry in pyomo_dict[parameter_name_with_prefix]]}")
#     #     for entry in pyomo_dict[parameter_name_with_prefix]:
#     #         # Trabajar directamente con las posiciones de las dimensiones
#     #         key_tuple = tuple(entry["index"])

#     #         # Modificar el valor del parámetro si la combinación existe
#     #         if key_tuple in values:
#     #             entry["value"] = values[key_tuple]
#     #             print(f"Parámetro '{parameter_name_with_prefix}' ajustado a {values[key_tuple]} para {key_tuple}")
#     #         else:
#     #             print(f"Advertencia: No se encontró una combinación para {key_tuple}")
#     # else:
#     parameter_name_with_prefix = f"p_{parameter_name}"
#     if parameter_name_with_prefix in pyomo_dict:
#         # Obtener las claves existentes
#         existing_keys = [tuple(entry["index"]) for entry in pyomo_dict[parameter_name_with_prefix]]
#         # print(f"Claves existentes: {existing_keys}")

#         # Crear un diccionario de valores para las claves existentes
#         values = {key: parameter_value for key in existing_keys}
#         # print(f"Combinaciones generadas: {list(values.keys())}")

#         # Modificar los valores en pyomo_dict
#         for entry in pyomo_dict[parameter_name_with_prefix]:
#             key_tuple = tuple(entry["index"])

#             # Modificar el valor del parámetro si la combinación existe
#             if key_tuple in values:
#                 entry["value"] = values[key_tuple]
#                 print(f"Parámetro '{parameter_name_with_prefix}' ajustado a {values[key_tuple]} para {key_tuple}")
#             else:
#                 print(f"Advertencia: No se encontró una combinación para {key_tuple}")
#     else:
#         print(f"El parámetro '{parameter_name_with_prefix}' no se encontró en el modelo.")


# def modify_parameter(pyomo_dict, parameter_name, dataframe_metadata, values=None, filters=None, operation=None, dimension_manager=None, use_existing_keys=True):
#     """
#     Modifica un parámetro del modelo Pyomo basado en valores existentes, filtros o una operación.

#     Args:
#         pyomo_dict (dict): Diccionario del modelo Pyomo.
#         parameter_name (str): Nombre del parámetro a modificar (sin el prefijo `p_`).
#         dataframe_metadata (dict): Diccionario con la configuración de los parámetros.
#         values (dict, list, o float, opcional): Valores a asignar. Puede ser un diccionario, lista o valor único.
#         filters (dict, opcional): Filtros para limitar las modificaciones (por ejemplo, {"REGION": "Cuba"}).
#         operation (callable, opcional): Operación matemática para modificar los valores (por ejemplo, incremento lineal).
#         dimension_manager (DimensionManager, opcional): Gestor de dimensiones para aplicar filtros.
#         use_existing_keys (bool, opcional): Si es True, usa las claves existentes en el parámetro. Si es False, usa los filtros para crear nuevas combinaciones.

#     Returns:
#         None
#     """
#     parameter_name_with_prefix = f"p_{parameter_name}"

#     if parameter_name not in dataframe_metadata:
#         print(f"El parámetro '{parameter_name}' no está definido en dataframe_metadata.")
#         return

#     # Obtener las dimensiones del parámetro
#     dimensions = dataframe_metadata[parameter_name]["indices"]

#     if use_existing_keys:
#         # Caso 1: Usar las claves existentes
#         if parameter_name_with_prefix in pyomo_dict:
#             # print(f"Claves existentes en '{parameter_name_with_prefix}': {[tuple(entry['index']) for entry in pyomo_dict[parameter_name_with_prefix]]}")
#             for entry in pyomo_dict[parameter_name_with_prefix]:
#                 key_tuple = tuple(entry["index"])
#                 key_dict = dict(zip(dimensions, key_tuple))

#                 # Aplicar filtros si se especifican
#                 if filters:
#                     if not all(key_dict.get(k) in v if isinstance(v, list) else key_dict.get(k) == v for k, v in filters.items()):
#                         continue

#                 # Modificar el valor del parámetro
#                 if isinstance(values, dict):
#                     new_value = values.get(key_tuple, None)
#                     if new_value is not None:
#                         entry["value"] = new_value
#                         print(f"Parámetro '{parameter_name_with_prefix}' ajustado a {new_value} para {key_tuple}")
#                 elif isinstance(values, (int, float)):
#                     entry["value"] = values
#                     print(f"Parámetro '{parameter_name_with_prefix}' ajustado a {values} para {key_tuple}")
#                 elif operation:
#                     entry["value"] = operation(entry["value"], key_dict)
#                     print(f"Parámetro '{parameter_name_with_prefix}' ajustado con operación para {key_tuple}")
#         else:
#             print(f"El parámetro '{parameter_name_with_prefix}' no se encontró en el modelo.")
#     else:
#         # Caso 2: Usar los filtros para crear nuevas combinaciones
#         print(f"Creando nuevas combinaciones para '{parameter_name_with_prefix}' usando filtros.")
#         if isinstance(values, dict):
#             for key_tuple, new_value in values.items():
#                 if all(key_tuple[dimensions.index(k)] in v if isinstance(v, list) else key_tuple[dimensions.index(k)] == v for k, v in filters.items()):
#                     pyomo_dict.setdefault(parameter_name_with_prefix, []).append({
#                         "index": list(key_tuple),
#                         "value": new_value
#                     })
#                     print(f"Parámetro '{parameter_name_with_prefix}' creado con valor {new_value} para {key_tuple}")
#         else:
#             # Generar combinaciones basadas en los filtros
#             filtered_dimensions = dimension_manager.get_filtered_dimensions(**filters)
#             combinations = [
#                 tuple(filtered_dimensions[dim] for dim in dimensions)
#                 for dim in dimensions
#             ]
#             for combination in zip(*combinations):
#                 pyomo_dict.setdefault(parameter_name_with_prefix, []).append({
#                     "index": list(combination),
#                     "value": values
#                 })
#                 print(f"Parámetro '{parameter_name_with_prefix}' creado con valor {values} para {combination}")



# def run_scenarios(scenarios, input_files, dataframe_metadata, dimension_manager):
#     tasks = []
#     for scenario in scenarios:
#         print(f"Running {scenario['name']}...")
#         for parameter in scenario["parameters"]:
#             for input_file in input_files:
#                 # Caso 1: Si los valores son una lista y no hay filtros, crea un subescenario para cada valor
#                 if isinstance(parameter["values"], list) and parameter.get("filters") is None:
#                     for value in parameter["values"]:
#                         tasks.append((
#                             input_file,
#                             parameter["name"],
#                             value,  # Pasa cada valor individualmente
#                             dataframe_metadata,
#                             dimension_manager,
#                             parameter.get("filters", None)
#                         ))
#                 # Caso 2: Si los valores son un diccionario o hay filtros, crea un único escenario
#                 elif isinstance(parameter["values"], dict) or parameter.get("filters") is not None:
#                     tasks.append((
#                         input_file,
#                         parameter["name"],
#                         parameter["values"],  # Pasa el diccionario completo
#                         dataframe_metadata,
#                         dimension_manager,
#                         parameter.get("filters", None)
#                     ))

#     # Ejecutar en paralelo
#     with Pool() as pool:
#         pool.starmap(process_file, tasks)
#     print("Todos los escenarios han sido procesados.")
# def run_scenarios(scenarios, input_files, dataframe_metadata, dimension_manager):
#     tasks = []
#     for scenario in scenarios:
#         print(f"Running {scenario['name']}...")
#         for parameter in scenario["parameters"]:
#             for input_file in input_files:
#                 # Caso 1: Crear un subescenario para cada valor sin filtros
#                 if isinstance(parameter["values"], list) and parameter.get("filters") is None:
#                     for value in parameter["values"]:
#                         subscenario_name = parameter.get("subscenario_name", f"{parameter['name']}_{value}")
#                         tasks.append((
#                             input_file,
#                             parameter["name"],
#                             value,  # Pasa cada valor individualmente
#                             dataframe_metadata,
#                             dimension_manager,
#                             parameter.get("filters", None),
#                             scenario.get("additional_parameters", None),
#                             subscenario_name
#                         ))

#                 # Caso 2: Crear un único escenario con filtros
#                 elif parameter.get("filters") is not None:
#                     subscenario_name = parameter.get("subscenario_name", f"{parameter['name']}_filtered")
#                     tasks.append((
#                         input_file,
#                         parameter["name"],
#                         parameter["values"],
#                         dataframe_metadata,
#                         dimension_manager,
#                         parameter.get("filters", None),
#                         scenario.get("additional_parameters", None),
#                         subscenario_name
#                     ))

#                 # Caso 3: Cambiar un parámetro con un filtro sin crear múltiples escenarios
#                 elif isinstance(parameter["values"], dict):
#                     subscenario_name = parameter.get("subscenario_name", f"{parameter['name']}_dict")
#                     tasks.append((
#                         input_file,
#                         parameter["name"],
#                         parameter["values"],
#                         dataframe_metadata,
#                         dimension_manager,
#                         parameter.get("filters", None),
#                         scenario.get("additional_parameters", None),
#                         subscenario_name
#                     ))

#                 # Caso 4: Combinación de cambios en un único escenario
#                 elif scenario.get("additional_parameters"):
#                     subscenario_name = parameter.get("subscenario_name", f"{parameter['name']}_combined")
#                     tasks.append((
#                         input_file,
#                         parameter["name"],
#                         parameter["values"],
#                         dataframe_metadata,
#                         dimension_manager,
#                         parameter.get("filters", None),
#                         scenario["additional_parameters"],  # Pasar parámetros adicionales
#                         subscenario_name
#                     ))

#                 # Caso 5: Cambiar otros parámetros dentro de subescenarios generados
#                 else:
#                     subscenario_name = parameter.get("subscenario_name", f"{parameter['name']}_{parameter['values']}")
#                     tasks.append((
#                         input_file,
#                         parameter["name"],
#                         parameter["values"],
#                         dataframe_metadata,
#                         dimension_manager,
#                         parameter.get("filters", None),
#                         scenario.get("additional_parameters", None),
#                         subscenario_name
#                     ))


    # Ejecutar en paralelo
    # with Pool() as pool:
    #     pool.starmap(process_file, tasks)
    # print("Todos los escenarios han sido procesados.")
# def create_scenarios_single_parameter(parameter_name, values):
#     """
#     Crea escenarios basados en un único parámetro con valores globales.

#     Args:
#         parameter_name (str): Nombre del parámetro.
#         values (list): Lista de valores para el parámetro.

#     Returns:
#         list: Lista de escenarios.
#     """
#     scenarios = [
#         {
#             "name": f"Scenario - {parameter_name}",
#             "parameters": [
#                 {
#                     "name": parameter_name,
#                     "values": values,
#                     "filters": None  # Sin filtros, aplica a todo
#                 }
#             ]
#         }
#     ]
#     return scenarios

# def create_filtered_parameter_scenario(parameter_name, values, filters):
#     """
#     Crea un escenario para modificar un único parámetro con filtros específicos.

#     Args:
#         parameter_name (str): Nombre del parámetro.
#         values (dict): Diccionario con los valores a asignar.
#         filters (dict): Filtros para limitar las modificaciones.

#     Returns:
#         dict: Escenario con el parámetro modificado.
#     """
#     scenario = {
#         "name": f"Scenario - Filtered {parameter_name}",
#         "parameters": [
#             {
#                 "name": parameter_name,
#                 "values": values,
#                 "filters": filters
#             }
#         ]
#     }
#     return scenario
# def create_multiple_parameters_scenario(parameters):
#     """
#     Crea un escenario que modifica varios parámetros.

#     Args:
#         parameters (list): Lista de diccionarios con los parámetros, valores y filtros.

#     Returns:
#         dict: Escenario con múltiples parámetros modificados.
#     """
#     scenario = {
#         "name": "Scenario - Multiple Parameters",
#         "parameters": parameters
#     }
#     return scenario

# def create_multiple_scenarios(scenarios_data):
#     """
#     Crea múltiples escenarios, cada uno con múltiples parámetros.

#     Args:
#         scenarios_data (list): Lista de escenarios, cada uno con sus parámetros.

#     Returns:
#         list: Lista de escenarios.
#     """
#     scenarios = []
#     for scenario_data in scenarios_data:
#         scenario = {
#             "name": scenario_data["name"],
#             "parameters": scenario_data["parameters"]
#         }
#         scenarios.append(scenario)
#     return scenarios

# def modify_single_parameter(pyomo_dict, parameter_name, values, dataframe_metadata):
#     """
#     Modifica un único parámetro en el modelo Pyomo reemplazando los valores existentes.

#     Args:
#         pyomo_dict (dict): Diccionario del modelo Pyomo.
#         parameter_name (str): Nombre del parámetro a modificar (sin el prefijo `p_`).
#         values (list): Lista de valores para el parámetro.
#         dataframe_metadata (dict): Diccionario con la configuración de los parámetros.

#     Returns:
#         list: Lista de escenarios generados con los valores modificados.
#     """
#     parameter_name_with_prefix = f"p_{parameter_name}"

#     if parameter_name not in dataframe_metadata:
#         print(f"El parámetro '{parameter_name}' no está definido en dataframe_metadata.")
#         return []

#     # Verificar si el parámetro existe en el diccionario Pyomo
#     if parameter_name_with_prefix not in pyomo_dict:
#         print(f"El parámetro '{parameter_name_with_prefix}' no se encontró en el modelo.")
#         return []

#     # Crear escenarios para cada valor
#     scenarios = []
#     for value in values:
#         # Reemplazar todos los valores existentes con el nuevo valor
#         for entry in pyomo_dict[parameter_name_with_prefix]:
#             entry["value"] = value
#         print(f"Parámetro '{parameter_name_with_prefix}' ajustado a {value}.")

#         # Crear un diccionario para el escenario
#         scenario = {
#             "name": f"Scenario - {parameter_name}_{value}",
#             "parameter_name": parameter_name,
#             "value": value,
#             "modified_data": pyomo_dict.copy()  # Copiar el diccionario modificado
#         }
#         scenarios.append(scenario)

#     return scenarios

# def process_single_parameter_scenario(input_file, parameter_name, values, dataframe_metadata, dimension_manager, root_folder):
#     """
#     Procesa un escenario basado en un único parámetro con valores globales.

#     Args:
#         input_file (str): Ruta del archivo de entrada.
#         parameter_name (str): Nombre del parámetro a modificar.
#         values (list): Lista de valores para el parámetro.
#         dataframe_metadata (dict): Metadatos del dataframe.
#         dimension_manager (DimensionManager): Gestor de dimensiones.
#         root_folder (str): Carpeta raíz del proyecto.

#     Returns:
#         None
#     """
#     try:
#         # Configurar rutas para cada archivo
#         paths = configure_paths(input_file, root_folder)

#         for value in values:
#             subscenario_name = f"{parameter_name}_{value}"
#             results_folder = os.path.join(paths['RESULTS_FOLDER'], subscenario_name)
#             os.makedirs(results_folder, exist_ok=True)

#             json_file_path = os.path.join(
#                 paths['OUTPUT_FOLDER_DATA'],
#                 f"{os.path.basename(input_file).replace('.xlsx', '')}_{subscenario_name}.json"
#             )

#             print(f"Procesando archivo de entrada: {input_file}")
#             print(f"Subescenario: {subscenario_name}")
#             print(f"Resultados se guardarán en: {results_folder}")
#             print(f"Archivo JSON se exportará a: {json_file_path}")

#             # Cargar y transformar los datos
#             dataframe = load_dataframes(input_file)
#             transf_data = transform_all_dataframes(dataframe)
#             dict_to_be_adjusted = dict_to_json(transf_data, input_file)
#             pyomo_dict = adjust_json_for_pyomo(dict_to_be_adjusted)

#             # Modificar el parámetro
#             parameter_name_with_prefix = f"p_{parameter_name}"
#             if parameter_name_with_prefix not in pyomo_dict:
#                 print(f"El parámetro '{parameter_name_with_prefix}' no se encontró en el modelo.")
#                 continue

#             for entry in pyomo_dict[parameter_name_with_prefix]:
#                 entry["value"] = value
#             print(f"Parámetro '{parameter_name_with_prefix}' ajustado a {value}.")

#             # Exportar los datos a JSON
#             if pyomo_dict:
#                 export_to_json(pyomo_dict, json_file_path)
#                 print(f"Archivo JSON exportado correctamente: {json_file_path}")
#             else:
#                 print("Advertencia: pyomo_dict está vacío. No se exportó el archivo JSON.")

#             # Ejecutar el modelo
#             instance = solve_model(
#                 input_file=input_file,
#                 solver_name="gurobi",  # Cambia esto al nombre del solver que estés usando
#                 json_file_path_or_dict=json_file_path,
#                 solver_options=None,
#                 tee=True
#             )

#             # Exportar resultados
#             export_results(instance, results_folder)
#             print(f"Modelo ejecutado exitosamente para el subescenario: {subscenario_name}")

#     except Exception as e:
#         print(f"Error al procesar el archivo {input_file} con parámetro {parameter_name}: {e}")
#         import traceback
#         traceback.print_exc()

# def generate_json_file(input_file, parameter_name, value, dataframe_metadata, dimension_manager, root_folder):
#     """
#     Genera archivos JSON para cada subescenario basado en un único parámetro.

#     Args:
#         input_file (str): Ruta del archivo de entrada.
#         parameter_name (str): Nombre del parámetro a modificar.
#         values (list): Lista de valores para el parámetro.
#         dataframe_metadata (dict): Metadatos del dataframe.
#         dimension_manager (DimensionManager): Gestor de dimensiones.
#         root_folder (str): Carpeta raíz del proyecto.

#     Returns:
#         list: Lista de rutas de los archivos JSON generados.
#     """
#     try:
#         # Configurar rutas
#         paths = configure_paths(input_file, root_folder)
#         subscenario_name = f"{parameter_name}_{value}"
#         results_folder = os.path.join(paths['RESULTS_FOLDER'], subscenario_name)
#         os.makedirs(results_folder, exist_ok=True)

#         json_file_path = os.path.join(
#             paths['OUTPUT_FOLDER_DATA'],
#             f"{os.path.basename(input_file).replace('.xlsx', '')}_{subscenario_name}.json"
#         )

#         print(f"Procesando subescenario: {subscenario_name}")
#         print(f"Archivo JSON se exportará a: {json_file_path}")

#         # Cargar y transformar los datos
#         dataframe = load_dataframes(input_file)
#         transf_data = transform_all_dataframes(dataframe)
#         dict_to_be_adjusted = dict_to_json(transf_data, input_file)
#         pyomo_dict = adjust_json_for_pyomo(dict_to_be_adjusted)

#         # Modificar el parámetro
#         parameter_name_with_prefix = f"p_{parameter_name}"
#         if parameter_name_with_prefix not in pyomo_dict:
#             print(f"El parámetro '{parameter_name_with_prefix}' no se encontró en el modelo.")
#             return None

#         for entry in pyomo_dict[parameter_name_with_prefix]:
#             entry["value"] = value
#         print(f"Parámetro '{parameter_name_with_prefix}' ajustado a {value}.")

#         # Exportar los datos a JSON
#         export_to_json(pyomo_dict, json_file_path)
#         print(f"Archivo JSON exportado correctamente: {json_file_path}")
#         return json_file_path

#     except Exception as e:
#         print(f"Error al generar el archivo JSON para el valor {value}: {e}")
#         return None
    
# def generate_json_files_in_parallel(input_file, parameter_name, values, dataframe_metadata, dimension_manager, root_folder):
#     """
#     Genera archivos JSON para cada subescenario en paralelo.

#     Args:
#         input_file (str): Ruta del archivo de entrada.
#         parameter_name (str): Nombre del parámetro a modificar.
#         values (list): Lista de valores para el parámetro.
#         dataframe_metadata (dict): Metadatos del dataframe.
#         dimension_manager (DimensionManager): Gestor de dimensiones.
#         root_folder (str): Carpeta raíz del proyecto.

#     Returns:
#         list: Lista de rutas de los archivos JSON generados.
#     """
#     with ProcessPoolExecutor() as executor:
#         # Ejecutar la generación de JSON en paralelo
#         tasks = [
#             executor.submit(
#                 generate_json_file,
#                 input_file,
#                 parameter_name,
#                 value,
#                 dataframe_metadata,
#                 dimension_manager,
#                 root_folder
#             )
#             for value in values
#         ]
#         # Recoger los resultados
#         json_files = [task.result() for task in tasks if task.result() is not None]
#     return json_files

# def solve_subscenarios(json_files, input_file, solver_name="gurobi"):
#     """
#     Resuelve los subescenarios cargando los archivos JSON generados.

#     Args:
#         json_files (list): Lista de rutas de los archivos JSON generados.
#         input_file (str): Ruta del archivo de entrada.
#         solver_name (str): Nombre del solver a utilizar.

#     Returns:
#         None
#     """
#     try:
#         for json_file_path in json_files:
#             subscenario_name = os.path.basename(json_file_path).replace(".json", "")
#             results_folder = os.path.join(os.path.dirname(json_file_path), subscenario_name)
#             os.makedirs(results_folder, exist_ok=True)

#             print(f"Resolviendo subescenario: {subscenario_name}")
#             print(f"Archivo JSON cargado: {json_file_path}")
#             print(f"Resultados se guardarán en: {results_folder}")

#             # Resolver el modelo
#             instance = solve_model(
#                 input_file=input_file,
#                 solver_name=solver_name,
#                 json_file_path_or_dict=json_file_path,
#                 solver_options=None,
#                 tee=True
#             )

#             # Exportar resultados
#             export_results(instance, results_folder)
#             print(f"Modelo resuelto exitosamente para el subescenario: {subscenario_name}")

#     except Exception as e:
#         print(f"Error al resolver los subescenarios: {e}")
#         import traceback
#         traceback.print_exc()

# def solve_subscenario(json_file_path, input_file, solver_name="gurobi"):
#     """
#     Resuelve un subescenario cargando un archivo JSON generado.

#     Args:
#         json_file_path (str): Ruta del archivo JSON generado.
#         input_file (str): Ruta del archivo de entrada.
#         solver_name (str): Nombre del solver a utilizar.

#     Returns:
#         str: Mensaje indicando el resultado de la ejecución.
#     """
#     try:
#         subscenario_name = os.path.basename(json_file_path).replace(".json", "")
#         results_folder = os.path.join(root_folder, "results", subscenario_name)
#         os.makedirs(results_folder, exist_ok=True)

#         print(f"Resolviendo subescenario: {subscenario_name}")
#         print(f"Archivo JSON cargado: {json_file_path}")
#         print(f"Resultados se guardarán en: {results_folder}")

#         # Resolver el modelo
#         instance = solve_model(
#             input_file=input_file,
#             solver_name=solver_name,
#             json_file_path_or_dict=json_file_path,
#             solver_options=None,
#             tee=True
#         )

#         # Exportar resultados
#         export_results(instance, results_folder)
#         return f"Modelo resuelto exitosamente para el subescenario: {subscenario_name}"

#     except Exception as e:
#         return f"Error al resolver el subescenario {subscenario_name}: {e}"
    
# def solve_subscenarios_in_parallel(json_files, input_file, solver_name="gurobi"):
#     """
#     Resuelve múltiples subescenarios en paralelo.

#     Args:
#         json_files (list): Lista de rutas de los archivos JSON generados.
#         input_file (str): Ruta del archivo de entrada.
#         solver_name (str): Nombre del solver a utilizar.

#     Returns:
#         None
#     """
#     with ProcessPoolExecutor() as executor:
#         # Ejecutar cada subescenario en paralelo
#         results = executor.map(solve_subscenario, json_files, [input_file] * len(json_files), [solver_name] * len(json_files))

#         # Imprimir resultados
#         for result in results:
#             print(result)
# def apply_linear_increment(values, start, end, step):
#     """
#     Aplica un incremento lineal a los valores de un parámetro.

#     Args:
#         values (dict): Diccionario de valores existentes.
#         start (float): Valor inicial.
#         end (float): Valor final.
#         step (float): Incremento por paso.

#     Returns:
#         dict: Diccionario con los valores incrementados.
#     """
#     incremented_values = {}
#     for key, value in values.items():
#         current_value = start
#         while current_value <= end:
#             incremented_values[key] = current_value
#             current_value += step
#     return incremented_values


# def apply_linear_decrement(values, start, end, step):
#     """
#     Aplica un decremento lineal a los valores de un parámetro.

#     Args:
#         values (dict): Diccionario de valores existentes.
#         start (float): Valor inicial.
#         end (float): Valor final.
#         step (float): Decremento por paso.

#     Returns:
#         dict: Diccionario con los valores decrementados.
#     """
#     decremented_values = {}
#     for key, value in values.items():
#         current_value = start
#         while current_value >= end:
#             decremented_values[key] = current_value
#             current_value -= step
#     return decremented_values


# def apply_scaling(values, factor):
#     """
#     Escala los valores existentes de un parámetro por un factor.

#     Args:
#         values (dict): Diccionario de valores existentes.
#         factor (float): Factor de escalado.

#     Returns:
#         dict: Diccionario con los valores escalados.
#     """
#     return {key: value * factor for key, value in values.items()}


# def apply_fixed_assignment(values, fixed_value):
#     """
#     Asigna un valor fijo a todas las combinaciones de un parámetro.

#     Args:
#         values (dict): Diccionario de valores existentes.
#         fixed_value (float): Valor fijo a asignar.

#     Returns:
#         dict: Diccionario con los valores asignados.
#     """
#     return {key: fixed_value for key in values.keys()}


# def apply_custom_transformation(values, transform_function):
#     """
#     Aplica una transformación personalizada a los valores de un parámetro.

#     Args:
#         values (dict): Diccionario de valores existentes.
#         transform_function (callable): Función que toma un valor y devuelve el valor transformado.

#     Returns:
#         dict: Diccionario con los valores transformados.
#     """
#     return {key: transform_function(value) for key, value in values.items()}

# def modify_parameters_for_scenario(pyomo_dict, parameter_name, values, filters, dimensions):
#     """
#     Modifica un parámetro del modelo Pyomo para un conjunto específico de dimensiones.

#     Args:
#         pyomo_dict (dict): Diccionario del modelo Pyomo.
#         parameter_name (str): Nombre del parámetro a modificar (sin el prefijo `p_`).
#         values (dict): Diccionario con los valores a asignar. Las claves deben coincidir con las dimensiones del parámetro.
#         filters (dict): Filtros para limitar las modificaciones (por ejemplo, {"REGION": "Cuba"}).
#         dimensions (list): Lista de dimensiones del parámetro.

#     Returns:
#         None
#     """
#     parameter_name_with_prefix = f"p_{parameter_name}"

#     # Crear el parámetro si no existe
#     if parameter_name_with_prefix not in pyomo_dict:
#         pyomo_dict[parameter_name_with_prefix] = []

#     if isinstance(values, list):
#         if filters is None:
#             filters = {}  # Asegurarse de que `filters` no sea None
#         values = {
#             tuple(filters.get(dim, None) for dim in dimensions): value
#             for value in values
#         }
#     if not filters:
#         for entry in pyomo_dict[parameter_name_with_prefix]:
#             entry["value"] = list(values.values())[0]  # Asignar el primer valor de `values`
#             print(f"Parámetro '{parameter_name_with_prefix}' ajustado a {entry['value']} para {entry['index']}")
#         return

#     existing_entries = pyomo_dict[parameter_name_with_prefix]
#     new_keys = set(values.keys())
#     pyomo_dict[parameter_name_with_prefix] = [
#         entry for entry in existing_entries
#         if tuple(entry["index"]) not in new_keys
#     ]




#     # Iterar sobre las combinaciones de valores
#     for key_tuple, value in values.items():
#         # Verificar si la combinación cumple con los filtros
#         if all(key_tuple[dimensions.index(k)] in v if isinstance(v, list) 
#                else key_tuple[dimensions.index(k)] == v for k, v in filters.items()):
#             # Agregar o modificar el valor en el parámetro
#             pyomo_dict[parameter_name_with_prefix].append({
#                 "index": list(key_tuple),
#                 "value": value
#             })
#             print(f"Parámetro '{parameter_name_with_prefix}' ajustado a {value} para {key_tuple}")

# def generate_json_file_2(input_file, parameters, dataframe_metadata, dimension_manager, root_folder, subscenario_name):
#     """
#     Genera un archivo JSON para un subescenario basado en un único parámetro.

#     Args:
#         input_file (str): Ruta del archivo de entrada.
#         parameter_name (str): Nombre del parámetro a modificar.
#         values (dict): Diccionario con los valores a asignar.
#         filters (dict): Filtros para limitar las modificaciones.
#         dataframe_metadata (dict): Metadatos del dataframe.
#         dimension_manager (DimensionManager): Gestor de dimensiones.
#         root_folder (str): Carpeta raíz del proyecto.
#         subscenario_name (str): Nombre personalizado del subescenario.

#     Returns:
#         str: Ruta del archivo JSON generado.
#     """
#     try:
#         # Configurar rutas
#         paths = configure_paths(input_file, root_folder)
#         results_folder = os.path.join(paths['RESULTS_FOLDER'], subscenario_name)
#         os.makedirs(results_folder, exist_ok=True)

#         json_file_path = os.path.join(
#             paths['OUTPUT_FOLDER_DATA'],
#             f"{os.path.basename(input_file).replace('.xlsx', '')}_{subscenario_name}.json"
#         )

#         print(f"Procesando archivo de entrada: {input_file}")
#         print(f"Subescenario: {subscenario_name}")
#         print(f"Archivo JSON se exportará a: {json_file_path}")

#         # Cargar y transformar los datos
#         dataframe = load_dataframes(input_file)
#         transf_data = transform_all_dataframes(dataframe)
#         dict_to_be_adjusted = dict_to_json(transf_data, input_file)
#         pyomo_dict = adjust_json_for_pyomo(dict_to_be_adjusted)

#         for param in parameters:
#             parameter_name = param["name"]
#             values = param["values"]
#             filters = param.get("filters", None)

#             # Obtener las dimensiones del parámetro
#             dimensions = dataframe_metadata[parameter_name]["indices"]

#             # Modificar el parámetro
#             modify_parameters_for_scenario(pyomo_dict, parameter_name, values, filters, dimensions)

#         # Exportar los datos a JSON
#         export_to_json(pyomo_dict, json_file_path)
#         print(f"Archivo JSON exportado correctamente: {json_file_path}")

#         return json_file_path

#     except Exception as e:
#         print(f"Error al generar el archivo JSON para el subescenario {subscenario_name}: {e}")
#         traceback.print_exc()
#         return None

# def generate_combined_scenarios(input_file, parameter_name, values, additional_parameters, dataframe_metadata, dimension_manager, root_folder):
#     """
#     Genera escenarios combinados donde se varía un parámetro principal y otros parámetros secundarios.

#     Args:
#         input_file (str): Ruta del archivo de entrada.
#         parameter_name (str): Nombre del parámetro principal a modificar.
#         values (list): Lista de valores para el parámetro principal.
#         additional_parameters (list): Lista de parámetros secundarios a modificar.
#         dataframe_metadata (dict): Metadatos del dataframe.
#         dimension_manager (DimensionManager): Gestor de dimensiones.
#         root_folder (str): Carpeta raíz del proyecto.

#     Returns:
#         list: Lista de rutas de los archivos JSON generados.
#     """
#     json_files = []

#     for value in values:
#         # Crear un subescenario para cada valor del parámetro principal
#         subscenario_name = f"{parameter_name}_{value}"
#         parameters = [{"name": parameter_name, "values": [value], "filters": None}]

#         # Agregar los parámetros secundarios al subescenario
#         for param in additional_parameters:
#             parameters.append(param)

#         # Generar el archivo JSON para el subescenario
#         json_file_path = generate_json_file_2(
#             input_file,
#             parameters,
#             dataframe_metadata,
#             dimension_manager,
#             root_folder,
#             subscenario_name
#         )

#         if json_file_path:
#             json_files.append(json_file_path)

    # return json_files   

if __name__ == "__main__":


    Default, REGION, YEAR, TECHNOLOGY, FUEL, SEASON, DAYTYPE, DAILYTIMEBRACKET, TIMESLICE, MODE_OF_OPERATION, STORAGE, EMISSION = load_sets(input_files_base_scenarios[0])

# Crear un diccionario con los sets
    sets = {
        "REGION": REGION,
        "YEAR": YEAR,
        "TECHNOLOGY": TECHNOLOGY,
        "FUEL": FUEL,
        "SEASON": SEASON,
        "DAYTYPE": DAYTYPE,
        "DAILYTIMEBRACKET": DAILYTIMEBRACKET,
        "TIMESLICE": TIMESLICE,
        "MODE_OF_OPERATION": MODE_OF_OPERATION,
        "STORAGE": STORAGE,
        "EMISSION": EMISSION
    }
    # dimension_manager = DimensionManager(sets)

    dimension_manager = DimensionManager(sets)
    scenario_manager = ScenarioManager(
        input_file=input_files_base_scenarios[0],
        root_folder=root_folder,
        dimension_manager=dimension_manager
    )
    # Generar escenarios
    parameter_name = "CostoRecuperacion"
    values = [500, 600, 700, 800]
    additional_parameters = [
        {
            "name": "CapitalCost",
            "values": {("Cuba", "PWRPV01", year): 1000 for year in range(2025, 2050)},
            "filters": {"REGION": ["Cuba"], "TECHNOLOGY": ["PWRPV01"], "YEAR": list(range(2025, 2050))}
        }
    ]
    json_files = scenario_manager.generate_combined_scenarios(parameter_name, values, additional_parameters)

    # Resolver escenarios
    scenario_manager.solve_subscenarios_in_parallel(json_files, solver_name="gurobi")


    # scenarios1 = create_scenarios_single_parameter("CostoRecuperacion", [500, 600, 700, 800])
    # print(scenarios1)

    ###############################################################################
    """Module 1 for creating scenarios with a single parameter"""
    ###############################################################################
    # parameter_name = "CostoRecuperacion"
    # values = [500, 600, 700, 800]
    # input_file = input_files_base_scenarios[0]
    # json_files = generate_json_files_in_parallel(
    #     input_file, 
    #     parameter_name, 
    #     values, 
    #     dataframe_metadata, 
    #     dimension_manager, 
    #     root_folder)
    # solve_subscenarios_in_parallel(json_files, input_file, solver_name="gurobi")


    ############################################################################
    """Module 2 for creating scenarios with filters and multiple parameters"""
    ############################################################################
    # parameters = [
    #     {
    #         "name": "TotalAnnualMaxCapacityInvestment",
    #         "values": {
    #             ("Cuba", "PWRBIO", year): 0.12 for year in range(2025, 2050)
    #         },
    #         "filters": {
    #             "REGION": ["Cuba"],
    #             "TECHNOLOGY": ["PWRBIO"],
    #             "YEAR": list(range(2025, 2050))
    #         }
    #     },
    #     # {
    #     #     "name": "CostoRecuperacion",
    #     #     "values": [800],
    #     #     "filters": None
    #     # },
    #     {
    #         "name": "CapitalCost",
    #         "values": {
    #             ("Cuba", "PWRPV01", year): 1000 for year in range(2025, 2050)
    #         },
    #         "filters": {
    #             "REGION": ["Cuba"],
    #             "TECHNOLOGY": ["PWRPV01"],
    #             "YEAR": list(range(2025, 2050))
    #         }
    #     }
    # ]
    # subscenario_name_mod2 = "MaxCapacity"

    # # Generar archivo JSON
    # input_file = input_files_base_scenarios[0]
    # json_file_path = generate_json_file_2(
    #     input_file, 
    #     parameters,
    #     dataframe_metadata, 
    #     dimension_manager, 
    #     root_folder, 
    #     subscenario_name_mod2
    # )

    # # Resolver el subescenario
    # if json_file_path:
    #     result_message = solve_subscenario(json_file_path, input_file, solver_name="gurobi")
    #     print(result_message)
    ############################################################################
    ############################################################################ 
    ############################################################################



##############################################################################
##############################################################################
    """Module 3 for creating scenarios with multiple parameters"""
##############################################################################
##############################################################################
    # parameter_name = "CostoRecuperacion"
    # values = [500, 600, 700, 800]

    # # Definir los parámetros secundarios
    # additional_parameters = [
    #     {
    #         "name": "TotalAnnualMaxCapacityInvestment",
    #         "values": {
    #             ("Cuba", "PWRBIO", year): 0.12 for year in range(2025, 2050)
    #         },
    #         "filters": {
    #             "REGION": ["Cuba"],
    #             "TECHNOLOGY": ["PWRBIO"],
    #             "YEAR": list(range(2025, 2050))
    #         }
    #     },
    #     {
    #         "name": "CapitalCost",
    #         "values": {
    #             ("Cuba", "PWRPV01", year): 1000 for year in range(2025, 2050)
    #         },
    #         "filters": {
    #             "REGION": ["Cuba"],
    #             "TECHNOLOGY": ["PWRPV01"],
    #             "YEAR": list(range(2025, 2050))
    #         }
    #     }
    # ]

    # # Generar los escenarios combinados
    # json_files = generate_combined_scenarios(
    #     input_file=input_files_base_scenarios[0],
    #     parameter_name=parameter_name,
    #     values=values,
    #     additional_parameters=additional_parameters,
    #     dataframe_metadata=dataframe_metadata,
    #     dimension_manager=dimension_manager,
    #     root_folder=root_folder
    # )


    # solve_subscenarios_in_parallel(json_files, 
    # input_files_base_scenarios[0], solver_name="gurobi")
###############################################################################
##############################################################################
##############################################################################
##############################################################################


    # Inicializar DimensionManager con los sets cargados
 
    # parameter_name = "CostoRecuperacion"
    # parameter_values = [500, 600, 700, 800] 
    # run_scenarios(scenarios2, input_files_base_scenarios, dataframe_metadata, dimension_manager)


 # Valores del parámetro a probar

    # Crear combinaciones de archivos de entrada y valores del parámetro


    # print("Iniciando ejecución en paralelo...")
    # with Pool() as pool:
    #     pool.starmap(process_file, tasks)
    # print("Ejecución en paralelo completada.")


#######################################################################
""" Plotting the results """
#######################################################################
# from OSeMOSYS.postprocessing.allplots import run_app_1, run_app_2, run_app_3, run_app_4, get_dependency_files
# from threading import Thread
# from OSeMOSYS.utils import dependency_keys
# # from




# years_simple = [2020, 2025, 2030] # para los super simples
# years_cuba_model = [2019, 2030, 2050]
# dependency_files = {
#     app: get_dependency_files(input_files_base_scenarios, key, base_folder="results") ##### cambiar el input_files por el que se quiera
#     for app, key in dependency_keys.items()
# }
# scenarios = list(dependency_files["app1"].keys()) 
# print(scenarios)

# # dependency_files_app1 = get_dependency_files(input_files_simple, dependency_key_app1, base_folder="results")
# # dependency_files_app2 = get_dependency_files(input_files_simple, dependency_key_app2, base_folder="results")
# # dependency_files_app4 = get_dependency_files(input_files_simple, dependency_key_app4, base_folder="results")
# # scenarios = list(dependency_files_app1.keys(input_files_simple))# Solo depende de laos input files, no hay que crear uno para uno pero se podría hacer
# app_runners = {
#     "app1": run_app_1,
#     "app2": run_app_2,
#     "app3": run_app_3,
#     "app4": run_app_4
# }

# # Inicializar y ejecutar las aplicaciones
# threads = []
# threads.append(Thread(target=run_app_1, args=(dependency_files["app1"], COLOR_VARIATIONS, scenarios)))
# threads.append(Thread(target=run_app_2, args=(dependency_files["app2"], COLOR_VARIATIONS, years_simple, scenarios)))
# threads.append(Thread(target=run_app_3, args=(dependency_files["app1"], scenarios)))
# threads.append(Thread(target=run_app_4, args=(dependency_files["app4"],)))
# # Esperar a que todos los hilos terminen
# for thread in threads:
#     thread.start()

# # Esperar a que todos los hilos terminen
# for thread in threads:
#     thread.join()
