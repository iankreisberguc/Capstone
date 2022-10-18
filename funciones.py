from json.encoder import INFINITY
from operator import itemgetter

def verificar_factibilidad_fisica(data_hydrostatic, data_buoyancy, barco):
    #centro de G incompleto
    dis_index = calcular_displacemnt_index(data_hydrostatic, barco)
    if verificar_esfuerfos_de_corte(data_buoyancy, barco, dis_index) and\
        verificar_centro_de_dravedad(barco, data_hydrostatic, dis_index):
        return True
    else:
        return False

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

def verificar_centro_de_dravedad(barco, data_hydrostatic, dis_index):
    cen_grav = calcular_centro_masa(barco)
    print(cen_grav)
    if cen_grav['lcg'] < data_hydrostatic.iloc[dis_index]['minLcg (m)'] or\
        cen_grav['lcg'] > data_hydrostatic.iloc[dis_index]['maxLcg (m)']:
        return False
    
    if cen_grav['tcg'] < data_hydrostatic.iloc[dis_index]['minTcg (m)'] or\
        cen_grav['tcg'] > data_hydrostatic.iloc[dis_index]['maxTcg (m)']:
        return False
    #falta el vcg que no se como verificarlo
    return True

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
    print(f"Displacemnt index:", dis_index)
    return dis_index

def calcular_esfuerzos_corte(data_buoyancy, bay, barco, dis_index):
    esfuerzo = barco.bays[bay].peso - data_buoyancy.iloc[dis_index][bay]
    return esfuerzo

def verificar_esfuerfos_de_corte(data_buoyancy, barco, dis_index):
    for bay in range(20):
        esfuezo = calcular_esfuerzos_corte(data_buoyancy, bay, barco, dis_index)
        if esfuezo > barco.bays[bay].max_esfuerzo_corte or\
            esfuezo < barco.bays[bay].min_esfuerzo_corte:
            return False
    return True


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
def listar_over_stowage(barco):
    over_stowage_list = [] #[(bay, stack, tier, slot, valor, aux), (....),....]
    for bay in barco.bays:
        for stack in range(16):
            aux_0 = 12
            aux_1 = 12
            for tier in range(18):
                slots = bay.espacio[tier][stack]
                if slots[0] not in [0, 1, 2, None]:
                    if aux_0 < slots[0].end_port:
                        if slots[0].es_cargado == False:
                            info = (bay, stack, tier, 0, slots[0].valor,aux_0)
                            over_stowage_list.append(info)
                    elif aux_0 > slots[0].end_port:
                        aux_0 = slots[0].end_port          
                    if slots[0].largo != 40:
                        if slots[1] not in [0, 1, 2, None]:
                            if aux_1 < slots[1].end_port:
                                if slots[1].es_cargado == False:
                                    info = (bay, stack, tier, 1, slots[1].valor,aux_1)
                                    over_stowage_list.append(info) 
                            elif aux_1 > slots[1].end_port:
                                aux_1 = slots[1].end_port
        over_stowage_list = sorted(over_stowage_list, key = itemgetter(4))
    return over_stowage_list


def destruccion(barco, numero):
    lista = listar_over_stowage(barco)
    lista_repuesta = []
    for i in range(numero):
        if len(lista) == 0:
            ## Para el segundo criterio de destrucción
            return
        info = lista.pop(0)
        lista_repuesta.append(info)
        bay = info[0]
        cont = bay.espacio[info[2]][info[1]][info[3]]
        tipo = cont.tipo_slot
        bay.espacio[info[2]][info[1]][info[3]] = tipo
        print(bay.espacio[info[2]][info[1]][info[3]])
    return lista_repuesta
      
    
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
    peso_restante = [[200 for stack in range(16)], [250 for stack in range(16)]]
    contador_tier = 0
    for tier in bay.espacios:
        for stack in range(16):
            for container in tier[stack]:
                if container not in [0, 1, 2, None]:
                    if contador_tier < 9:
                        peso_restante[0][stack] -= container.peso
                    
                    if contador_tier > 9:
                        peso_restante[1][stack] -= container.peso
        contador_tier += 1
    return peso_restante
