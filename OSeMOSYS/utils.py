sets = ['REGION', 'YEAR', 'TECHNOLOGY', 'FUEL', 'SEASON', 'DAYTYPE', 'DAILYTIMEBRACKET', 'TIMESLICE', 'MODE_OF_OPERATION', 'STORAGE', 'EMISSION']
variable_mapping = {'REGION': REGION, 
                    'YEAR': YEAR,
                    'TECHNOLOGY':TECHNOLOGY,
                    'FUEL':FUEL,
                    'SEASON':  SEASON,
                    'DAYTYPE' :DAYTYPE,
                    'DAILYTIMEBRACKET':DAILYTIMEBRACKET,
                    'TIMESLICE': TIMESLICE,
                    'MODE_OF_OPERATION': MODE_OF_OPERATION,
                    'STORAGE': STORAGE,
                    'EMISSION': EMISSION
                    }


lists_dict = {
    'LY': ['TIMESLICE', 'YEAR'],
    'LLS': ['TIMESLICE', 'SEASON'],
    'LLD': ['TIMESLICE', 'DAYTYPE'],
    'LLH': ['TIMESLICE', 'DAILYTIMEBRACKET'],
    'LHY': ['DAILYTIMEBRACKET', 'YEAR'],
    'LSLDY': ['SEASON', 'DAYTYPE', 'YEAR'],
    'RFY': ['REGION','FUEL','YEAR'],
    'RFLY': ['REGION','FUEL','TIMESLICE','YEAR'],
    'RTY': ['REGION','TECHNOLOGY','YEAR'],
    'RTLY': ['REGION', 'TECHNOLOGY','TIMESLICE','YEAR'],
    'RF': ['REGION','FUEL'],
    'RT': ['REGION','TECHNOLOGY'],
    'RTFMY': ['REGION','TECHNOLOGY','FUEL','MODE_OF_OPERATION','YEAR'],
    'RTMY': ['REGION','TECHNOLOGY','MODE_OF_OPERATION','YEAR'],
    'RTSM': ['REGION','TECHNOLOGY','STORAGE','MODE_OF_OPERATION'],
    'RS': ['REGION','STORAGE'],
    'RSY': ['REGION','STORAGE','YEAR'],
    'RY': ['REGION','YEAR'],
    'RTEM': ['REGION','TECHNOLOGY','EMISSION','MODE_OF_OPERATION'],
    'RTEMY': ['REGION','TECHNOLOGY','EMISSION','MODE_OF_OPERATION','YEAR'],
    'REY': ['REGION','EMISSION','YEAR'],
    'RE': ['REGION','EMISSION']
}

LY = ['TIMESLICE', 'YEAR']
LLS = ['TIMESLICE', 'SEASON']
LLD = ['TIMESLICE', 'DAYTYPE']
LLH= ['TIMESLICE', 'DAILYTIMEBRACKET']
LHY= ['DAILYTIMEBRACKET', 'YEAR']
LSLDY= ['SEASON', 'DAYTYPE', 'YEAR']
RFY= ['REGION','FUEL','YEAR']
RFLY= ['REGION','FUEL','TIMESLICE','YEAR']
RTY= ['REGION','TECHNOLOGY','YEAR']
RTLY= ['REGION', 'TECHNOLOGY','TIMESLICE','YEAR']
RF= ['REGION','FUEL']
RT= ['REGION','TECHNOLOGY']
RTFMY= ['REGION','TECHNOLOGY','FUEL','MODE_OF_OPERATION','YEAR']
RTMY= ['REGION','TECHNOLOGY','MODE_OF_OPERATION','YEAR']
RTSM= ['REGION','TECHNOLOGY','STORAGE','MODE_OF_OPERATION']
RS= ['REGION','STORAGE']
RSY= ['REGION','STORAGE','YEAR']
RY= ['REGION','YEAR']
RTEM= ['REGION','TECHNOLOGY','EMISSION','MODE_OF_OPERATION']
RTEMY= ['REGION','TECHNOLOGY','EMISSION','MODE_OF_OPERATION','YEAR']
REY= ['REGION','EMISSION','YEAR']
RE= ['REGION','EMISSION']



sheet_names = ["YS", "LLS", "LLD","LLH", "DS", "DIDT", "SAD", "SDP", "AAD", "C2AU", "CF", "AF", "OL", "RC", "IAR", "OAR", "CC", "VC", "FC", "TTS", "TFS", "StLS",
            "StMxChR", "StMxDCh", "MinStCh", "OpLiSt", "CCSt", "ReStCap", "C1TU", "TAMaxC", "TAMinC", "TAMaxCI", "TAMinCI", "TTAAUL", "TTAALL", "TTMPAUL",
            "TTMPALL", "RMTT", "RMTF", "RM", "ReTagT", "ReTagF", "REMinPT", "EmAR", "EmP", "AExEm", "AEmLim", "MPExEm", "MPEmLim", "CNA", "MOL", "Avail",
            "NOEU", "CostoRec", "VUR", 'Maintenance',  "Exp", "MustRunTech","MustRunFuel", "MustRun"]

  
dataframe_names = ["YearSplit", "Conversionls", "Conversionld","Conversionlh",
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
                "NumberOfExistingUnits", "CostoRecuperacion", "VidaUtilRecuperada", "ExportPrice", "MustRunTech","MustRunFuel","MustRun"]