import pandas as pd 
from clases import Bay, Barco, Container
from funciones import generar_espacios, calcular_centro_masa,\
    over_stowage, calcular_valor, verificar_esfuerfos_de_corte


data_barco = pd.read_excel('container_ship_data.xlsx', 'Ship_bays_estr_data', skiprows=4, usecols="C:I", header=1)
data_loaded = pd.read_excel('container_ship_data.xlsx', 'Loaded_containers_data')
data_slot = pd.read_excel('container_ship_data.xlsx', 'Slot_data')
data_hydrostatic = pd.read_excel('container_ship_data.xlsx', 'Ship_hydrostatic_data', skiprows=6, usecols="B:H", header=1)
data_buoyancy = pd.read_excel('container_ship_data.xlsx', 'Ship_buoyancy_data', skiprows=4, usecols="C:X", header=1)

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

    if bay == 15 and stack == 1:
        if barco.bays[int(bay)].espacio[int(tier)][int(stack)][int(slot)-1] == None:
            print('Revisa el codigo que hay un error pq hay un comteiner en una posicion invalida')
        
        else:
            barco.bays[int(bay)].espacio[int(tier)][int(stack)][int(slot)-1] = container  
