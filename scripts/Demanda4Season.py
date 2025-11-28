# %%
import pandas as pd
import numpy as np
import calendar
# Función para mapear meses a estaciones usando un diccionario
def map_seasons(data, season_mapping):
    def get_season(month):
        for season, months in season_mapping.items():
            if month in months:
                return season
        return "Unknown"
    data['Season'] = data['Month'].apply(get_season)
    return data

# Función para definir los días tipo
def map_daytypes(data, daytype_mapping):
    def get_daytype(day_of_week):
        for daytype, days in daytype_mapping.items():
            if day_of_week in days:
                return daytype
        return "Unknown"
    data['DayType'] = data['Date'].dt.dayofweek.apply(get_daytype)
    return data

# Función para definir los bloques horarios
def map_daylight_brackets(data, bracket_mapping):
    def get_bracket(hour):
        for bracket, hours in bracket_mapping.items():
            if hour in hours:
                return bracket
        return "Unknown"
    data['DaylyTimeBracket'] = data['Hour'].apply(get_bracket)
    return data

# Función para calcular los timeslices
def calculate_timeslices(seasons, daytypes, brackets):
    timeslices = []
    for season in seasons:
        for daytype in daytypes:
            for bracket in brackets:
                timeslices.append(f"{season}_{daytype}_{bracket}")
    return timeslices

# Función para calcular el promedio de factores de capacidad
def calculate_capacity_factor(data, cf_data):
    # Identificar columnas que contienen "Node" en su nombre
    node_columns = [col for col in cf_data.columns if "Node" in col]

    # Verificar que se encontraron columnas de nodos
    if not node_columns:
        raise ValueError("No se encontraron columnas con 'Node' en el nombre en los datos de factor de capacidad.")

    # Calcular el promedio de los factores de capacidad entre los nodos
    cf_data['Average_CF'] = cf_data[node_columns].mean(axis=1)

    # Agregar el promedio al DataFrame principal
    data['Average_CF'] = cf_data['Average_CF']

    return data

# Función para calcular los factores de capacidad ajustados a los timeslices
def calculate_cf_timeslices(data):
    # Agrupar por timeslices y calcular el promedio del factor de capacidad
    grouped = data.groupby(['Season', 'DayType', 'DaylyTimeBracket'])
    cf_timeslices = grouped['Average_CF'].mean().reset_index()

    # Agregar los timeslices como columna
    cf_timeslices['Timeslice'] = cf_timeslices['Season']+cf_timeslices['DayType']+cf_timeslices['DaylyTimeBracket']
    return cf_timeslices
def transform_to_hourly(results, bracket_mapping, daytype_mapping, season_mapping):
    # Crear un DataFrame vacío para almacenar los resultados horarios
    hourly_results = []

    # Iterar sobre cada fila de los resultados por timeslice
    for _, row in results.iterrows():
        region = row['REGION']
        timeslice = row['TIMESLICE']
        fuel = row['FUEL']
        year = row['YEAR']
        value = row['value']

        # Determinar las horas correspondientes al bloque horario (bracket_mapping)
        hours = bracket_mapping[timeslice]

        # Calcular el valor por hora
        hourly_value = value / len(hours)

        # Generar las filas horarias
        for hour in hours:
            hourly_results.append({
                'REGION': region,
                'FUEL': fuel,
                'YEAR': year,
                'HOUR': hour,
                'VALUE': hourly_value
            })

    # Convertir la lista de resultados horarios en un DataFrame
    hourly_results_df = pd.DataFrame(hourly_results)

    return hourly_results_df

def calculate_yearsplit(season_mapping, daytype_mapping, bracket_mapping, year):
    # Total de horas en un año
    total_hours = 8760

    # Crear un DataFrame para almacenar los resultados
    yearsplit = []

    # Iterar sobre cada estación
    for season, months in season_mapping.items():
        # Calcular la duración de la estación en horas usando días exactos
        season_hours = sum(calendar.monthrange(year, month)[1] * 24 for month in months)

        # Iterar sobre cada día tipo
        for daytype, days in daytype_mapping.items():
            daytype_hours = season_hours / len(daytype_mapping)  # Dividir entre los días tipo

            # Iterar sobre cada bloque horario
            for bracket, hours in bracket_mapping.items():
                bracket_hours = len(hours) * daytype_hours / 24  # Dividir entre las 24 horas del día
                fraction = bracket_hours / total_hours

                # Agregar el resultado al DataFrame
                yearsplit.append({
                    'Season': season,
                    'DayType': daytype,
                    'Bracket': bracket,
                    'YearSplit': fraction
                })

    # Convertir a DataFrame
    yearsplit_df = pd.DataFrame(yearsplit)

    # Normalizar los valores para que la suma sea exactamente 1
    yearsplit_df['YearSplit'] = yearsplit_df['YearSplit'] / yearsplit_df['YearSplit'].sum()

    return yearsplit_df

def calculate_specified_demand_profile(data):
    # Agrupar la demanda total por Season, DayType y DaylyTimeBracket
    grouped_demand = data.groupby(['Season', 'DayType', 'DaylyTimeBracket'])['Total'].sum().reset_index()

    # Calcular la fracción de la demanda total
    total_demand = grouped_demand['Total'].sum()
    grouped_demand['SpecifiedDemandProfile'] = grouped_demand['Total'] / total_demand

    return grouped_demand[['Season', 'DayType', 'DaylyTimeBracket', 'SpecifiedDemandProfile']]

def calculate_daysplit(bracket_mapping, year):
    """
    Calcula el DaySplit para cada bloque horario como la fracción del año.
    """
    total_hours_in_year = 8760  # Total de horas en un año (365 días * 24 horas)
    days_in_year = 365  # Número de días en un año no bisiesto
    day_split = []

    for bracket, hours in bracket_mapping.items():
        # Calcular la duración del bloque horario en horas
        bracket_hours = len(hours)
        # Calcular DaySplit como fracción del año
        day_split_fraction = (bracket_hours / 24) / days_in_year
        day_split.append({
            'Bracket': bracket,
            'DaySplit': day_split_fraction
        })

    # Convertir a DataFrame
    day_split_df = pd.DataFrame(day_split)
    return day_split_df

def round_and_adjust(df, column_name):
    """
    Redondea los valores de una columna a dos decimales y ajusta el último valor
    para garantizar que la suma sea exactamente 1.

    Args:
        df (pd.DataFrame): DataFrame que contiene los datos.
        column_name (str): Nombre de la columna a redondear y ajustar.

    Returns:
        pd.DataFrame: DataFrame con los valores ajustados.
    """
    # Redondear todos los valores a dos decimales
    df[column_name] = df[column_name].round(3)

    # Calcular la diferencia para ajustar
    diff = 1.0 - df[column_name].sum()

    # Ajustar el último valor para que la suma sea exactamente 1
    if abs(diff) > 1e-6:  # Evitar ajustes innecesarios por errores numéricos muy pequeños
        df.loc[df.index[-1], column_name] += diff

    return df

# Main script
if __name__ == "__main__":
    # Leer datos
    year = 2023
    data = pd.read_excel('/home/david/Documents/001 - Proyectos/CubaOSeMOSYS/DatosCub.xlsx', sheet_name="DEMAND")
    cfwind = pd.read_excel('/home/david/Documents/001 - Proyectos/CubaOSeMOSYS/DatosCub.xlsx', sheet_name="CFWIND")
    cfpv = pd.read_excel('/home/david/Documents/001 - Proyectos/CubaOSeMOSYS/DatosCub.xlsx', sheet_name="CFSOL")
    # cfpv = cfpv['Average'].astype(float)
    # print(cfpv)
    data['Total'] =data.loc[:,'Node1':].sum(axis=1)

    if 'Date' not in data.columns:
        print("La columna 'Date' no existe. Creando un rango de fechas automáticamente...")
        start_date = f'{year}-01-01'
        end_date = f'{year}-12-31 23:00:00'
        date_range = pd.date_range(start=start_date, end=end_date, freq='h')
        data['Date'] = date_range
        # print(data)

    ##############################################################################
    # Configuración de las estaciones, días tipo y bloques horarios
    ################################################################################
    # Configuración del modelo
    # season_mapping = {
    #     "Winter": [12, 1, 2],
    #     "Spring": [3, 4, 5],
    #     "Summer": [6, 7, 8],
    #     "Autumn": [9, 10, 11]
    # }
    # daytype_mapping = {
    #     "Workday": [0, 1, 2, 3, 4],
    #     "Weekend": [5, 6]
    # }
    # bracket_mapping = {
    #     "Night": list(range(0, 6)),
    #     "Morning": list(range(6, 12)),
    #     "Afternoon": list(range(12, 18)),
    #     "Evening": list(range(18, 24))
    # }
    #  Configuración para simular cada día de la semana por separado
    # daytype_mapping = {
    #     "Monday": [0],
    #     "Tuesday": [1],
    #     "Wednesday": [2],
    #     "Thursday": [3],
    #     "Friday": [4],
    #     "Saturday": [5],
    #     "Sunday": [6]
    # }

    # Configuración para 1 estación, 1 tipo de día y 2 bloques horarios dia y noche   
    # season_mapping = {
    #     "": list(range(1, 13))  # Todos los meses pertenecen a la misma estación
    # }
    # daytype_mapping = {
    #     "": list(range(0, 7)) # Todos los días pertenecen al mismo tipo
    # }
    # bracket_mapping = {
    #     "Night": list(range(0, 6)) + list(range(18, 24)),  # De 00:00 a 06:00 y de 18:00 a 24:00
    #     "Day": list(range(6, 18))  # De 06:00 a 18:00
    # }
    season_mapping = {
    "1": [12, 1, 2],  # Invierno
    "2": [3, 4, 5],   # Primavera
    "3": [6, 7, 8],   # Verano
    "4": [9, 10, 11]  # Otoño
    }

    daytype_mapping = {
        "1": [0, 1, 2, 3, 4],  # Workdays (lunes a viernes)
        "2": [5, 6]            # Weekends (sábado y domingo)
    }

    bracket_mapping = {
        "1": list(range(20, 24)) + list(range(0, 1)),
        "2": list(range(1, 6)),
        "3": list(range(6, 8)),
        "4": list(range(8, 11)),
        "5": list(range(11, 13)),
        "6": list(range(13, 16)),
        "7": list(range(16, 18)),
        "8": list(range(18, 20))
    }




    # Preprocesar datos
    data['Month'] = data['Date'].dt.month
    data['Hour'] = data['Date'].dt.hour
    # data['Weekend'] = data['Date'].dt.dayofweek >= 5

    # Mapear estaciones, días tipo y bloques horarios
    data = map_seasons(data, season_mapping)
    data = map_daytypes(data, daytype_mapping)
    data = map_daylight_brackets(data, bracket_mapping)
    

    # Calcular factores de capacidad para solar
    data = calculate_capacity_factor(data, cfpv)

    # Calcular factores de capacidad ajustados a los timeslices para solar
    cf_timeslices_pv = calculate_cf_timeslices(data)

    # Calcular factores de capacidad para viento
    data = calculate_capacity_factor(data, cfwind)

    # Calcular factores de capacidad ajustados a los timeslices para viento
    cf_timeslices_wind = calculate_cf_timeslices(data)

    # Calcular YearSplit
    yearsplit = calculate_yearsplit(season_mapping, daytype_mapping, bracket_mapping, year)


    # Calcular Specified Demand Profile
    specified_demand_profile = calculate_specified_demand_profile(data)

    daysplit = calculate_daysplit(bracket_mapping, year)

    # Calcular timeslices
    # timeslices = calculate_timeslices(
    #     seasons=season_mapping.keys(),
    #     daytypes=daytype_mapping.values(),
    #     brackets=bracket_mapping.keys()
    # )

    # Normalizar datos horarios
    total_sum = data['Total'].sum()
    normalized_hourly_sum = data.groupby(['Season', 'DayType', 'DaylyTimeBracket'])['Total'].sum() / total_sum

    # Redondear los valores a dos decimales antes de exportar
    cf_timeslices_pv['Average_CF'] = cf_timeslices_pv['Average_CF'].round(3)
    cf_timeslices_wind['Average_CF'] = cf_timeslices_wind['Average_CF'].round(3)
    yearsplit = round_and_adjust(yearsplit, "YearSplit")
    specified_demand_profile['SpecifiedDemandProfile'] = specified_demand_profile['SpecifiedDemandProfile'].round(3)
    data = data.round(3) 


    # Exportar resultados
    with pd.ExcelWriter('output4.xlsx') as writer:
        # pd.DataFrame({'Timeslices': timeslices}).to_excel(writer, sheet_name='Timeslices', index=False)
        # normalized_hourly_sum.reset_index(name='Value').to_excel(writer, sheet_name='Normalized', index=False)
        # cf_timeslices.to_excel(writer, sheet_name='CFPV', index=True)
    # with pd.ExcelWriter('output4.xlsx') as writer:
        cf_timeslices_pv[['Timeslice', 'Average_CF']].to_excel(writer, sheet_name='CFPV', index=False)
        cf_timeslices_wind[['Timeslice', 'Average_CF']].to_excel(writer, sheet_name='CFWIND', index=False)
        yearsplit.to_excel(writer, sheet_name='YearSplit', index=False)
        specified_demand_profile.to_excel(writer, sheet_name='SpecifiedDemandProfile', index=False)
        data.to_excel(writer, sheet_name='DemandData', index=False)
        daysplit.to_excel(writer, sheet_name='DaySplit', index=False)
    


    

