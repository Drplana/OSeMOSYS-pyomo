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
    RFY = (pd.DataFrame('',index= RFY, columns=YEAR))
    #REGION FUEL TIMESLICE YEAR
    RFLY = pd.MultiIndex.from_product([REGION,
                                        FUEL,
                                        TIMESLICE],
                                       names=['REGION',
                                              'FUEL',
                                              'TIMESLICE'])
    RFLY = (pd.DataFrame('',index= RFLY, columns=YEAR))
    # REGION TECHNOLOGY
    RT = pd.MultiIndex.from_product([REGION], names=['REGION'])
    RT = pd.DataFrame('', index = RT, columns = TECHNOLOGY)
    #REGION TECHNOLOGY TIMESLICE YEAR
    RTLY = pd.MultiIndex.from_product([REGION,TECHNOLOGY,TIMESLICE],names=['REGION','TECHNOLOGY','TIMESLICE'])
    RTLY = pd.DataFrame('', index = RTLY, columns= YEAR)
    #REGION TECHNOLOGY YEAR
    RTY = pd.MultiIndex.from_product([REGION, TECHNOLOGY], names= ['REGION', 'TECHNOLOGY'])
    RTY = pd.DataFrame('', index = RTY, columns= YEAR)
    # REGION TECHNOLOGY FUEL MODE_OF_OPERATION YEAR
    RTFMY = pd.MultiIndex.from_product([REGION,
                                        TECHNOLOGY,
                                        FUEL,
                                        MODE_OF_OPERATION],
                                       names = ['REGION',
                                                'TECHNOLOGY',
                                                'FUEL',
                                                'MODE_OF_OPERATION'])
    RTFMY = pd.DataFrame('',index= RTFMY, columns=YEAR)
    # REGION TECHNOLOGY MODE_OF_OPERATION YEAR
    RTMY = pd.MultiIndex.from_product([REGION,
                                        TECHNOLOGY,
                                        MODE_OF_OPERATION,
                                        ],
                                       names = ['REGION',
                                                'TECHNOLOGY',
                                                'MODE_OF_OPERATION'])
    #REGION TECHNOLOGY MODE_OF_OPERATION YEAR
    RTMY = pd.DataFrame('',index= RTMY, columns=YEAR)
    RTSM = pd.MultiIndex.from_product([REGION,
                                       TECHNOLOGY,
                                       STORAGE,
                                       ], names=['REGION',
                                       'TECHNOLOGY',
                                       'STORAGE'] )
    RTSM = pd.DataFrame('', index = RTSM, columns= MODE_OF_OPERATION)
    #REGION STORAGE
    RS = pd.MultiIndex.from_product([REGION], names=['REGION'])
    RS = pd.DataFrame('', index= RS, columns= STORAGE)
    #REGION STORAGE YEAR
    RSY = pd.MultiIndex.from_product([REGION, STORAGE],
                                     names=['REGION', 'STORAGE'])
    RSY = pd.DataFrame('', index= RSY, columns=YEAR)

    RY = pd.MultiIndex.from_product([REGION], names=['REGION'])
    RY = pd.DataFrame('', index= RY, columns= YEAR)
    RTEMY = pd.MultiIndex.from_product([REGION,
                                        TECHNOLOGY,
                                        EMISSION,
                                        MODE_OF_OPERATION],
                                       names= ['REGION',
                                        'TECHNOLOGY',
                                        'EMISSION',
                                        'MODE_OF_OPERATION'])
    RTEMY = pd.DataFrame('', index = RTEMY, columns= YEAR)
    REY = pd.MultiIndex.from_product([REGION,
                                      EMISSION],
                                     names=['REGION',
                                      'EMISSION'])
    REY = pd.DataFrame('',index= REY, columns= YEAR)
    RE = pd.MultiIndex.from_product([REGION], names=['REGION'])
    RE = pd.DataFrame('', index= RE, columns= EMISSION)
    LY = pd.MultiIndex.from_product([TIMESLICE], names=['TIMESLICE'])
    LY = pd.DataFrame('', index = LY, columns = YEAR)
    LLS = pd.MultiIndex.from_product([TIMESLICE], names=['TIMESLICE'])
    LLS = pd.DataFrame('', index = LLS, columns = SEASON)
    LLD = pd.MultiIndex.from_product([TIMESLICE], names=['TIMESLICE'])
    LLD = pd.DataFrame('', index = LLD, columns = DAYTYPE)
    LLH = pd.MultiIndex.from_product([TIMESLICE], names=['TIMESLICE'])
    LLH = pd.DataFrame('', index = LLH, columns = DAILYTIMEBRACKET)

    LHY = pd.MultiIndex.from_product([DAILYTIMEBRACKET], names=['DAILYTIMEBRACKET'])
    LHY = pd.DataFrame('', index = LHY, columns = YEAR)
    LSLDY = pd.MultiIndex.from_product([SEASON, DAYTYPE], names=['SEASON', 'DAYTYPE'])
    LSLDY = pd.DataFrame('', index = LSLDY, columns = YEAR)

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

    # %%
    with pd.ExcelWriter("../data/OsemosysNew.xlsx",
                        mode="a",
                        engine="openpyxl",
                        if_sheet_exists= "replace"
                        ) as writer:
        ####  Global Parameters:  ###
        YearSplit.to_excel(writer, sheet_name = "YS")
        Conversionls.to_excel(writer, sheet_name = "LLS")
        Conversionld.to_excel(writer, sheet_name = "LLD")
        Conversionlh.to_excel(writer, sheet_name = "LLH")
        DaySplit.to_excel(writer, sheet_name = "DS")
        DaysInDayType.to_excel(writer, sheet_name = "DIDT")
        # # # Demands 3
        SpecifiedAnnualDemand.to_excel(writer, sheet_name="SAD", startrow = 1)
        SpecifiedDemandProfile.to_excel(writer, sheet_name="SDP", startrow = 1)
        AccumulatedAnnualDemand.to_excel(writer, sheet_name = "AAD", startrow = 0)

        ### performance 7
        CapacityToActivityUnit.to_excel(writer, sheet_name = "C2AU", startrow = 0)
        CapacityFactor.to_excel(writer, sheet_name = "CF")
        AvailabilityFactor.to_excel(writer, sheet_name = "AF")
        OperationalLife.to_excel(writer, sheet_name= "OL")
        ResidualCapacity.to_excel(writer, sheet_name = "RC")
        InputActivityRatio.to_excel(writer, sheet_name = "IAR")
        OutputActivityRatio.to_excel(writer, sheet_name = "OAR")

        ##TEchnology Cost 3
        CapitalCost.to_excel(writer, sheet_name = "CC")
        VariableCost.to_excel(writer, sheet_name = "VC")
        FixedCost.to_excel(writer,sheet_name = "FC")

        ###storage
        # TechnologyToStorage.to_excel(writer,sheet_name = "TTS")
        # TechnologyFromStorage.to_excel(writer,sheet_name = "TFS")
        # StorageLevelStart.to_excel(writer,sheet_name = "StLS")
        # StorageMaxChargeRate.to_excel(writer,sheet_name = "StMxChR")
        # StorageMaxDischargeRate.to_excel(writer, sheet_name = "StMxDCh")
        # MinStorageCharge.to_excel(writer, sheet_name = "MinStCh")
        # OperationalLifeStorage.to_excel(writer, sheet_name = "OpLiSt")
        # CapitalCostStorage.to_excel(writer, sheet_name = "CCSt")
        # ResidualStorageCapacity.to_excel(writer, sheet_name = "ReStCap")

        ###Capacity Constraint
        CapacityOfOneTechnologyUnit.to_excel(writer, sheet_name = "C1TU")
        TotalAnnualMaxCapacity.to_excel(writer, sheet_name = "TAMaxC")
        TotalAnnualMinCapacity.to_excel(writer, sheet_name = "TAMinC")
        TotalAnnualMaxCapacityInvestment.to_excel(writer, sheet_name = "TAMaxCI")
        TotalAnnualMinCapacityInvestment.to_excel(writer, sheet_name = "TAMinCI")

        # # Activity constraints
        TotalTechnologyAnnualActivityUpperLimit.to_excel(writer, sheet_name = "TTAAUL")
        TotalTechnologyAnnualActivityLowerLimit.to_excel(writer, sheet_name = "TTAALL")
        TotalTechnologyModelPeriodActivityUpperLimit.to_excel(writer, sheet_name = "TTMPAUL")
        TotalTechnologyModelPeriodActivityLowerLimit.to_excel(writer, sheet_name = "TTMPALL")

        ## REserve Margin
        ReserveMarginTagTechnology.to_excel(writer, sheet_name = "RMTT")
        ReserveMarginTagFuel.to_excel(writer, sheet_name = "RMTF")
        ReserveMargin.to_excel(writer, sheet_name = "RM")

        ##RE Generation Targeet
        RETagTechnology.to_excel(writer, sheet_name = "ReTagT")
        RETagFuel.to_excel(writer, sheet_name = "ReTagF")
        REMinProductionTarget.to_excel(writer, sheet_name = "REMinPT")

        # Emissions
        # EmissionActivityRatio.to_excel(writer, sheet_name = "EmAR")
        # EmissionsPenalty.to_excel(writer, sheet_name = "EmP")
        # AnnualExogenousEmission.to_excel(writer, sheet_name = "AExEm")
        # AnnualEmissionLimit.to_excel(writer, sheet_name = "AEmLim")
        # ModelPeriodExogenousEmission.to_excel(writer, sheet_name = "MPExEm")
        # ModelPeriodEmissionLimit.to_excel(writer, sheet_name = "MPEmLim")

        #Parametros nuevos
        CostoNoAsociado.to_excel(writer, sheet_name = "CNA")
        MinimumOperatingLoad.to_excel(writer, sheet_name =  "MOL")
        Availability.to_excel(writer,sheet_name="Avail")
        NumberOfExistingUnits.to_excel(writer,sheet_name="NOEU")
        CostoRecuperacion.to_excel(writer,sheet_name= "CostoRec")
        VidaUtilRecuperada.to_excel(writer, sheet_name= "VUR")

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



