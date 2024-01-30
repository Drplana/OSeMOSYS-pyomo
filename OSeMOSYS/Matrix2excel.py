#%%
import json
import pandas as pd
from ReadSets import *
import warnings

### DataFrames with all possible matrix configuration.
result_dataframes = create_multiindex_dataframe(lists_dict)

# %%


### Use the created DataFrames for the parameters
YearSplit = result_dataframes['LY']
Conversionls = result_dataframes['LLS']
Conversionld = result_dataframes['LLD']
Conversionlh = result_dataframes['LLH']
DaySplit = result_dataframes['LHY']
DaysInDayType = result_dataframes['LSLDY']
##### Demands 3                     
SpecifiedAnnualDemand = result_dataframes['RFY']
SpecifiedDemandProfile = result_dataframes['RFLY']
AccumulatedAnnualDemand = result_dataframes['RFY']
######## Performance 7
CapacityToActivityUnit = result_dataframes['RT']
CapacityFactor = result_dataframes['RTLY']
AvailabilityFactor = result_dataframes['RTY']
OperationalLife = result_dataframes['RT']
ResidualCapacity = result_dataframes['RTY']
InputActivityRatio = result_dataframes['RTFMY']
OutputActivityRatio = result_dataframes['RTFMY']

######## Technology costs 3
CapitalCost = result_dataframes['RTY']
VariableCost = result_dataframes['RTMY']
FixedCost = result_dataframes['RTY']

###### STORAGE PARAMETERS 9
TechnologyToStorage = result_dataframes['RTSM']
TechnologyFromStorage = result_dataframes['RTSM']
StorageLevelStart = result_dataframes['RS']
StorageMaxChargeRate = result_dataframes['RS']
StorageMaxDischargeRate = result_dataframes['RS']
MinStorageCharge = result_dataframes['RSY']
OperationalLifeStorage = result_dataframes['RS']
CapitalCostStorage = result_dataframes['RSY']
ResidualStorageCapacity = result_dataframes['RSY']
####### Capacity Constraints 5
CapacityOfOneTechnologyUnit = result_dataframes['RTY']
TotalAnnualMaxCapacity = result_dataframes['RTY']
TotalAnnualMinCapacity = result_dataframes['RTY']
TotalAnnualMaxCapacityInvestment = result_dataframes['RTY']
TotalAnnualMinCapacityInvestment = result_dataframes['RTY']
####### Activity Constraints 4
TotalTechnologyAnnualActivityUpperLimit = result_dataframes['RTY']
TotalTechnologyAnnualActivityLowerLimit = result_dataframes['RTY']
TotalTechnologyModelPeriodActivityUpperLimit = result_dataframes['RT']
TotalTechnologyModelPeriodActivityLowerLimit = result_dataframes['RT']
####### Reserve Margin 3 
ReserveMarginTagTechnology = result_dataframes['RTY']
ReserveMarginTagFuel = result_dataframes['RFY']
ReserveMargin = result_dataframes['RY']
####### result_dataframes['RE'] Generation Target 3 
RETagTechnology = result_dataframes['RTY']
RETagFuel = result_dataframes['RFY']
REMinProductionTarget = result_dataframes['RY']
######## EMISSIONS 6
EmissionActivityRatio = result_dataframes['RTEMY']
EmissionsPenalty = result_dataframes['REY']
AnnualExogenousEmission = result_dataframes['REY']
AnnualEmissionLimit = result_dataframes['REY']
ModelPeriodExogenousEmission = result_dataframes['RE']
ModelPeriodEmissionLimit = result_dataframes['RE']
####Parametros nuevos
MinimumOperatingLoad = result_dataframes['RTY']
CostoNoAsociado = result_dataframes['RTY']
Availability  = result_dataframes['RTY']
NumberOfExistingUnits = result_dataframes['RTY']
CostoRecuperacion = result_dataframes['RTY']
VidaUtilRecuperada = result_dataframes['RTY']

dataframes = [globals()[name] for name in dataframe_names if name in globals() and isinstance(globals()[name], pd.DataFrame)]

# %%

with pd.ExcelWriter("../data/OsemosysNew.xlsx",
                    mode="a",
                    engine="openpyxl",
                    if_sheet_exists= "replace"
                    ) as writer:
    for df, sheet_names in zip(dataframes, sheet_names):
        # df
        df.to_excel(writer, sheet_name=sheet_names, index = False)

        # Access and add filters to each sheet
        workbook = writer.book
        sheet = workbook[sheet_names]
        sheet.auto_filter.ref = sheet.dimensions
        sheet.freeze_panes = 'A2'


# if __name__ == "__main__":   # if the file is run in standalone
#     filename = pd.ExcelFile('../data/OsemosysNew.xlsx')
#     process_excel(filename)





















#
# 
# Specified Demand Profile
# SDP = pd.MultiIndex.from_product([REGION, 
#                                     FUEL], 
#                                    names=['REGION', 'FUEL'])                           
# df = (pd.DataFrame('',index= SPD, columns=YEAR))

# %%
# for reg in REGION:
#     # FUEL.insert(0, reg)
#     SAD_sheet.append([reg])
#     eSAD = pd.DataFrame(index= FUEL, columns = YEAR)

# %%
#for r in dataframe_to_rows(df, index=True, header = True):
#   (SAD_sheet.append(r))


# %%

     

# %%
# writer = pd.ExcelWriter("OsemosysData.xlsx", engine = "xlsxwriter")
# SAD_sheet  = writer.sheets['SAD']
# SAD_sheet = write(0,0, x)


# xlsfile = load_workbook('OsemosysData.xlsx')
# SAD_sheet = xlsfile['SAD']
# SAD_sheet['A1'] = 'SpecifiedAnnualDemmand'
# xlsfile.save('OsemosysData.xlsx')
# xlsfile.close()

# writer = save()

# with pd.ExcelWriter(
#     "OsemosysData.xlsx", 
#     mode="a", 
#     engine="openpyxl", 
#     if_sheet_exists= "replace",
#     ) as writer:
#     df.to_excel(writer, sheet_name="SAD", startrow=2)

# %%

 
    
# xlsfile.close() 

# %%
# import os
# os.system("start EXCEL.EXE Osemosys.xlsx")

# %%


# %%



