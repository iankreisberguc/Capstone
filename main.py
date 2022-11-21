from matplotlib.container import BarContainer
import pandas as pd 

from clases import Barco
from construccion import cargar
from funciones import *
from destruccion import destruccion
from primer_orden import movimiento_contenedores
import time
from graficos import *

data_barco = pd.read_excel('container_ship_data.xlsx', 'Ship_bays_estr_data', skiprows=4, usecols="C:I", header=1)
data_loaded = pd.read_excel('container_ship_data.xlsx', 'Loaded_containers_data')
data_slot = pd.read_excel('container_ship_data.xlsx', 'Slot_data')
data_hydrostatic = pd.read_excel('container_ship_data.xlsx', 'Ship_hydrostatic_data', skiprows=6, usecols="B:I", header=1)
data_buoyancy = pd.read_excel('container_ship_data.xlsx', 'Ship_buoyancy_data', skiprows=4, usecols="C:X", header=1)
data_cargamento = pd.read_excel("container_ship_data.xlsx","Loading_list_data")

valor_kpi = 0
contenedores_cargados = []

############## ESPACIO PARA DECIDIR COMO ORDENAR LOS CONTENEDORES POR CARGAR ################
# data_cargamento_filtrada = data_cargamento[data_cargamento["KPI"] > valor_kpi].reset_index()
# data_ordenada = data_cargamento_filtrada.groupby("END_PORT", \
#     group_keys=False).apply(lambda x: x).sort_values(by=["END_PORT", "VALUE (USD)"], ascending=False)
# data_ordenada = data_cargamento.groupby("END", \
#               group_keys=False).apply(lambda x: x).sort_values(by=["END_PORT", "VALUE (USD)"], ascending=False)

data20 = data_cargamento[data_cargamento["LENGTH (ft)"] == 20].sort_values(by=["WEIGHT (ton)"], ascending=False)
data40 = data_cargamento[data_cargamento["LENGTH (ft)"] == 40].sort_values(by=["WEIGHT (ton)"], ascending=False)

data_ordenada = pd.concat([data20, data40], axis=0).reset_index()

data_ordenada = data_ordenada.drop(['index'], axis=1)

##############################################################################################
barco = Barco()

inicio = time.time()

barco.generar_bays(data_barco)
generar_espacios(data_slot, barco)

primera_carga(data_loaded, data_slot, barco)  #carga los contenedores que ya estan en el barco desde la data
barco.actualizar_peso()
print(barco.peso)
print(calcular_centro_masa(barco))
contenedores_movidos = movimiento_contenedores(barco, 0, data_slot, data_loaded, data_barco, data_hydrostatic, data_buoyancy)

cargar(data_ordenada, data_slot, barco, contenedores_cargados, data_hydrostatic, data_buoyancy, data_barco)
barco.actualizar_peso()
print(barco.peso)

print(calcular_centro_masa(barco))

# for i in range(50):
#     lista_destruccion = destruccion(barco, 10)
#     cargar(data_ordenada, data_slot, barco, contenedores_cargados, data_hydrostatic, data_buoyancy)

resultado_barco_cargado = calcular_valor(barco) - over_stowage(barco)*60 - contenedores_movidos*45

print(f"valor barco:",resultado_barco_cargado)

fin = time.time()

print(f"El tiempo de ejecucion es: {fin - inicio}")

# for bay in range(21):      
#     data = bending(barco.bays[bay], bay, data_barco)
#     print(data)

###############################################################################
import matplotlib.pyplot as plt
import pickle

with open('peso_output.pickle', 'wb') as handle:
    pickle.dump({bay_id: barco.bays[bay_id].peso_cargado() for bay_id in range(len(barco.bays))}, handle)


# aux_pesos = []

# for bay in range(21):
#     data = 0
#     for tier in barco.bays[bay].espacio:
#         for stack in range(16):
#             for container in tier[stack]:
#                 if container not in [0, 1, 2, None]:
#                     data += container.peso
#     data += barco.bays[bay].peso
#     valor_bending = bending(barco, bay, data_barco, data_hydrostatic, data_buoyancy)
#     valor_por_cargar = bending_final(barco, bay, data_barco, data_hydrostatic, data_buoyancy)
#     aux_pesos.append(data)
#     print(f"El bay {bay}: {data}, {valor_por_cargar}, {valor_bending}")

# plt.figure("Peso cargado en el barco")
# plt.bar(x=[a for a in range(len(aux_pesos))], height = aux_pesos, color ="red", edgecolor = "black")
# plt.xlabel("Bay")
# plt.ylabel("Peso cargado")
# plt.xticks(list(range(len(aux_pesos))), [i+1 for i in range(len(aux_pesos))])
# plt.tight_layout()
# plt.show()


# for tier in range(18):
#     barco.bays[10].espacio[tier]
#     for stack in range(16):
#         if barco.bays[10].espacio[tier][stack][1] not in [0, 1, 2, None]:
#             print(f'Tier:{tier}, Stack:{stack}->{barco.bays[10].espacio[tier][stack]} / {barco.bays[10].espacio[tier][stack][0].largo}, {barco.bays[10].espacio[tier][stack][1].largo}')
#         elif barco.bays[10].espacio[tier][stack][0] not in [0, 1, 2, None]:
#             print(f'Tier:{tier}, Stack:{stack}->{barco.bays[10].espacio[tier][stack]} / {barco.bays[10].espacio[tier][stack][0].largo}')
#         else:
#             print(f'Tier:{tier}, Stack:{stack}->{barco.bays[10].espacio[tier][stack]}')


# print("-"*50)

# for tier in barco.bays[9].espacio:
#     print(tier)

############################ AQUI ESTAMOS VISUALIZANDO ###################
# print(calcular_centro_masa(barco))

# import matplotlib.pyplot as plt
# import seaborn as sns

# for i in range(1, 21):
#     if i != 14:
#         diccionario = {}
#         for tier in range(18):
#             lista = []
#             for stack in barco.bays[i].espacio[tier]:
#                 if stack[0] not in [0, 1, 2, None]:
#                     peso = stack[0].peso
#                     if stack[1] not in [0, 1, 2, None]: peso += stack[1].peso
#                     lista.append(peso)
#                     # if stack[0].es_cargado :
#                     #     lista.append(8)
#                     # else:
#                     #     lista.append(10)

#                 elif stack[0] == None:
#                     lista.append(0)

#                 elif stack[0] == 1:
#                     lista.append(2)
                
#                 else:
#                     lista.append(1)

#             diccionario[f"{tier}"] = lista        
#         df = pd.DataFrame(diccionario)
#         plt.figure(figsize=(8,8))
#         plt.xlabel('TIER', size = 15)
#         plt.ylabel('STACK', size = 15)
#         plt.title('VISUALIZACIÓN DEL BARCO CARGADO EN EL BAY %i' %i, size = 15)
#         visualizacion = sns.heatmap(df.transpose(), annot=True, fmt=".0f", linewidths=.5, square = True, cmap = 'YlGnBu', vmin=0, vmax= 10)
#         visualizacion.invert_yaxis()
# plt.show()




#########################################
########Para graficar descomentar########
#########################################

#grafico_parametros(barco, data_slot, data_hydrostatic, data_loaded)

# grafico_peso_barco()

grafico_comparativo_peso_barco(barco, data_hydrostatic, data_buoyancy)