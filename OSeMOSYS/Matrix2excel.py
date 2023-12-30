#%% [markdown]
# Create Table of Contents


# %% [markdown]
# #### Código para probar data frame

# %% [markdown]
# Importar bibliotecas
#%%
import json
import pandas as pd


#%%
# Delete sheets
# wb = openpyxl.load_workbook('testdel.xlsx')

# keep_sheets = ['R', 'Sheet50', 'Sheet75', 'Sheet100']
# for sheetName in wb.sheetnames:
#     if sheetName not in keep_sheets:
#         del wb[sheetName]
# wb.save('testdel2.xlsx')



def process_excel(DataExcel):
    """Load Sets"""
    REGION =  (list(pd.read_excel(DataExcel, sheet_name = 'R')['REGION']))
    #### MEJORADO PARA QUE NO SE MAREE AL CARGAR LA HOJA DE EXCEL#####

    initialyear = (pd.read_excel(DataExcel, sheet_name = 'Y')['START_YEAR'])
    finalyear = (pd.read_excel(DataExcel, sheet_name = 'Y')['FINAL_YEAR'])
    YEAR = []
    for years in range(int(initialyear[0]),int(finalyear[0])+1):
        YEAR.append(years)


    TECHNOLOGY = list(pd.read_excel(DataExcel, sheet_name = 'T')['TECHNOLOGY'])
    FUEL = list(pd.read_excel(DataExcel, sheet_name = 'F')['FUEL'])
    SEASON =list(pd.read_excel(DataExcel, sheet_name = 'LS')['SEASON'])
    DAYTYPE = list(pd.read_excel(DataExcel, sheet_name = 'LD')['DAYTYPE'])
    DAILYTIMEBRACKET = list(pd.read_excel(DataExcel, sheet_name = 'LH')['DAILYTIMEBRACKET'])
    TIMESLICE = list(pd.read_excel(DataExcel, sheet_name = 'L')['TIMESLICE'])
    MODE_OF_OPERATION = list(pd.read_excel(DataExcel, sheet_name = 'M')['ModeOfOperation'])
    STORAGE = list(pd.read_excel(DataExcel, sheet_name = 'S')['STORAGE'])
    EMISSION = list(pd.read_excel(DataExcel, sheet_name = 'E')['EMISSION'])




    # %%
    """General Data Frames """
    #REION FUEL YEAR
    RFY = pd.MultiIndex.from_product([REGION, 
                                        FUEL], 
                                    names=['REGION', 'FUEL'])
    RFY = (pd.DataFrame('',index= RFY, columns=YEAR, )).reset_index()

    #REGION FUEL TIMESLICE YEAR
    RFLY = pd.MultiIndex.from_product([REGION, 
                                        FUEL, 
                                        TIMESLICE], 
                                    names=['REGION', 
                                            'FUEL', 
                                            'TIMESLICE'])
    RFLY = (pd.DataFrame('',index= RFLY, columns=YEAR)).reset_index()
    # REGION TECHNOLOGY
    RT = pd.MultiIndex.from_product([REGION], names=['REGION'])
    RT = pd.DataFrame('', index = RT, columns = TECHNOLOGY).reset_index()
    #REGION TECHNOLOGY TIMESLICE YEAR
    RTLY = pd.MultiIndex.from_product([REGION,TECHNOLOGY,TIMESLICE],names=['REGION','TECHNOLOGY','TIMESLICE'])
    RTLY = pd.DataFrame('', index = RTLY, columns= YEAR).reset_index()
    #REGION TECHNOLOGY YEAR
    RTY = pd.MultiIndex.from_product([REGION, TECHNOLOGY], names= ['REGION', 'TECHNOLOGY'])
    RTY = pd.DataFrame('', index = RTY, columns= YEAR).reset_index()
    # REGION TECHNOLOGY FUEL MODE_OF_OPERATION YEAR
    RTFMY = pd.MultiIndex.from_product([REGION, 
                                        TECHNOLOGY, 
                                        FUEL, 
                                        MODE_OF_OPERATION], 
                                    names = ['REGION', 
                                                'TECHNOLOGY', 
                                                'FUEL', 
                                                'MODE_OF_OPERATION'])
    RTFMY = pd.DataFrame('',index= RTFMY, columns=YEAR).reset_index()
    # REGION TECHNOLOGY MODE_OF_OPERATION YEAR
    RTMY = pd.MultiIndex.from_product([REGION, 
                                        TECHNOLOGY, 
                                        MODE_OF_OPERATION,
                                        ], 
                                    names = ['REGION', 
                                                'TECHNOLOGY', 
                                                'MODE_OF_OPERATION'])
    #REGION TECHNOLOGY MODE_OF_OPERATION YEAR
    RTMY = pd.DataFrame('',index= RTMY, columns=YEAR).reset_index()
    RTSM = pd.MultiIndex.from_product([REGION,
                                    TECHNOLOGY,
                                    STORAGE,
                                    ], names=['REGION',
                                    'TECHNOLOGY',
                                    'STORAGE'] )
    RTSM = pd.DataFrame('', index = RTSM, columns= MODE_OF_OPERATION).reset_index()
    #REGION STORAGE
    RS = pd.MultiIndex.from_product([REGION], names=['REGION'])
    RS = pd.DataFrame('', index= RS, columns= STORAGE).reset_index()
    #REGION STORAGE YEAR
    RSY = pd.MultiIndex.from_product([REGION, STORAGE], 
                                    names=['REGION', 'STORAGE'])
    RSY = pd.DataFrame('', index= RSY, columns=YEAR).reset_index()

    RY = pd.MultiIndex.from_product([REGION], names=['REGION'])
    RY = pd.DataFrame('', index= RY, columns= YEAR).reset_index()
    RTEMY = pd.MultiIndex.from_product([REGION,
                                        TECHNOLOGY,
                                        EMISSION,
                                        MODE_OF_OPERATION],
                                    names= ['REGION',
                                        'TECHNOLOGY',
                                        'EMISSION',
                                        'MODE_OF_OPERATION'])
    RTEMY = pd.DataFrame('', index = RTEMY, columns= YEAR).reset_index()
    REY = pd.MultiIndex.from_product([REGION,
                                    EMISSION], 
                                    names=['REGION',
                                    'EMISSION'])
    REY = pd.DataFrame('',index= REY, columns= YEAR).reset_index()
    RE = pd.MultiIndex.from_product([REGION], names=['REGION'])
    RE = pd.DataFrame('', index= RE, columns= EMISSION).reset_index()
    LY = pd.MultiIndex.from_product([TIMESLICE], names=['TIMESLICE'])
    LY = pd.DataFrame('', index = LY, columns = YEAR).reset_index()
    LLS = pd.MultiIndex.from_product([TIMESLICE], names=['TIMESLICE'])
    LLS = pd.DataFrame('', index = LLS, columns = SEASON).reset_index()
    LLD = pd.MultiIndex.from_product([TIMESLICE], names=['TIMESLICE'])
    LLD = pd.DataFrame('', index = LLD, columns = DAYTYPE).reset_index()
    LLH = pd.MultiIndex.from_product([TIMESLICE], names=['TIMESLICE'])
    LLH = pd.DataFrame('', index = LLH, columns = DAILYTIMEBRACKET).reset_index()

    LHY = pd.MultiIndex.from_product([DAILYTIMEBRACKET], names=['DAILYTIMEBRACKET'])
    LHY = pd.DataFrame('', index = LHY, columns = YEAR).reset_index()
    LSLDY = pd.MultiIndex.from_product([SEASON, DAYTYPE], names=['SEASON', 'DAYTYPE'])
    LSLDY = pd.DataFrame('', index = LSLDY, columns = YEAR).reset_index()

    #%%

    """"Model parameters"""
    ######## Global Parameters ###########
    YearSplit = LY
    Conversionls = LLS
    Conversionld = LLD
    Conversionlh = LLH
    DaySplit = LHY
    DaysInDayType = LSLDY
    ##### Demands 3                     
    SpecifiedAnnualDemand = RFY
    SpecifiedDemandProfile = RFLY
    AccumulatedAnnualDemand = RFY
    ######## Performance 7
    CapacityToActivityUnit = RT
    CapacityFactor = RTLY
    AvailabilityFactor = RTY
    OperationalLife = RT
    ResidualCapacity = RTY
    InputActivityRatio = RTFMY
    OutputActivityRatio = RTFMY

    ######## Technology costs 3
    CapitalCost = RTY
    VariableCost = RTMY
    FixedCost = RTY

    ###### STORAGE PARAMETERS 9
    TechnologyToStorage = RTSM
    TechnologyFromStorage = RTSM
    StorageLevelStart = RS
    StorageMaxChargeRate = RS
    StorageMaxDischargeRate = RS
    MinStorageCharge = RSY
    OperationalLifeStorage = RSY
    CapitalCostStorage = RSY
    ResidualStorageCapacity = RSY
    ####### Capacity Constraints 5
    CapacityOfOneTechnologyUnit = RTY
    TotalAnnualMaxCapacity = RTY
    TotalAnnualMinCapacity = RTY
    TotalAnnualMaxCapacityInvestment = RTY
    TotalAnnualMinCapacityInvestment = RTY
    ####### Activity Constraints 4
    TotalTechnologyAnnualActivityUpperLimit = RTY
    TotalTechnologyAnnualActivityLowerLimit = RTY
    TotalTechnologyModelPeriodActivityUpperLimit = RT
    TotalTechnologyModelPeriodActivityLowerLimit = RT
    ####### Reserve Margin 3 
    ReserveMarginTagTechnology = RTY
    ReserveMarginTagFuel = RFY
    ReserveMargin = RY
    ####### RE Generation Target 3 
    RETagTechnology = RTY
    RETagFuel = RFY
    REMinProductionTarget = RY
    ######## EMISSIONS 6
    EmissionActivityRatio = RTEMY
    EmissionsPenalty = REY
    AnnualExogenousEmission = REY
    AnnualEmissionLimit = REY
    ModelPeriodExogenousEmission = RE
    ModelPeriodEmissionLimit = RE
    ####Parametros nuevos
    MinimumOperatingLoad = RTY
    CostoNoAsociado = RTY
    Availability  = RTY
    NumberOfExistingUnits = RTY
    CostoRecuperacion = RTY
    VidaUtilRecuperada = RT
    dataframe_names = ["YearSplit", "Conversionls", "Conversionld",
                    "DaySplit", "DaysInDayType", "SpecifiedAnnualDemand", 
                    "SpecifiedDemandProfile", "AccumulatedAnnualDemand", 
                    "CapacityToActivityUnit", "CapacityFactor", "AvailabilityFactor", 
                    "OperationalLife", "ResidualCapacity", "InputActivityRatio", 
                    "OutputActivityRatio", "CapitalCost", "VariableCost", "FixedCost", 
                    "TechnologyToStorage", "TechnologyFromStorage", "StorageLevelStart", 
                    "StorageMaxChargeRate", "StorageMaxDischargeRate", "MinStorageCharge", 
                    "OperationalLifeStorage", "CapitalCostStorage", "ResidualStorageCapacity", 
                    "CapacityOfOneTechnologyUnit", "TotalAnnualMaxCapacity", "TotalAnnualMinCapacity", 
                    "TotalAnnualMaxCapacityInvestment", "TotalAnnualMinCapacityInvestment", 
                    "TotalTechnologyAnnualActivityUpperLimit", "TotalTechnologyAnnualActivityLowerLimit",
                    "TotalTechnologyModelPeriodActivityUpperLimit", 
                    "TotalTechnologyModelPeriodActivityLowerLimit", 
                    "ReserveMarginTagTechnology", "ReserveMarginTagFuel", 
                    "ReserveMargin", "RETagTechnology", "RETagFuel", "REMinProductionTarget",
                    "EmissionActivityRatio", "EmissionsPenalty", "AnnualExogenousEmission", 
                    "AnnualEmissionLimit", "ModelPeriodExogenousEmission", "ModelPeriodEmissionLimit", 
                    "CostoNoAsociado", "MinimumOperatingLoad", "Availability", 
                    "NumberOfExistingUnits", "CostoRecuperacion", "VidaUtilRecuperada"]
    dataframes = [globals()[name] for name in dataframe_names if name in globals() and isinstance(globals()[name], pd.DataFrame)]
    sheet_names = ["YS", "LLS", "LLD", "DS", "DIDT", "SAD", "SDP", "AAD", "C2AU", "CF", "AF", "OL", "RC", "IAR", "OAR", "CC", "VC", "FC", "TTS", "TFS", "StLS",
               "StMxChR", "StMxDCh", "MinStCh", "OpLiSt", "CCSt", "ReStCap", "C1TU", "TAMaxC", "TAMinC", "TAMaxCI", "TAMinCI", "TTAAUL", "TTAALL", "TTMPAUL",
               "TTMPALL", "RMTT", "RMTF", "RM", "ReTagT", "ReTagF", "REMinPT", "EmAR", "EmP", "AExEm", "AEmLim", "MPExEm", "MPEmLim", "CNA", "MOL", "Avail",
               "NOEU", "CostoRec", "VUR"]  
    # %%

    with pd.ExcelWriter("../data/OsemosysNew.xlsx",
                        mode="a",
                        engine="openpyxl",
                        if_sheet_exists= "replace"
                        ) as writer:
        for df, sheet_name in zip(dataframes, sheet_names):
            df.to_excel(writer, sheet_name=sheet_name, index=False)

            # Access and add filters to each sheet
            workbook = writer.book
            sheet = workbook[sheet_name]
            sheet.auto_filter.ref = sheet.dimensions

    DataExcel.close()
    return True

if __name__ == "__main__":   # if the file is run in standalone
    filename = pd.ExcelFile('../data/OsemosysNew.xlsx')
    process_excel(filename)





















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



