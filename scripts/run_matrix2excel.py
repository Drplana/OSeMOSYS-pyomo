import sys
import os

# Agregar la carpeta raíz del proyecto al PYTHONPATH
root_folder = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(root_folder)

# Importar el módulo Matrix2excel
from OSeMOSYS.Matrix2excel import generate_excel_file, assign_parameters
from OSeMOSYS.ReadSets import create_multiindex_dataframe, load_sets
from OSeMOSYS.utils import create_variable_mapping
from OSeMOSYS.config import INPUT_FILE_PATH

def run_matrix2excel(input_file=INPUT_FILE_PATH):
    """
    Función principal para ejecutar el script Matrix2excel.
    Carga los conjuntos de datos, asigna parámetros y genera un archivo Excel.
    """
    Default, REGION, YEAR, TECHNOLOGY, FUEL, SEASON, DAYTYPE, DAILYTIMEBRACKET, TIMESLICE, MODE_OF_OPERATION, STORAGE, EMISSION = load_sets(input_file)
    variable_mapping = create_variable_mapping(
        REGION, YEAR, TECHNOLOGY, FUEL, SEASON, DAYTYPE, DAILYTIMEBRACKET, TIMESLICE, MODE_OF_OPERATION, STORAGE, EMISSION
    )
    result_dataframes = create_multiindex_dataframe(variable_mapping)
    parameters = assign_parameters(result_dataframes)
    generate_excel_file(parameters, input_file)
    print(f"Archivo Excel generado exitosamente para el archivo de entrada: {input_file}")
if __name__ == "__main__":
    # Ejecutar la función principal y trabajar con multiples archivos de entrada
    run_matrix2excel(input_file=INPUT_FILE_PATH) # ruta del primer archivo configurado en config.py
    supersimple2 = '/home/david/OSeMOSYS-pyomo/data/SuperSimplePVTSDT.xlsx' # ruta del segundo archivo
    run_matrix2excel(input_file=supersimple2)

