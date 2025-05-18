#%%
import os, sys
import json
import pandas as pd
root_folder = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(root_folder)

from OSeMOSYS.ReadSets import load_sets, read_excel_sheets_1
from OSeMOSYS.utils import dataframe_metadata, sheet_names, dataframe_names, create_variable_mapping
# from OSeMOSYS.config import INPUT_FILE_PATH
# REGION, YEAR, TECHNOLOGY, FUEL, SEASON, DAYTYPE, DAILYTIMEBRACKET, TIMESLICE, MODE_OF_OPERATION, STORAGE, EMISSION = load_sets(file_path)


# This will creata a dict with all sets forms inside the yaml file

#%%
# Default, REGION, YEAR, TECHNOLOGY, FUEL, SEASON, DAYTYPE, DAILYTIMEBRACKET, TIMESLICE, MODE_OF_OPERATION, STORAGE, EMISSION = load_sets(INPUT_FILE_PATH)
# Printing the RFY set
# print("RFY set values:", RFY_set)
def load_dataframes(INPUT_FILE_PATH):
    """
    Load dataframes from the specified Excel file.
    args:
        file_path (str): Path to the Excel file.

    Returns:
        dict: Dictionary of DataFrames with specified names.
    """

    return read_excel_sheets_1(INPUT_FILE_PATH, sheet_names=sheet_names, dataframe_names=dataframe_names)

#%%
# def transform_dataframes(data_frames):
#     """
#     Transform the dataframes by stacking and renaming columns.
#     args:
#         data_frames (dict): Dictionary of DataFrames to transform.

#     Returns:
#         dict: Transformed DataFrames.
#     """
#     # Transforming the dataframes
#     RT = ['REGION', 'TECHNOLOGY']
#     RF = ['REGION', 'FUEL']
#     RE = ['REGION', 'EMISSION']
#     RY = ['REGION', 'YEAR']
#     RFLY = ['REGION', 'FUEL', 'YEAR']
#     RTLY = ['REGION', 'TECHNOLOGY', 'TIMESLICE', 'YEAR']
#     RTFMY = ['REGION', 'TECHNOLOGY', 'FUEL', 'MODE_OF_OPERATION', 'YEAR']
#     REY = ['REGION', 'EMISSION', 'YEAR']
#     RS = ['REGION','STORAGE']
#     RSY = ['REGION','STORAGE','YEAR']
# data_frames = load_dataframes()

def transform_all_dataframes(data_frames):
    """
    Transforma todos los DataFrames en data_frames según las configuraciones en dataframe_metadata.

    Args:
        data_frames (dict): Diccionario de DataFrames cargados.

    Returns:
        dict: Diccionario de DataFrames transformados.
    """
    transformed_dataframes = {}

    for param, config in dataframe_metadata.items():
        try:
            # Obtener el DataFrame y las configuraciones
            df = data_frames[param]
            indices = config["indices"]
            last_index = indices[-1]
            level = f"level_{len(indices) - 1}"

            # Transformar el DataFrame
            transformed_df = (
                df.set_index(indices[:-1])  # Usar todos los índices excepto el último
                  .stack()  # Apilar los datos
                  .reset_index()  # Restablecer el índice
                  .rename(columns={level: last_index, 0: "value"})  # Renombrar columnas
            )

            # Guardar el DataFrame transformado
            transformed_dataframes[param] = transformed_df

        except KeyError:
            print(f"Warning: El DataFrame '{param}' no se encuentra en data_frames.")
        except Exception as e:
            print(f"Error al transformar el DataFrame '{param}': {e}")

    return transformed_dataframes

def save_dataframes_to_csv(dataframes, input_file_path):
    """
    Guarda los DataFrames transformados en archivos CSV dentro de una carpeta específica.

    Args:
        dataframes (dict): Diccionario de DataFrames transformados.
        input_file_path (str): Ruta del archivo de entrada.
    """
    import os

    # Obtener la ruta base del proyecto
    root_folder = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

    # Definir la carpeta de salida global
    input_dir = os.path.dirname(input_file_path)

    # Obtener el nombre del archivo sin extensión
    file_name = os.path.splitext(os.path.basename(input_file_path))[0]

    # Crear la carpeta de salida basada en el nombre del archivo
    output_folder = os.path.join(input_dir, file_name)
    os.makedirs(output_folder, exist_ok=True)

    # Guardar cada DataFrame en un archivo CSV
    for df_name, df in dataframes.items():
        output_path = os.path.join(output_folder, f"{df_name}.csv")
        df.to_csv(output_path, index=False)
        print(f"Saved: {output_path}")



def dict_to_json(dataframe_dicts, input_file_path):
    """
    Crea un archivo JSON para Pyomo combinando conjuntos y parámetros.

    Args:
        dataframe_dicts (dict): Diccionario de DataFrames transformados.
        input_file_path (str): Ruta del archivo de entrada.
    """


    # Cargar los conjuntos usando load_sets
    Default, REGION, YEAR, TECHNOLOGY, FUEL, SEASON, DAYTYPE, DAILYTIMEBRACKET, TIMESLICE, MODE_OF_OPERATION, STORAGE, EMISSION = load_sets(input_file_path)
    
    # Crear el diccionario de conjuntos automáticamente usando create_variable_mapping
    sets_dict = create_variable_mapping(
        REGION, YEAR, TECHNOLOGY, FUEL, SEASON, DAYTYPE, DAILYTIMEBRACKET, TIMESLICE, MODE_OF_OPERATION, STORAGE, EMISSION
    )

    # Crear el diccionario para Pyomo
    pyomo_dict = {"sets": sets_dict, "parameters": {}}

    # Convertir cada DataFrame a un diccionario indexado
    for param, dictionary in dataframe_dicts.items():
        try:
            # Convertir las claves de tuplas a cadenas para JSON
            param_dict = dictionary.set_index(dataframe_metadata[param]["indices"]).to_dict('index')
            param_dict = {str(k): v["value"] for k, v in param_dict.items()}
            pyomo_dict["parameters"][param] = param_dict
        except KeyError:
            print(f"Warning: El DataFrame '{param}' no se encuentra en dataframe_dicts.")
        except Exception as e:
            print(f"Error al procesar el parámetro '{param}': {e}")
    return pyomo_dict

def adjust_json_for_pyomo(pyomo_dict):
    """
    Ajusta el JSON para que siga la estructura del ejemplo de Pyomo.

    Args:
        pyomo_dict (dict): Diccionario original con conjuntos y parámetros.

    Returns:
        dict: Diccionario ajustado.
    """
    adjusted_dict = {}

    # Ajustar conjuntos
    adjusted_dict.update(pyomo_dict["sets"])

    # Ajustar parámetros
    # adjusted_dict["parameters"] = {}
    for param, values in pyomo_dict["parameters"].items():
        if isinstance(values, dict):
            # adjusted_dict["parameters"][param] = [
            #     {"index": eval(k), "value": v} for k, v in values.items()
            # ]
            adjusted_dict[f"p_{param}"] = [
                {"index": eval(k), "value": v} for k, v in values.items()
            ]
        else:
            # adjusted_dict["parameters"][param] = values
             adjusted_dict[f"p_{param}"] = values
    return adjusted_dict
def transform_to_pyomo_format(input_dict):
    """
    Transforma un diccionario en el formato requerido por Pyomo.

    Args:
        input_dict (dict): Diccionario de entrada con conjuntos y parámetros.

    Returns:
        dict: Diccionario transformado en el formato requerido por Pyomo.
    """
    pyomo_data = {None: {}}

    # Procesar conjuntos
    if "sets" in input_dict:
        for set_name, set_values in input_dict["sets"].items():
            pyomo_data[None][set_name] = {None: set_values}

    # Procesar parámetros
    if "parameters" in input_dict:
        for param_name, param_values in input_dict["parameters"].items():
            if isinstance(param_values, list):
                # Convertir lista de índices y valores a un diccionario
                pyomo_data[None][param_name] = {
                    None: {tuple(entry["index"]): entry["value"] for entry in param_values}
                }
            elif isinstance(param_values, dict):
                # Convertir índices de cadenas a tuplas reales y añadir None
                pyomo_data[None][param_name] = {
                    None: {eval(k): v for k, v in param_values.items()}
                }
            else:
                # Parámetros escalares (añadir None como índice)
                pyomo_data[None][param_name] = {None: param_values}

    return pyomo_data

def export_to_json(data, output_path):
    """
    Exporta un diccionario a un archivo JSON.

    Args:
        data (dict): Diccionario a exportar.
        output_path (str): Ruta donde se guardará el archivo JSON.

    Returns:
        None
    """
    import json
    import os

    # Crear la carpeta de salida si no existe
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Guardar el archivo JSON
    with open(output_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)
    print(f"Archivo JSON guardado en: {output_path}")


# def generate_output_path(input_file_path, file_suffix=".json"):
#     """
#     Genera la ruta de salida para un archivo basado en el archivo de entrada.

#     Args:
#         input_file_path (str): Ruta del archivo de entrada.
#         file_suffix (str): Sufijo para el archivo de salida (por defecto "_adjusted.json").

#     Returns:
#         str: Ruta completa del archivo de salida.
#     """
#     import os

#     # Obtener la ruta base del proyecto
#     root_folder = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

#     # Definir la carpeta de salida global
#     output_base_folder = os.path.join(root_folder, "data")

#     # Obtener el nombre del archivo sin extensión
#     file_name = os.path.splitext(os.path.basename(input_file_path))[0]

#     # Crear la carpeta de salida basada en el nombre del archivo
#     output_folder = os.path.join(output_base_folder, file_name)
#     os.makedirs(output_folder, exist_ok=True)

#     # Generar la ruta completa del archivo de salida
#     output_path = os.path.join(output_folder, f"{file_name}{file_suffix}")
#     return output_path
def generate_output_path(input_file_path, file_suffix=".json"):
    """
    Genera la ruta de salida para un archivo basado en el archivo de entrada.

    Args:
        input_file_path (str): Ruta del archivo de entrada.
        file_suffix (str): Sufijo para el archivo de salida (por defecto ".json").

    Returns:
        str: Ruta completa del archivo de salida.
    """
    # Obtener el directorio y el nombre base del archivo de entrada
    input_dir = os.path.dirname(input_file_path)  # Directorio del archivo de entrada
    file_name = os.path.splitext(os.path.basename(input_file_path))[0]  # Nombre del archivo sin extensión

    # Crear una carpeta dentro del directorio del archivo de entrada con el mismo nombre que el archivo
    output_folder = os.path.join(input_dir, file_name)
    os.makedirs(output_folder, exist_ok=True)  # Crear la carpeta si no existe

    # Generar la ruta completa para el archivo JSON de salida
    output_path = os.path.join(output_folder, f"{file_name}{file_suffix}")
    return output_path



if __name__ == "__main__":
    # Cargar los DataFrames
    INPUT_FILE_PATH = '/home/david/OSeMOSYS-pyomo/data/Antiguos/SuperSimple.xlsx'
    data_frames = load_dataframes(INPUT_FILE_PATH)
    # Transformar los DataFrames
    transformed_dataframes = transform_all_dataframes(data_frames)

    # print(transformed_dataframes["CapitalCost"].head())  
    save_dataframes_to_csv(transformed_dataframes, INPUT_FILE_PATH)
    pyomo_dict = dict_to_json(transformed_dataframes, INPUT_FILE_PATH)
    adjusted_dict = adjust_json_for_pyomo(pyomo_dict)


        # Definir la ruta del archivo JSON ajustado
    adjusted_json_file_path = generate_output_path(INPUT_FILE_PATH)
    export_to_json(adjusted_dict, adjusted_json_file_path)
    # Ajustar y exportar el archivo JSON


  # Imprime las primeras filas del DataFrame transformado
# Ejemplo: Acceder a un DataFrame transformado
 # Imprime las primeras filas del DataFrame transformado

    # Transforming the dataframes
# YearSplit  = data_frames['YearSplit'].set_index('TIMESLICE').stack().reset_index().rename(columns = {"level_1": "YEAR", 0:"value"})
# DaySplit = data_frames['DaySplit'].set_index('DAILYTIMEBRACKET').stack().reset_index().rename(columns = {"level_1": "YEAR", 0:"value"})
# DaysInDayType =  data_frames['DaysInDayType'].set_index(['SEASON','DAYTYPE']).stack().reset_index().rename(columns = {"level_2": "YEAR", 0:"value"})
# Conversionls = data_frames['Conversionls'].set_index(['TIMESLICE']).stack().reset_index().rename(columns = {"level_1": "SEASON", 0:"value"})
# Conversionld = data_frames['Conversionld'].set_index(['TIMESLICE']).stack().reset_index().rename(columns = {"level_1": "DAYTYPE", 0:"value"})
# Conversionlh = data_frames['Conversionlh'].set_index(['TIMESLICE']).stack().reset_index().rename(columns = {"level_1": "DAILYTIMEBRACKET", 0:"value"})

# SpecifiedAnnualDemand = data_frames['SpecifiedAnnualDemand'].set_index(['REGION','FUEL']).stack().reset_index().rename(columns = {"level_2": "YEAR", 0:"value"})
# SpecifiedDemandProfile = data_frames['SpecifiedDemandProfile'].set_index(['REGION','FUEL','TIMESLICE']).stack().reset_index().rename(columns = {"level_3": "YEAR", 0:"value"})
# AccumulatedAnnualDemand = data_frames['AccumulatedAnnualDemand'].set_index(['REGION','FUEL']).stack().reset_index().rename(columns={"level_2": "YEAR",0:"value"})
# "Performance"
# CapacityToActivityUnit = data_frames['CapacityToActivityUnit'].set_index(['REGION']).stack().reset_index().rename(columns={"level_1": "TECHNOLOGY",0:"value"})
# CapacityFactor = data_frames['CapacityFactor'].set_index(['REGION','TECHNOLOGY','TIMESLICE']).stack().reset_index().rename(columns = {"level_3": "YEAR", 0:"value"})
# AvailabilityFactor = data_frames['AvailabilityFactor'].set_index(['REGION','TECHNOLOGY']).stack().reset_index().rename(columns={"level_2": "YEAR",0:"value"})
# OperationalLife = data_frames['OperationalLife'].set_index(['REGION']).stack().reset_index().rename(columns={"level_1": "TECHNOLOGY",0:"value"})
# ResidualCapacity = data_frames['ResidualCapacity'].set_index(['REGION','TECHNOLOGY'])  .stack().reset_index().rename(columns={"level_2": "YEAR",0:"value"})
# InputActivityRatio = data_frames['InputActivityRatio'].set_index(['REGION','TECHNOLOGY','FUEL','MODE_OF_OPERATION']).stack().reset_index().rename(columns={"level_4": "YEAR",0:"value"})
# OutputActivityRatio = data_frames['OutputActivityRatio'].set_index(['REGION','TECHNOLOGY','FUEL','MODE_OF_OPERATION']).stack().reset_index().rename(columns={"level_4": "YEAR",0:"value"})
# "Technology Costs"
# CapitalCost = data_frames['CapitalCost'].set_index(['REGION','TECHNOLOGY']).stack().reset_index().rename(columns={"level_2": "YEAR",0:"value"})
# VariableCost =data_frames['VariableCost'].set_index(['REGION','TECHNOLOGY','MODE_OF_OPERATION']).stack().reset_index().rename(columns={"level_3": "YEAR",0:"value"})
# FixedCost = data_frames['FixedCost'].set_index(['REGION','TECHNOLOGY']).stack().reset_index().rename(columns={"level_2": "YEAR",0:"value"})
# "Storage"
# TechnologyToStorage = data_frames['TechnologyToStorage'].set_index(['REGION','TECHNOLOGY','STORAGE']).stack().reset_index().rename(columns={"level_3": "MODE_OF_OPERATION",0:"value"})
# TechnologyFromStorage = data_frames['TechnologyFromStorage'].set_index(['REGION','TECHNOLOGY','STORAGE']).stack().reset_index().rename(columns={"level_3": "MODE_OF_OPERATION",0:"value"})
# StorageLevelStart = data_frames['StorageLevelStart'].set_index(['REGION']).stack().reset_index().rename(columns={"level_1": "STORAGE",0:"value"})
# StorageMaxChargeRate = data_frames['StorageMaxChargeRate'].set_index(['REGION']).stack().reset_index().rename(columns={"level_1": "STORAGE",0:"value"})
# StorageMaxDischargeRate = data_frames['StorageMaxDischargeRate'].set_index(['REGION']).stack().reset_index().rename(columns={"level_1": "STORAGE",0:"value"})
# MinStorageCharge = data_frames['MinStorageCharge'].set_index(['REGION','STORAGE']).stack().reset_index().rename(columns={"level_2": "YEAR",0:"value"})
# OperationalLifeStorage= data_frames['OperationalLifeStorage'].set_index(['REGION']).stack().reset_index().rename(columns={"level_1":'STORAGE',0:"value"})
# CapitalCostStorage =  data_frames['CapitalCostStorage'].set_index(['REGION','STORAGE']).stack().reset_index().rename(columns={"level_2": "YEAR",0:"value"})
# ResidualStorageCapacity = data_frames['ResidualStorageCapacity'].set_index(['REGION','STORAGE']).stack().reset_index().rename(columns={"level_2": "YEAR",0:"value"})
# "Capacity"
# CapacityOfOneTechnologyUnit =  data_frames['CapacityOfOneTechnologyUnit'].set_index(RT).stack().reset_index().rename(columns={"level_2": "YEAR",0:"value"})
# TotalAnnualMaxCapacity = data_frames['TotalAnnualMaxCapacity'].set_index(RT).stack().reset_index().rename(columns={"level_2": "YEAR",0:"value"})
# TotalAnnualMinCapacity  = data_frames['TotalAnnualMinCapacity'].set_index(RT).stack().reset_index().rename(columns={"level_2": "YEAR",0:"value"})
# TotalAnnualMaxCapacityInvestment = data_frames['TotalAnnualMaxCapacityInvestment'].set_index(RT).stack().reset_index().rename(columns={"level_2": "YEAR",0:"value"})
# TotalAnnualMinCapacityInvestment = data_frames['TotalAnnualMinCapacityInvestment'].set_index(RT).stack().reset_index().rename(columns={"level_2": "YEAR",0:"value"})
# "Activity constraints"
# TotalTechnologyAnnualActivityUpperLimit = data_frames['TotalTechnologyAnnualActivityUpperLimit'].set_index(RT).stack().reset_index().rename(columns={"level_2": "YEAR",0:"value"})
# TotalTechnologyAnnualActivityLowerLimit = data_frames['TotalTechnologyAnnualActivityLowerLimit'].set_index(RT).stack().reset_index().rename(columns={"level_2": "YEAR",0:"value"})
# TotalTechnologyModelPeriodActivityUpperLimit = data_frames['TotalTechnologyModelPeriodActivityUpperLimit'].set_index('REGION').stack().reset_index().rename(columns={"level_1": "TECHNOLOGY",0:"value"})
# TotalTechnologyModelPeriodActivityLowerLimit = data_frames['TotalTechnologyModelPeriodActivityLowerLimit'].set_index('REGION').stack().reset_index().rename(columns={"level_1": "TECHNOLOGY",0:"value"})
# "Reserve Margin"
# ReserveMarginTagTechnology = data_frames['ReserveMarginTagTechnology'].set_index(RT) .stack().reset_index().rename(columns={"level_2": "YEAR",0:"value"})
# ReserveMarginTagFuel = data_frames['ReserveMarginTagFuel'].set_index(RF) .stack().reset_index().rename(columns={"level_2": "YEAR",0:"value"})
# ReserveMargin = data_frames['ReserveMargin'].set_index('REGION')  .stack().reset_index().rename(columns={"level_1": "YEAR",0:"value"})
# """RE Generation Target"""
# RETagTechnology = data_frames['RETagTechnology'].set_index(RT).stack().reset_index().rename(columns={"level_2": "YEAR",0:"value"})
# RETagFuel = data_frames['RETagFuel'].set_index(RF).stack().reset_index().rename(columns={"level_2": "YEAR",0:"value"})
# REMinProductionTarget = data_frames['REMinProductionTarget'].set_index('REGION').stack().reset_index().rename(columns={"level_1": "YEAR",0:"value"})
# """Emissions"""
# EmissionActivityRatio = data_frames['EmissionActivityRatio'].set_index(RTEM).stack().reset_index().rename(columns={f"level_{len(RTEMY)-1}": "YEAR",0:"value"})
# EmissionsPenalty = data_frames['EmissionsPenalty'].set_index(RE).stack().reset_index().rename(columns={f"level_{len(REY)-1}": "YEAR",0:"value"})
# AnnualExogenousEmission= data_frames['AnnualExogenousEmission'].set_index(RE).stack().reset_index().rename(columns={f"level_{len(REY)-1}": "YEAR",0:"value"})
# AnnualEmissionLimit=   data_frames['AnnualEmissionLimit'].set_index(RE).stack().reset_index().rename(columns={f"level_{len(REY)-1}": "YEAR",0:"value"})
# ModelPeriodExogenousEmission=  data_frames['ModelPeriodExogenousEmission'].set_index('REGION').stack().reset_index().rename(columns={f"level_{len(RE)-1}": "EMISSION",0:"value"})
# ModelPeriodEmissionLimit= data_frames['ModelPeriodEmissionLimit'].set_index('REGION'). stack().reset_index().rename(columns={f"level_{len(RE)-1}": "EMISSION",0:"value"})
# """ New Parameters"""
# NumberOfExistingUnits =  data_frames['NumberOfExistingUnits'].set_index(RT).stack().reset_index().rename(columns={"level_2": "YEAR",0:"value"})
# VidaUtilRecuperada = data_frames['VidaUtilRecuperada'].set_index(['REGION']).stack().reset_index().rename(columns={"level_1": "TECHNOLOGY",0:"value"})
# CostoRecuperacion = data_frames['CostoRecuperacion'].set_index(RT).stack().reset_index().rename(columns={"level_2": "YEAR",0:"value"})
# ExportPrice = data_frames['ExportPrice'].set_index(RF).stack().reset_index().rename(columns={"level_2": "YEAR",0:"value"})
# MustRunTech  = data_frames['MustRunTech'].set_index(RT).stack().reset_index().rename(columns= {"level_2": "YEAR",0:"value"})
# MustRunFuel  = data_frames['MustRunFuel'].set_index(['REGION','FUEL','TIMESLICE']).stack().reset_index().rename(columns = {"level_3": "YEAR", 0:"value"})
# MustRun = data_frames['MustRun'].set_index('REGION').stack().reset_index().rename(columns={"level_1": "YEAR",0:"value"})
#%%

# def save_dataframes_to_csv(names_list, folder_path=DATA_FILE_PATH):
#     # Create the target folder if it doesn't exist
#     os.makedirs(folder_path, exist_ok=True)

#     for df_name in names_list:
#         # Check if the DataFrame name exists in the current global environment
#         if df_name in globals():
#             df = globals()[df_name]

#             # Construct the full file path
#             file_path = os.path.join(folder_path, f"{df_name}.csv")

#             # Save DataFrame to CSV
#             df.to_csv(file_path, index=False)

#             print(f"{df_name} saved to {file_path}")
#         else:
#             print(f"Error: DataFrame {df_name} not found in the current environment")




#%%

# YearSplit = YearSplit.set_index(['TIMESLICE', 'YEAR']).to_dict('index')
# print(YearSplit)
# DaySplit = DaySplit.set_index(['DAILYTIMEBRACKET', 'YEAR']).to_dict('index')
# DaysInDayType = DaysInDayType.set_index(['SEASON','DAYTYPE', 'YEAR']).to_dict('index')
# Conversionls = Conversionls.set_index(['TIMESLICE', 'SEASON']).to_dict('index')
# Conversionld = Conversionld.set_index(['TIMESLICE', 'DAYTYPE']).to_dict('index')
# Conversionlh = Conversionlh.set_index(['TIMESLICE', 'DAILYTIMEBRACKET']).to_dict('index')
# SpecifiedAnnualDemand = SpecifiedAnnualDemand.set_index(RFY).to_dict('index')
# SpecifiedDemandProfile = SpecifiedDemandProfile.set_index(RFLY).to_dict('index')
# AccumulatedAnnualDemand = AccumulatedAnnualDemand.set_index(RFY).to_dict('index')
# CapacityToActivityUnit = CapacityToActivityUnit.set_index(RT).to_dict('index')
# CapacityFactor = CapacityFactor.set_index(RTLY).to_dict('index')
# AvailabilityFactor = AvailabilityFactor.set_index(RTY).to_dict('index')
# OperationalLife = OperationalLife.set_index(RT).to_dict('index')
# ResidualCapacity = ResidualCapacity.set_index(RTY).to_dict('index')
# InputActivityRatio = InputActivityRatio.set_index(RTFMY).to_dict('index')
# OutputActivityRatio = OutputActivityRatio.set_index(RTFMY).to_dict('index')
# CapitalCost = CapitalCost.set_index(RTY).to_dict('index')
# VariableCost = VariableCost.set_index(RTMY).to_dict('index')
# FixedCost = FixedCost.set_index(RTY).to_dict('index')
# TechnologyToStorage = TechnologyToStorage.set_index(RTSM).to_dict('index')
# TechnologyFromStorage = TechnologyFromStorage.set_index(RTSM).to_dict('index')
# StorageLevelStart = StorageLevelStart.set_index(RS).to_dict('index')
# StorageMaxChargeRate = StorageMaxChargeRate.set_index(RS).to_dict('index')
# StorageMaxDischargeRate = StorageMaxDischargeRate.set_index(RS).to_dict('index')
# MinStorageCharge = MinStorageCharge.set_index(RSY).to_dict('index')
# OperationalLifeStorage = OperationalLifeStorage.set_index(RS).to_dict('index')
# CapitalCostStorage = CapitalCostStorage.set_index(RSY).to_dict('index')
# ResidualStorageCapacity = ResidualStorageCapacity.set_index(RSY).to_dict('index')
# CapacityOfOneTechnologyUnit = CapacityOfOneTechnologyUnit.set_index(RTY).to_dict('index')
# TotalAnnualMaxCapacity = TotalAnnualMaxCapacity.set_index(RTY).to_dict('index')
# TotalAnnualMinCapacity = TotalAnnualMinCapacity.set_index(RTY).to_dict('index') 
# TotalAnnualMaxCapacityInvestment = TotalAnnualMaxCapacityInvestment.set_index(RTY).to_dict('index')
# TotalAnnualMinCapacityInvestment = TotalAnnualMinCapacityInvestment.set_index(RTY).to_dict('index')
# TotalTechnologyAnnualActivityUpperLimit = TotalTechnologyAnnualActivityUpperLimit.set_index(RTY).to_dict('index') 
# TotalTechnologyAnnualActivityLowerLimit = TotalTechnologyAnnualActivityLowerLimit.set_index(RTY).to_dict('index')
# TotalTechnologyModelPeriodActivityUpperLimit = TotalTechnologyModelPeriodActivityUpperLimit.set_index(RT).to_dict('index')
# TotalTechnologyModelPeriodActivityLowerLimit = TotalTechnologyModelPeriodActivityLowerLimit.set_index(RT).to_dict('index')
# ReserveMarginTagTechnology = ReserveMarginTagTechnology.set_index(RTY).to_dict('index')
# ReserveMarginTagFuel = ReserveMarginTagFuel.set_index(RFY).to_dict('index')
# ReserveMargin = ReserveMargin.set_index(RY).to_dict('index')
# RETagTechnology = RETagTechnology.set_index(RTY).to_dict('index')
# RETagFuel = RETagFuel.set_index(RFY).to_dict('index')
# REMinProductionTarget = REMinProductionTarget.set_index(RY).to_dict('index')
# EmissionActivityRatio = EmissionActivityRatio.set_index(RTEMY).to_dict('index')
# EmissionsPenalty = EmissionsPenalty.set_index(REY).to_dict('index')
# AnnualExogenousEmission = AnnualExogenousEmission.set_index(REY).to_dict('index')
# AnnualEmissionLimit = AnnualEmissionLimit.set_index(REY).to_dict('index')
# ModelPeriodExogenousEmission = ModelPeriodExogenousEmission.set_index(RE).to_dict('index')
# ModelPeriodEmissionLimit = ModelPeriodEmissionLimit.set_index(RE).to_dict('index')
# NumberOfExistingUnits = NumberOfExistingUnits.set_index(RTY).to_dict('index')
# VidaUtilRecuperada = VidaUtilRecuperada.set_index(RT).to_dict('index')
# CostoRecuperacion = CostoRecuperacion.set_index(RTY).to_dict('index')
# ExportPrice = ExportPrice.set_index(RFY).to_dict('index')
# MustRunTech = MustRunTech.set_index(RTY).to_dict('index')
# MustRunFuel = MustRunFuel.set_index(RFLY).to_dict('index')
# MustRun = MustRun.set_index(RY).to_dict('index')
#%%



# def ListDict(name, dictionary):
#     my_list = []
#     for row in dictionary.items():
#         # iterar sobre las posiciones del dataframe
#             # print(row[1]['value']) #diccionario
#             # print(row[0][0]) #lista
#         new_row = {"index":row[0], "value":row[1]["value"]} 
#         my_list.append(new_row)
#     # return {name:my_list}    
#     return {name: json.loads(json.dumps(my_list))}
# # #%%

# def parameters_dict(dataframe_names):
#     param_dict = {}
#     for name in dataframe_names:
#         if name in globals():
#             param_dict[name] = globals()[name]

#     for data in list(param_dict):  # Use list(param_dict) to create a snapshot of keys
#         try:
#             new_key = f"p_{data}"  # Add "p_" prefix to the key
#             param_dict[new_key] = param_dict.pop(data)
#             param_dict.update(ListDict(new_key, param_dict[new_key]))
#         except KeyError:
#             print(f"KeyError: {data}")

#     return param_dict
            
# def dict_to_json():
#     ParamDict = parameters_dict(dataframe_names) 
#     #%%
#     OsemosysDict = {
#         "REGION":REGION,
#         "YEAR":YEAR,
#         "TECHNOLOGY":TECHNOLOGY,
#         "FUEL":FUEL,
#         "SEASON":SEASON,
#         "DAYTYPE":DAYTYPE,
#         "DAILYTIMEBRACKET":DAILYTIMEBRACKET,
#         "TIMESLICE":TIMESLICE,
#         "MODE_OF_OPERATION":MODE_OF_OPERATION,
#         "STORAGE":STORAGE,
#         "EMISSION":EMISSION,
#         # OsemosysDict
#     }
#     if isinstance (ParamDict, dict):
#         OsemosysDict.update(ParamDict)


#     with open('../data/'+'/Data.json', 'w') as json_file:
#         json.dump(OsemosysDict, json_file) 

# if __name__ == "__main__":
#     dict_to_json()
#     save_dataframes_to_csv(dataframe_names)
