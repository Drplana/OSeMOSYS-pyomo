#%%
import json
import pandas as pd
import os
import sys
root_folder = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(root_folder)
from OSeMOSYS.ReadSets import create_multiindex_dataframe2, load_sets, generate_lists_dict, create_multiindex_dataframe
from OSeMOSYS.utils import sheet_names, create_variable_mapping, dataframe_metadata
# from OSeMOSYS.config import INPUT_FILE_PATH
import warnings


def read_existing_data(file_path, sheet_names):
    """
    Lee los datos existentes de un archivo Excel.

    Args:
        file_path (str): Ruta al archivo Excel.
        sheet_names (list): Lista de nombres de hojas a leer.

    Returns:
        dict: Diccionario con los datos existentes, donde las claves son los nombres de las hojas.
    """
    existing_data = {}
    try:
        with pd.ExcelFile(file_path) as xls:
            for sheet_name in sheet_names:
                try:
                    existing_data[sheet_name] = pd.read_excel(xls, sheet_name=sheet_name)
                except ValueError:
                    print(f"Hoja {sheet_name} no encontrada en el archivo. Se ignorará.")
                    existing_data[sheet_name] = pd.DataFrame()
    except FileNotFoundError:
        print(f"Archivo {file_path} no encontrado. Se asumirá que no hay datos existentes.")
    return existing_data

def combine_data(existing_data, new_data, index_columns):
    """
    Combina los datos existentes con los nuevos, evitando duplicados y preservando los datos existentes.

    Args:
        existing_data (pd.DataFrame): Datos existentes.
        new_data (pd.DataFrame): Nuevos datos a agregar.
        index_columns (list): Columnas que definen las combinaciones únicas (índices).

    Returns:
        pd.DataFrame: Datos combinados sin duplicados, con nuevas combinaciones agregadas.
    """
    if existing_data.empty:
        return new_data

    # Validar que las columnas de índice existan en ambos DataFrames
    missing_columns_existing = [col for col in index_columns if col not in existing_data.columns]
    missing_columns_new = [col for col in index_columns if col not in new_data.columns]

    if missing_columns_existing:
        print(f"Advertencia: Las siguientes columnas faltan en los datos existentes: {missing_columns_existing}")
        for col in missing_columns_existing:
            existing_data[col] = None

    if missing_columns_new:
        print(f"Advertencia: Las siguientes columnas faltan en los nuevos datos: {missing_columns_new}")
        for col in missing_columns_new:
            new_data[col] = None

    # Verificar si las columnas de índice están presentes después de agregar las faltantes
    if not all(col in existing_data.columns for col in index_columns) or not all(col in new_data.columns for col in index_columns):
        print(f"Error: No se pueden encontrar todas las columnas de índice en los DataFrames. Índices esperados: {index_columns}")
        return existing_data

    # Identificar combinaciones únicas en los datos existentes
    existing_combinations = existing_data[index_columns].drop_duplicates()

    # Identificar combinaciones nuevas que no están en los datos existentes
    new_combinations = new_data[index_columns].drop_duplicates()

    if existing_combinations.empty or new_combinations.empty:
        print("Advertencia: No hay combinaciones únicas para comparar. Se devolverán los datos existentes.")
        return existing_data

    unique_combinations = pd.merge(
        new_combinations,
        existing_combinations,
        on=index_columns,
        how="left",
        indicator=True
    ).query('_merge == "left_only"').drop(columns=["_merge"])

    if unique_combinations.empty:
        print("Advertencia: No se encontraron combinaciones nuevas para agregar.")
        return existing_data

    # Filtrar los nuevos datos para incluir solo las combinaciones únicas
    new_data_filtered = pd.merge(new_data, unique_combinations, on=index_columns, how="inner")

    # Combinar los datos existentes con los nuevos filtrados
    combined_data = pd.concat([existing_data, new_data_filtered], ignore_index=True)

    return combined_data


def assign_parameters(result_dataframes):
    """
    Asigna los DataFrames generados a un diccionario de parámetros dinámicamente.

    Args:
        result_dataframes (dict): Diccionario con los DataFrames generados.

    Returns:
        dict: Diccionario con los parámetros organizados.
    """
    parameters = {}
    for df_name, metadata in dataframe_metadata.items():
        key = metadata["key"]
        if key in result_dataframes:
            parameters[df_name] = result_dataframes[key]  # Usar df_name como clave
        else:
            print(f"Warning: DataFrame '{key}' not found in result_dataframes. Skipping...")
    return parameters


def generate_excel_file(parameters, INPUT_FILE_PATH):
    """
    Generates an Excel file with the specified parameters.

    Args:
        parameters (dict): Dictionary containing DataFrames to be written to Excel.
        output_file_path (str): Path to the output Excel file.
    """
    # dataframes = [globals()[name] for name in dataframe_names if name in globals() and isinstance(globals()[name], pd.DataFrame)]
    dataframes = {key: value for key, value in parameters.items() if isinstance(value, pd.DataFrame)}

    if len(sheet_names) != len(dataframes):
        raise ValueError("El número de nombres de hojas no coincide con el número de DataFrames.")

# %%
    try:
        with pd.ExcelWriter(INPUT_FILE_PATH,
                        mode="a",
                        engine="openpyxl",
                        if_sheet_exists= "replace"
                        ) as writer:
            for sheet_name,df in zip(sheet_names, dataframes.values()):
                if df.empty:
                    print(f"Skipping empty DataFrame for sheet: {sheet_name}")
                    continue
                print(f"Writing DataFrame to sheet: {sheet_name}")
                df.to_excel(writer, sheet_name=sheet_name, index = False)

                # Access and add filters to each sheet
                workbook = writer.book
                sheet = workbook[sheet_name]
                sheet.auto_filter.ref = sheet.dimensions
                sheet.freeze_panes = 'A2'
        print(f"Archivo Excel generado exitosamente en: {INPUT_FILE_PATH}")
    except Exception as e:
        print(f"Error while writing to Excel: {e}")
def generate_excel_file_new(parameters, INPUT_FILE_PATH):
    """
    Generates an Excel file with the specified parameters, updating existing sheets without overwriting data.

    Args:
        parameters (dict): Dictionary containing DataFrames to be written to Excel.
        INPUT_FILE_PATH (str): Path to the output Excel file.
    """
    # Leer los datos existentes del archivo Excel
    existing_data = {}
    try:
        with pd.ExcelFile(INPUT_FILE_PATH) as excel_file:
            for sheet_name in sheet_names:
                if sheet_name in excel_file.sheet_names:
                    existing_data[sheet_name] = pd.read_excel(excel_file, sheet_name=sheet_name)
    except FileNotFoundError:
        print(f"El archivo {INPUT_FILE_PATH} no existe. Se creará uno nuevo.")

    # Combinar los datos existentes con los nuevos
    updated_data = {}
    for sheet_name, new_df in zip(sheet_names, parameters.values()):
        index_columns = dataframe_metadata.get(sheet_name, {}).get("indices", [])
        if not index_columns:
            print(f"Advertencia: No se encontraron índices para la hoja {sheet_name}. Se omitirá.")
            continue
        updated_data[sheet_name] = combine_data(
            existing_data.get(sheet_name, pd.DataFrame()),
            new_df,
            index_columns
        )

    # Escribir los datos actualizados en el archivo Excel
    try:
        with pd.ExcelWriter(INPUT_FILE_PATH, mode="w", engine="openpyxl") as writer:
            for sheet_name, df in updated_data.items():
                if df.empty:
                    print(f"Skipping empty DataFrame for sheet: {sheet_name}")
                    continue
                print(f"Writing updated DataFrame to sheet: {sheet_name}")
                df.to_excel(writer, sheet_name=sheet_name, index=False)

                # Agregar filtros y congelar la primera fila
                workbook = writer.book
                sheet = workbook[sheet_name]
                sheet.auto_filter.ref = sheet.dimensions
                sheet.freeze_panes = 'A2'
        print(f"Archivo Excel actualizado exitosamente en: {INPUT_FILE_PATH}")
    except Exception as e:
        print(f"Error while writing to Excel: {e}")

if __name__ == "__main__":   # if the file is run in standalone
    # Load the sets and create the DataFrames
    INPUT_FILE_PATH = os.path.join(root_folder, 'data', '01-BaseScenarioVOLL.xlsx')
    Default, REGION, YEAR, TECHNOLOGY, FUEL, SEASON, DAYTYPE, DAILYTIMEBRACKET, TIMESLICE, MODE_OF_OPERATION, STORAGE, EMISSION = load_sets(INPUT_FILE_PATH)
    # Create the variable mapping
    variable_mapping = create_variable_mapping(
        REGION, YEAR, TECHNOLOGY, FUEL, SEASON, DAYTYPE, DAILYTIMEBRACKET, TIMESLICE, MODE_OF_OPERATION, STORAGE, EMISSION
    )
    """
    Two ways to create the DataFrames:
    1. Using the lists_dict and variable_mapping
    2. Using the dataframe_metadata and variable_mapping
    """    
    lists_dict = generate_lists_dict(dataframe_metadata)
    result_dataframes = create_multiindex_dataframe2(lists_dict, variable_mapping)
    result_dataframes_1 = create_multiindex_dataframe(variable_mapping)
    # print(result_dataframes)
    parameters = assign_parameters(result_dataframes_1)

    # print(parameters2)
    # # parameters = assign_parameters(result_dataframes)
    # # # print(parameters)
    
    generate_excel_file(parameters, INPUT_FILE_PATH)
    # generate_excel_file_new(parameters, INPUT_FILE_PATH)

























# %%
