import pandas as pd
import os, sys
root_folder = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(root_folder)
from OSeMOSYS.config import INPUT_FILE_PATH

file_path = INPUT_FILE_PATH
print(file_path)
def load_sets(file_path):
    
    DataExcel = pd.ExcelFile(file_path)
    Default = (pd.read_excel(DataExcel, sheet_name = 'Default Parameters', index_col=0))
    REGION = list(pd.read_excel(DataExcel, sheet_name='R')['REGION'])
    initial_year = pd.read_excel(DataExcel, sheet_name='Y')['START_YEAR'][0]
    final_year = pd.read_excel(DataExcel, sheet_name='Y')['FINAL_YEAR'][0]
    YEAR = list(range(int(initial_year), int(final_year) + 1))

    TECHNOLOGY = list(pd.read_excel(DataExcel, sheet_name='T')['TECHNOLOGY'])
    FUEL = list(pd.read_excel(DataExcel, sheet_name='F')['FUEL'])
    SEASON = list(pd.read_excel(DataExcel, sheet_name='LS')['SEASON'])
    DAYTYPE = list(pd.read_excel(DataExcel, sheet_name='LD')['DAYTYPE'])
    DAILYTIMEBRACKET = list(pd.read_excel(DataExcel, sheet_name='LH')['DAILYTIMEBRACKET'])
    TIMESLICE = list(pd.read_excel(DataExcel, sheet_name='L')['TIMESLICE'])
    MODE_OF_OPERATION = list(pd.read_excel(DataExcel, sheet_name='M')['ModeOfOperation'])
    STORAGE = list(pd.read_excel(DataExcel, sheet_name='S')['STORAGE'])
    EMISSION = list(pd.read_excel(DataExcel, sheet_name='E')['EMISSION'])
    DataExcel.close()
    return Default, REGION, YEAR, TECHNOLOGY, FUEL, SEASON, DAYTYPE, DAILYTIMEBRACKET, TIMESLICE, MODE_OF_OPERATION, STORAGE, EMISSION

# Default, REGION, YEAR, TECHNOLOGY, FUEL, SEASON, DAYTYPE, DAILYTIMEBRACKET, TIMESLICE, MODE_OF_OPERATION, STORAGE, EMISSION = load_sets(file_path)

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

def read_excel_sheets(file_path, sheet_names, dataframe_names):
    """
    Reads Excel sheets and returns a dictionary of DataFrames with specified names.

    Parameters:
    - file_path (str): Path to the Excel file.
    - sheet_names (list): List of sheet names to read.
    - dataframe_names (list): List of desired DataFrame names.

    Returns:
    - dict: Dictionary of DataFrames with specified names.
    """
    data_frames = {}
    for sheet_name, df_name in zip(sheet_names, dataframe_names):
        data_frames[df_name] = pd.read_excel(file_path, sheet_name=sheet_name)

    return data_frames

def create_multiindex_dataframe(lists_dict):

    """_summary_

    Returns:
        -dict: _description_
    """    

    result_dict = {}
    for key, value in lists_dict.items():
        df = pd.MultiIndex.from_product([globals()[item] for item in value[:-1]], names=value[:-1])
        result_df = pd.DataFrame('', index= df, columns=globals()[value[-1]]).reset_index()
        result_dict[key] = result_df
    return result_dict

# def read_defaults(filename):
#     DataExcel = pd.ExcelFile(filename)
#     Default = (pd.read_excel(DataExcel, sheet_name = 'Default Parameters', index_col=0))

#     DataExcel.close()
#     return Default
if __name__ == "__main__":
    filename = INPUT_FILE_PATH
    # ParamDict, OsemosysDict = read_excel(file_path)
    Default = load_sets(INPUT_FILE_PATH)
    a= 1
# Example usage
