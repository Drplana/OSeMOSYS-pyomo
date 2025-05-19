import os
import sys
root_folder = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)
import traceback
from concurrent.futures import ProcessPoolExecutor
from OSeMOSYS.utils import dataframe_metadata
from OSeMOSYS.SolveSolutions import solve_model, export_results
from OSeMOSYS.readXlsData import load_dataframes, transform_all_dataframes, save_dataframes_to_csv, dict_to_json, adjust_json_for_pyomo, export_to_json
from OSeMOSYS.config import configure_paths

def generate_task(task):
    """
    Función global para generar un archivo JSON para un subescenario específico.

    Args:
        task (tuple): Tupla que contiene el valor del parámetro principal y los parámetros secundarios.

    Returns:
        str: Ruta del archivo JSON generado.
    """
    scenario_manager, value, parameters, parameter_name = task
    subscenario_name = f"{parameter_name}_{value}"
    return scenario_manager.generate_json_file_2(parameters, subscenario_name)

class ScenarioManager:
    def __init__(self, input_file, root_folder, dimension_manager):
        """
        Inicializa el gestor de escenarios.

        Args:
            input_file (str): Ruta del archivo de entrada.
            root_folder (str): Carpeta raíz del proyecto.
            dimension_manager (DimensionManager): Gestor de dimensiones.
        """
        self.input_file = input_file
        self.root_folder = root_folder
        self.dimension_manager = dimension_manager
        self.dataframe_metadata = dataframe_metadata

    def generate_json_file(self, parameter_name, value, subscenario_name):
        """
        Genera un archivo JSON para un subescenario basado en un único parámetro.

        Args:
            parameter_name (str): Nombre del parámetro a modificar.
            value (float): Valor del parámetro.
            subscenario_name (str): Nombre del subescenario.

        Returns:
            str: Ruta del archivo JSON generado.
        """
        try:
            # Configurar rutas
            input_file_name = os.path.splitext(os.path.basename(self.input_file))[0]
            data_folder = os.path.join(self.root_folder, "data", input_file_name)
            os.makedirs(data_folder, exist_ok=True)

            json_file_path = os.path.join(data_folder, f"{subscenario_name}.json")
            results_folder = os.path.join(self.root_folder, "results", subscenario_name)
            os.makedirs(results_folder, exist_ok=True)

            # json_file_path = os.path.join(
            #     self.root_folder, "data", f"{os.path.basename(self.input_file).replace('.xlsx', '')}_{subscenario_name}.json"
            # )

            # Cargar y transformar los datos
            dataframe = load_dataframes(self.input_file)
            transf_data = transform_all_dataframes(dataframe)
            dict_to_be_adjusted = dict_to_json(transf_data, self.input_file)
            pyomo_dict = adjust_json_for_pyomo(dict_to_be_adjusted)

            # Modificar el parámetro
            parameter_name_with_prefix = f"p_{parameter_name}"
            if parameter_name_with_prefix not in pyomo_dict:
                print(f"El parámetro '{parameter_name_with_prefix}' no se encontró en el modelo.")
                return None

            for entry in pyomo_dict[parameter_name_with_prefix]:
                entry["value"] = value
            print(f"Parámetro '{parameter_name_with_prefix}' ajustado a {value}.")

            # Exportar los datos a JSON
            export_to_json(pyomo_dict, json_file_path)
            print(f"Archivo JSON exportado correctamente: {json_file_path}")
            return json_file_path

        except Exception as e:
            print(f"Error al generar el archivo JSON para el subescenario {subscenario_name}: {e}")
            traceback.print_exc()
            return None

    def generate_combined_scenarios(self, parameter_name, values, additional_parameters):
        """
        Genera escenarios combinados donde se varía un parámetro principal y otros parámetros secundarios.

        Args:
            parameter_name (str): Nombre del parámetro principal a modificar.
            values (list): Lista de valores para el parámetro principal.
            additional_parameters (list): Lista de parámetros secundarios a modificar.

        Returns:
            list: Lista de rutas de los archivos JSON generados.
        """
        json_files = []
        tasks = [
            (self, value, [{"name": parameter_name, "values": [value], "filters": None}] + additional_parameters, parameter_name)
            for value in values
        ]

        # for value in values:
        #     subscenario_name = f"{parameter_name}_{value}"
        #     parameters = [{"name": parameter_name, "values": [value], "filters": None}]

        #     # Agregar los parámetros secundarios
        #     parameters.extend(additional_parameters)

        #     # Generar el archivo JSON
        #     json_file_path = self.generate_json_file_2(parameters, subscenario_name)
        #     if json_file_path:
        #         json_files.append(json_file_path)
            # Función para generar un archivo JSON

        # Ejecutar las tareas en paralelo
        with ProcessPoolExecutor() as executor:
            results = executor.map(generate_task, tasks)
            json_files.extend(filter(None, results))  # Filtrar resultados válidos
        

        return json_files

    def generate_json_file_2(self, parameters, subscenario_name):
        """
        Genera un archivo JSON para un subescenario con múltiples parámetros.

        Args:
            parameters (list): Lista de parámetros a modificar.
            subscenario_name (str): Nombre del subescenario.

        Returns:
            str: Ruta del archivo JSON generado.
        """
        try:
            # Configurar rutas
            input_file_name = os.path.splitext(os.path.basename(self.input_file))[0]
            data_folder = os.path.join(self.root_folder, "data", input_file_name)
            json_file_path = os.path.join(data_folder, f"{subscenario_name}.json")
            results_folder = os.path.join(self.root_folder, "results", subscenario_name)
            os.makedirs(results_folder, exist_ok=True)

            # json_file_path = os.path.join(
            #     self.root_folder, "data", f"{os.path.basename(self.input_file).replace('.xlsx', '')}_{subscenario_name}.json"
            # )

            # Cargar y transformar los datos
            dataframe = load_dataframes(self.input_file)
            transf_data = transform_all_dataframes(dataframe)
            dict_to_be_adjusted = dict_to_json(transf_data, self.input_file)
            pyomo_dict = adjust_json_for_pyomo(dict_to_be_adjusted)

            for param in parameters:
                parameter_name = param["name"]
                values = param["values"]
                filters = param.get("filters", None)

                # Obtener las dimensiones del parámetro
                dimensions = self.dataframe_metadata[parameter_name]["indices"]

                # Modificar el parámetro
                self.modify_parameters_for_scenario(pyomo_dict, parameter_name, values, filters, dimensions)

            # Exportar los datos a JSON
            export_to_json(pyomo_dict, json_file_path)
            print(f"Archivo JSON exportado correctamente: {json_file_path}")
            return json_file_path

        except Exception as e:
            print(f"Error al generar el archivo JSON para el subescenario {subscenario_name}: {e}")
            traceback.print_exc()
            return None

    def modify_parameters_for_scenario(self, pyomo_dict, parameter_name, values, filters, dimensions):
        """
        Modifica un parámetro del modelo Pyomo para un conjunto específico de dimensiones.

        Args:
            pyomo_dict (dict): Diccionario del modelo Pyomo.
            parameter_name (str): Nombre del parámetro a modificar.
            values (dict): Diccionario con los valores a asignar.
            filters (dict): Filtros para limitar las modificaciones.
            dimensions (list): Lista de dimensiones del parámetro.

        Returns:
            None
        """
        parameter_name_with_prefix = f"p_{parameter_name}"

        if parameter_name_with_prefix not in pyomo_dict:
            pyomo_dict[parameter_name_with_prefix] = []

        if isinstance(values, list):
            if filters is None:
                filters = {}
            values = {
                tuple(filters.get(dim, None) for dim in dimensions): value
                for value in values
            }

        if not filters:
            for entry in pyomo_dict[parameter_name_with_prefix]:
                entry["value"] = list(values.values())[0]
                print(f"Parámetro '{parameter_name_with_prefix}' ajustado a {entry['value']} para {entry['index']}")
            return

        existing_entries = pyomo_dict[parameter_name_with_prefix]
        new_keys = set(values.keys())
        pyomo_dict[parameter_name_with_prefix] = [
            entry for entry in existing_entries
            if tuple(entry["index"]) not in new_keys
        ]

        for key_tuple, value in values.items():
            if all(key_tuple[dimensions.index(k)] in v if isinstance(v, list)
                   else key_tuple[dimensions.index(k)] == v for k, v in filters.items()):
                pyomo_dict[parameter_name_with_prefix].append({
                    "index": list(key_tuple),
                    "value": value
                })
                print(f"Parámetro '{parameter_name_with_prefix}' ajustado a {value} para {key_tuple}")

    def solve_subscenarios_in_parallel(self, json_files, solver_name="gurobi"):
        """
        Resuelve múltiples subescenarios en paralelo.

        Args:
            json_files (list): Lista de rutas de los archivos JSON generados.
            solver_name (str): Nombre del solver a utilizar.

        Returns:
            None
        """
        with ProcessPoolExecutor() as executor:
            results = executor.map(self.solve_subscenario, json_files, [solver_name] * len(json_files))
            for result in results:
                print(result)

    def solve_subscenario(self, json_file_path, solver_name="gurobi"):
        """
        Resuelve un subescenario cargando un archivo JSON generado.

        Args:
            json_file_path (str): Ruta del archivo JSON generado.
            solver_name (str): Nombre del solver a utilizar.

        Returns:
            str: Mensaje indicando el resultado de la ejecución.
        """
        try:
            subscenario_name = os.path.basename(json_file_path).replace(".json", "")
            results_folder = os.path.join(self.root_folder, "results", subscenario_name)
            os.makedirs(results_folder, exist_ok=True)

            print(f"Resolviendo subescenario: {subscenario_name}")
            print(f"Archivo JSON cargado: {json_file_path}")
            print(f"Resultados se guardarán en: {results_folder}")

            # Resolver el modelo
            instance = solve_model(
                input_file=self.input_file,
                solver_name=solver_name,
                json_file_path_or_dict=json_file_path,
                solver_options=None,
                tee=True
            )

            # Exportar resultados
            export_results(instance, results_folder)
            return f"Modelo resuelto exitosamente para el subescenario: {subscenario_name}"

        except Exception as e:
            return f"Error al resolver el subescenario {subscenario_name}: {e}"
        

    def process_file(self, input_file, solver_name="gurobi"):
        """
        Procesa un archivo de entrada ejecutando el modelo y guardando los resultados.

        Args:
            input_file (str): Ruta del archivo de entrada.
            solver_name (str): Nombre del solver a utilizar.

        Returns:
            str: Mensaje indicando el resultado del procesamiento.
        """
        try:
            # Configurar rutas
            paths = configure_paths(input_file, self.root_folder)
            results_folder = paths['RESULTS_FOLDER']
            json_file_path = paths['OUTPUT_JSON_DATA_PATH']

            # Cargar y transformar los datos
            dataframe = load_dataframes(input_file)
            transf_data = transform_all_dataframes(dataframe)
            dict_to_be_adjusted = dict_to_json(transf_data, input_file)
            pyomo_dict = adjust_json_for_pyomo(dict_to_be_adjusted)

            # Exportar los datos a JSON
            export_to_json(pyomo_dict, json_file_path)

            # Ejecutar el modelo
            instance = solve_model(
                input_file=input_file,
                solver_name=solver_name,
                json_file_path_or_dict=json_file_path,
                solver_options=None,
                tee=True
            )

            # Exportar resultados
            export_results(instance, results_folder)
            return f"Modelo ejecutado exitosamente para: {input_file}"

        except Exception as e:
            error_message = f"Error al procesar el archivo {input_file}: {e}"
            traceback.print_exc()
            return error_message

    def run_files_in_parallel(self, input_files, solver_name="gurobi"):
        """
        Ejecuta múltiples archivos de entrada en paralelo.

        Args:
            input_files (list): Lista de rutas de archivos de entrada.
            solver_name (str): Nombre del solver a utilizar.

        Returns:
            None
        """
        with ProcessPoolExecutor() as executor:
            results = executor.map(self.process_file, input_files, [solver_name] * len(input_files))
            for result in results:
                print(result)
    def run_files_in_batches(self, input_files, batch_size=3, solver_name="gurobi"):
        """
        Ejecuta los archivos de entrada en lotes secuenciales.

        Args:
            input_files (list): Lista de rutas de archivos de entrada.
            batch_size (int): Tamaño del lote (número de archivos por grupo).
            solver_name (str): Nombre del solver a utilizar.

        Returns:
            None
        """
        for i in range(0, len(input_files), batch_size):
            batch = input_files[i:i + batch_size]
            print(f"Ejecutando lote {i // batch_size + 1}: {batch}")
            self.run_files_in_parallel(batch, solver_name)   


    def run_hybrid_scenarios_with_custom_parameters(self, input_files, batch_size, scenarios_config, solver_name="gurobi"):
        """
        Ejecuta un enfoque híbrido de escenarios: múltiples archivos en paralelo y escenarios combinados con parámetros específicos por archivo.

        Args:
            input_files (list): Lista de rutas de archivos de entrada.
            batch_size (int): Tamaño del lote (número de archivos por grupo).
            scenarios_config (dict): Configuración de parámetros y valores para cada archivo.
            solver_name (str): Nombre del solver a utilizar.

        Returns:
            None
        """
        for i in range(0, len(input_files), batch_size):
            batch = input_files[i:i + batch_size]
            print(f"Ejecutando lote {i // batch_size + 1}: {batch}")

            # Ejecutar los archivos base directamente
            with ProcessPoolExecutor() as executor:
                base_results = executor.map(self.execute_base_file, batch, [solver_name] * len(batch))
                for result in base_results:
                    print(result)

            # Ejecutar subescenarios para cada archivo en paralelo dentro del lote
            with ProcessPoolExecutor() as executor:
                results = executor.map(
                    self.process_file_with_custom_scenarios,
                    batch,
                    [scenarios_config] * len(batch),
                    [solver_name] * len(batch)
                )
                for result in results:
                    print(result)

    def process_file_with_custom_scenarios(self, input_file, scenarios_config, solver_name):
        """
        Procesa un archivo de entrada generando y resolviendo escenarios combinados según su configuración específica.

        Args:
            input_file (str): Ruta del archivo de entrada.
            scenarios_config (dict): Configuración de parámetros y valores para cada archivo.
            solver_name (str): Nombre del solver a utilizar.

        Returns:
            str: Mensaje indicando el resultado del procesamiento.
        """
        try:
            # Configurar el ScenarioManager para el archivo actual
            self.input_file = input_file

            # Obtener la configuración específica para este archivo
            if input_file not in scenarios_config:
                return f"No se definieron escenarios para el archivo: {input_file}"

            config = scenarios_config[input_file]
            parameter_name = config["parameter_name"]
            values = config["values"]

            # Caso 1: Usar generate_combined_scenarios y solve_subscenarios_in_parallel
            if isinstance(values, list):
                json_files = self.generate_combined_scenarios(parameter_name, values, [])
                self.solve_subscenarios_in_parallel(json_files, solver_name)

            # Caso 2: Usar generate_json_file_2 y solve_subscenario
            elif isinstance(values, dict):
                subscenario_name = f"{parameter_name}_custom"
                json_file_path = self.generate_json_file_2([{"name": parameter_name, "values": values["values"], "filters": values["filters"]}], subscenario_name)
                if json_file_path:
                    result_message = self.solve_subscenario(json_file_path, solver_name)
                    print(result_message)

            return f"Procesamiento completado para: {input_file}"

        except Exception as e:
            return f"Error al procesar el archivo {input_file}: {e}"
        
    def execute_base_file(self, input_file, solver_name):
        """
        Ejecuta directamente un archivo base sin generar subescenarios.

        Args:
            input_file (str): Ruta del archivo base.
            solver_name (str): Nombre del solver a utilizar.

        Returns:
            None
        """
        try:
            # Configurar rutas
            paths = configure_paths(input_file, self.root_folder)
            json_file_path = paths['OUTPUT_JSON_DATA_PATH']
            results_folder = paths['RESULTS_FOLDER']

            # Cargar y transformar los datos
            dataframe = load_dataframes(input_file)
            transf_data = transform_all_dataframes(dataframe)
            dict_to_be_adjusted = dict_to_json(transf_data, input_file)
            pyomo_dict = adjust_json_for_pyomo(dict_to_be_adjusted)

            # Exportar los datos a JSON
            export_to_json(pyomo_dict, json_file_path)

            # Ejecutar el modelo
            instance = solve_model(
                input_file=input_file,
                solver_name=solver_name,
                json_file_path_or_dict=json_file_path,
                solver_options=None,
                tee=True
            )

            # Exportar resultados
            export_results(instance, results_folder)
            print(f"Archivo base ejecutado exitosamente: {input_file}")

        except Exception as e:
            print(f"Error al ejecutar el archivo base {input_file}: {e}")
    