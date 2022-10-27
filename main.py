from matplotlib.container import BarContainer
import pandas as pd 

from clases import Barco
# from funciones import generar_espacios, calcular_centro_masa,\
#     over_stowage, calcular_valor, verificar_esfuerfos_de_corte, verificar_factibilidad_fisica
from construccion import cargar
from funciones import *
from destruccion import destruccion
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

primera_carga(data_loaded, data_slot, barco)  #carga los contenedores que ya estan en el barco desde la data
barco.actualizar_peso()
print(barco.peso)
# data_RC = data_ordenada[data_ordenada["TYPE"] == "RC"]
# data_noRC = data_ordenada[data_ordenada["TYPE"] != "RC"]


#cargar(data_ordenada, data_slot, barco, contenedores_cargados, data_hydrostatic, data_buoyancy)

#barco.actualizar_peso()
# print(barco.peso)
#print(len(contenedores_cargados))


# for i in range(50):
#     lista_destruccion = destruccion(barco, 10)
#     cargar(data_ordenada, data_slot, barco, contenedores_cargados, data_hydrostatic, data_buoyancy)

# print(lista_destruccion)

# resultado_barco_cargado = calcular_valor(barco) - over_stowage(barco)*60
# barco.actualizar_peso()
# print(barco.peso)
# print(f"valor barco:",resultado_barco_cargado)

fin = time.time()

print(f"El tiempo de ejecucion es: {fin - inicio}")

# for bay in barco.bays:
#     primera, segunda = maximo_peso(bay)
#     print(primera)

# print(barco.bays[15].espacio)
# print(calcular_centro_masa(barco))
# print(f"Factible: ", verificar_factibilidad_fisica(data_hydrostatic, data_buoyancy,barco))
# barco.actualizar_peso()
# print(f"Peso:", barco.peso)
# print(f"Carga:", barco.carga/70.33)
# print(f"contenedores de 40 ft", barco.contador_40)
# print(f"contenedores de 20 ft", barco.contador_20)
# print(f"over stowage:", over_stowage(barco))
# print("---------------------------")
# primera_solucion = crear_primera_solucion(data_prueba, data_slot, barco)
# print(primera_solucion)

# for bay in barco.bays:
#     for tier in bay.espacio:
#         print(tier)


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


############################ AQUI ESTAMOS VISUALIZANDO ###################
print(calcular_centro_masa(barco))

import matplotlib.pyplot as plt
import seaborn as sns

for i in range(1, 21):
    if i != 14:
        diccionario = {}
        for tier in range(18):
            lista = []
            for stack in barco.bays[i].espacio[tier]:
                if stack[0] not in [0, 1, 2, None]:
                    peso = stack[0].peso
                    if stack[1] not in [0, 1, 2, None]: peso += stack[1].peso
                    lista.append(peso)
                    # if stack[0].es_cargado :
                    #     lista.append(8)
                    # else:
                    #     lista.append(10)

                elif stack[0] == None:
                    lista.append(0)

                elif stack[0] == 1:
                    lista.append(2)
                
                else:
                    lista.append(1)

            diccionario[f"{tier}"] = lista        
        df = pd.DataFrame(diccionario)
        plt.figure(figsize=(8,8))
        plt.xlabel('TIER', size = 15)
        plt.ylabel('STACK', size = 15)
        plt.title('VISUALIZACIÓN DEL BARCO CARGADO EN EL BAY %i' %i, size = 15)
        visualizacion = sns.heatmap(df.transpose(), annot=True, fmt=".0f", linewidths=.5, square = True, cmap = 'YlGnBu', vmin=0, vmax= 10)
        visualizacion.invert_yaxis()
plt.show()

