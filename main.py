from matplotlib.container import BarContainer
import pandas as pd 

from clases import Barco
# from funciones import generar_espacios, calcular_centro_masa,\
#     over_stowage, calcular_valor, verificar_esfuerfos_de_corte, verificar_factibilidad_fisica
from primera_carga import cargar
from funciones import *
import time

data_barco = pd.read_excel('container_ship_data.xlsx', 'Ship_bays_estr_data', skiprows=4, usecols="C:I", header=1)
data_loaded = pd.read_excel('container_ship_data.xlsx', 'Loaded_containers_data')
data_slot = pd.read_excel('container_ship_data.xlsx', 'Slot_data')
data_hydrostatic = pd.read_excel('container_ship_data.xlsx', 'Ship_hydrostatic_data', skiprows=6, usecols="B:H", header=1)
data_buoyancy = pd.read_excel('container_ship_data.xlsx', 'Ship_buoyancy_data', skiprows=4, usecols="C:X", header=1)
data_cargamento = pd.read_excel("container_ship_data.xlsx","Loading_list_data")

valor_kpi = 0
contenedores_cargados = []
data_cargamento_filtrada = data_cargamento[data_cargamento["KPI"] > valor_kpi].reset_index()
data_ordenada = data_cargamento_filtrada.groupby("END_PORT", \
    group_keys=False).apply(lambda x: x).sort_values(by=["END_PORT", "VALUE (USD)"], ascending=False)
barco = Barco()

inicio = time.time()

barco.generar_bays(data_barco)
generar_espacios(data_slot, barco)

for index, row in data_loaded.iterrows():
    bay = row['BAY']
    stack = row['STACK']
    tier = row['TIER']
    slot = row['SLOT']
    peso = row['WEIGHT (ton)']
    tipo = row['TYPE']
    valor = 0
    es_cargado = True
    end_port = row['END_PORT']
    largo = row['LENGTH (ft)']
    tcg = float(data_slot[(data_slot.BAY==bay) & (data_slot.STACK==stack) & (data_slot.TIER==tier) & (data_slot.SLOT==1)].TCG)
    vcg = float(data_slot[(data_slot.BAY==bay) & (data_slot.STACK==stack) & (data_slot.TIER==tier) & (data_slot.SLOT==1)].VCG)
    container = Container(peso, tipo, valor, end_port, largo, tcg, vcg, es_cargado)

    #if bay == 15:
    if barco.bays[int(bay)].espacio[int(tier)][int(stack)][int(slot)-1] == None:
        print('Revisa el codigo que hay un error pq hay un comteiner en una posicion invalida')
    
    else:
        aux = barco.bays[int(bay)].espacio[int(tier)][int(stack)][int(slot)-1]
        barco.bays[int(bay)].espacio[int(tier)][int(stack)][int(slot)-1] = container
        container.tipo_slot = aux

# primera_carga(data_loaded, data_slot, barco)  #carga los contenedores que ya estan en el barco desde la data

data_RC = data_ordenada[data_ordenada["TYPE"] == "RC"]
data_noRC = data_ordenada[data_ordenada["TYPE"] != "RC"]

# barco.actualizar_peso()
# print(barco.peso)

cargar(data_ordenada, data_slot, barco, contenedores_cargados, data_hydrostatic, data_buoyancy)
# print(contenedores_cargados)

print(len(contenedores_cargados))
barco.actualizar_peso()
print(barco.peso)
fin = time.time()

print(f"El tiempo de ejecucion es: {fin - inicio}")

for bay in barco.bays:
    primera, segunda = maximo_peso(bay)
    print(primera)

# print(data_RC)
# print(data_noRC)

# print(barco.bays[15].espacio)
# print(calcular_centro_masa(barco))
# print(f"Factible: ", verificar_factibilidad_fisica(data_hydrostatic, data_buoyancy,barco))
# barco.actualizar_peso()
# print(f"Peso:", barco.peso)
# print(f"Carga:", barco.carga/70.33)
# print(f"contenedores de 40 ft", barco.contador_40)
# print(f"contenedores de 20 ft", barco.contador_20)
# print(f"over stowage:", over_stowage(barco))
# resultado_barco_cargado = calcular_valor(barco) - over_stowage(barco)*60

# print(f"valor barco:",resultado_barco_cargado)
# print("---------------------------")
# primera_solucion = crear_primera_solucion(data_prueba, data_slot, barco)
# print(primera_solucion)

# # for bay in barco.bays:
# #     for tier in bay.espacio:
# #         print(tier)


# resultado_caso_base = calcular_valor(barco) - over_stowage(barco)*60 - primera_solucion*40

# print(f"valor barco:",resultado_caso_base)


# print(f"Factible: ", verificar_factibilidad_fisica(data_hydrostatic, data_buoyancy,barco))
# barco.actualizar_peso()
# print(f"Peso:", barco.peso)
# print(f"Carga:", barco.carga/70.33)
# print(f"contenedores de 40 ft", barco.contador_40)
# print(f"contenedores de 20 ft", barco.contador_20)
# print(f"over stowage:", over_stowage(barco))

# print("-----------------------")
# print(listar_over_stowage(barco))

# destruccion(barco, 1)

############################ AQUI ESTAMOS VISUALIZANDO ###################

# import matplotlib.pyplot as plt
# import seaborn as sns

# for i in range(1, 21):
#     if i != 14:
#         diccionario = {}
#         for tier in range(18):
#             lista = []
#             for stack in barco.bays[i].espacio[tier]:
#                 if stack[0] not in [0, 1, 2, None]:
#                     if stack[0].es_cargado :
#                         lista.append(8)
#                     else:
#                         lista.append(10)

#                 elif stack[0] == None:
#                     lista.append(0)

#                 elif stack[0] == 1:
#                     lista.append(5)
                
#                 else:
#                     lista.append(3)

#             diccionario[f"{tier}"] = lista        
#         df = pd.DataFrame(diccionario)
#         plt.figure(figsize=(8,8))
#         plt.xlabel('TIER', size = 15)
#         plt.ylabel('STACK', size = 15)
#         plt.title('VISUALIZACIÓN DEL BARCO CARGADO EN EL BAY %i' %i, size = 15)
#         visualizacion = sns.heatmap(df.transpose(), annot=True, fmt=".0f", linewidths=.5, square = True, cmap = 'YlGnBu', vmin=0, vmax= 10)
#         visualizacion.invert_yaxis()
# plt.show()

