import pandas as pd
import os, sys
root_folder = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(root_folder)
# from OSeMOSYS.config import INPUT_FILE_PATH
from OSeMOSYS.utils import create_variable_mapping, dataframe_names, sheet_names, dataframe_metadata

# file_path = INPUT_FILE_PATH
# print(file_path)
def load_sets(INPUT_FILE_PATH):
    
    DataExcel = pd.ExcelFile(INPUT_FILE_PATH)
    Default = (pd.read_excel(DataExcel, sheet_name = 'Default Parameters', index_col=0))
    REGION = list(pd.read_excel(DataExcel, sheet_name='R')['REGION'])
    initial_year = pd.read_excel(DataExcel, sheet_name='Y')['START_YEAR'][0]
    final_year = pd.read_excel(DataExcel, sheet_name='Y')['FINAL_YEAR'][0]
    YEAR = list(range(int(initial_year), int(final_year) + 1))

    TECHNOLOGY = list(pd.read_excel(DataExcel, sheet_name='T')['TECHNOLOGY'])
    FUEL = list(pd.read_excel(DataExcel, sheet_name='F')['FUEL'])
    SEASON = list(pd.read_excel(DataExcel, sheet_name='LS')['SEASON'])
    DAYTYPE = list(pd.read_excel(DataExcel, sheet_name='LD')['DAYTYPE'])
    DAILYTIMEBRACKET = list(pd.read_excel(DataExcel, sheet_name='LH')['DAILYTIMEBRACKET'])
    TIMESLICE = list(pd.read_excel(DataExcel, sheet_name='L')['TIMESLICE'])
    MODE_OF_OPERATION = list(pd.read_excel(DataExcel, sheet_name='M')['ModeOfOperation'])
    STORAGE = list(pd.read_excel(DataExcel, sheet_name='S')['STORAGE'])
    EMISSION = list(pd.read_excel(DataExcel, sheet_name='E')['EMISSION'])
    DataExcel.close()
    return Default, REGION, YEAR, TECHNOLOGY, FUEL, SEASON, DAYTYPE, DAILYTIMEBRACKET, TIMESLICE, MODE_OF_OPERATION, STORAGE, EMISSION

# Default, REGION, YEAR, TECHNOLOGY, FUEL, SEASON, DAYTYPE, DAILYTIMEBRACKET, TIMESLICE, MODE_OF_OPERATION, STORAGE, EMISSION = load_sets(INPUT_FILE_PATH)

# variable_mapping = create_variable_mapping(
#     REGION, YEAR, TECHNOLOGY, FUEL, SEASON, DAYTYPE, DAILYTIMEBRACKET, TIMESLICE, MODE_OF_OPERATION, STORAGE, EMISSION
# )
def read_excel_sheets_2(INPUT_FILE_PATH, sheet_names, dataframe_names):
    """
    Reads Excel sheets and returns a dictionary of DataFrames with specified names.

    Parameters:
    - file_path (str): Path to the Excel file.
    - sheet_names (list): List of sheet names to read.
    - dataframe_names (list): List of desired DataFrame names.

    Returns:
    - dict: Dictionary of DataFrames with specified names.
    """
    data_frames = {}
    for sheet_name, df_name in zip(sheet_names, dataframe_names):
        data_frames[df_name] = pd.read_excel(INPUT_FILE_PATH, sheet_name=sheet_name)

    return data_frames


def read_excel_sheets_1(INPUT_FILE_PATH, sheet_names, dataframe_names):
    """
    Reads Excel sheets and returns a dictionary of DataFrames with specified names.

    Parameters:
    - INPUT_FILE_PATH (str): Path to the Excel file.
    - sheet_names (list): List of sheet names to read.
    - dataframe_metadata (dict): Dictionary containing metadata for each DataFrame.

    Returns:
    - dict: Dictionary of DataFrames with specified names.
    """
    data_frames = {}

    for sheet_name, df_name in zip(sheet_names, dataframe_names):
        try:
            # Leer la hoja de Excel
            df = pd.read_excel(INPUT_FILE_PATH, sheet_name=sheet_name)

            # Verificar si el DataFrame está vacío
            if df.empty:
                print(f"Warning: Sheet '{sheet_name}' is empty in {INPUT_FILE_PATH}. Skipping...")
                continue

            # Asignar el DataFrame al diccionario
            data_frames[df_name] = df
        except ValueError as e:
            print(f"Warning: Sheet '{sheet_name}' not found in {INPUT_FILE_PATH}. Skipping...")
            continue

    return data_frames

def generate_lists_dict(dataframe_metadata):
    """
    Genera un diccionario lists_dict a partir de dataframe_metadata.

    Args:
        dataframe_metadata (dict): Diccionario que contiene la metadata de los DataFrames.

    Returns:
        dict: Diccionario lists_dict con las claves y combinaciones de índices.
    """
    lists_dict = {metadata["key"]: metadata["indices"] for metadata in dataframe_metadata.values()}
    return lists_dict


def create_multiindex_dataframe2(lists_dict, data_dict):
    """
    Crea un diccionario de DataFrames con índices MultiIndex basados en los conjuntos.

    Args:
        lists_dict (dict): Diccionario que define las combinaciones de índices.
        data_dict (dict): Diccionario que contiene las listas necesarias para los índices.

    Returns:
        dict: Diccionario de DataFrames con índices MultiIndex.
    """
    result_dict = {}
    for key, value in lists_dict.items():
        index_lists = [data_dict[item] for item in value[:-1]]
        df = pd.MultiIndex.from_product(index_lists, names=value[:-1])
        result_df = pd.DataFrame('', index=df, columns=data_dict[value[-1]]).reset_index()
        result_dict[key] = result_df
    return result_dict
def create_multiindex_dataframe(data_dict):
    """
    Crea un diccionario de DataFrames con índices MultiIndex basados en dataframe_metadata.

    Args:
        data_dict (dict): Diccionario que contiene las listas necesarias para los índices.

    Returns:
        dict: Diccionario de DataFrames con índices MultiIndex.
    """
    # Generar lists_dict desde dataframe_metadata
    lists_dict = {metadata["key"]: metadata["indices"] for metadata in dataframe_metadata.values()}
    
    result_dict = {}
    for key, value in lists_dict.items():
        try:
            # Obtener las listas de índices
            index_lists = [data_dict[item] for item in value[:-1]]
            
            # Crear el índice MultiIndex
            df = pd.MultiIndex.from_product(index_lists, names=value[:-1])
            
            # Crear las columnas basadas en el último índice
            columns = data_dict[value[-1]] if value[-1] in data_dict else []
            
            # Crear el DataFrame
            result_df = pd.DataFrame('', index=df, columns=columns).reset_index()
            
            # Usar la clave de lists_dict
            result_dict[key] = result_df
        except KeyError as e:
            print(f"Error: La clave {e} no se encuentra en data_dict para el DataFrame '{key}'.")
        except ValueError as e:
            print(f"Error al crear el DataFrame '{key}': {e}")
    return result_dict

# def read_defaults(filename):
#     DataExcel = pd.ExcelFile(filename)
#     Default = (pd.read_excel(DataExcel, sheet_name = 'Default Parameters', index_col=0))

#     DataExcel.close()
#     return Default
if __name__ == "__main__":
    INPUT_FILE_PATH= os.path.join(root_folder, 'data', 'SuperSimpleExpanded.xlsx')
    Default, REGION, YEAR, TECHNOLOGY, FUEL, SEASON, DAYTYPE, DAILYTIMEBRACKET, TIMESLICE, MODE_OF_OPERATION, STORAGE, EMISSION = load_sets(INPUT_FILE_PATH)
    variable_mapping = create_variable_mapping(
        REGION, YEAR, TECHNOLOGY, FUEL, SEASON, DAYTYPE, DAILYTIMEBRACKET, TIMESLICE, MODE_OF_OPERATION, STORAGE, EMISSION
    )
    lists_dict = generate_lists_dict(dataframe_metadata)
    # print(lists_dict)
    result_dataframes_1 = create_multiindex_dataframe(variable_mapping)
    # print(result_dataframes_1)
    result_dataframes_2 = create_multiindex_dataframe2(lists_dict, variable_mapping)
    # # print(result_dataframes_2)
    # result_dataframes_1 = create_multiindex_dataframe(variable_mapping)
    # result_dataframes_2 = create_multiindex_dataframe2(lists_dict, variable_mapping)

    # Comparar las claves generadas
    print("Claves generadas por create_multiindex_dataframe:")
    print(result_dataframes_1.keys())
    print("\nClaves generadas por create_multiindex_dataframe2:")
    print(result_dataframes_2.keys())

    # Comparar las estructuras de los DataFrames
    for key in result_dataframes_1.keys():
        if key in result_dataframes_2:
            print(f"\nComparando DataFrame para la clave: {key}")
            print("Salida de create_multiindex_dataframe:")
            print(result_dataframes_1[key].head())
            print("\nSalida de create_multiindex_dataframe2:")
            print(result_dataframes_2[key].head())
        else:
            print(f"\nLa clave '{key}' no está presente en result_dataframes_2.")
    


    # data_frames_1 = read_excel_sheets_1(INPUT_FILE_PATH, sheet_names)
    # data_frames_2 = read_excel_sheets_2(INPUT_FILE_PATH, sheet_names, dataframe_names)

    # # Comparar las claves generadas
    # print("\nComparando estructuras de los DataFrames:")
    # for key in data_frames_1.keys():
    #     if key in data_frames_2:
    #         print(f"\nComparando DataFrame para la clave: {key}")
    #         print("Salida de read_excel_sheets_1:")
    #         print(data_frames_1[key].head())
    #         print("\nSalida de read_excel_sheets_2:")
    #         print(data_frames_2[key].head())
    #     else:
    #         print(f"\nLa clave '{key}' no está presente en data_frames_2.")

    # for key in data_frames_2.keys():
    #     if key not in data_frames_1:
    #         print(f"\nLa clave '{key}' no está presente en data_frames_1.")