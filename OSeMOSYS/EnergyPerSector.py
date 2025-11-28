import plotly.io as pio
import plotly.graph_objects as go

portadores = {
    "gas_natural": {
        "produccion_nacional": 955.0,     # 2023, MMm³
        "unidad_original": "MMm³",
        "factor_conversion": 9.5,         # GWh/MMm³
        "valor_GWh": 955.0 * 9.5,         # 9,072.5 GWh
    },
    "bagazo_cana": {
        "produccion_nacional": 1556.0,    # 2023, mil toneladas
        "unidad_original": "mil toneladas",
        "factor_conversion": 4.75,        # GWh/kt
        "valor_GWh": 1556.0 * 4.75,       # 7,381 GWh
    },
    "leña": {
        "produccion_nacional": 15.1,      # 2023, Mm³
        "unidad_original": "Mm³",
        "factor_conversion": 1200,        # GWh/Mm³ (estimado)
        "valor_GWh": 15.1 * 1200,         # 18,120 GWh
    },
    "carbon_vegetal": {
        "produccion_nacional": 6.7,       # 2023, mil toneladas
        "unidad_original": "mil toneladas",
        "factor_conversion": 8.3,         # GWh/kt (promedio)
        "valor_GWh": 6.7 * 8.3,           # 55.61 GWh
    },
    "electricidad_bruta": {
        "produccion_nacional": 15331.1,   # 2023, GWh
        "unidad_original": "GWh",
        "factor_conversion": 1.0,
        "valor_GWh": 15331.1,
    },
    # Importaciones (2022)
    "derivados_petroleo": {
        "importe": 2342.1,                # 2022, mil toneladas
        "unidad_original": "mil toneladas",
        "factor_conversion": 11.63,       # GWh/kt
        "valor_GWh": 2342.1 * 11.63,      # 27,241 GWh
    },
    "glp": {
        "importe": 187.5,                 # 2022, mil toneladas
        "unidad_original": "mil toneladas",
        "factor_conversion": 13.8,        # GWh/kt
        "valor_GWh": 187.5 * 13.8,        # 2,587.5 GWh
    },
    "gasolina_motor": {
        "importe": 380.7,                 # 2022, mil toneladas
        "unidad_original": "mil toneladas",
        "factor_conversion": 11.5,        # GWh/kt (estimado)
        "valor_GWh": 380.7 * 11.5,        # 4,378.05 GWh
    },
    "diesel": {
        "importe": 876.0,                 # 2022, mil toneladas
        "unidad_original": "mil toneladas",
        "factor_conversion": 11.9,        # GWh/kt (estimado)
        "valor_GWh": 876.0 * 11.9,        # 10,424.4 GWh
    },
    "fuel_oil": {
        "importe": 679.2,                 # 2022, mil toneladas
        "unidad_original": "mil toneladas",
        "factor_conversion": 11.63,       # GWh/kt
        "valor_GWh": 679.2 * 11.63,       # 7,899.6 GWh
    },
    "gas_manufacturado": {
        "importe": 175.0,                 # 2023, MMm³
        "unidad_original": "MMm³",
        "factor_conversion": 9.5,         # GWh/MMm³
        "valor_GWh": 175.0 * 9.5,         # 1,662.5 GWh
    },
}

# Paso a paso de conversiones (para verificación)

# Gas natural
gas_natural_MMm3 = 955.0
factor_gas_natural = 9.5
gas_natural_GWh = gas_natural_MMm3 * factor_gas_natural
print(f"Gas natural: {gas_natural_MMm3} MMm3 * {factor_gas_natural} = {gas_natural_GWh} GWh")

# Bagazo de caña
bagazo_kt = 1556.0
factor_bagazo = 4.75
bagazo_GWh = bagazo_kt * factor_bagazo
print(f"Bagazo de caña: {bagazo_kt} kt * {factor_bagazo} = {bagazo_GWh} GWh")

# Leña
lenia_Mm3 = 15.1
factor_lenia = 1200
lenia_GWh = lenia_Mm3 * factor_lenia
print(f"Leña: {lenia_Mm3} Mm3 * {factor_lenia} = {lenia_GWh} GWh")

# Carbón vegetal
carbon_kt = 6.7
factor_carbon = 8.3
carbon_GWh = carbon_kt * factor_carbon
print(f"Carbón vegetal: {carbon_kt} kt * {factor_carbon} = {carbon_GWh} GWh")

# Electricidad bruta
electricidad_GWh = 15331.1
print(f"Electricidad bruta: {electricidad_GWh} GWh")

# Derivados del petróleo (importaciones)
derivados_kt = 2342.1
factor_derivados = 11.63
derivados_GWh = derivados_kt * factor_derivados
print(f"Derivados petróleo: {derivados_kt} kt * {factor_derivados} = {derivados_GWh} GWh")

# GLP (importaciones)
glp_kt = 187.5
factor_glp = 13.8
glp_GWh = glp_kt * factor_glp
print(f"GLP: {glp_kt} kt * {factor_glp} = {glp_GWh} GWh")

# Gasolina motor
gasolina_kt = 380.7
factor_gasolina = 11.5
gasolina_GWh = gasolina_kt * factor_gasolina
print(f"Gasolina motor: {gasolina_kt} kt * {factor_gasolina} = {gasolina_GWh} GWh")

# Diesel
diesel_kt = 876.0
factor_diesel = 11.9
diesel_GWh = diesel_kt * factor_diesel
print(f"Diesel: {diesel_kt} kt * {factor_diesel} = {diesel_GWh} GWh")

# Fuel oil
fuel_kt = 679.2
factor_fuel = 11.63
fuel_GWh = fuel_kt * factor_fuel
print(f"Fuel oil: {fuel_kt} kt * {factor_fuel} = {fuel_GWh} GWh")

# Gas manufacturado
gasman_MMm3 = 175.0
factor_gasman = 9.5
gasman_GWh = gasman_MMm3 * factor_gasman
print(f"Gas manufacturado: {gasman_MMm3} MMm3 * {factor_gasman} = {gasman_GWh} GWh")


portadores = {
    "gas_natural": {
        "nombre": "Gas natural",
        "produccion_nacional": 955.0,
        "unidad_original": "MMm³",
        "factor_conversion": 9.5,
        "valor_GWh": 955.0 * 9.5, # 9,073 GWh
        "usos_finales": {
            "Generación eléctrica": 8_166,    # 90% aprox.
            "Industria": 907,                 # 10% aprox.
        }
    },
    "bagazo_cana": {
        "nombre": "Bagazo de caña",
        "produccion_nacional": 1556.0,
        "unidad_original": "mil toneladas",
        "factor_conversion": 4.75,
        "valor_GWh": 1556.0 * 4.75, # 7,381 GWh
        "usos_finales": {
            "Generación eléctrica": 7_012,    # 95%
            "Industria": 369,                 # 5%
        }
    },
    "leña": {
        "nombre": "Leña",
        "produccion_nacional": 15.1,
        "unidad_original": "Mm³",
        "factor_conversion": 1200,
        "valor_GWh": 15.1 * 1200,  # 18,120 GWh
        "usos_finales": {
            "Cocción residencial": 18_120,
        }
    },
    "carbon_vegetal": {
        "nombre": "Carbón vegetal",
        "produccion_nacional": 6.7,
        "unidad_original": "mil toneladas",
        "factor_conversion": 8.3,
        "valor_GWh": 6.7 * 8.3,    # 55.6 GWh
        "usos_finales": {
            "Otros": 55.6,
        }
    },
    "electricidad_bruta": {
        "nombre": "Electricidad bruta",
        "produccion_nacional": 15331.1,
        "unidad_original": "GWh",
        "factor_conversion": 1.0,
        "valor_GWh": 15331.1,
        "usos_finales": {
            # Después se reparte entre sectores según los datos sectoriales
        }
    },
    "derivados_petroleo": {
        "nombre": "Derivados de petróleo (imp)",
        "importe": 2342.1,
        "unidad_original": "mil toneladas",
        "factor_conversion": 11.63,
        "valor_GWh": 2342.1 * 11.63, # 27,241 GWh
        "usos_finales": {
            "Generación eléctrica": 26_697,  # 98%
            "Transporte": 544,               # 2%
        }
    },
    "glp": {
        "nombre": "GLP (imp)",
        "importe": 187.5,
        "unidad_original": "mil toneladas",
        "factor_conversion": 13.8,
        "valor_GWh": 187.5 * 13.8, # 2,588 GWh
        "usos_finales": {
            "Cocción residencial": 2_588,
        }
    },
    "gasolina_motor": {
        "nombre": "Gasolina (imp)",
        "importe": 380.7,
        "unidad_original": "mil toneladas",
        "factor_conversion": 11.5,
        "valor_GWh": 380.7 * 11.5, # 4,378 GWh
        "usos_finales": {
            "Transporte": 4_378,
        }
    },
    "diesel": {
        "nombre": "Diesel (imp)",
        "importe": 876.0,
        "unidad_original": "mil toneladas",
        "factor_conversion": 11.9,
        "valor_GWh": 876.0 * 11.9,  # 10,424 GWh
        "usos_finales": {
            "Transporte": 10_424,
        }
    },
    "fuel_oil": {
        "nombre": "Fuel oil (imp)",
        "importe": 679.2,
        "unidad_original": "mil toneladas",
        "factor_conversion": 11.63,
        "valor_GWh": 679.2 * 11.63, # 7,900 GWh
        "usos_finales": {
            "Generación eléctrica": 7_742,  # 98%
            "Transporte": 158,              # 2%
        }
    },
    "gas_manufacturado": {
        "nombre": "Gas manufacturado (imp)",
        "importe": 175.0,
        "unidad_original": "MMm³",
        "factor_conversion": 9.5,
        "valor_GWh": 175.0 * 9.5,  # 1,663 GWh
        "usos_finales": {
            "Cocción residencial": 1_663,
        }
    },
}

portadores = {
    "petroleo_crudo": {
        "nombre": "Petróleo crudo",
        "tipo": "producción nacional",
        "produccion_nacional": None,
        "unidad_original": "mil toneladas",
        "factor_conversion": 11.63,
        "valor_GWh": None,
        "valor_original": None,
        "flows_to": [
            {"to": "Productos refinados", "valor_GWh": None}
        ]
    },
    "gas_natural": {
        "nombre": "Gas natural",
        "tipo": "producción nacional",
        "produccion_nacional": 955.0,
        "unidad_original": "MMm³",
        "factor_conversion": 9.5,
        "valor_GWh": 955.0 * 9.5,
        "valor_original": 955.0,
        "flows_to": [
            {"to": "Electricidad generada", "valor_GWh": 8166},
            {"to": "Industria", "valor_GWh": 907},
            {"to": "Red de gas", "valor_GWh": 0.9}
        ]
    },
    "bagazo_cana": {
        "nombre": "Bagazo de caña",
        "tipo": "producción nacional",
        "produccion_nacional": 1556.0,
        "unidad_original": "mil toneladas",
        "factor_conversion": 4.75,
        "valor_GWh": 1556.0 * 4.75,
        "valor_original": 1556.0,
        "flows_to": [
            {"to": "Electricidad generada", "valor_GWh": 7012},
            {"to": "Industria", "valor_GWh": 369}
        ]
    },
    "leña": {
        "nombre": "Leña",
        "tipo": "producción nacional",
        "produccion_nacional": 15.1,
        "unidad_original": "Mm³",
        "factor_conversion": 1200,
        "valor_GWh": 15.1 * 1200,
        "valor_original": 15.1,
        "flows_to": [
            {"to": "Cocción residencial", "valor_GWh": 18120}
        ]
    },
    "carbon_vegetal": {
        "nombre": "Carbón vegetal",
        "tipo": "producción nacional",
        "produccion_nacional": 6.7,
        "unidad_original": "mil toneladas",
        "factor_conversion": 8.3,
        "valor_GWh": 6.7 * 8.3,
        "valor_original": 6.7,
        "flows_to": [
            {"to": "Otros", "valor_GWh": 56}
        ]
    },
    "solar": {
        "nombre": "Solar",
        "tipo": "producción nacional",
        "produccion_nacional": None,
        "unidad_original": "GWh",
        "factor_conversion": 1.0,
        "valor_GWh": 510,
        "valor_original": 510,
        "flows_to": [
            {"to": "Electricidad generada", "valor_GWh": 510}
        ]
    },
    "eolica": {
        "nombre": "Eólica",
        "tipo": "producción nacional",
        "produccion_nacional": None,
        "unidad_original": "GWh",
        "factor_conversion": 1.0,
        "valor_GWh": 270,
        "valor_original": 270,
        "flows_to": [
            {"to": "Electricidad generada", "valor_GWh": 270}
        ]
    },
    "hidro": {
        "nombre": "Hidro",
        "tipo": "producción nacional",
        "produccion_nacional": None,
        "unidad_original": "GWh",
        "factor_conversion": 1.0,
        "valor_GWh": 60,
        "valor_original": 60,
        "flows_to": [
            {"to": "Electricidad generada", "valor_GWh": 60}
        ]
    },
    "glp": {
        "nombre": "GLP",
        "tipo": "importación",
        "importe": 187.5,
        "unidad_original": "mil toneladas",
        "factor_conversion": 13.8,
        "valor_GWh": 187.5 * 13.8,
        "valor_original": 187.5,
        "flows_to": [
            {"to": "Cocción residencial", "valor_GWh": 2588}
        ]
    },
    "gasolina": {
        "nombre": "Gasolina",
        "tipo": "importación",
        "importe": 380.7,
        "unidad_original": "mil toneladas",
        "factor_conversion": 11.5,
        "valor_GWh": 380.7 * 11.5,
        "valor_original": 380.7,
        "flows_to": [
            {"to": "Combustibles líquidos", "valor_GWh": 4378}
        ]
    },
    "diesel": {
        "nombre": "Diesel",
        "tipo": "importación",
        "importe": 876.0,
        "unidad_original": "mil toneladas",
        "factor_conversion": 11.9,
        "valor_GWh": 876.0 * 11.9,
        "valor_original": 876.0,
        "flows_to": [
            {"to": "Combustibles líquidos", "valor_GWh": 10424}
        ]
    },
    "fuel_oil": {
        "nombre": "Fuel oil",
        "tipo": "importación",
        "importe": 679.2,
        "unidad_original": "mil toneladas",
        "factor_conversion": 11.63,
        "valor_GWh": 679.2 * 11.63,
        "valor_original": 679.2,
        "flows_to": [
            {"to": "Electricidad generada", "valor_GWh": 7741},
            {"to": "Combustibles líquidos", "valor_GWh": 158}
        ]
    },
    "gas_manufacturado": {
        "nombre": "Gas manufacturado",
        "tipo": "importación",
        "importe": 175.0,
        "unidad_original": "MMm³",
        "factor_conversion": 9.5,
        "valor_GWh": 175.0 * 9.5,
        "valor_original": 175.0,
        "flows_to": [
            {"to": "Cocción residencial", "valor_GWh": 1663}
        ]
    },
    "derivados_petroleo": {
        "nombre": "Derivados de petróleo",
        "tipo": "importación",
        "importe": 2342.1,
        "unidad_original": "mil toneladas",
        "factor_conversion": 11.63,
        "valor_GWh": 2342.1 * 11.63,
        "valor_original": 2342.1,
        "flows_to": [
            {"to": "Electricidad generada", "valor_GWh": 26700},
            {"to": "Combustibles líquidos", "valor_GWh": 544}
        ]
    },
    "electricidad_generada": {
        "nombre": "Electricidad generada",
        "tipo": "secundaria",
        "valor_GWh": 15331,
        "unidad_original": "GWh",
        "flows_to": [
            {"to": "Red eléctrica", "valor_GWh": 15331}
        ]
    },
    "red_electrica": {
        "nombre": "Red eléctrica",
        "tipo": "red",
        "valor_GWh": 15331,
        "flows_to": [
            {"to": "Electricidad disponible", "valor_GWh": 15331}
        ]
    },
    "electricidad_disponible": {
        "nombre": "Electricidad disponible",
        "tipo": "energía final",
        "valor_GWh": 15331,
        "flows_to": [
            {"to": "Residencial", "valor_GWh": 9040},
            {"to": "Industria", "valor_GWh": 3851},
            {"to": "Transporte", "valor_GWh": 232},
            {"to": "Comercio", "valor_GWh": 406},
            {"to": "Agropecuario", "valor_GWh": 177},
            {"to": "Construcción", "valor_GWh": 61},
            {"to": "Estatal", "valor_GWh": 7070},
            {"to": "Otros", "valor_GWh": 2343},
            {"to": "Pérdidas", "valor_GWh": 3717}
        ]
    },
    "coccion_residencial": {
        "nombre": "Cocción residencial",
        "tipo": "energía final",
        "valor_GWh": 18120 + 2588 + 1663,
        "flows_to": [
            {"to": "Residencial", "valor_GWh": 22371}
        ]
    },
    "combustibles_liquidos": {
        "nombre": "Combustibles líquidos",
        "tipo": "energía final",
        "valor_GWh": 4378 + 10424 + 158 + 544,
        "flows_to": [
            {"to": "Transporte", "valor_GWh": 15484}
        ]
    },
    "red_de_gas": {
        "nombre": "Red de gas",
        "tipo": "red",
        "valor_GWh": 0.9,
        "flows_to": [
            {"to": "Gas final", "valor_GWh": 0.9}
        ]
    },
    "gas_final": {
        "nombre": "Gas final",
        "tipo": "energía final",
        "valor_GWh": 0.9,
        "flows_to": [
            {"to": "Industria", "valor_GWh": 0.9}
        ]
    }
}



# Lista de nodos
# usos_intermedios = ["Generación eléctrica", "Cocción residencial", "Transporte", "Industria", "Otros"]
# sectores_finales = ["Residencial", "Estatal", "Industria", "Transporte", "Agropecuario", "Construcción", "Comercio", "Otros", "Pérdidas"]
# labels = [v["nombre"] for v in portadores.values()]
# for uso in usos_intermedios:
#     if uso not in labels:
#         labels.append(uso)
# for sec in sectores_finales:
#     if sec not in labels:
#         labels.append(sec)

# # Consumos eléctricos por sector (GWh)
# sectores_electricos = {
#     "Residencial": 9038,
#     "Estatal": 7070,
#     "Industria": 3851,
#     "Transporte": 232,
#     "Agropecuario": 177,
#     "Construcción": 61,
#     "Comercio": 406,
#     "Otros": 2343,
#     "Pérdidas": 3717
# }

color_map = {
    # PETRÓLEO Y DERIVADOS
    "Petróleo crudo": "rgba(100,100,100,0.7)",
    "Derivados de petróleo": "rgba(150,150,150,0.7)",
    "Gasolina": "rgba(180,180,180,0.7)",
    "Diesel": "rgba(120,120,120,0.7)",
    "Fuel oil": "rgba(210,66,66,0.8)",  # Rojo fuel oil
    "Combustibles líquidos": "rgba(180,120,120,0.7)",
    # GASES
    "Gas natural": "rgba(255,140,0,0.7)",
    "GLP": "rgba(255,178,34,0.7)",
    "Gas manufacturado": "rgba(255,200,100,0.7)",
    "Red de gas": "rgba(255,178,34,0.7)",
    "Gas final": "rgba(255,200,100,0.7)",
    # BIOMASAS
    "Bagazo de caña": "rgba(44,130,36,0.7)",
    "Leña": "rgba(106,176,76,0.7)",
    "Carbón vegetal": "rgba(180,238,180,0.7)",
    # ENERGÍA ELÉCTRICA
    "Electricidad generada": "rgba(33,150,243,0.7)",
    "Red eléctrica": "rgba(33,150,243,0.7)",
    "Electricidad disponible": "rgba(33,150,243,0.7)",
    # ENERGÍAS RENOVABLES DIRECTAS
    "Solar": "rgba(255, 223, 70, 0.8)",
    "Eólica": "rgba(145, 237, 255, 0.8)",
    "Hidro": "rgba(51, 153, 255, 0.8)",
    # USO FINAL COCCIÓN
    "Cocción residencial": "rgba(205,133,63,0.6)",
    # PÉRDIDAS
    "Pérdidas": "rgba(200,200,200,0.5)",
}


labels = []
for v in portadores.values():
    if v["nombre"] not in labels:
        labels.append(v["nombre"])
    for flow in v.get("flows_to", []):
        if flow["to"] not in labels:
            labels.append(flow["to"])


# Para saber desde dónde sale cada flujo, arma un diccionario inverso:
import collections

# 1. Diccionario: destino -> lista de orígenes
flujos_inversos = collections.defaultdict(list)
for v in portadores.values():
    for flow in v.get("flows_to", []):
        if flow["valor_GWh"] is not None:
            flujos_inversos[flow["to"]].append(v["nombre"])


# Función que encuentra el portador primario de un nodo (siguiendo el camino inverso)
def portador_primario_para_flujo(origen, portadores_primarios):
    # Si el origen es primario, retorna
    if origen in portadores_primarios:
        return origen
    # Si no, busca hacia atrás recursivamente
    padres = flujos_inversos.get(origen, [])
    if not padres:
        return origen
    # Si hay más de un padre, retorna cada uno por separado (pero en Sankey, solo lo necesitamos para cada flujo directo)
    # Tomaremos el primero en la lista para cada barra, pero para mayor fidelidad lo ideal es que el Sankey venga desglosado por origen real.
    return portador_primario_para_flujo(padres[0], portadores_primarios)

# Los que no son destino de ningún flow
todos_destinos = set(flow["to"] for v in portadores.values() for flow in v.get("flows_to", []))
portadores_primarios = [v["nombre"] for v in portadores.values() if v["nombre"] not in todos_destinos]

# Armar arrays para Sankey
source = []
target = []
value = []
link_colors = []



# 1. Define colores por portador raíz
# color_map = {
#     "Petróleo crudo": "#8f8e8c",
#     "Gas natural": "#ffa600",
#     "Bagazo de caña": "#30c422",
#     "Leña": "#7b4c00",
#     "Carbón vegetal": "#305F32",
#     "Solar": "#ffdc00",
#     "Eólica": "#2697e2",
#     "Hidro": "#00419c",
#     "GLP": "#f8aa00",
#     "Gasolina": "#bba800",
#     "Diesel": "#bb8f00",
#     "Fuel oil": "#9B9992",
#     "Gas manufacturado": "#e68911",
#     "Derivados de petróleo": "#7f6000",
#     "Electricidad generada": "#e53935",
#     "Red eléctrica": "#e53935",
#     "Electricidad disponible": "#e53935",
#     "Combustibles líquidos": "#bb8f00",
#     "Cocción residencial": "#f48fb1",
#     "Red de gas": "#a19cfc",
#     "Pérdidas": "#c7c7c7",
# }


# 2. Al construir los flujos, determina el color raíz del portador de origen
link_colors = []



for v in portadores.values():
    from_idx = labels.index(v["nombre"])  
    # from_color = color_map.get(v['nombre'], "rgba(200,200,200,0.5)")
    for flow in v.get("flows_to", []):
        if flow["valor_GWh"] is not None:        
            to_idx = labels.index(flow["to"])
            source.append(from_idx)
            target.append(to_idx)
            value.append(round(flow["valor_GWh"]/1000, 2))  # A TWh, con dos decimales
            # link_colors.append(from_color)
            portador_raiz = portador_primario_para_flujo(v["nombre"], portadores_primarios)
            link_colors.append(color_map.get(portador_raiz, "rgba(200,200,200,0.5)"))

# ======= Paso 3: Graficar Sankey =======
fig = go.Figure(data=[go.Sankey(
    node=dict(
        pad=15, thickness=20,
        line=dict(color="black", width=0.5),
        label=labels,
    ),
    link=dict(
        source=source,
        target=target,
        value=value,
        color=link_colors,
    ))])

pio.renderers.default = "browser"
fig.update_layout(title_text="Balance energético nacional de Cuba (2023, TWh, usos finales)", 
                  font_size=12,
                #   opacity=0.8,
                  )
fig.show()
