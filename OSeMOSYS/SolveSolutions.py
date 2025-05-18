#%%
import os, sys
root_folder = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(root_folder)
import json
import pandas as pd
from pyomo.environ import value, Var, AbstractModel, DataPortal
from pyomo.opt import SolverFactory
from itertools import count
from OSeMOSYS.MainModel import define_model
# from OSeMOSYS.config import INPUT_FILE_PATH, DATA_FILE_PATH, RESULTS_FOLDER
from OSeMOSYS.readXlsData import generate_output_path
import plotly.express as px
import matplotlib.pyplot as plt
#%%
# from vincent.colors import brews

def solve_model(input_file, solver_name ,  json_file_path_or_dict, solver_options=None, tee=True):
    """
    Resuelve el modelo Pyomo utilizando el archivo JSON de entrada.

    Args:
        input_file (str): Ruta al archivo de entrada.
        solver_name (str): Nombre del solver a utilizar (por ejemplo, "gurobi", "cbc").
        json_file_path (str): Ruta al archivo JSON generado.
        solver_options (dict, optional): Opciones específicas para el solver.
        tee (bool, optional): Mostrar la salida del solver en la consola.

    Returns:
        instance: Instancia del modelo resuelto.
    """
    print("Definiendo el modelo...")
    model = define_model(input_file)

    print("Creando la instancia del modelo...")
    if isinstance(json_file_path_or_dict, dict):
        # Si es un diccionario, usarlo directamente
        instance = model.create_instance(json_file_path_or_dict)
    elif isinstance(json_file_path_or_dict, str):
        # Si es una ruta, cargar los datos desde el archivo JSON
        instance = model.create_instance(json_file_path_or_dict)
    else:
        raise ValueError("El argumento 'json_file_path_or_dict' debe ser una ruta (str) o un diccionario (dict).")

    print("Resolviendo el modelo...")
    solver = SolverFactory(solver_name)  # Cambia "gurobi" por el solver que estés usando
    if solver_options:
        for option, value in solver_options.items():
            solver.options[option] = value


    results = solver.solve(instance, tee=True)

    print(f"Estado de la solución: {results.solver.status}")
    print(f"Resultado de la solución: {results.solver.termination_condition}")

    return instance


def export_results(instance, results_folder):
    """
    Exporta las soluciones del modelo a archivos CSV.

    Args:
        instance: Instancia del modelo resuelto.
        results_folder (str): Carpeta donde se guardarán los archivos CSV.
    """
    print("Exportando soluciones a archivos CSV...")
    os.makedirs(results_folder, exist_ok=True)

    for var in instance.component_objects(Var, active=True):
        var_name = var.name.lstrip("v_")  # Quitar el prefijo "v_"
        var_data = []

        # Verificar si la variable tiene índices
        if var.is_indexed():
            for index in var:
                value_ = var[index].value
                if value_ is not None:  # Ignorar valores no definidos
                    # Si el índice es una tupla, descomponerlo; si no, usarlo directamente
                    if isinstance(index, tuple):
                        var_data.append((*index, value_))
                    else:
                        var_data.append((index, value_))
        else:
            # Variable escalar (sin índices)
            value_ = var.value
            if value_ is not None:
                var_data.append((value_,))

        # Crear un DataFrame para la variable
        if var_data:
            # Determinar las columnas del DataFrame
            if var.is_indexed():
                if isinstance(next(iter(var.index_set())), tuple):
                    columns = list(var.index_set().set_tuple) + ["value"]
                else:
                    columns = ["index", "value"]
            else:
                columns = ["value"]

            df = pd.DataFrame(var_data, columns=columns)

            # Guardar el DataFrame en un archivo CSV
            output_file = os.path.join(results_folder, f"{var_name}.csv")
            df.to_csv(output_file, index=False)
            print(f"Solución guardada: {output_file}")
def get_variable_dependencies(instance):
    """
    Determina los conjuntos de los que depende cada variable en el modelo.

    Args:
        instance: Instancia del modelo Pyomo.

    Returns:
        dict: Un diccionario donde las claves son los nombres de las variables
              y los valores son listas de conjuntos de los que dependen.
    """
    dependencies = {}

    for var in instance.component_objects(Var, active=True):
        var_name = var.name.lstrip("v_")  # Quitar el prefijo "v_"
        index_set = var.index_set()

        # Si la variable no está indexada
        if not var.is_indexed():
            dependencies[var_name] = []
        else:
            # Obtener los conjuntos individuales del índice
            if isinstance(index_set, tuple):
                dependencies[var_name] = [str(s) for s in index_set]
            else:
                dependencies[var_name] = [str(index_set)]

    return dependencies
# def plot_grouped_variables(instance, dependencies, target_dependency, title):
#     """
#     Genera gráficos de barras apiladas para variables con dependencias específicas.

#     Args:
#         instance: Instancia del modelo Pyomo.
#         dependencies (dict): Diccionario con las dependencias de las variables.
#         target_dependency (list): Dependencias objetivo para agrupar las variables.
#         title (str): Título del gráfico.
#     """
#     # Filtrar variables con las dependencias objetivo
#     target_vars = [var for var, deps in dependencies.items() if deps == target_dependency]

#     if not target_vars:
#         print(f"No se encontraron variables con dependencias {target_dependency}.")
#         return

#     # Crear un DataFrame para almacenar los datos de todas las variables
#     combined_data = []

#     for var_name in target_vars:
#         var = getattr(instance, f"v_{var_name}", None)
#         if var is None:
#             print(f"Variable {var_name} no encontrada en la instancia.")
#             continue

#         # Extraer datos de la variable
#         for index in var:
#             value_ = var[index].value
#             if value_ is not None:
#                 combined_data.append((*index, var_name, value_))

#     # Crear un DataFrame con los datos combinados
#     columns = target_dependency + ["variable", "value"]
#     df = pd.DataFrame(combined_data, columns=columns)

#     # Crear el gráfico de barras apiladas
#     fig = px.bar(
#         df,
#         x="YEAR",
#         y="value",
#         color="TECHNOLOGY",
#         facet_col="REGION",
#         title=title,
#         labels={"value": "Valor", "YEAR": "Año", "TECHNOLOGY": "Tecnología"},
#     )
#     fig.update_layout(barmode="stack")
#     fig.show()
def area(instance, formatted_dependencies, target_dependency):
    """
    Genera un gráfico interactivo con dos menús desplegables: uno para seleccionar variables y otro para tipos de gráficos.

    Args:
        instance: Instancia del modelo Pyomo.
        formatted_dependencies (dict): Diccionario con dependencias formateadas y variables asociadas.
        target_dependency (str): Dependencia objetivo en formato formateado (e.g., "['REGION','TECHNOLOGY','FUEL','YEAR']").
    """
    # Verificar si la dependencia objetivo existe en el diccionario
    if target_dependency not in formatted_dependencies:
        print(f"No se encontraron variables con la dependencia {target_dependency}.")
        return

    # Obtener las variables asociadas a la dependencia
    target_vars = formatted_dependencies[target_dependency]

    # Crear un DataFrame para almacenar los datos de todas las variables
    combined_data = []

    for var_name in target_vars:
        var = getattr(instance, f"v_{var_name}", None)
        if var is None:
            print(f"Variable {var_name} no encontrada en la instancia.")
            continue

        # Extraer datos de la variable
        for index in var:
            value_ = var[index].value
            if value_ is not None:
                combined_data.append((*index, var_name, value_))

    # Dividir la dependencia en columnas
    dependency_columns = target_dependency.strip("[]").replace("'", "").split(",")
    columns = dependency_columns + ["variable", "value"]

    # Crear el DataFrame
    df = pd.DataFrame(combined_data, columns=columns)

    # Depuración: imprimir el DataFrame
    print("Contenido del DataFrame:")
    print(df)

    # Pivotar los datos para apilar correctamente las áreas
    pivot_data = df.pivot_table(
        index="YEAR", columns="TECHNOLOGY", values="value", aggfunc="sum"
    ).fillna(0)

    # Convertir los datos pivotados de nuevo a un formato largo para Plotly
    stacked_data = pivot_data.reset_index().melt(id_vars=["YEAR"], var_name="TECHNOLOGY", value_name="value")

    # Crear el gráfico de área apilada
    fig = px.area(
        stacked_data,
        x="YEAR",
        y="value",
        color="TECHNOLOGY",
        labels={"value": "Valor", "YEAR": "Año", "TECHNOLOGY": "Tecnología"},
        title=f"Gráfico de área apilada para {target_dependency}",
    )

    # Mostrar el gráfico
    fig.show()
  

import matplotlib.pyplot as plt

def plot_variables_with_matplotlib(instance, formatted_dependencies, target_dependency):
    """
    Genera gráficos de barras apiladas y áreas apiladas utilizando Matplotlib.

    Args:
        instance: Instancia del modelo Pyomo.
        formatted_dependencies (dict): Diccionario con dependencias formateadas y variables asociadas.
        target_dependency (str): Dependencia objetivo en formato formateado (e.g., "['REGION','TECHNOLOGY','FUEL','YEAR']").
    """
    # Verificar si la dependencia objetivo existe en el diccionario
    if target_dependency not in formatted_dependencies:
        print(f"No se encontraron variables con la dependencia {target_dependency}.")
        return

    # Obtener las variables asociadas a la dependencia
    target_vars = formatted_dependencies[target_dependency]

    # Crear un DataFrame para almacenar los datos de todas las variables
    combined_data = []

    for var_name in target_vars:
        var = getattr(instance, f"v_{var_name}", None)
        if var is None:
            print(f"Variable {var_name} no encontrada en la instancia.")
            continue

        # Extraer datos de la variable
        for index in var:
            value_ = var[index].value
            if value_ is not None:
                combined_data.append((*index, var_name, value_))

    # Dividir la dependencia en columnas
    dependency_columns = target_dependency.strip("[]").replace("'", "").split(",")
    columns = dependency_columns + ["variable", "value"]

    # Crear el DataFrame
    df = pd.DataFrame(combined_data, columns=columns)

    # Depuración: imprimir el DataFrame
    print("Contenido del DataFrame:")
    print(df)

    # Crear un gráfico de área apilada para cada región
    for region in df["REGION"].unique():
        region_data = df[df["REGION"] == region]

        # Pivotar los datos para que las tecnologías sean columnas
        pivot_data = region_data.pivot_table(
            index="YEAR", columns="TECHNOLOGY", values="value", aggfunc="sum"
        ).fillna(0)

        # Crear el gráfico de área apilada
        pivot_data.plot.area(figsize=(10, 6), alpha=0.7)
        plt.title(f"Área apilada para la región: {region}")
        plt.xlabel("Año")
        plt.ylabel("Valor")
        plt.legend(title="Tecnología", bbox_to_anchor=(1.05, 1), loc="upper left")
        plt.tight_layout()
        plt.show()

    # Crear un gráfico de barras apiladas para cada región
    for region in df["REGION"].unique():
        region_data = df[df["REGION"] == region]

        # Pivotar los datos para que las tecnologías sean columnas
        pivot_data = region_data.pivot_table(
            index="YEAR", columns="TECHNOLOGY", values="value", aggfunc="sum"
        ).fillna(0)

        # Crear el gráfico de barras apiladas
        pivot_data.plot(kind="bar", stacked=True, figsize=(10, 6), alpha=0.7)
        plt.title(f"Barras apiladas para la región: {region}")
        plt.xlabel("Año")
        plt.ylabel("Valor")
        plt.legend(title="Tecnología", bbox_to_anchor=(1.05, 1), loc="upper left")
        plt.tight_layout()
        plt.show()

def generate_dependency_dict(variable_dependencies):
    """
    Genera un diccionario estructurado donde las claves son las dependencias formateadas
    y los valores son listas de variables que tienen esa dependencia.

    Args:
        variable_dependencies (dict): Diccionario con las variables y sus dependencias en formato original.

    Returns:
        dict: Diccionario estructurado con dependencias formateadas como claves y listas de variables como valores.
    """
    formatted_dependencies = {}

    for variable, dependency_list in variable_dependencies.items():
        # Formatear la dependencia (reemplazar '*' por ',' y envolver cada elemento entre comillas simples)
        for dependency in dependency_list:
            formatted_dependency = "['" + dependency.replace("*", "','") + "']"

            # Agregar la variable al diccionario estructurado
            if formatted_dependency not in formatted_dependencies:
                formatted_dependencies[formatted_dependency] = []
            formatted_dependencies[formatted_dependency].append(variable)

    return formatted_dependencies




if __name__ == "__main__":
    # Configuración de rutas
    input_file = '/home/david/OSeMOSYS-pyomo/data/Antiguos/SuperSimple.xlsx'

    json_file_path = generate_output_path(input_file_path=input_file)
    solver_name = "gurobi"  # Cambia esto al nombre del solver que estés usando
    solver_options = {"TimeLimit": 600, "MIPGap": 0.01}  # Opciones del solver (ver qué opciones son válidas para tu solver)

    try:
        instance = solve_model(
            input_file=input_file,
            solver_name=solver_name,
            json_file_path_or_dict=json_file_path,
            solver_options=solver_options,
            tee=True
        )
        print("Modelo resuelto con éxito.")

        export_results(instance, RESULTS_FOLDER)
        dependencies = get_variable_dependencies(instance)
        target_dependency = "['REGION','TECHNOLOGY','FUEL','YEAR']"
        # target_dependency =  ['REGION','TECHNOLOGY','FUEL','YEAR']

        # plot_grouped_variables(instance, dependencies, target_dependency, "Producción Anual por Tecnología")
        formatted_dependencies = generate_dependency_dict(dependencies)
        with open(json_file_path, 'w') as json_file:
            json.dump(formatted_dependencies, json_file, indent=4)
        # print("Dependencias formateadas:")
        # formatted_dependencies.to_json(json_file_path, indent=4)



        # plot_variables_with_matplotlib(instance, formatted_dependencies, target_dependency)          
        # plot_variables_with_dropdown(instance, formatted_dependencies, target_dependency)
    except Exception as e:
        print(f"Error al resolver el modelo: {e}")

# Ejemplo de uso


# from readXlsData import read_excel

# from highspy import *






# def solve_model(input_file,results_folder):

#     # ParamDict, OsemosysDict = read_excel(input_file,results_folder=results_folder)

#     #define the model with default values:
#     model = define_model(input_file)

#     # TODO: use the OsemosysDIct directly instead of passing through the json file
#     instance = model.create_instance('../data/Data.json')
#     # instance.EBa11_EnergyBalanceEachTS5.pprint()
#     # instance.Must_Run.pprint()
#     # instance.SpecifiedDemand_EQ.pprint()
#     # instance.EBa9_EnergyBalanceEachTS3.pprint()
#     # instance.EBa11_EnergyBalanceEachTS5.pprint()
#     #%%
#     "Solvers used - cbc, ***scip*** or highs"
#     #opt = SolverFactory("appsi_highs")
#     #opt = SolverFactory("scip", tempdir = new_folder_path)
#     # cbc_path = "C:/Program Files (x86)/COIN-OR/1.7.4/win32-msvc15/bin/cbc.exe"
#     # opt = SolverFactory('cbc', executable=cbc_path)
#     opt = SolverFactory("gurobi")
#     #%%
#     # opt.solve(instance)
#     results = opt.solve(instance)
#     results.write()

#     # %%
#     # import numpy as np
#     # import plotly.express as px
#     # from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
#     # instance.solutions.load_from(results)
#     column_map = {
#             # Variables with ['REGION', 'TECHNOLOGY', 'YEAR'] set
#             'v_NumberOfNewTechnologyUnits': ['REGION', 'TECHNOLOGY', 'YEAR', 'value'],
#             'v_NewCapacity': ['REGION', 'TECHNOLOGY', 'YEAR', 'value'],
#             'v_AccumulatedNewCapacity': ['REGION', 'TECHNOLOGY', 'YEAR', 'value'],
#             'v_TotalCapacityAnnual': ['REGION', 'TECHNOLOGY', 'YEAR', 'value'],
#             'v_CapitalInvestment': ['REGION', 'TECHNOLOGY', 'YEAR', 'value'],
#             'v_DiscountedCapitalInvestment': ['REGION', 'TECHNOLOGY', 'YEAR', 'value'],
#             'v_SalvageValue': ['REGION', 'TECHNOLOGY', 'YEAR', 'value'],
#             'v_DiscountedSalvageValue': ['REGION', 'TECHNOLOGY', 'YEAR', 'value'],
#             'v_OperatingCost': ['REGION', 'TECHNOLOGY', 'YEAR', 'value'],
#             'v_DiscountedOperatingCost': ['REGION', 'TECHNOLOGY', 'YEAR', 'value'],
#             'v_AnnualVariableOperatingCost': ['REGION', 'TECHNOLOGY', 'YEAR', 'value'],
#             'v_AnnualFixedOperatingCost': ['REGION', 'TECHNOLOGY', 'YEAR', 'value'],
#             'v_TotalDiscountedCostByTechnology': ['REGION', 'TECHNOLOGY', 'YEAR', 'value'],
#             'v_TotalTechnologyAnnualActivity': ['REGION', 'TECHNOLOGY', 'YEAR', 'value'],
#             'v_AnnualTechnologyEmissionsPenalty': ['REGION', 'TECHNOLOGY', 'YEAR', 'value'],
#             'v_DiscountedTechnologyEmissionsPenalty': ['REGION', 'TECHNOLOGY', 'YEAR', 'value'],
#             'v_NumeroUnidadesRecuperadas': ['REGION', 'TECHNOLOGY', 'YEAR', 'value'],
#             'v_ResidualCapacity': ['REGION', 'TECHNOLOGY', 'YEAR', 'value'],
#             'v_Abandono':['REGION', 'TECHNOLOGY', 'TIMESLICE', 'YEAR', 'value'],
#             'v_Cubrimiento':['REGION', 'TECHNOLOGY', 'TIMESLICE', 'YEAR', 'value'],
#             'v_RecoveredExistingUnits':['REGION', 'TECHNOLOGY',  'YEAR', 'value'],
#             'v_AccumulatedRecoveredUnits':['REGION', 'TECHNOLOGY',  'YEAR', 'value'],
#             'v_AccumulatedRecoveredCapacity':['REGION', 'TECHNOLOGY',  'YEAR', 'value'],
#             'v_RecoveredCapacity':['REGION', 'TECHNOLOGY',  'YEAR', 'value'],
#             # Variables with ['REGION', 'TIMESLICE', 'FUEL', 'YEAR'] set
#             'v_RateOfProduction': ['REGION', 'TIMESLICE', 'FUEL', 'YEAR', 'value'],
#             'v_RateOfDemand': ['REGION', 'TIMESLICE', 'FUEL', 'YEAR', 'value'],
#             'v_Demand': ['REGION', 'TIMESLICE', 'FUEL', 'YEAR', 'value'],
#             'v_Production': ['REGION', 'TIMESLICE', 'FUEL', 'YEAR', 'value'],
#             'v_RateOfUse': ['REGION', 'TIMESLICE', 'FUEL', 'YEAR', 'value'],
#             'v_Use': ['REGION', 'TIMESLICE', 'FUEL', 'YEAR', 'value'],
#             'v_ConnectedUnits': ['REGION', 'TECHNOLOGY', 'SEASON', 'YEAR', 'value'],
#             'v_Export': ['REGION', 'TIMESLICE', 'FUEL', 'YEAR', 'value'],

#             # Variables with ['REGION', 'STORAGE', 'SEASON', 'DAYTYPE', 'DAILYTIMEBRACKET', 'YEAR'] set
#             'v_RateOfStorageCharge': ['REGION', 'STORAGE', 'SEASON', 'DAYTYPE', 'DAILYTIMEBRACKET', 'YEAR', 'value'],
#             'v_RateOfStorageDischarge': ['REGION', 'STORAGE', 'SEASON', 'DAYTYPE', 'DAILYTIMEBRACKET', 'YEAR', 'value'],
#             'v_NetChargeWithinYear': ['REGION', 'STORAGE', 'SEASON', 'DAYTYPE', 'DAILYTIMEBRACKET', 'YEAR', 'value'],
#             'v_NetChargeWithinDay': ['REGION', 'STORAGE', 'SEASON', 'DAYTYPE', 'DAILYTIMEBRACKET', 'YEAR', 'value'],
#             'v_StorageLevel' : ['REGION', 'STORAGE', 'SEASON', 'DAYTYPE', 'DAILYTIMEBRACKET', 'YEAR', 'value'],

#             # Variables with ['REGION', 'STORAGE', 'YEAR'] set
#             'v_StorageLevelYearStart': ['REGION', 'STORAGE', 'YEAR', 'value'],
#             'v_StorageLevelYearFinish': ['REGION', 'STORAGE', 'YEAR', 'value'],
#             'v_StorageLowerLimit': ['REGION', 'STORAGE', 'YEAR', 'value'],
#             'v_StorageUpperLimit': ['REGION', 'STORAGE', 'YEAR', 'value'],
#             'v_AccumulatedNewStorageCapacity': ['REGION', 'STORAGE', 'YEAR', 'value'],
#             'v_NewStorageCapacity': ['REGION', 'STORAGE', 'YEAR', 'value'],
#             'v_CapitalInvestmentStorage': ['REGION', 'STORAGE', 'YEAR', 'value'],
#             'v_DiscountedCapitalInvestmentStorage': ['REGION', 'STORAGE', 'YEAR', 'value'],
#             'v_SalvageValueStorage': ['REGION', 'STORAGE', 'YEAR', 'value'],
#             'v_DiscountedSalvageValueStorage': ['REGION', 'STORAGE', 'YEAR', 'value'],
#             'v_TotalDiscountedStorageCost': ['REGION', 'STORAGE', 'YEAR', 'value'],

#             # Variables with ['REGION', 'STORAGE', 'SEASON', 'YEAR'] set
#             'v_StorageLevelSeasonStart': ['REGION', 'STORAGE', 'SEASON', 'YEAR', 'value'],

#             # Variables with ['REGION', 'STORAGE', 'SEASON', 'DAYTYPE', 'YEAR'] set
#             'v_StorageLevelDayTypeStart': ['REGION', 'STORAGE', 'SEASON', 'DAYTYPE', 'YEAR', 'value'],
#             'v_StorageLevelDayTypeFinish': ['REGION', 'STORAGE', 'SEASON', 'DAYTYPE', 'YEAR', 'value'],
                      
#             # Variables with ['REGION', 'TIMESLICE', 'TECHNOLOGY', 'MODE_OF_OPERATION', 'YEAR'] set
#             'v_RateOfActivity': ['REGION', 'TIMESLICE', 'TECHNOLOGY', 'MODE_OF_OPERATION', 'YEAR', 'value'],

#             # Variables with ['REGION', 'TECHNOLOGY', 'TIMESLICE', 'YEAR'] set
#             'v_RateOfTotalActivity': ['REGION', 'TECHNOLOGY', 'TIMESLICE', 'YEAR', 'value'],

#             # Variables with ['REGION', 'TECHNOLOGY', 'MODE_OF_OPERATION', 'YEAR'] set
#             'v_TotalAnnualTechnologyActivityByMode': ['REGION', 'TECHNOLOGY', 'MODE_OF_OPERATION', 'YEAR', 'value'],

#             # Variables with ['REGION', 'TECHNOLOGY'] set
#             'v_TotalTechnologyModelPeriodActivity': ['REGION', 'TECHNOLOGY', 'value'],

#             # Variables with ['REGION', 'TIMESLICE', 'TECHNOLOGY', 'MODE_OF_OPERATION', 'FUEL', 'YEAR'] set
#             'v_RateOfProductionByTechnologyByMode': ['REGION', 'TIMESLICE', 'TECHNOLOGY', 'MODE_OF_OPERATION', 'FUEL', 'YEAR', 'value'],
#             'v_RateOfUseByTechnologyByMode': ['REGION', 'TIMESLICE', 'TECHNOLOGY', 'MODE_OF_OPERATION', 'FUEL', 'YEAR', 'value'],

#             # Variables with ['REGION', 'TIMESLICE', 'TECHNOLOGY', 'FUEL', 'YEAR'] set
#             'v_RateOfProductionByTechnology': ['REGION', 'TIMESLICE', 'TECHNOLOGY', 'FUEL', 'YEAR', 'value'],
#             'v_ProductionByTechnology': ['REGION', 'TIMESLICE', 'TECHNOLOGY', 'FUEL', 'YEAR', 'value'],
#             'v_RateOfUseByTechnology': ['REGION', 'TIMESLICE', 'TECHNOLOGY', 'FUEL', 'YEAR', 'value'],
#             'v_UseByTechnology': ['REGION', 'TIMESLICE', 'TECHNOLOGY', 'FUEL', 'YEAR', 'value'],

#             # Variables with ['REGION', 'TECHNOLOGY', 'FUEL', 'YEAR'] set
#             'v_ProductionByTechnologyAnnual': ['REGION', 'TECHNOLOGY', 'FUEL', 'YEAR', 'value'],
#             'v_UseByTechnologyAnnual': ['REGION', 'TECHNOLOGY', 'FUEL', 'YEAR', 'value'],

#             # Variables with ['REGION', 'REGION', 'TIMESLICE', 'FUEL', 'YEAR'] set
#             'v_Trade': ['REGION', 'REGION', 'TIMESLICE', 'FUEL', 'YEAR', 'value'],

#             # Variables with ['REGION', 'REGION', 'FUEL', 'YEAR'] set
#             'v_TradeAnnual': ['REGION', 'REGION', 'FUEL', 'YEAR', 'value'],

#             # Variables with ['REGION', 'FUEL', 'YEAR'] set
#             'v_ProductionAnnual': ['REGION', 'FUEL', 'YEAR', 'value'],
#             'v_UseAnnual': ['REGION', 'FUEL', 'YEAR', 'value'],

#             # Variables with ['REGION', 'YEAR'] set
#             'v_TotalDiscountedCost': ['REGION', 'YEAR', 'value'],
#             'v_TotalCapacityInReserveMargin': ['REGION', 'YEAR', 'value'],
#             'v_TotalREProductionAnnual': ['REGION', 'YEAR', 'value'],
#             'v_RETotalProductionOfTargetFuelAnnual': ['REGION', 'YEAR', 'value'],

#             # Variables with ['REGION'] set
#             'v_ModelPeriodCostByRegion': ['REGION', 'value'],

#             # Variables with ['REGION', 'TIMESLICE', 'YEAR'] set
#             'v_DemandNeedingReserveMargin': ['REGION', 'TIMESLICE', 'YEAR', 'value'],

#             # Variables with ['REGION', 'TECHNOLOGY', 'EMISSION', 'MODE_OF_OPERATION', 'YEAR'] set
#             'v_AnnualTechnologyEmissionByMode': ['REGION', 'TECHNOLOGY', 'EMISSION', 'MODE_OF_OPERATION', 'YEAR', 'value'],

#             # Variables with ['REGION', 'TECHNOLOGY', 'EMISSION', 'YEAR'] set
#             'v_AnnualTechnologyEmission': ['REGION', 'TECHNOLOGY', 'EMISSION', 'YEAR', 'value'],
#             'v_AnnualTechnologyEmissionPenaltyByEmission': ['REGION', 'TECHNOLOGY', 'EMISSION', 'YEAR', 'value'],

#             # Variables with ['REGION', 'EMISSION', 'YEAR'] set
#             'v_AnnualEmissions': ['REGION', 'EMISSION', 'YEAR', 'value'],

#             # Variables with ['REGION', 'EMISSION'] set
#             'v_ModelPeriodEmissions': ['REGION', 'EMISSION', 'value'],

#         }
#     def getColumns(var_name):
#         return column_map.get(var_name, [])
#     datas = {}

#     for v in instance.component_objects(Var, active=True):
#         lista = []
#         if v.dim() == 1:
#             for index in v:
#                 x = value(v[index])
#                 lista.append([index, x])
#         else:
#             for index in v:
#                 x = value(v[index])
#                 lista.append([*index, x])
#         try:
#             # Create a DataFrame using the column map for the variable
#             df = pd.DataFrame(lista, columns=getColumns(str(v)))
#             print(v)

#             # Export the DataFrame to a CSV file
#             # df.to_csv(f"./{results_folder}/{v}.csv", index=False)
#             output_file = os.path.join(results_folder, f"{v}.csv")
#             df.to_csv(output_file, index=False)

#             # Store the DataFrame in the datas dictionary
#             datas[str(v)] = df

#         except ValueError as e:
#             print(f"Error creating DataFrame for {v}: {e}")
#             # Optionally, you can provide a default action or leave it empty to just skip the error
#             pass



    # %%
    # return instance
# if __name__ == '__main__':
#     # results = '../results'
#     results = RESULTS_FOLDER
#     data = '../data'
#     input_file = INPUT_FILE_PATH
#     solve_model(input_file,results)