'''
This file illustrates the use of the osemodsys-pyomo library to run a test case

It load the main function from the library and provides as parameters the input excel file and the folder where
the results should be written
'''

import os
from OSeMOSYS.SolveSolutions import solve_model
from OSeMOSYS.postprocessing.plots import plot_activity

# go up one folder to be in the main repository folder
os.chdir('..')

# Define the input file and the folder to store the results and run the model
results_folder = 'results'
input_file = 'data/OsemosysNew.xlsx'
solve_model(input_file, results_folder)

# plot the results
datafile = results_folder + '/v_RateOfActivity.csv'
plot_activity(datafile)