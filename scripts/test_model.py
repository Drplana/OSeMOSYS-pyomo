'''
This file illustrates the use of the osemodsys-pyomo library to run a test case

It loads the main function from the library and provides as parameters the input excel file and the folder where
the results should be written
'''
import os,sys
# include the main library path (the parent folder) in the path environment variable
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

#Two solution to import the library
# as a package (defined in __init__.py) => function calls are
import OSeMOSYS as om

# as separate functions:
from OSeMOSYS.SolveSolutions import solve_model
from OSeMOSYS.postprocessing.plots import plot_activity

# Define the input file and the folder to store the results and run the model
results_folder = '../results'
input_file = '../data/OsemosysNew.xlsx'
om.solve_model(input_file, results_folder)

# plot the results
datafile = results_folder + '/v_RateOfActivity.csv'
om.plot_activity(datafile)