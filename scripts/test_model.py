'''
This file illustrates the use of the osemodsys-pyomo library to run a test case

It loads the main function from the library and provides as parameters the input excel file and the folder where
the results should be written
'''
import os,sys
# include the main library path (the parent folder) in the path environment variable
root_folder = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(root_folder)


#Two solution to import the library
# (1) as a package (defined in __init__.py) => function calls are done through the lpackage (eg om.solve_model)
import OSeMOSYS as om

# (2) as separate functions:
from OSeMOSYS.SolveSolutions import solve_model
from OSeMOSYS.postprocessing.plots import plot_activity, assign_colors
from OSeMOSYS.config import INPUT_FILE_PATH, RESULTS_FOLDER,COLOR_DICT, keyword_colors
from OSeMOSYS.readXlsData import dict_to_json
# Define the input file and the folder to store the results and run the model
# results_folder = '../results'
results_folder = RESULTS_FOLDER
input_file = INPUT_FILE_PATH
# om.solve_model(input_file, results_folder)
dict_to_json()


# plot the results
try:
    print(f"Ejecutando el modelo con el archivo de entrada: {input_file}")
    print(f"Los resultados se guardarán en: {results_folder}")
    om.solve_model(input_file, results_folder)
    print("Modelo ejecutado con éxito.")
except Exception as e:
    print(f"Error al ejecutar el modelo: {e}")
    sys.exit(1)

# Graficar los resultados
try:
    datafile = os.path.join(results_folder, 'v_ProductionByTechnologyAnnual.csv')
    print(f"Generating chart from: {datafile}")
    technologies = datafile['TECHNOLOGY'].unique()
    om.plot_activity(datafile)
    rate_file = os.path.join(RESULTS_FOLDER, 'v_RateOfProductionByTechnology.csv')
    

    
    color_dict = assign_colors(technologies, keyword_colors)
    om.create_production_plot(om.load_and_prepare_data(rate_file), color_dict)
    SELECTED_YEARS = [2020, 2024, 2025, 2030,  2040, 2050]
    om.plot_accumulated_capacity(RESULTS_FOLDER, SELECTED_YEARS, color_dict=color_dict)




    print("Charts generated.")
except FileNotFoundError:
    print(f"Error: File not found: {datafile}")
except Exception as e:
    print(f"Generating charts error: {e}")