import pandas as pd 
from clases import Bay, Barco, Container
from funciones import generar_espacios, calcular_centro_masa,\
    over_stowage, calcular_valor, verificar_esfuerfos_de_corte, verificar_factibilidad_fisica
from primera_carga import crear_primera_solucion

data_barco = pd.read_excel('container_ship_data.xlsx', 'Ship_bays_estr_data', skiprows=4, usecols="C:I", header=1)
data_loaded = pd.read_excel('container_ship_data.xlsx', 'Loaded_containers_data')
data_slot = pd.read_excel('container_ship_data.xlsx', 'Slot_data')
data_hydrostatic = pd.read_excel('container_ship_data.xlsx', 'Ship_hydrostatic_data', skiprows=6, usecols="B:H", header=1)
data_buoyancy = pd.read_excel('container_ship_data.xlsx', 'Ship_buoyancy_data', skiprows=4, usecols="C:X", header=1)
data_cargamento = pd.read_excel("container_ship_data.xlsx","Loading_list_data")


valor_kpi = 0
data_cargamento_filtrada = data_cargamento[data_cargamento["KPI"] > valor_kpi].reset_index()
data_prueba = data_cargamento_filtrada.groupby("END_PORT", group_keys=False).apply(lambda x: x).sort_values(by=["END_PORT", "VALUE (USD)"], ascending=False)
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

    #if bay == 15:
    if barco.bays[int(bay)].espacio[int(tier)][int(stack)][int(slot)-1] == None:
        print('Revisa el codigo que hay un error pq hay un comteiner en una posicion invalida')
    
    else:
        barco.bays[int(bay)].espacio[int(tier)][int(stack)][int(slot)-1] = container  

# print(barco.bays[15].espacio)
# print(calcular_centro_masa(barco))
print(f"Factible: ", verificar_factibilidad_fisica(data_hydrostatic, data_buoyancy,barco))
barco.actualizar_peso()
print(f"Peso:", barco.peso)
print(f"Carga:", barco.carga/70.33)
print(f"contenedores de 40 ft", barco.contador_40)
print(f"contenedores de 20 ft", barco.contador_20)
print(f"over stowage:", over_stowage(barco))
resultado_barco_cargado = calcular_valor(barco) - over_stowage(barco)*60

print(f"valor barco:",resultado_barco_cargado)
print("---------------------------")
primera_solucion = crear_primera_solucion(data_prueba, data_slot, barco)
print(primera_solucion)

# for bay in barco.bays:
#     for tier in bay.espacio:
#         print(tier)


resultado_caso_base = calcular_valor(barco) - over_stowage(barco)*60 - primera_solucion*40

print(f"valor barco:",resultado_caso_base)

print(f"Factible: ", verificar_factibilidad_fisica(data_hydrostatic, data_buoyancy,barco))
barco.actualizar_peso()
print(f"Peso:", barco.peso)
print(f"Carga:", barco.carga/70.33)
print(f"contenedores de 40 ft", barco.contador_40)
print(f"contenedores de 20 ft", barco.contador_20)
print(f"over stowage:", over_stowage(barco))