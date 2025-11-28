from itertools import cycle
import plotly.express as px

sets = ['REGION', 'YEAR', 'TECHNOLOGY', 'FUEL', 'SEASON', 'DAYTYPE', 'DAILYTIMEBRACKET', 'TIMESLICE', 'MODE_OF_OPERATION', 'STORAGE', 'EMISSION']

def create_variable_mapping(REGION, YEAR, TECHNOLOGY, FUEL, SEASON, DAYTYPE, DAILYTIMEBRACKET, TIMESLICE, MODE_OF_OPERATION, STORAGE, EMISSION):
    """
    Crea un diccionario que mapea nombres de conjuntos a sus valores.

    Args:
        REGION, YEAR, TECHNOLOGY, FUEL, SEASON, DAYTYPE, DAILYTIMEBRACKET, TIMESLICE, MODE_OF_OPERATION, STORAGE, EMISSION:
        Listas que representan los conjuntos.

    Returns:
        dict: Diccionario que mapea nombres de conjuntos a sus valores.s
    """
    return {
        'REGION': REGION,
        'YEAR': YEAR,
        'TECHNOLOGY': TECHNOLOGY,
        'FUEL': FUEL,
        'SEASON': SEASON,
        'DAYTYPE': DAYTYPE,
        'DAILYTIMEBRACKET': DAILYTIMEBRACKET,
        'TIMESLICE': TIMESLICE,
        'MODE_OF_OPERATION': MODE_OF_OPERATION,
        'STORAGE': STORAGE,
        'EMISSION': EMISSION
    }


# lists_dict = {
#     'LY': ['TIMESLICE', 'YEAR'],
#     'LLS': ['TIMESLICE', 'SEASON'],
#     'LLD': ['TIMESLICE', 'DAYTYPE'],
#     'LLH': ['TIMESLICE', 'DAILYTIMEBRACKET'],
#     'LHY': ['DAILYTIMEBRACKET', 'YEAR'],
#     'LSLDY': ['SEASON', 'DAYTYPE', 'YEAR'],
#     'RFY': ['REGION','FUEL','YEAR'],
#     'RFLY': ['REGION','FUEL','TIMESLICE','YEAR'],
#     'RTY': ['REGION','TECHNOLOGY','YEAR'],
#     'RTLY': ['REGION', 'TECHNOLOGY','TIMESLICE','YEAR'],
#     'RF': ['REGION','FUEL'],
#     'RT': ['REGION','TECHNOLOGY'],
#     'RTFMY': ['REGION','TECHNOLOGY','FUEL','MODE_OF_OPERATION','YEAR'],
#     'RTMY': ['REGION','TECHNOLOGY','MODE_OF_OPERATION','YEAR'],
#     'RTSM': ['REGION','TECHNOLOGY','STORAGE','MODE_OF_OPERATION'],
#     'RS': ['REGION','STORAGE'],
#     'RSY': ['REGION','STORAGE','YEAR'],
#     'RY': ['REGION','YEAR'],
#     'RTEM': ['REGION','TECHNOLOGY','EMISSION','MODE_OF_OPERATION'],
#     'RTEMY': ['REGION','TECHNOLOGY','EMISSION','MODE_OF_OPERATION','YEAR'],
#     'REY': ['REGION','EMISSION','YEAR'],
#     'RE': ['REGION','EMISSION']
# }

# LY = ['TIMESLICE', 'YEAR']
# LLS = ['TIMESLICE', 'SEASON']
# LLD = ['TIMESLICE', 'DAYTYPE']
# LLH= ['TIMESLICE', 'DAILYTIMEBRACKET']
# LHY= ['DAILYTIMEBRACKET', 'YEAR']
# LSLDY= ['SEASON', 'DAYTYPE', 'YEAR']
# RFY= ['REGION','FUEL','YEAR']
# RFLY= ['REGION','FUEL','TIMESLICE','YEAR']
# RTY= ['REGION','TECHNOLOGY','YEAR']
# RTLY= ['REGION', 'TECHNOLOGY','TIMESLICE','YEAR']
# RF= ['REGION','FUEL']
# RT= ['REGION','TECHNOLOGY']
# RTFMY= ['REGION','TECHNOLOGY','FUEL','MODE_OF_OPERATION','YEAR']
# RTMY= ['REGION','TECHNOLOGY','MODE_OF_OPERATION','YEAR']
# RTSM= ['REGION','TECHNOLOGY','STORAGE','MODE_OF_OPERATION']
# RS= ['REGION','STORAGE']
# RSY= ['REGION','STORAGE','YEAR']
# RY= ['REGION','YEAR']
# RTEM= ['REGION','TECHNOLOGY','EMISSION','MODE_OF_OPERATION']
# RTEMY= ['REGION','TECHNOLOGY','EMISSION','MODE_OF_OPERATION','YEAR']
# REY= ['REGION','EMISSION','YEAR']
# RE= ['REGION','EMISSION']



sheet_names = ["YS", "LLS", "LLD","LLH", "DS", "DIDT", "SAD", "SDP", "AAD", "C2AU", "CF", "AF", "OL", "RC", "IAR", "OAR", "CC", "VC", "FC", "TTS", "TFS", "StLS",
            "StMxChR", "StMxDCh", "MinStCh", "OpLiSt", "CCSt", "ReStCap", "C1TU", "TAMaxC", "TAMinC", "TAMaxCI", "TAMinCI", "TTAAUL", "TTAALL", "TTMPAUL",
            "TTMPALL", "RMTT", "RMTF", "RM", "ReTagT", "ReTagF", "REMinPT", "EmAR", "EmP", "AExEm", "AEmLim", "MPExEm", "MPEmLim", "CNA", "MOL", "Avail",
            "NOEU", "CostoRec", "VUR", "Maintenance",  "Exp", "MustRunTech","MustRunFuel", "MustRun"]

dataframe_metadata = {
    "YearSplit": {"key": "LY", "indices": ["TIMESLICE", "YEAR"]},
    "Conversionls": {"key": "LLS", "indices": ["TIMESLICE", "SEASON"]},
    "Conversionld": {"key": "LLD", "indices": ["TIMESLICE", "DAYTYPE"]},
    "Conversionlh": {"key": "LLH", "indices": ["TIMESLICE", "DAILYTIMEBRACKET"]},
    "DaySplit": {"key": "LHY", "indices": ["DAILYTIMEBRACKET", "YEAR"]},
    "DaysInDayType": {"key": "LSLDY", "indices": ["SEASON", "DAYTYPE", "YEAR"]},
    "SpecifiedAnnualDemand": {"key": "RFY", "indices": ["REGION", "FUEL", "YEAR"]},
    "SpecifiedDemandProfile": {"key": "RFLY", "indices": ["REGION", "FUEL", "TIMESLICE", "YEAR"]},
    "AccumulatedAnnualDemand": {"key": "RFY", "indices": ["REGION", "FUEL", "YEAR"]},
    "CapacityToActivityUnit": {"key": "RT", "indices": ["REGION", "TECHNOLOGY"]},
    "CapacityFactor": {"key": "RTLY", "indices": ["REGION", "TECHNOLOGY", "TIMESLICE", "YEAR"]},
    "AvailabilityFactor": {"key": "RTY", "indices": ["REGION", "TECHNOLOGY", "YEAR"]},
    "OperationalLife": {"key": "RT", "indices": ["REGION", "TECHNOLOGY"]},
    "ResidualCapacity": {"key": "RTY", "indices": ["REGION", "TECHNOLOGY", "YEAR"]},
    "InputActivityRatio": {"key": "RTFMY", "indices": ["REGION", "TECHNOLOGY", "FUEL", "MODE_OF_OPERATION", "YEAR"]},
    "OutputActivityRatio": {"key": "RTFMY", "indices": ["REGION", "TECHNOLOGY", "FUEL", "MODE_OF_OPERATION", "YEAR"]},
    "CapitalCost": {"key": "RTY", "indices": ["REGION", "TECHNOLOGY", "YEAR"]},
    "VariableCost": {"key": "RTMY", "indices": ["REGION", "TECHNOLOGY", "MODE_OF_OPERATION", "YEAR"]},
    "FixedCost": {"key": "RTY", "indices": ["REGION", "TECHNOLOGY", "YEAR"]},
    "TechnologyToStorage": {"key": "RTSM", "indices": ["REGION", "TECHNOLOGY", "STORAGE", "MODE_OF_OPERATION"]},
    "TechnologyFromStorage": {"key": "RTSM", "indices": ["REGION", "TECHNOLOGY", "STORAGE", "MODE_OF_OPERATION"]},
    "StorageLevelStart": {"key": "RS", "indices": ["REGION", "STORAGE"]},
    "StorageMaxChargeRate": {"key": "RS", "indices": ["REGION", "STORAGE"]},
    "StorageMaxDischargeRate": {"key": "RS", "indices": ["REGION", "STORAGE"]},
    "MinStorageCharge": {"key": "RSY", "indices": ["REGION", "STORAGE", "YEAR"]},
    "OperationalLifeStorage": {"key": "RS", "indices": ["REGION", "STORAGE"]},
    "CapitalCostStorage": {"key": "RSY", "indices": ["REGION", "STORAGE", "YEAR"]},
    "ResidualStorageCapacity": {"key": "RSY", "indices": ["REGION", "STORAGE", "YEAR"]},
    "CapacityOfOneTechnologyUnit": {"key": "RTY", "indices": ["REGION", "TECHNOLOGY", "YEAR"]},
    "TotalAnnualMaxCapacity": {"key": "RTY", "indices": ["REGION", "TECHNOLOGY", "YEAR"]},
    "TotalAnnualMinCapacity": {"key": "RTY", "indices": ["REGION", "TECHNOLOGY", "YEAR"]},
    "TotalAnnualMaxCapacityInvestment": {"key": "RTY", "indices": ["REGION", "TECHNOLOGY", "YEAR"]},
    "TotalAnnualMinCapacityInvestment": {"key": "RTY", "indices": ["REGION", "TECHNOLOGY", "YEAR"]},
    "TotalTechnologyAnnualActivityUpperLimit": {"key": "RTY", "indices": ["REGION", "TECHNOLOGY", "YEAR"]},
    "TotalTechnologyAnnualActivityLowerLimit": {"key": "RTY", "indices": ["REGION", "TECHNOLOGY", "YEAR"]},
    "TotalTechnologyModelPeriodActivityUpperLimit": {"key": "RT", "indices": ["REGION", "TECHNOLOGY"]},
    "TotalTechnologyModelPeriodActivityLowerLimit": {"key": "RT", "indices": ["REGION", "TECHNOLOGY"]},
    "ReserveMarginTagTechnology": {"key": "RTY", "indices": ["REGION", "TECHNOLOGY", "YEAR"]},
    "ReserveMarginTagFuel": {"key": "RFY", "indices": ["REGION", "FUEL", "YEAR"]},
    "ReserveMargin": {"key": "RY", "indices": ["REGION", "YEAR"]},
    "RETagTechnology": {"key": "RTY", "indices": ["REGION", "TECHNOLOGY", "YEAR"]},
    "RETagFuel": {"key": "RFY", "indices": ["REGION", "FUEL", "YEAR"]},
    "REMinProductionTarget": {"key": "RY", "indices": ["REGION", "YEAR"]},
    "EmissionActivityRatio": {"key": "RTEMY", "indices": ["REGION", "TECHNOLOGY", "EMISSION", "MODE_OF_OPERATION", "YEAR"]},
    "EmissionsPenalty": {"key": "REY", "indices": ["REGION", "EMISSION", "YEAR"]},
    "AnnualExogenousEmission": {"key": "REY", "indices": ["REGION", "EMISSION", "YEAR"]},
    "AnnualEmissionLimit": {"key": "REY", "indices": ["REGION", "EMISSION", "YEAR"]},
    "ModelPeriodExogenousEmission": {"key": "RE", "indices": ["REGION", "EMISSION"]},
    "ModelPeriodEmissionLimit": {"key": "RE", "indices": ["REGION", "EMISSION"]},
    "MinimumOperatingLoad": {"key": "RTY", "indices": ["REGION", "TECHNOLOGY", "YEAR"]},
    "CostoNoAsociado": {"key": "RTY", "indices": ["REGION", "TECHNOLOGY", "YEAR"]},
    "Availability": {"key": "RTY", "indices": ["REGION", "TECHNOLOGY", "YEAR"]},
    "NumberOfExistingUnits": {"key": "RTY", "indices": ["REGION", "TECHNOLOGY", "YEAR"]},
    "CostoRecuperacion": {"key": "RTY", "indices": ["REGION", "TECHNOLOGY", "YEAR"]},
    "VidaUtilRecuperada": {"key": "RT", "indices": ["REGION", "TECHNOLOGY"]},
    "Maintenance": {"key": "RTLY", "indices": ["REGION", "TECHNOLOGY", "TIMESLICE", "YEAR"]},
    "ExportPrice": {"key": "RFY", "indices": ["REGION", "FUEL", "YEAR"]},
    "MustRunTech": {"key": "RTY", "indices": ["REGION", "TECHNOLOGY", "YEAR"]},
    "MustRunFuel": {"key": "RFTY", "indices": ["REGION", "FUEL", "TIMESLICE", "YEAR"]},
    "MustRun": {"key": "RY", "indices": ["REGION", "YEAR"]},
}
dataframe_names = list(dataframe_metadata.keys())
# print(dataframe_names)



COLOR_VARIATIONS = {
# Keyword: [variaciones en orden]
'crud': ['#2F4F4F','#696969','gray', 'dimgray', 'darkgray', 'silver', 'lightgray', 'gainsboro', 'whitesmoke','black' ],
'pwrcrud008':['black'],
'fo': ['#8B0000', '#6A0000', '#A80000', '#C50000', '#D30000'],
'ng': ['orange', 'darkorange', '#FF8C00', '#FFA500', '#FFB732'],
'gas': ['orange', 'darkorange', '#FF8C00', '#FFA500', '#FFB732'],
'bio': ['#9ACD32', '#8BB92D', '#7BA428', '#A8D645', '#B6E052'],
'wnd': ['deepskyblue', '#00BFFF', '#0099CC', '#007399', '#005266'],
'wind': ['deepskyblue', '#00BFFF', "#0099CC", '#007399', '#005266'],
'pv': ['#FFD700', '#CCAC00', '#B38F00', '#FFE55C', '#FFF380'],
'sol': ['#FFD700', '#CCAC00', '#B38F00', '#FFE55C', '#FFF380'],
'hyd': ['#0d5c91', '#1f77b4', '#1560BD', '#2E8BFF', '#4AA6FF'],
'diesel': ['brown', '#8B4513', '#A0522D', '#CD853F', '#DEB887'],
'dsl': ['brown', '#8B4513', '#A0522D', '#CD853F', '#DEB887'],
'csp': ['#a87b05', '#efb810','#f9db5c', '#ffff94', '#A9A9A9'],
'nuclear': ['#FF6961', '#FF7F7F', '#FF8C8C', '#FF9999', '#FFAFAF'],
'solar': ['#FFD700', '#FFC300', '#FFA500', '#FF8C00', '#FF7F50'],
'coal': ['gray', 'dimgray', 'darkgray', 'silver', 'lightgray'],
'ccp': ['gray', 'dimgray', 'darkgray', 'silver', 'lightgray'],
'cimp': ['gray', 'dimgray', 'darkgray', 'silver', 'lightgray'],
'elc': ['orange', 'darkorange', '#FF8C00', '#FFA500', '#FFB732'],
'trans':['#510A32'],
'dist' :['#510A32'],
'bs' :['#510A32'],
'backst' :['#510A32'],
'backstop' :['#510A32'],
'dem' :['#510A32'],
}

DEPENDENCIES_VAR_DICT = {
    "['REGION','TIMESLICE','FUEL','YEAR']": [
        "RateOfDemand",
        "Demand",
        "RateOfProduction",
        "Production",
        "RateOfUse",
        "Use",
        "Export"
    ],
    "['REGION','STORAGE','SEASON','DAYTYPE','DAILYTIMEBRACKET','YEAR']": [
        "RateOfStorageCharge",
        "RateOfStorageDischarge",
        "NetChargeWithinYear",
        "NetChargeWithinDay",
        "StorageLevel"
    ],
    "['REGION','STORAGE','YEAR']": [
        "StorageLevelYearStart",
        "StorageLevelYearFinish",
        "StorageLowerLimit",
        "StorageUpperLimit",
        "AccumulatedNewStorageCapacity",
        "NewStorageCapacity",
        "CapitalInvestmentStorage",
        "DiscountedCapitalInvestmentStorage",
        "SalvageValueStorage",
        "DiscountedSalvageValueStorage",
        "TotalDiscountedStorageCost"
    ],
    "['REGION','STORAGE','SEASON','YEAR']": [
        "StorageLevelSeasonStart"
    ],
    "['REGION','STORAGE','SEASON','DAYTYPE','YEAR']": [
        "StorageLevelDayTypeStart",
        "StorageLevelDayTypeFinish"
    ],
    "['REGION','TECHNOLOGY','YEAR']": [
        "NumberOfNewTechnologyUnits",
        "NewCapacity",
        "AccumulatedNewCapacity",
        "TotalCapacityAnnual",
        "TotalTechnologyAnnualActivity",
        "CapitalInvestment",
        "DiscountedCapitalInvestment",
        "SalvageValue",
        "DiscountedSalvageValue",
        "OperatingCost",
        "DiscountedOperatingCost",
        "AnnualVariableOperatingCost",
        "AnnualFixedOperatingCost",
        "TotalDiscountedCostByTechnology",
        "AnnualTechnologyEmissionsPenalty",
        "DiscountedTechnologyEmissionsPenalty",
        "ResidualCapacity",
        "AccumulatedRecoveredUnits",
        "AccumulatedRecoveredCapacity",
        "AccumulatedRecoveredNewCapacity",
        "RecoveredExistingUnits",
        "RecoveredCapacity",
        "RecoveredNewCapacity"
    ],
    "['REGION','TIMESLICE','TECHNOLOGY','MODE_OF_OPERATION','YEAR']": [
        "RateOfActivity"
    ],
    "['REGION','TECHNOLOGY','TIMESLICE','YEAR']": [
        "RateOfTotalActivity"
    ],
    "['REGION','TECHNOLOGY','MODE_OF_OPERATION','YEAR']": [
        "TotalAnnualTechnologyActivityByMode"
    ],
    "['REGION','TECHNOLOGY']": [
        "TotalTechnologyModelPeriodActivity"
    ],
    "['REGION','TIMESLICE','TECHNOLOGY','MODE_OF_OPERATION','FUEL','YEAR']": [
        "RateOfProductionByTechnologyByMode",
        "RateOfUseByTechnologyByMode"
    ],
    "['REGION','TIMESLICE','TECHNOLOGY','FUEL','YEAR']": [
        "RateOfProductionByTechnology",
        "ProductionByTechnology",
        "RateOfUseByTechnology",
        "UseByTechnology"
    ],
    "['REGION','TECHNOLOGY','FUEL','YEAR']": [
        "ProductionByTechnologyAnnual",
        "UseByTechnologyAnnual"
    ],
    "['REGION','REGION','TIMESLICE','FUEL','YEAR']": [
        "Trade"
    ],
    "['REGION','REGION','FUEL','YEAR']": [
        "TradeAnnual"
    ],
    "['REGION','FUEL','YEAR']": [
        "ProductionAnnual",
        "UseAnnual"
    ],
    "['REGION','YEAR']": [
        "TotalDiscountedCost",
        "TotalCapacityInReserveMargin",
        "TotalREProductionAnnual",
        "RETotalProductionOfTargetFuelAnnual"
    ],
    "['REGION']": [
        "ModelPeriodCostByRegion"
    ],
    "['REGION','TIMESLICE','YEAR']": [
        "DemandNeedingReserveMargin"
    ],
    "['REGION','TECHNOLOGY','EMISSION','MODE_OF_OPERATION','YEAR']": [
        "AnnualTechnologyEmissionByMode"
    ],
    "['REGION','TECHNOLOGY','EMISSION','YEAR']": [
        "AnnualTechnologyEmission",
        "AnnualTechnologyEmissionPenaltyByEmission"
    ],
    "['REGION','EMISSION','YEAR']": [
        "AnnualEmissions"
    ],
    "['REGION','EMISSION']": [
        "ModelPeriodEmissions"
    ],
    "['REGION','TECHNOLOGY','SEASON','YEAR']": [
        "ConnectedUnits"
    ]
}

region_tech_year_files = DEPENDENCIES_VAR_DICT["['REGION','TECHNOLOGY','YEAR']"]
# print(region_tech_year_files)

def assign_colors_to_technologies(data, color_column, COLOR_VARIATIONS):
    """
    Asigna colores a las tecnologías basándose en coincidencias parciales con COLOR_VARIATIONS.

    Args:
        data (pd.DataFrame): DataFrame con los datos.
        color_column (str): Nombre de la columna que contiene las tecnologías.
        COLOR_VARIATIONS (dict): Diccionario que asigna colores a las tecnologías.

    Returns:
        dict: Diccionario que asigna colores a cada tecnología en los datos.
    """
    # Crear una lista de colores por defecto para tecnologías no definidas
    default_colors = cycle(px.colors.qualitative.Plotly)

    # Crear un mapeo entre tecnologías y colores
    technology_colors = {}
    used_colors = {key.lower(): cycle(colors) for key, colors in COLOR_VARIATIONS.items()}  # Ciclos de colores por clave

    for tech in data[color_column].unique():
        tech_lower = tech.lower()
        matched = False
        # Buscar el color en COLOR_VARIATIONS basado en coincidencias parciales
        for key, color_cycle in used_colors.items():
            if key in tech_lower:  # Coincidencia parcial (ignorando mayúsculas)
                technology_colors[tech] = next(color_cycle)  # Tomar el siguiente color disponible
                matched = True
                break
        if not matched:
            # Si no se encuentra un color, asignar uno por defecto
            technology_colors[tech] = next(default_colors)

    return technology_colors


######################################################
""" Dependencias de los gráficos de las aplicaciones """
######################################################

dependency_keys = {
    "app1": "['REGION','TECHNOLOGY','YEAR']",
    "app2": "['REGION','TECHNOLOGY','FUEL','YEAR']",
    "app4": "['REGION','YEAR']"
}

dependency_key_app1 = "['REGION','TECHNOLOGY','YEAR']"
dependency_key_app2 = "['REGION','TECHNOLOGY','FUEL','YEAR']"
dependency_key_app4 = "['REGION','YEAR']"
dependency_key_app5 = "['REGION','TIMESLICE','TECHNOLOGY','FUEL','YEAR']"

def modify_parameter(pyomo_dict, parameter_name, dataframe_metadata, values, filters=None):
    """
    Modifica un parámetro del modelo Pyomo basado en su configuración en dataframe_metadata.

    Args:
        pyomo_dict (dict): Diccionario del modelo Pyomo.
        parameter_name (str): Nombre del parámetro a modificar (sin el prefijo `p_`).
        dataframe_metadata (dict): Diccionario con la configuración de los parámetros.
        values (dict): Diccionario con los valores a asignar. Las claves deben coincidir con las dimensiones del parámetro.
        filters (dict, opcional): Filtros para limitar las modificaciones (por ejemplo, {"REGION": "Cuba"}).

    Returns:
        None
    """
    # Asegurarse de que el nombre del parámetro tenga el prefijo `p_`
    parameter_name_with_prefix = f"p_{parameter_name}"

    if parameter_name not in dataframe_metadata:
        print(f"El parámetro '{parameter_name}' no está definido en dataframe_metadata.")
        return

    # Obtener las dimensiones del parámetro
    dimensions = dataframe_metadata[parameter_name]["indices"]

    # Iterar sobre las claves del parámetro en el modelo
    if parameter_name_with_prefix in pyomo_dict:
        for key in pyomo_dict[parameter_name_with_prefix]:
            # Crear un diccionario de la clave actual
            key_dict = dict(zip(dimensions, key))

            # Aplicar filtros (si se especifican)
            if filters:
                if not all(key_dict.get(k) == v for k, v in filters.items()):
                    continue

            # Modificar el valor del parámetro
            new_value = values.get(tuple(key_dict[d] for d in dimensions), None)
            if new_value is not None:
                pyomo_dict[parameter_name_with_prefix][key] = new_value
                print(f"Parámetro '{parameter_name_with_prefix}' ajustado a {new_value} para {key}")
    else:
        print(f"El parámetro '{parameter_name_with_prefix}' no se encontró en el modelo.")


