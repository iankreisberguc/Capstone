import pandas as pd 
from clases import Bay, Barco, Container
from funciones import generar_espacios, calcular_centro_masa,\
    over_stowage, calcular_valor, calcular_esfuerzos_corte
from prueba import crear_primera_solucion


data_barco = pd.read_excel('container_ship_data.xlsx', 'Ship_bays_estr_data', skiprows=4, usecols="C:I", header=1)
data_loaded = pd.read_excel('container_ship_data.xlsx', 'Loaded_containers_data')
data_slot = pd.read_excel('container_ship_data.xlsx', 'Slot_data')
data_hydrostatic = pd.read_excel('container_ship_data.xlsx', 'Ship_hydrostatic_data', skiprows=6, usecols="B:H", header=1)
data_buoyancy = pd.read_excel('container_ship_data.xlsx', 'Ship_buoyancy_data', skiprows=4, usecols="C:X", header=1)
data_cargamento = pd.read_excel("container_ship_data.xlsx","Loading_list_data")

valor_kpi = 50
data_cargamento_filtrada = data_cargamento[data_cargamento["KPI"] > valor_kpi].reset_index()
barco = Barco()

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

    if barco.bays[int(bay)].espacio[int(tier)][int(stack)][int(slot)-1] == None:
        print('Revisa el codigo que hay un error')
    
    else:
        barco.bays[int(bay)].espacio[int(tier)][int(stack)][int(slot)-1] = container  

data_prueba = data_cargamento_filtrada.groupby("END_PORT", group_keys=False).apply(lambda x: x).sort_values(by=["END_PORT", "VALUE (USD)"], ascending=False)
data_RC = data_prueba[data_prueba["TYPE"] == "RC"]
data_DG = data_prueba[data_prueba["TYPE"] == "DG"]
data_DC = data_prueba[data_prueba["TYPE"] == "DC"]

# print(data_prueba)
# print(data_RC.iloc[0]['VALUE (USD)'])
# print(data_DG)
# print(len(data_DG))
# print(data_DC)

# crear_primera_solucion(data_prueba, data_slot, barco)

# contador_bay = 0
# for bay in barco.bays:
#     for tier in bay.espacio:
#         for stack in tier:
#             if stack[1] not in [0, 1, 2, None]:
#                 if stack[0].es_cargado and stack[1].es_cargado and contador_bay == 15:
#                     print(stack[0].largo, stack[0].tipo, stack[0].end_port)
#                     print(stack[1].largo, stack[1].tipo, stack[1].end_port)
#                     print("-"*50)
#     contador_bay += 1