# -*- coding: utf-8 -*-
"""
Created on Sat Jan  8 17:52:35 2022

@author: David
"""
#%%
import json
import pandas as pd





#from Matrix2excel import CostoNoAsociado, MinimumOperatingLoad


"""
Soluciones a problemas
new_df.groupby(['REGION']).size().unstack().to_dict(orient='index')
indexing = []
for i in range(len(new_df.index)):
    indexing.append("index")

"""
#%%
"""Load Sets"""

def read_excel(filename,results_folder='.'):

    DataExcel = pd.ExcelFile(filename)
    REGION =  (list(pd.read_excel(DataExcel, sheet_name = 'R')['REGION']))
    initialyear = (pd.read_excel(DataExcel, sheet_name = 'Y')['START_YEAR'])
    finalyear = (pd.read_excel(DataExcel, sheet_name = 'Y')['FINAL_YEAR'])
    YEAR = []
    for years in range(int(initialyear[0]),int(finalyear[0])+1):
        YEAR.append(years)
        
    #%%
    # YEAR = (list(pd.read_excel(DataExcel, sheet_name = 'Y')['YEAR']))
    # YEAR = [x for x in YEAR if pd.isnull(x) == False]  # YEAR = [x for x in YEAR if x != 'nan']
    # YEAR = [int(i) for i in YEAR]
    TECHNOLOGY = list(pd.read_excel(DataExcel, sheet_name = 'T')['TECHNOLOGY'])
    FUEL = list(pd.read_excel(DataExcel, sheet_name = 'F')['FUEL'])
    SEASON =list(pd.read_excel(DataExcel, sheet_name = 'LS')['SEASON'])
    DAYTYPE = list(pd.read_excel(DataExcel, sheet_name = 'LD')['DAYTYPE'])
    DAILYTIMEBRACKET = list(pd.read_excel(DataExcel, sheet_name = 'LH')['DAILYTIMEBRACKET'])
    TIMESLICE = list(pd.read_excel(DataExcel, sheet_name = 'L')['TIMESLICE'])
    MODE_OF_OPERATION = list(pd.read_excel(DataExcel, sheet_name = 'M')['ModeOfOperation'])
    STORAGE = list(pd.read_excel(DataExcel, sheet_name = 'S')['STORAGE'])
    EMISSION = list(pd.read_excel(DataExcel, sheet_name = 'E')['EMISSION'])
    #%%
    # DataExcel = pd.ExcelFile('OsemosysAtlantisReserveEmission.xlsx')
    RFY = ['REGION','FUEL','YEAR']
    RFLY = ['REGION','FUEL','TIMESLICE','YEAR']
    RTY = ['REGION','TECHNOLOGY','YEAR']
    RTLY = ['REGION', 'TECHNOLOGY','TIMESLICE','YEAR']
    RF = ['REGION','FUEL']
    RT = ['REGION','TECHNOLOGY']
    RTFMY = ['REGION','TECHNOLOGY','FUEL','MODE_OF_OPERATION','YEAR']
    RTMY = ['REGION','TECHNOLOGY','MODE_OF_OPERATION','YEAR']
    RTSM = ['REGION','TECHNOLOGY','STORAGE','MODE_OF_OPERATION']
    RS = ['REGION','STORAGE']
    RS = ['REGION','STORAGE','YEAR']
    RY  = ['REGION','YEAR']
    RTEMY = ['REGION','TECHNOLOGY','EMISSION','MODE_OF_OPERATION','YEAR']
    REY = ['REGION','EMISSION','YEAR']
    RE = ['REGION','EMISSION']

    ### global parameters
    YearSplit = pd.read_excel(DataExcel, index_col = [0], sheet_name="YS")
    YearSplit = YearSplit.stack().reset_index().rename(columns = {"level_1": "YEAR", 0:"value"})
    YearSplit = YearSplit.set_index(['TIMESLICE', 'YEAR']).to_dict('index')
    DaySplit = pd.read_excel(DataExcel, index_col = [0], sheet_name="DS")
    DaySplit = DaySplit.stack().reset_index().rename(columns = {"level_1": "YEAR", 0:"value"})
    DaySplit = DaySplit.set_index(['DAILYTIMEBRACKET', 'YEAR']).to_dict('index')
    DaysInDayType = pd.read_excel(DataExcel, index_col = [0,1], sheet_name="DIDT")
    DaysInDayType = DaysInDayType.stack().reset_index().rename(columns = {"level_2": "YEAR", 0:"value"})
    DaysInDayType = DaysInDayType.set_index(['SEASON','DAYTYPE', 'YEAR']).to_dict('index')
    Conversionls = pd.read_excel(DataExcel, index_col = [0], sheet_name="LLS")
    Conversionls = Conversionls.stack().reset_index().rename(columns = {"level_1": "SEASON", 0:"value"})
    Conversionls = Conversionls.set_index(['TIMESLICE', 'SEASON']).to_dict('index')
    #%%
    """Demands"""
    SpecifiedAnnualDemand = pd.read_excel(DataExcel,index_col=[0,1],  sheet_name = 'SAD',skiprows=1)
    SpecifiedAnnualDemand = SpecifiedAnnualDemand.dropna().stack().reset_index().rename(columns={"level_2": "YEAR",0:"value"})
    SpecifiedAnnualDemand = SpecifiedAnnualDemand.set_index(RFY).to_dict('index')

    SpecifiedDemandProfile = pd.read_excel(DataExcel, index_col = [0,1,2], sheet_name="SDP", skiprows= 1)
    SpecifiedDemandProfile = SpecifiedDemandProfile.dropna().stack().reset_index().rename(columns={"level_3": "YEAR",0:"value"}).set_index(RFLY).to_dict('index')

    AccumulatedAnnualDemand=(
        pd.read_excel(DataExcel,index_col = [0,1], sheet_name = "AAD")
        .stack().reset_index().rename(columns={"level_2": "YEAR",0:"value"})
        .set_index(RFY).to_dict('index')
                            )
    #%%
    """Performance"""
    CapacityToActivityUnit = (
        pd.read_excel(DataExcel,index_col = [0], sheet_name = "C2AU")
        .stack().reset_index().rename(columns={"level_1": "FUEL",0:"value"})
        .set_index(RF).to_dict('index')
                                        )
    CapacityFactor =(
        pd.read_excel(DataExcel,index_col = [0,1,2], sheet_name = "CF")
        .stack().reset_index().rename(columns={"level_3": "YEAR",0:"value"})
        .set_index(RTLY).to_dict('index')
                                        )
    AvailabilityFactor = (
        pd.read_excel(DataExcel,index_col = [0,1], sheet_name = "AF")
        .stack().reset_index().rename(columns={"level_2": "YEAR",0:"value"})
        .set_index(RTY).to_dict('index')
    )
    OperationalLife = (
        pd.read_excel(DataExcel,index_col = [0], sheet_name = "OL")
        .stack().reset_index().rename(columns={"level_1": "TECHNOLOGY",0:"value"})
        .set_index(RT).to_dict('index')
    )
    ResidualCapacity = (
        pd.read_excel(DataExcel,index_col = [0,1], sheet_name = "RC")
        .stack().reset_index().rename(columns={"level_2": "YEAR",0:"value"})
        .set_index(RTY).to_dict('index')
    )
    InputActivityRatio = (
        pd.read_excel(DataExcel,index_col = [0,1,2,3], sheet_name = "IAR")
        .stack().reset_index().rename(columns={"level_4": "YEAR",0:"value"})
        .set_index(RTFMY).to_dict('index')
    )
    OutputActivityRatio = (
        pd.read_excel(DataExcel,index_col = [0,1,2,3], sheet_name = "OAR")
        .stack().reset_index().rename(columns={"level_4": "YEAR",0:"value"})
        .set_index(RTFMY).to_dict('index')
    )
    MinimumOperatingLoad = (pd.read_excel(DataExcel,index_col = [0,1], sheet_name = "MOL")
        .stack().reset_index().rename(columns={"level_2": "YEAR",0:"value"})
        .set_index(RTY).to_dict('index')
    )
    #%%
    """TECHNOLOGY COSTS"""
    CapitalCost = (
        pd.read_excel(DataExcel,index_col = [0,1], sheet_name = "CC")
        .stack().reset_index().rename(columns={"level_2": "YEAR",0:"value"})
        .set_index(RTY).to_dict('index')
    )
    VariableCost = (
        pd.read_excel(DataExcel,index_col = [0,1,2], sheet_name = "VC")
        .stack().reset_index().rename(columns={"level_3": "YEAR",0:"value"})
        .set_index(RTMY).to_dict('index')
    )
    FixedCost =(
        pd.read_excel(DataExcel,index_col = [0,1], sheet_name = "FC")
        .stack().reset_index().rename(columns={"level_2": "YEAR",0:"value"})
        .set_index(RTY).to_dict('index')
    )
    CostoNoAsociado =(
        pd.read_excel(DataExcel,index_col = [0,1], sheet_name = "CNA")
        .stack().reset_index().rename(columns={"level_2": "YEAR",0:"value"})
        .set_index(RTY).to_dict('index')
    )
    """Parámetros nuevos"""
    NumberOfExistingUnits =(
        pd.read_excel(DataExcel,index_col = [0,1], sheet_name = "NOEU")
        .stack().reset_index().rename(columns={"level_2": "YEAR",0:"value"})
        .set_index(RTY).to_dict('index')
    )
    Availability =(
        pd.read_excel(DataExcel,index_col = [0,1], sheet_name = "Avail")
        .stack().reset_index().rename(columns={"level_2": "YEAR",0:"value"})
        .set_index(RTY).to_dict('index')
    )
    VidaUtilRecuperada = (
        pd.read_excel(DataExcel,index_col = [0], sheet_name = "VUR")
        .stack().reset_index().rename(columns={"level_1": "TECHNOLOGY",0:"value"})
        .set_index(RT).to_dict('index')
    )
    CostoRecuperacion = (
        pd.read_excel(DataExcel,index_col = [0,1], sheet_name = "CostoRec")
        .stack().reset_index().rename(columns={"level_2": "YEAR",0:"value"})
        .set_index(RTY).to_dict('index')
    )
    #%%
    """Storage"""
    # TechnologyToStorage = (
    #     pd.read_excel(DataExcel,index_col = list(range(len(RTSM)-1)), sheet_name = "TTS")
    #     .stack().reset_index().rename(columns={f"level_{len(RTSM)-1}": "MODE_OF_OPERATION",0:"value"})
    #     .set_index(RTSM).to_dict('index')
    # )


    #%%
    """Capacity"""
    CapacityOfOneTechnologyUnit =  (
        pd.read_excel(DataExcel,index_col = [0,1], sheet_name = "C1TU")
        .stack().reset_index().rename(columns={"level_2": "YEAR",0:"value"})
        .set_index(RTY).to_dict('index')
    )
    TotalAnnualMaxCapacity = (
        pd.read_excel(DataExcel,index_col = [0,1], sheet_name = "TAMaxC")
        .stack().reset_index().rename(columns={"level_2": "YEAR",0:"value"})
        .set_index(RTY).to_dict('index')
    )
    TotalAnnualMinCapacity = (
        pd.read_excel(DataExcel,index_col = [0,1], sheet_name = "TAMinC")
        .stack().reset_index().rename(columns={"level_2": "YEAR",0:"value"})
        .set_index(RTY).to_dict('index')    
    )
    TotalAnnualMaxCapacityInvestment = TotalAnnualMinCapacity = (
        pd.read_excel(DataExcel,index_col = [0,1], sheet_name = "TAMaxCI")
        .stack().reset_index().rename(columns={"level_2": "YEAR",0:"value"})
        .set_index(RTY).to_dict('index')    
    )
    TotalAnnualMinCapacityInvestment = (
        pd.read_excel(DataExcel,index_col = [0,1], sheet_name = "TAMinCI")
        .stack().reset_index().rename(columns={"level_2": "YEAR",0:"value"})
        .set_index(RTY).to_dict('index')    
    )
    #%%
    """Activity constraints"""
    TotalTechnologyAnnualActivityUpperLimit = (
        pd.read_excel(DataExcel,index_col = [0,1], sheet_name = "TTAAUL")
        .stack().reset_index().rename(columns={"level_2": "YEAR",0:"value"})
        .set_index(RTY).to_dict('index')    
    )
    TotalTechnologyAnnualActivityLowerLimit= (
        pd.read_excel(DataExcel,index_col = [0,1], sheet_name = "TTAALL")
        .stack().reset_index().rename(columns={"level_2": "YEAR",0:"value"})
        .set_index(RTY).to_dict('index')    
    )
    TotalTechnologyModelPeriodActivityUpperLimit = (
        pd.read_excel(DataExcel,index_col = [0], sheet_name = "TTMPAUL")
        .stack().reset_index().rename(columns={"level_1": "TECHNOLOGY",0:"value"})
        .set_index(RT).to_dict('index')    
    )
    TotalTechnologyModelPeriodActivityLowerLimit= (
        pd.read_excel(DataExcel,index_col = [0], sheet_name = "TTMPALL")
        .stack().reset_index().rename(columns={"level_1": "TECHNOLOGY",0:"value"})
        .set_index(RT).to_dict('index')    
    )
    #%%
    """Reserve Margin"""
    ReserveMarginTagTechnology = (
        pd.read_excel(DataExcel,index_col = [0,1], sheet_name = "RMTT")
        .stack().reset_index().rename(columns={"level_2": "YEAR",0:"value"})
        .set_index(RTY).to_dict('index')    
    )
    ReserveMarginTagFuel = (
        pd.read_excel(DataExcel,index_col = [0,1], sheet_name = "RMTF")
        .stack().reset_index().rename(columns={"level_2": "YEAR",0:"value"})
        .set_index(RFY).to_dict('index')    
    )

    ReserveMargin = (
        pd.read_excel(DataExcel,index_col = [0], sheet_name = "RM")
        .stack().reset_index().rename(columns={"level_1": "YEAR",0:"value"})
        .set_index(RY).to_dict('index')    
    )


    #%%
    """RE Generation Target"""
    RETagTechnology = (
        pd.read_excel(DataExcel,index_col = [0,1], sheet_name = "ReTagT")
        .stack().reset_index().rename(columns={"level_2": "YEAR",0:"value"})
        .set_index(RTY).to_dict('index')
    )
    RETagFuel= (
        pd.read_excel(DataExcel,index_col = [0,1], sheet_name = "ReTagF")
        .stack().reset_index().rename(columns={"level_2": "YEAR",0:"value"})
        .set_index(RFY).to_dict('index')
    )
    REMinProductionTarget = (
        pd.read_excel(DataExcel,index_col = [0], sheet_name = "REMinPT")
        .stack().reset_index().rename(columns={"level_1": "YEAR",0:"value"})
        .set_index(RY).to_dict('index')
    )
    """Emissions"""
    # EmissionActivityRatio = (
    #     pd.read_excel(DataExcel,index_col = list(range(len(RTEMY)-1)), sheet_name = "EmAR")
    #     .stack().reset_index().rename(columns={f"level_{len(RTEMY)-1}": "YEAR",0:"value"})
    #     .set_index(RTEMY).to_dict('index')
    # )
    # EmissionsPenalty = (
    #     pd.read_excel(DataExcel,index_col = list(range(len(REY)-1)), sheet_name = "EmP")
    #     .stack().reset_index().rename(columns={f"level_{len(REY)-1}": "YEAR",0:"value"})
    #     .set_index(REY).to_dict('index')
    # )
    # AnnualExogenousEmission= (
    #     pd.read_excel(DataExcel,index_col = list(range(len(REY)-1)), sheet_name = "AExEm")
    #     .stack().reset_index().rename(columns={f"level_{len(REY)-1}": "YEAR",0:"value"})
    #     .set_index(REY).to_dict('index')
    # )
    # AnnualEmissionLimit= (
    #     pd.read_excel(DataExcel,index_col = list(range(len(REY)-1)), sheet_name = "AEmLim")
    #     .stack().reset_index().rename(columns={f"level_{len(REY)-1}": "YEAR",0:"value"})
    #     .set_index(REY).to_dict('index')
    # )
    # ModelPeriodExogenousEmission= (
    #     pd.read_excel(DataExcel,index_col = list(range(len(RE)-1)), sheet_name = "MPExEm")
    #     .stack().reset_index().rename(columns={f"level_{len(RE)-1}": "EMISSION",0:"value"})
    #     .set_index(RE).to_dict('index')
    # )
    # ModelPeriodEmissionLimit= (
    #     pd.read_excel(DataExcel,index_col = list(range(len(RE)-1)), sheet_name = "MPEmLim")
    #     .stack().reset_index().rename(columns={f"level_{len(RE)-1}": "EMISSION",0:"value"})
    #     .set_index(RE).to_dict('index')
    # )



    # %%
    """Convert dict to json with index and value"""
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
    """Create dictionary lists"""
    YearSplit = ListDict("p_YearSplit",YearSplit)
    DaySplit = ListDict("p_DaySplit", DaySplit)
    DaysInDayType = ListDict("p_DaysInDayType", DaysInDayType)
    Conversionls = ListDict('p_Conversionls', Conversionls)

    SpecifiedAnnualDemand = ListDict('p_SpecifiedAnnualDemand',SpecifiedAnnualDemand)
    SpecifiedDemandProfile = ListDict('p_SpecifiedDemandProfile', SpecifiedDemandProfile)
    AccumulatedAnnualDemand = ListDict('p_AccumulatedAnnualDemand', AccumulatedAnnualDemand)

    CapacityToActivityUnit = ListDict('p_CapacityToActivityUnit', CapacityToActivityUnit)
    CapacityFactor = ListDict('p_CapacityFactor', CapacityFactor)
    AvailabilityFactor = ListDict('p_AvailabilityFactor', AvailabilityFactor)
    OperationalLife = ListDict('p_OperationalLife', OperationalLife)
    ResidualCapacity = ListDict('p_ResidualCapacity', ResidualCapacity)
    InputActivityRatio = ListDict('p_InputActivityRatio', InputActivityRatio)
    OutputActivityRatio = ListDict('p_OutputActivityRatio', OutputActivityRatio)
    MinimumOperatingLoad = ListDict('p_MinimumOperatingLoad', MinimumOperatingLoad)

    CapitalCost = ListDict('p_CapitalCost', CapitalCost)
    VariableCost = ListDict('p_VariableCost', VariableCost)
    FixedCost = ListDict('p_FixedCost', FixedCost)
    CostoNoAsociado = ListDict('p_CostoNoAsociado', CostoNoAsociado)

    CapacityOfOneTechnologyUnit = ListDict('p_CapacityOfOneTechnologyUnit', CapacityOfOneTechnologyUnit)
    TotalAnnualMaxCapacity = ListDict('p_TotalAnnualMaxCapacity', TotalAnnualMaxCapacity)
    TotalAnnualMinCapacity = ListDict('p_TotalAnnualMinCapacity', TotalAnnualMinCapacity)
    TotalAnnualMaxCapacityInvestment = ListDict('p_TotalAnnualMaxCapacityInvestment', TotalAnnualMaxCapacityInvestment)
    TotalAnnualMinCapacityInvestment = ListDict('p_TotalAnnualMinCapacityInvestment', TotalAnnualMinCapacityInvestment)

    TotalTechnologyAnnualActivityUpperLimit = ListDict('p_TotalTechnologyAnnualActivityUpperLimit', TotalTechnologyAnnualActivityUpperLimit)
    TotalTechnologyAnnualActivityLowerLimit = ListDict('p_TotalTechnologyAnnualActivityLowerLimit', TotalTechnologyAnnualActivityLowerLimit)
    TotalTechnologyModelPeriodActivityUpperLimit = ListDict('p_TotalTechnologyModelPeriodActivityUpperLimit', TotalTechnologyModelPeriodActivityUpperLimit)
    TotalTechnologyModelPeriodActivityLowerLimit = ListDict('p_TotalTechnologyModelPeriodActivityLowerLimit', TotalTechnologyModelPeriodActivityLowerLimit)

    ReserveMarginTagTechnology = ListDict('p_ReserveMarginTagTechnology', ReserveMarginTagTechnology)
    ReserveMarginTagFuel = ListDict('p_ReserveMarginTagFuel', ReserveMarginTagFuel)
    ReserveMargin = ListDict('p_ReserveMargin', ReserveMargin)

    RETagTechnology = ListDict('p_RETagTechnology', RETagTechnology)
    RETagFuel = ListDict('p_RETagFuel', RETagFuel)
    REMinProductionTarget  = ListDict('p_REMinProductionTarget', REMinProductionTarget)

    NumberOfExistingUnits = ListDict('p_NumberOfExistingUnits', NumberOfExistingUnits)
    Availability = ListDict('p_Availability',Availability)
    CostoRecuperacion = ListDict('p_CostoRecuperacion', CostoRecuperacion)
    VidaUtilRecuperada = ListDict('p_VidaUtilRecuperada', VidaUtilRecuperada)

    # EmissionActivityRatio = ListDict('p_EmissionActivityRatio', EmissionActivityRatio)
    # EmissionsPenalty = ListDict('p_EmissionsPenalty',EmissionsPenalty)
    # AnnualExogenousEmission = ListDict('p_AnnualExogenousEmission',AnnualExogenousEmission)
    # AnnualEmissionLimit = ListDict('p_AnnualEmissionLimit',AnnualEmissionLimit)
    # ModelPeriodExogenousEmission = ListDict('p_ModelPeriodExogenousEmission',ModelPeriodExogenousEmission)
    # ModelPeriodEmissionLimit = ListDict('p_ModelPeriodEmissionLimit',ModelPeriodEmissionLimit)
    #%%
    ParamDict = {}
    for d in (
        YearSplit, DaySplit, DaysInDayType, Conversionls,
        
        SpecifiedAnnualDemand,SpecifiedDemandProfile,AccumulatedAnnualDemand,
        
        CapacityToActivityUnit,CapacityFactor,AvailabilityFactor,OperationalLife,
        ResidualCapacity,InputActivityRatio,OutputActivityRatio, MinimumOperatingLoad,
        
        CapitalCost,VariableCost,FixedCost, CostoNoAsociado,
        
        CapacityOfOneTechnologyUnit, TotalAnnualMaxCapacity, TotalAnnualMinCapacity,
        TotalAnnualMaxCapacityInvestment, TotalAnnualMinCapacityInvestment,
        
        TotalTechnologyAnnualActivityUpperLimit, TotalTechnologyAnnualActivityLowerLimit,
        TotalTechnologyModelPeriodActivityUpperLimit, TotalTechnologyModelPeriodActivityLowerLimit,
        
        ReserveMarginTagTechnology, ReserveMarginTagFuel, ReserveMargin,
        
        RETagTechnology, RETagFuel, REMinProductionTarget,
        
        Availability, NumberOfExistingUnits, VidaUtilRecuperada, CostoRecuperacion
        # EmissionActivityRatio, EmissionsPenalty, AnnualExogenousEmission, 
        # AnnualEmissionLimit, ModelPeriodExogenousEmission, ModelPeriodEmissionLimit
    ):ParamDict.update(d)

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
    OsemosysDict.update(ParamDict)


    with open(results_folder+'/Data.json', 'w') as json_file:
        json.dump(OsemosysDict, json_file)
    #%%
    # json.loads(json.dumps(OsemosysDict))
    # OsemosysDict.to_json('Datap.json')
        
    # EmissionActivityRatio = ListDict('EmissionActivityRatio', EmissionActivityRatio)
    # EmissionsPenalty = ListDict('EmissionsPenalty', EmissionsPenalty)
    # AnnualExogenousEmission = ListDict('AnnualExogenousEmission', AnnualExogenousEmission)
    # AnnualEmissionLimit = ListDict('AnnualEmissionLimit', AnnualEmissionLimit)
    # ModelPeriodExogenousEmission = ListDict('ModelPeriodExogenousEmission', ModelPeriodExogenousEmission)
    # ModelPeriodEmissionLimit = ListDict('ModelPeriodEmissionLimit', ModelPeriodEmissionLimit)


            
        
    # OsemosysJson = json.loads(json.dumps(my_list))

    # %%
    DataExcel.close()
    return ParamDict, OsemosysDict    
    
    """Leer todo en el excel"""
    # sheet_to_df_map = {}
    # for sheet_name in DataExcel.sheet_names:
    #     sheet_to_df_map[sheet_name] = DataExcel.parse(sheet_name)


    # SpecifiedAnnualDemand = SpecifiedAnnualDemand.reset_index().rename(columns={"level_2": "YEAR",0:"value"})
    # SpecifiedAnnualDemand = SpecifiedAnnualDemand.set_index(['REGION', 'FUEL', 'YEAR'])
    # Osemosysjson = json.loads(json.dumps(my_list))        
    #
    # indexing = []
    # for i in range(len(SpecifiedAnnualDemand.index)):
    #     indexing.append("index")

    # new_df = SpecifiedAnnualDemand.reset_index().rename(columns={"level_2": "YEAR",0:"value"}).set_axis(indexing).reset_index().rename(columns={0: "index"})
    # SpecifiedAnnualDemand = SpecifiedAnnualDemand.to_json(orient="index")


    # SpecifiedAnnualDemand = SpecifiedAnnualDemand.replace("'","\"")
    # SpecifiedAnnualDemand = SpecifiedAnnualDemand.replace('(','index":[')
    # SpecifiedAnnualDemand = SpecifiedAnnualDemand.replace(')"','],"value"')
    # SpecifiedAnnualDemand = SpecifiedAnnualDemand.replace(',"i','},"i')
    # SpecifiedAnnualDemand = SpecifiedAnnualDemand.replace('"index"','{"index"')
    # SpecifiedAnnualDemand = SpecifiedAnnualDemand.replace('{{','{')

    # SpecifiedAnnualDemand = json.loads('{"pdasda": ['+SpecifiedAnnualDemand+']}')

    # SpecifiedAnnualDemand = pd.read_excel(DataExcel,index_col=[0,1],  sheet_name = 'SAD',skiprows=1).stack()

    # SpecifiedAnnualDemand = SpecifiedAnnualDemand.set_index(['REGION','FUEL' ], inplace=False).stack()#.to_frame('Values')
    # table = pd.pivot_table(SpecifiedAnnualDemand, 
    #                        index=['REGION', 'FUEL'])

# %%
def read_defaults(filename):
    DataExcel = pd.ExcelFile(filename)
    Default = (pd.read_excel(DataExcel, sheet_name = 'Default Parameters', index_col=0))

    DataExcel.close()
    return Default


if __name__ == "__main__":
    filename = '../data/OsemosysNew.xlsx'
    ParamDict, OsemosysDict = read_excel(filename)
    Default = read_defaults(filename)
    a= 1