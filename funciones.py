from json.encoder import INFINITY
from clases import Container

def generar_espacios(data, barco):
    for index_data_slot, row_data_slot in data.iterrows():
        bay = int(row_data_slot['BAY'])
        stack = int(row_data_slot['STACK'])
        tier = int(row_data_slot['TIER'])
        refrigerado = row_data_slot['REEFER']
        carga_peligrosa = row_data_slot['DA']
        barco.bays[bay].espacio[tier][stack][0] = 0 + refrigerado
        barco.bays[bay].espacio[tier][stack][1] = 0 + refrigerado

        if carga_peligrosa == 0:
            barco.bays[bay].espacio[tier][stack][0] += 2
            barco.bays[bay].espacio[tier][stack][1] += 2


def calcular_centro_masa(barco):
    centro_gravedad = {'lcg': 0, 'tcg': 0, 'vcg': 15}
    peso = 0
    peso_otro = 36075
    for bay in barco.bays:
        for tier in bay.espacio:
            for slots in tier:
                for container in slots:
                    if container not in [0, 1, 2, None]:
                        aux_tcg = centro_gravedad['tcg']
                        aux_vcg = centro_gravedad['vcg']
                        aux_lcg = centro_gravedad['lcg']
                        centro_gravedad['tcg'] = (aux_tcg * peso_otro + container.tcg * container.peso) / (peso_otro + container.peso)
                        centro_gravedad['vcg'] = (aux_vcg * peso_otro + container.vcg * container.peso) / (peso_otro + container.peso)
                        centro_gravedad['lcg'] = (aux_lcg * peso + bay.lcg * container.peso) / (peso + container.peso)
                        peso_otro += container.peso
                        peso += container.peso
        aux_lcg = centro_gravedad['lcg']
        centro_gravedad['lcg'] = (aux_lcg * peso + bay.lcg * bay.peso) / (peso + bay.peso)
        peso += bay.peso
    
    return centro_gravedad


def calcular_displacemnt_index(data_hydrostatic, barco):
    #El displacemnt index en realidad es -1 pues se utilizo el index fe DF.
    barco.actualizar_peso()
    menor_index = -1
    menor_val = INFINITY
    for i in range(len(data_hydrostatic)):
        delta = abs(data_hydrostatic.iloc[i]['displacement (ton)']-barco.peso)
        if delta<menor_val:
            menor_val = delta
            menor_index = i
    dis_index = menor_index
    return dis_index


def over_stowage(barco):
    contador = 0
    contador_bay = 0
    for bay in barco.bays:
        for stack in range(16):
            aux = 12
            for tier in range(18):
                slots = bay.espacio[tier][stack]
                if slots[0] not in [0, 1, 2, None]:
                    if aux < slots[0].end_port:
                        contador += 1 
                    elif aux > slots[0].end_port:
                        aux = slots[0].end_port  
                        continue               
                    if slots[0].largo == 40:
                        continue
                        
                if slots[1] not in [0, 1, 2, None]:
                    if aux < slots[0].end_port:
                        contador += 1 
                    elif aux > slots[0].end_port:
                        aux = slots[0].end_port
        contador_bay += 1
    return contador


def calcular_valor(barco):
    valor = 0
    for bay in barco.bays:
        for tier in bay.espacio:
            for slots in tier:
                for container in slots:
                    if container not in [0, 1, 2, None]:
                        valor += container.valor
    return valor


def maximo_peso(bay):
    peso_restante = [[350 for stack in range(16)], [300 for stack in range(16)]]
    hay_contenedor20 = [[False for stack in range(16)], [False for stack in range(16)]]
    contador_tier = 0
    for tier in bay.espacio:
        for stack in range(16):
            for container in tier[stack]:
                if container not in [0, 1, 2, None]:
                    if contador_tier < 9:
                        peso_restante[0][stack] -= container.peso
                        if container.largo == 20:
                            hay_contenedor20[0][stack] = True
                    if contador_tier > 9:
                        peso_restante[1][stack] -= container.peso
                        if container.largo == 20:
                            hay_contenedor20[1][stack] = True
        contador_tier += 1
    
    for cubierta in range(2):
        for stack in range(16):
            if hay_contenedor20[cubierta][stack]:
                peso_restante[cubierta][stack] -= 100

    return peso_restante, hay_contenedor20


def primera_carga(data_loaded, data_slot, barco):
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

####Solo funciones de verificación#######

def verificar_factibilidad_fisica(data_hydrostatic, data_buoyancy, barco):
    #centro de G incompleto
    dis_index = calcular_displacemnt_index(data_hydrostatic, barco)
    if verificar_esfuerfos_de_corte(data_buoyancy, barco, dis_index) and\
        verificar_centro_de_dravedad(barco, data_hydrostatic, dis_index):
        return True
    else:
        return False

def verificar_centro_de_dravedad(barco, data_hydrostatic, dis_index):
    cen_grav = calcular_centro_masa(barco)
    print(cen_grav)
    if cen_grav['lcg'] < data_hydrostatic.iloc[dis_index]['minLcg (m)'] or\
        cen_grav['lcg'] > data_hydrostatic.iloc[dis_index]['maxLcg (m)']:
        return False
    
    if cen_grav['tcg'] < data_hydrostatic.iloc[dis_index]['minTcg (m)'] or\
        cen_grav['tcg'] > data_hydrostatic.iloc[dis_index]['maxTcg (m)']:
        return False
    #falta el vcg 
    return True
    
def calcular_esfuerzos_corte(data_buoyancy, bay, barco, dis_index):
    esfuerzo = barco.bays[bay].peso - data_buoyancy.iloc[dis_index][bay]
    return esfuerzo

def verificar_esfuerfos_de_corte(data_buoyancy, barco, dis_index):
    for bay in range(21):
        esfuezo = calcular_esfuerzos_corte(data_buoyancy, bay, barco, dis_index)
        if esfuezo > barco.bays[bay].max_esfuerzo_corte or\
            esfuezo < barco.bays[bay].min_esfuerzo_corte:
            return False
    return True