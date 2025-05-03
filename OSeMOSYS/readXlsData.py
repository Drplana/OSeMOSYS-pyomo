#%%
import pandas as pd
from OSeMOSYS.ReadSets import load_sets, read_excel_sheets, lists_dict, dataframe_names, sheet_names
import os, sys
root_folder = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(root_folder)
  # Replace with the actual file path
import json
import pandas as pd
from OSeMOSYS.config import INPUT_FILE_PATH, DATA_FILE_PATH
# REGION, YEAR, TECHNOLOGY, FUEL, SEASON, DAYTYPE, DAILYTIMEBRACKET, TIMESLICE, MODE_OF_OPERATION, STORAGE, EMISSION = load_sets(file_path)


# This will creata a dict with all sets forms inside the yaml file

#%%
Default, REGION, YEAR, TECHNOLOGY, FUEL, SEASON, DAYTYPE, DAILYTIMEBRACKET, TIMESLICE, MODE_OF_OPERATION, STORAGE, EMISSION = load_sets(file_path)
# Printing the RFY set
# print("RFY set values:", RFY_set)

data_frames = read_excel_sheets(file_path=INPUT_FILE_PATH, sheet_names=sheet_names, dataframe_names=dataframe_names)
#%%
YearSplit  = data_frames['YearSplit'].set_index('TIMESLICE').stack().reset_index().rename(columns = {"level_1": "YEAR", 0:"value"})
DaySplit = data_frames['DaySplit'].set_index('DAILYTIMEBRACKET').stack().reset_index().rename(columns = {"level_1": "YEAR", 0:"value"})
DaysInDayType =  data_frames['DaysInDayType'].set_index(['SEASON','DAYTYPE']).stack().reset_index().rename(columns = {"level_2": "YEAR", 0:"value"})
Conversionls = data_frames['Conversionls'].set_index(['TIMESLICE']).stack().reset_index().rename(columns = {"level_1": "SEASON", 0:"value"})
Conversionld = data_frames['Conversionld'].set_index(['TIMESLICE']).stack().reset_index().rename(columns = {"level_1": "DAYTYPE", 0:"value"})
Conversionlh = data_frames['Conversionlh'].set_index(['TIMESLICE']).stack().reset_index().rename(columns = {"level_1": "DAILYTIMEBRACKET", 0:"value"})

SpecifiedAnnualDemand = data_frames['SpecifiedAnnualDemand'].set_index(['REGION','FUEL']).stack().reset_index().rename(columns = {"level_2": "YEAR", 0:"value"})
SpecifiedDemandProfile = data_frames['SpecifiedDemandProfile'].set_index(['REGION','FUEL','TIMESLICE']).stack().reset_index().rename(columns = {"level_3": "YEAR", 0:"value"})
AccumulatedAnnualDemand = data_frames['AccumulatedAnnualDemand'].set_index(['REGION','FUEL']).stack().reset_index().rename(columns={"level_2": "YEAR",0:"value"})
"Performance"
CapacityToActivityUnit = data_frames['CapacityToActivityUnit'].set_index(['REGION']).stack().reset_index().rename(columns={"level_1": "TECHNOLOGY",0:"value"})
CapacityFactor = data_frames['CapacityFactor'].set_index(['REGION','TECHNOLOGY','TIMESLICE']).stack().reset_index().rename(columns = {"level_3": "YEAR", 0:"value"})
AvailabilityFactor = data_frames['AvailabilityFactor'].set_index(['REGION','TECHNOLOGY']).stack().reset_index().rename(columns={"level_2": "YEAR",0:"value"})
OperationalLife = data_frames['OperationalLife'].set_index(['REGION']).stack().reset_index().rename(columns={"level_1": "TECHNOLOGY",0:"value"})
ResidualCapacity = data_frames['ResidualCapacity'].set_index(['REGION','TECHNOLOGY'])  .stack().reset_index().rename(columns={"level_2": "YEAR",0:"value"})
InputActivityRatio = data_frames['InputActivityRatio'].set_index(['REGION','TECHNOLOGY','FUEL','MODE_OF_OPERATION']).stack().reset_index().rename(columns={"level_4": "YEAR",0:"value"})
OutputActivityRatio = data_frames['OutputActivityRatio'].set_index(['REGION','TECHNOLOGY','FUEL','MODE_OF_OPERATION']).stack().reset_index().rename(columns={"level_4": "YEAR",0:"value"})
"Technology Costs"
CapitalCost = data_frames['CapitalCost'].set_index(['REGION','TECHNOLOGY']).stack().reset_index().rename(columns={"level_2": "YEAR",0:"value"})
VariableCost =data_frames['VariableCost'].set_index(['REGION','TECHNOLOGY','MODE_OF_OPERATION']).stack().reset_index().rename(columns={"level_3": "YEAR",0:"value"})
FixedCost = data_frames['FixedCost'].set_index(['REGION','TECHNOLOGY']).stack().reset_index().rename(columns={"level_2": "YEAR",0:"value"})
"Storage"
TechnologyToStorage = data_frames['TechnologyToStorage'].set_index(['REGION','TECHNOLOGY','STORAGE']).stack().reset_index().rename(columns={"level_3": "MODE_OF_OPERATION",0:"value"})
TechnologyFromStorage = data_frames['TechnologyFromStorage'].set_index(['REGION','TECHNOLOGY','STORAGE']).stack().reset_index().rename(columns={"level_3": "MODE_OF_OPERATION",0:"value"})
StorageLevelStart = data_frames['StorageLevelStart'].set_index(['REGION']).stack().reset_index().rename(columns={"level_1": "STORAGE",0:"value"})
StorageMaxChargeRate = data_frames['StorageMaxChargeRate'].set_index(['REGION']).stack().reset_index().rename(columns={"level_1": "STORAGE",0:"value"})
StorageMaxDischargeRate = data_frames['StorageMaxDischargeRate'].set_index(['REGION']).stack().reset_index().rename(columns={"level_1": "STORAGE",0:"value"})
MinStorageCharge = data_frames['MinStorageCharge'].set_index(['REGION','STORAGE']).stack().reset_index().rename(columns={"level_2": "YEAR",0:"value"})
OperationalLifeStorage= data_frames['OperationalLifeStorage'].set_index(['REGION']).stack().reset_index().rename(columns={"level_1":'STORAGE',0:"value"})
CapitalCostStorage =  data_frames['CapitalCostStorage'].set_index(['REGION','STORAGE']).stack().reset_index().rename(columns={"level_2": "YEAR",0:"value"})
ResidualStorageCapacity = data_frames['ResidualStorageCapacity'].set_index(['REGION','STORAGE']).stack().reset_index().rename(columns={"level_2": "YEAR",0:"value"})
"Capacity"
CapacityOfOneTechnologyUnit =  data_frames['CapacityOfOneTechnologyUnit'].set_index(RT).stack().reset_index().rename(columns={"level_2": "YEAR",0:"value"})
TotalAnnualMaxCapacity = data_frames['TotalAnnualMaxCapacity'].set_index(RT).stack().reset_index().rename(columns={"level_2": "YEAR",0:"value"})
TotalAnnualMinCapacity  = data_frames['TotalAnnualMinCapacity'].set_index(RT).stack().reset_index().rename(columns={"level_2": "YEAR",0:"value"})
TotalAnnualMaxCapacityInvestment = data_frames['TotalAnnualMaxCapacityInvestment'].set_index(RT).stack().reset_index().rename(columns={"level_2": "YEAR",0:"value"})
TotalAnnualMinCapacityInvestment = data_frames['TotalAnnualMinCapacityInvestment'].set_index(RT).stack().reset_index().rename(columns={"level_2": "YEAR",0:"value"})
"Activity constraints"
TotalTechnologyAnnualActivityUpperLimit = data_frames['TotalTechnologyAnnualActivityUpperLimit'].set_index(RT).stack().reset_index().rename(columns={"level_2": "YEAR",0:"value"})
TotalTechnologyAnnualActivityLowerLimit = data_frames['TotalTechnologyAnnualActivityLowerLimit'].set_index(RT).stack().reset_index().rename(columns={"level_2": "YEAR",0:"value"})
TotalTechnologyModelPeriodActivityUpperLimit = data_frames['TotalTechnologyModelPeriodActivityUpperLimit'].set_index('REGION').stack().reset_index().rename(columns={"level_1": "TECHNOLOGY",0:"value"})
TotalTechnologyModelPeriodActivityLowerLimit = data_frames['TotalTechnologyModelPeriodActivityLowerLimit'].set_index('REGION').stack().reset_index().rename(columns={"level_1": "TECHNOLOGY",0:"value"})
"Reserve Margin"
ReserveMarginTagTechnology = data_frames['ReserveMarginTagTechnology'].set_index(RT) .stack().reset_index().rename(columns={"level_2": "YEAR",0:"value"})
ReserveMarginTagFuel = data_frames['ReserveMarginTagFuel'].set_index(RF) .stack().reset_index().rename(columns={"level_2": "YEAR",0:"value"})
ReserveMargin = data_frames['ReserveMargin'].set_index('REGION')  .stack().reset_index().rename(columns={"level_1": "YEAR",0:"value"})
"""RE Generation Target"""
RETagTechnology = data_frames['RETagTechnology'].set_index(RT).stack().reset_index().rename(columns={"level_2": "YEAR",0:"value"})
RETagFuel = data_frames['RETagFuel'].set_index(RF).stack().reset_index().rename(columns={"level_2": "YEAR",0:"value"})
REMinProductionTarget = data_frames['REMinProductionTarget'].set_index('REGION').stack().reset_index().rename(columns={"level_1": "YEAR",0:"value"})
"""Emissions"""
EmissionActivityRatio = data_frames['EmissionActivityRatio'].set_index(RTEM).stack().reset_index().rename(columns={f"level_{len(RTEMY)-1}": "YEAR",0:"value"})
EmissionsPenalty = data_frames['EmissionsPenalty'].set_index(RE).stack().reset_index().rename(columns={f"level_{len(REY)-1}": "YEAR",0:"value"})
AnnualExogenousEmission= data_frames['AnnualExogenousEmission'].set_index(RE).stack().reset_index().rename(columns={f"level_{len(REY)-1}": "YEAR",0:"value"})
AnnualEmissionLimit=   data_frames['AnnualEmissionLimit'].set_index(RE).stack().reset_index().rename(columns={f"level_{len(REY)-1}": "YEAR",0:"value"})
ModelPeriodExogenousEmission=  data_frames['ModelPeriodExogenousEmission'].set_index('REGION').stack().reset_index().rename(columns={f"level_{len(RE)-1}": "EMISSION",0:"value"})
ModelPeriodEmissionLimit= data_frames['ModelPeriodEmissionLimit'].set_index('REGION'). stack().reset_index().rename(columns={f"level_{len(RE)-1}": "EMISSION",0:"value"})
""" New Parameters"""
NumberOfExistingUnits =  data_frames['NumberOfExistingUnits'].set_index(RT).stack().reset_index().rename(columns={"level_2": "YEAR",0:"value"})
VidaUtilRecuperada = data_frames['VidaUtilRecuperada'].set_index(['REGION']).stack().reset_index().rename(columns={"level_1": "TECHNOLOGY",0:"value"})
CostoRecuperacion = data_frames['CostoRecuperacion'].set_index(RT).stack().reset_index().rename(columns={"level_2": "YEAR",0:"value"})
ExportPrice = data_frames['ExportPrice'].set_index(RF).stack().reset_index().rename(columns={"level_2": "YEAR",0:"value"})
MustRunTech  = data_frames['MustRunTech'].set_index(RT).stack().reset_index().rename(columns= {"level_2": "YEAR",0:"value"})
MustRunFuel  = data_frames['MustRunFuel'].set_index(['REGION','FUEL','TIMESLICE']).stack().reset_index().rename(columns = {"level_3": "YEAR", 0:"value"})
MustRun = data_frames['MustRun'].set_index('REGION').stack().reset_index().rename(columns={"level_1": "YEAR",0:"value"})
#%%
def save_dataframes_to_csv(names_list, folder_path=DATA_FILE_PATH):
    # Create the target folder if it doesn't exist
    os.makedirs(folder_path, exist_ok=True)

    for df_name in names_list:
        # Check if the DataFrame name exists in the current global environment
        if df_name in globals():
            df = globals()[df_name]

            # Construct the full file path
            file_path = os.path.join(folder_path, f"{df_name}.csv")

            # Save DataFrame to CSV
            df.to_csv(file_path, index=False)

            print(f"{df_name} saved to {file_path}")
        else:
            print(f"Error: DataFrame {df_name} not found in the current environment")


#%%

YearSplit = YearSplit.set_index(['TIMESLICE', 'YEAR']).to_dict('index')
DaySplit = DaySplit.set_index(['DAILYTIMEBRACKET', 'YEAR']).to_dict('index')
DaysInDayType = DaysInDayType.set_index(['SEASON','DAYTYPE', 'YEAR']).to_dict('index')
Conversionls = Conversionls.set_index(['TIMESLICE', 'SEASON']).to_dict('index')
Conversionld = Conversionld.set_index(['TIMESLICE', 'DAYTYPE']).to_dict('index')
Conversionlh = Conversionlh.set_index(['TIMESLICE', 'DAILYTIMEBRACKET']).to_dict('index')
SpecifiedAnnualDemand = SpecifiedAnnualDemand.set_index(RFY).to_dict('index')
SpecifiedDemandProfile = SpecifiedDemandProfile.set_index(RFLY).to_dict('index')
AccumulatedAnnualDemand = AccumulatedAnnualDemand.set_index(RFY).to_dict('index')
CapacityToActivityUnit = CapacityToActivityUnit.set_index(RT).to_dict('index')
CapacityFactor = CapacityFactor.set_index(RTLY).to_dict('index')
AvailabilityFactor = AvailabilityFactor.set_index(RTY).to_dict('index')
OperationalLife = OperationalLife.set_index(RT).to_dict('index')
ResidualCapacity = ResidualCapacity.set_index(RTY).to_dict('index')
InputActivityRatio = InputActivityRatio.set_index(RTFMY).to_dict('index')
OutputActivityRatio = OutputActivityRatio.set_index(RTFMY).to_dict('index')
CapitalCost = CapitalCost.set_index(RTY).to_dict('index')
VariableCost = VariableCost.set_index(RTMY).to_dict('index')
FixedCost = FixedCost.set_index(RTY).to_dict('index')
TechnologyToStorage = TechnologyToStorage.set_index(RTSM).to_dict('index')
TechnologyFromStorage = TechnologyFromStorage.set_index(RTSM).to_dict('index')
StorageLevelStart = StorageLevelStart.set_index(RS).to_dict('index')
StorageMaxChargeRate = StorageMaxChargeRate.set_index(RS).to_dict('index')
StorageMaxDischargeRate = StorageMaxDischargeRate.set_index(RS).to_dict('index')
MinStorageCharge = MinStorageCharge.set_index(RSY).to_dict('index')
OperationalLifeStorage = OperationalLifeStorage.set_index(RS).to_dict('index')
CapitalCostStorage = CapitalCostStorage.set_index(RSY).to_dict('index')
ResidualStorageCapacity = ResidualStorageCapacity.set_index(RSY).to_dict('index')
CapacityOfOneTechnologyUnit = CapacityOfOneTechnologyUnit.set_index(RTY).to_dict('index')
TotalAnnualMaxCapacity = TotalAnnualMaxCapacity.set_index(RTY).to_dict('index')
TotalAnnualMinCapacity = TotalAnnualMinCapacity.set_index(RTY).to_dict('index') 
TotalAnnualMaxCapacityInvestment = TotalAnnualMaxCapacityInvestment.set_index(RTY).to_dict('index')
TotalAnnualMinCapacityInvestment = TotalAnnualMinCapacityInvestment.set_index(RTY).to_dict('index')
TotalTechnologyAnnualActivityUpperLimit = TotalTechnologyAnnualActivityUpperLimit.set_index(RTY).to_dict('index') 
TotalTechnologyAnnualActivityLowerLimit = TotalTechnologyAnnualActivityLowerLimit.set_index(RTY).to_dict('index')
TotalTechnologyModelPeriodActivityUpperLimit = TotalTechnologyModelPeriodActivityUpperLimit.set_index(RT).to_dict('index')
TotalTechnologyModelPeriodActivityLowerLimit = TotalTechnologyModelPeriodActivityLowerLimit.set_index(RT).to_dict('index')
ReserveMarginTagTechnology = ReserveMarginTagTechnology.set_index(RTY).to_dict('index')
ReserveMarginTagFuel = ReserveMarginTagFuel.set_index(RFY).to_dict('index')
ReserveMargin = ReserveMargin.set_index(RY).to_dict('index')
RETagTechnology = RETagTechnology.set_index(RTY).to_dict('index')
RETagFuel = RETagFuel.set_index(RFY).to_dict('index')
REMinProductionTarget = REMinProductionTarget.set_index(RY).to_dict('index')
EmissionActivityRatio = EmissionActivityRatio.set_index(RTEMY).to_dict('index')
EmissionsPenalty = EmissionsPenalty.set_index(REY).to_dict('index')
AnnualExogenousEmission = AnnualExogenousEmission.set_index(REY).to_dict('index')
AnnualEmissionLimit = AnnualEmissionLimit.set_index(REY).to_dict('index')
ModelPeriodExogenousEmission = ModelPeriodExogenousEmission.set_index(RE).to_dict('index')
ModelPeriodEmissionLimit = ModelPeriodEmissionLimit.set_index(RE).to_dict('index')
NumberOfExistingUnits = NumberOfExistingUnits.set_index(RTY).to_dict('index')
VidaUtilRecuperada = VidaUtilRecuperada.set_index(RT).to_dict('index')
CostoRecuperacion = CostoRecuperacion.set_index(RTY).to_dict('index')
ExportPrice = ExportPrice.set_index(RFY).to_dict('index')
MustRunTech = MustRunTech.set_index(RTY).to_dict('index')
MustRunFuel = MustRunFuel.set_index(RFLY).to_dict('index')
MustRun = MustRun.set_index(RY).to_dict('index')
#%%
# def ListDict(name, dictionary):
#     return {name: [{"index": index, "value": data["value"]} for index, data in dictionary.items()]}


def ListDict(name, dictionary):
    my_list = []
    for row in dictionary.items():
        # iterar sobre las posiciones del dataframe
            # print(row[1]['value']) #diccionario
            # print(row[0][0]) #lista
        new_row = {"index":row[0], "value":row[1]["value"]} 
        my_list.append(new_row)
    # return {name:my_list}    
    return {name: json.loads(json.dumps(my_list))}
#%%

def parameters_dict(dataframe_names):
    param_dict = {}
    for name in dataframe_names:
        if name in globals():
            param_dict[name] = globals()[name]

    for data in list(param_dict):  # Use list(param_dict) to create a snapshot of keys
        try:
            new_key = f"p_{data}"  # Add "p_" prefix to the key
            param_dict[new_key] = param_dict.pop(data)
            param_dict.update(ListDict(new_key, param_dict[new_key]))
        except KeyError:
            print(f"KeyError: {data}")

    return param_dict
            
# ParamDict = {}
# for name in dataframe_names:
#     if name in globals():
#         ParamDict[name] = globals()[name]
# for data in ParamDict:
#     print(data)
#     try:
#      ParamDict.update((ListDict(data,ParamDict[data]))) 
#     except KeyError:
#         print(f"KeyError: {data}")
def dict_to_json():
    ParamDict = parameters_dict(dataframe_names) 
    #%%
    OsemosysDict = {
        "REGION":REGION,
        "YEAR":YEAR,
        "TECHNOLOGY":TECHNOLOGY,
        "FUEL":FUEL,
        "SEASON":SEASON,
        "DAYTYPE":DAYTYPE,
        "DAILYTIMEBRACKET":DAILYTIMEBRACKET,
        "TIMESLICE":TIMESLICE,
        "MODE_OF_OPERATION":MODE_OF_OPERATION,
        "STORAGE":STORAGE,
        "EMISSION":EMISSION,
        # OsemosysDict
    }
    if isinstance (ParamDict, dict):
        OsemosysDict.update(ParamDict)


    with open('../data/'+'/Data.json', 'w') as json_file:
        json.dump(OsemosysDict, json_file) 

if __name__ == "__main__":
    dict_to_json()
    save_dataframes_to_csv(dataframe_names)
