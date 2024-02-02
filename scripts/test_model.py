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
from OSeMOSYS.postprocessing.plots import plot_activity

# Define the input file and the folder to store the results and run the model
results_folder = '../results'
input_file = '../data/OsemosysNew.xlsx'
om.solve_model(input_file, results_folder)

# plot the results
datafile = results_folder + '/v_RateOfActivity.csv'
om.plot_activity(datafile)