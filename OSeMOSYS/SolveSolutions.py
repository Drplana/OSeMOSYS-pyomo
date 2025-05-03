#%%
import os
import pandas as pd
from pyomo.environ import value, Var
from pyomo.opt import SolverFactory
from itertools import count
from .MainModel import define_model
#%%
from vincent.colors import brews
from .config import INPUT_FILE_PATH, RESULTS_FOLDER

# from readXlsData import read_excel

# from highspy import *

def solve_model(input_file,results_folder):

    # ParamDict, OsemosysDict = read_excel(input_file,results_folder=results_folder)

    #define the model with default values:
    model = define_model(input_file)

    # TODO: use the OsemosysDIct directly instead of passing through the json file
    instance = model.create_instance('../data/Data.json')
    # instance.EBa11_EnergyBalanceEachTS5.pprint()
    # instance.Must_Run.pprint()
    # instance.SpecifiedDemand_EQ.pprint()
    # instance.EBa9_EnergyBalanceEachTS3.pprint()
    # instance.EBa11_EnergyBalanceEachTS5.pprint()
    #%%
    "Solvers used - cbc, ***scip*** or highs"
    #opt = SolverFactory("appsi_highs")
    #opt = SolverFactory("scip", tempdir = new_folder_path)
    # cbc_path = "C:/Program Files (x86)/COIN-OR/1.7.4/win32-msvc15/bin/cbc.exe"
    # opt = SolverFactory('cbc', executable=cbc_path)
    opt = SolverFactory("gurobi")
    #%%
    # opt.solve(instance)
    results = opt.solve(instance)
    results.write()

    # %%
    # import numpy as np
    # import plotly.express as px
    # from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
    # instance.solutions.load_from(results)
    column_map = {
            # Variables with ['REGION', 'TECHNOLOGY', 'YEAR'] set
            'v_NumberOfNewTechnologyUnits': ['REGION', 'TECHNOLOGY', 'YEAR', 'value'],
            'v_NewCapacity': ['REGION', 'TECHNOLOGY', 'YEAR', 'value'],
            'v_AccumulatedNewCapacity': ['REGION', 'TECHNOLOGY', 'YEAR', 'value'],
            'v_TotalCapacityAnnual': ['REGION', 'TECHNOLOGY', 'YEAR', 'value'],
            'v_CapitalInvestment': ['REGION', 'TECHNOLOGY', 'YEAR', 'value'],
            'v_DiscountedCapitalInvestment': ['REGION', 'TECHNOLOGY', 'YEAR', 'value'],
            'v_SalvageValue': ['REGION', 'TECHNOLOGY', 'YEAR', 'value'],
            'v_DiscountedSalvageValue': ['REGION', 'TECHNOLOGY', 'YEAR', 'value'],
            'v_OperatingCost': ['REGION', 'TECHNOLOGY', 'YEAR', 'value'],
            'v_DiscountedOperatingCost': ['REGION', 'TECHNOLOGY', 'YEAR', 'value'],
            'v_AnnualVariableOperatingCost': ['REGION', 'TECHNOLOGY', 'YEAR', 'value'],
            'v_AnnualFixedOperatingCost': ['REGION', 'TECHNOLOGY', 'YEAR', 'value'],
            'v_TotalDiscountedCostByTechnology': ['REGION', 'TECHNOLOGY', 'YEAR', 'value'],
            'v_TotalTechnologyAnnualActivity': ['REGION', 'TECHNOLOGY', 'YEAR', 'value'],
            'v_AnnualTechnologyEmissionsPenalty': ['REGION', 'TECHNOLOGY', 'YEAR', 'value'],
            'v_DiscountedTechnologyEmissionsPenalty': ['REGION', 'TECHNOLOGY', 'YEAR', 'value'],
            'v_NumeroUnidadesRecuperadas': ['REGION', 'TECHNOLOGY', 'YEAR', 'value'],
            'v_ResidualCapacity': ['REGION', 'TECHNOLOGY', 'YEAR', 'value'],
            'v_Abandono':['REGION', 'TECHNOLOGY', 'TIMESLICE', 'YEAR', 'value'],
            'v_Cubrimiento':['REGION', 'TECHNOLOGY', 'TIMESLICE', 'YEAR', 'value'],
            'v_RecoveredExistingUnits':['REGION', 'TECHNOLOGY',  'YEAR', 'value'],
            'v_AccumulatedRecoveredUnits':['REGION', 'TECHNOLOGY',  'YEAR', 'value'],
            'v_AccumulatedRecoveredCapacity':['REGION', 'TECHNOLOGY',  'YEAR', 'value'],
            'v_RecoveredCapacity':['REGION', 'TECHNOLOGY',  'YEAR', 'value'],
            # Variables with ['REGION', 'TIMESLICE', 'FUEL', 'YEAR'] set
            'v_RateOfProduction': ['REGION', 'TIMESLICE', 'FUEL', 'YEAR', 'value'],
            'v_RateOfDemand': ['REGION', 'TIMESLICE', 'FUEL', 'YEAR', 'value'],
            'v_Demand': ['REGION', 'TIMESLICE', 'FUEL', 'YEAR', 'value'],
            'v_Production': ['REGION', 'TIMESLICE', 'FUEL', 'YEAR', 'value'],
            'v_RateOfUse': ['REGION', 'TIMESLICE', 'FUEL', 'YEAR', 'value'],
            'v_Use': ['REGION', 'TIMESLICE', 'FUEL', 'YEAR', 'value'],
            'v_ConnectedUnits': ['REGION', 'TECHNOLOGY', 'SEASON', 'YEAR', 'value'],
            'v_Export': ['REGION', 'TIMESLICE', 'FUEL', 'YEAR', 'value'],

            # Variables with ['REGION', 'STORAGE', 'SEASON', 'DAYTYPE', 'DAILYTIMEBRACKET', 'YEAR'] set
            'v_RateOfStorageCharge': ['REGION', 'STORAGE', 'SEASON', 'DAYTYPE', 'DAILYTIMEBRACKET', 'YEAR', 'value'],
            'v_RateOfStorageDischarge': ['REGION', 'STORAGE', 'SEASON', 'DAYTYPE', 'DAILYTIMEBRACKET', 'YEAR', 'value'],
            'v_NetChargeWithinYear': ['REGION', 'STORAGE', 'SEASON', 'DAYTYPE', 'DAILYTIMEBRACKET', 'YEAR', 'value'],
            'v_NetChargeWithinDay': ['REGION', 'STORAGE', 'SEASON', 'DAYTYPE', 'DAILYTIMEBRACKET', 'YEAR', 'value'],
            'v_StorageLevel' : ['REGION', 'STORAGE', 'SEASON', 'DAYTYPE', 'DAILYTIMEBRACKET', 'YEAR', 'value'],

            # Variables with ['REGION', 'STORAGE', 'YEAR'] set
            'v_StorageLevelYearStart': ['REGION', 'STORAGE', 'YEAR', 'value'],
            'v_StorageLevelYearFinish': ['REGION', 'STORAGE', 'YEAR', 'value'],
            'v_StorageLowerLimit': ['REGION', 'STORAGE', 'YEAR', 'value'],
            'v_StorageUpperLimit': ['REGION', 'STORAGE', 'YEAR', 'value'],
            'v_AccumulatedNewStorageCapacity': ['REGION', 'STORAGE', 'YEAR', 'value'],
            'v_NewStorageCapacity': ['REGION', 'STORAGE', 'YEAR', 'value'],
            'v_CapitalInvestmentStorage': ['REGION', 'STORAGE', 'YEAR', 'value'],
            'v_DiscountedCapitalInvestmentStorage': ['REGION', 'STORAGE', 'YEAR', 'value'],
            'v_SalvageValueStorage': ['REGION', 'STORAGE', 'YEAR', 'value'],
            'v_DiscountedSalvageValueStorage': ['REGION', 'STORAGE', 'YEAR', 'value'],
            'v_TotalDiscountedStorageCost': ['REGION', 'STORAGE', 'YEAR', 'value'],

            # Variables with ['REGION', 'STORAGE', 'SEASON', 'YEAR'] set
            'v_StorageLevelSeasonStart': ['REGION', 'STORAGE', 'SEASON', 'YEAR', 'value'],

            # Variables with ['REGION', 'STORAGE', 'SEASON', 'DAYTYPE', 'YEAR'] set
            'v_StorageLevelDayTypeStart': ['REGION', 'STORAGE', 'SEASON', 'DAYTYPE', 'YEAR', 'value'],
            'v_StorageLevelDayTypeFinish': ['REGION', 'STORAGE', 'SEASON', 'DAYTYPE', 'YEAR', 'value'],
                      
            # Variables with ['REGION', 'TIMESLICE', 'TECHNOLOGY', 'MODE_OF_OPERATION', 'YEAR'] set
            'v_RateOfActivity': ['REGION', 'TIMESLICE', 'TECHNOLOGY', 'MODE_OF_OPERATION', 'YEAR', 'value'],

            # Variables with ['REGION', 'TECHNOLOGY', 'TIMESLICE', 'YEAR'] set
            'v_RateOfTotalActivity': ['REGION', 'TECHNOLOGY', 'TIMESLICE', 'YEAR', 'value'],

            # Variables with ['REGION', 'TECHNOLOGY', 'MODE_OF_OPERATION', 'YEAR'] set
            'v_TotalAnnualTechnologyActivityByMode': ['REGION', 'TECHNOLOGY', 'MODE_OF_OPERATION', 'YEAR', 'value'],

            # Variables with ['REGION', 'TECHNOLOGY'] set
            'v_TotalTechnologyModelPeriodActivity': ['REGION', 'TECHNOLOGY', 'value'],

            # Variables with ['REGION', 'TIMESLICE', 'TECHNOLOGY', 'MODE_OF_OPERATION', 'FUEL', 'YEAR'] set
            'v_RateOfProductionByTechnologyByMode': ['REGION', 'TIMESLICE', 'TECHNOLOGY', 'MODE_OF_OPERATION', 'FUEL', 'YEAR', 'value'],
            'v_RateOfUseByTechnologyByMode': ['REGION', 'TIMESLICE', 'TECHNOLOGY', 'MODE_OF_OPERATION', 'FUEL', 'YEAR', 'value'],

            # Variables with ['REGION', 'TIMESLICE', 'TECHNOLOGY', 'FUEL', 'YEAR'] set
            'v_RateOfProductionByTechnology': ['REGION', 'TIMESLICE', 'TECHNOLOGY', 'FUEL', 'YEAR', 'value'],
            'v_ProductionByTechnology': ['REGION', 'TIMESLICE', 'TECHNOLOGY', 'FUEL', 'YEAR', 'value'],
            'v_RateOfUseByTechnology': ['REGION', 'TIMESLICE', 'TECHNOLOGY', 'FUEL', 'YEAR', 'value'],
            'v_UseByTechnology': ['REGION', 'TIMESLICE', 'TECHNOLOGY', 'FUEL', 'YEAR', 'value'],

            # Variables with ['REGION', 'TECHNOLOGY', 'FUEL', 'YEAR'] set
            'v_ProductionByTechnologyAnnual': ['REGION', 'TECHNOLOGY', 'FUEL', 'YEAR', 'value'],
            'v_UseByTechnologyAnnual': ['REGION', 'TECHNOLOGY', 'FUEL', 'YEAR', 'value'],

            # Variables with ['REGION', 'REGION', 'TIMESLICE', 'FUEL', 'YEAR'] set
            'v_Trade': ['REGION', 'REGION', 'TIMESLICE', 'FUEL', 'YEAR', 'value'],

            # Variables with ['REGION', 'REGION', 'FUEL', 'YEAR'] set
            'v_TradeAnnual': ['REGION', 'REGION', 'FUEL', 'YEAR', 'value'],

            # Variables with ['REGION', 'FUEL', 'YEAR'] set
            'v_ProductionAnnual': ['REGION', 'FUEL', 'YEAR', 'value'],
            'v_UseAnnual': ['REGION', 'FUEL', 'YEAR', 'value'],

            # Variables with ['REGION', 'YEAR'] set
            'v_TotalDiscountedCost': ['REGION', 'YEAR', 'value'],
            'v_TotalCapacityInReserveMargin': ['REGION', 'YEAR', 'value'],
            'v_TotalREProductionAnnual': ['REGION', 'YEAR', 'value'],
            'v_RETotalProductionOfTargetFuelAnnual': ['REGION', 'YEAR', 'value'],

            # Variables with ['REGION'] set
            'v_ModelPeriodCostByRegion': ['REGION', 'value'],

            # Variables with ['REGION', 'TIMESLICE', 'YEAR'] set
            'v_DemandNeedingReserveMargin': ['REGION', 'TIMESLICE', 'YEAR', 'value'],

            # Variables with ['REGION', 'TECHNOLOGY', 'EMISSION', 'MODE_OF_OPERATION', 'YEAR'] set
            'v_AnnualTechnologyEmissionByMode': ['REGION', 'TECHNOLOGY', 'EMISSION', 'MODE_OF_OPERATION', 'YEAR', 'value'],

            # Variables with ['REGION', 'TECHNOLOGY', 'EMISSION', 'YEAR'] set
            'v_AnnualTechnologyEmission': ['REGION', 'TECHNOLOGY', 'EMISSION', 'YEAR', 'value'],
            'v_AnnualTechnologyEmissionPenaltyByEmission': ['REGION', 'TECHNOLOGY', 'EMISSION', 'YEAR', 'value'],

            # Variables with ['REGION', 'EMISSION', 'YEAR'] set
            'v_AnnualEmissions': ['REGION', 'EMISSION', 'YEAR', 'value'],

            # Variables with ['REGION', 'EMISSION'] set
            'v_ModelPeriodEmissions': ['REGION', 'EMISSION', 'value'],

        }
    def getColumns(var_name):
        return column_map.get(var_name, [])
    datas = {}

    for v in instance.component_objects(Var, active=True):
        lista = []
        if v.dim() == 1:
            for index in v:
                x = value(v[index])
                lista.append([index, x])
        else:
            for index in v:
                x = value(v[index])
                lista.append([*index, x])
        try:
            # Create a DataFrame using the column map for the variable
            df = pd.DataFrame(lista, columns=getColumns(str(v)))
            print(v)

            # Export the DataFrame to a CSV file
            # df.to_csv(f"./{results_folder}/{v}.csv", index=False)
            output_file = os.path.join(results_folder, f"{v}.csv")
            df.to_csv(output_file, index=False)

            # Store the DataFrame in the datas dictionary
            datas[str(v)] = df

        except ValueError as e:
            print(f"Error creating DataFrame for {v}: {e}")
            # Optionally, you can provide a default action or leave it empty to just skip the error
            pass

        """Plotly library to check quickly results but is not finished"""
        # if len(df)>1:
        #     if df.columns[-3] == 'FUEL' and df.columns[-4] =='TECHNOLOGY':
        #         piv1 =pd.pivot_table(df, values='value', index=df.columns[-2],  columns=df.columns[-4], aggfunc=np.sum)
        #         plot(px.area(piv1), filename = "./solutions/"+str(v)+".html", auto_open = False)
        #     elif df.columns[-3] == 'FUEL' or df.columns[-3] =='TECHNOLOGY':
        #         piv1 =pd.pivot_table(df, values='value', index=df.columns[-2],  columns=df.columns[-3], aggfunc=np.sum)
        #         plot(px.area(piv1), filename = "./solutions/"+str(v)+".html", auto_open = False)

    # %%
    return instance
if __name__ == '__main__':
    # results = '../results'
    results = RESULTS_FOLDER
    data = '../data'
    input_file = INPUT_FILE_PATH
    solve_model(input_file,results)