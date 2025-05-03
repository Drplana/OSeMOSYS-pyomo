import os, sys
root_folder = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(root_folder)
import pandas as pd
from OSeMOSYS.config import INPUT_FILE_PATH

def load_sets(file_path):
    """
    Carga los conjuntos y parámetros desde un archivo Excel.

    Args:
        file_path (str): Ruta al archivo Excel.

    Returns:
        tuple: Contiene los conjuntos y parámetros cargados desde el archivo Excel.
    """
    DataExcel = pd.ExcelFile(file_path)
    Default = pd.read_excel(DataExcel, sheet_name='Default Parameters', index_col=0)
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

def read_excel_sheets(file_path, sheet_names, dataframe_names):
    """
    Lee hojas de Excel y devuelve un diccionario de DataFrames con nombres especificados.

    Args:
        file_path (str): Ruta al archivo Excel.
        sheet_names (list): Lista de nombres de hojas a leer.
        dataframe_names (list): Lista de nombres deseados para los DataFrames.

    Returns:
        dict: Diccionario de DataFrames con nombres especificados.
    """
    data_frames = {}
    for sheet_name, df_name in zip(sheet_names, dataframe_names):
        data_frames[df_name] = pd.read_excel(file_path, sheet_name=sheet_name)
    return data_frames

if __name__ == "__main__":
    # Ejemplo de uso
    print(f"Usando archivo de entrada: {INPUT_FILE_PATH}")
    Default, REGION, YEAR, TECHNOLOGY, FUEL, SEASON, DAYTYPE, DAILYTIMEBRACKET, TIMESLICE, MODE_OF_OPERATION, STORAGE, EMISSION = load_sets(INPUT_FILE_PATH)
    print("Conjuntos y parámetros cargados correctamente.")