from json.encoder import INFINITY

def verificar_factibilidad_fisica(data_hydrostatic, data_buoyancy,barco):
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
    centro_gravedad = {'lcg': 0, 'tcg': 0, 'vcg': 0}
    peso = 0
    for bay in barco.bays:
        for tier in bay.espacio:
            for slots in tier:
                for container in slots:
                    if container not in [0, 1, 2, None]:
                        aux_tcg = centro_gravedad['tcg']
                        aux_vcg = centro_gravedad['vcg']
                        centro_gravedad['tcg'] = (aux_tcg * peso + container.tcg * container.peso) / (peso + container.peso)
                        centro_gravedad['vcg'] = (aux_vcg * peso + container.vcg * container.peso) / (peso + container.peso)
                        peso += container.peso
        aux_lcg = centro_gravedad['lcg']
        aux_vcg = centro_gravedad['vcg']
        centro_gravedad['lcg'] = (aux_lcg * peso + bay.lcg * bay.peso) / (peso + bay.peso)
        centro_gravedad['vcg'] = (aux_vcg * peso + 15 * bay.peso) / (peso + bay.peso)
        peso += bay.peso
    
    return centro_gravedad

def verificar_centro_de_dravedad(barco, data_hydrostatic, dis_index):
    cen_grav = calcular_centro_masa(barco)
    
    if cen_grav['lcg'] < data_hydrostatic.iloc[dis_index]['minLcg (m)'] or\
        cen_grav['lcg'] > ata_hydrostatic.iloc[dis_index]['maxLcg (m)']:
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
    for bay in barco.bays:
        for stack in range(16):
            ya_revisados = []
            for i in range(18):
                aux = [None, None]
                if bay.espacio[i][stack][0] not in [0, 1, 2, None]:
                    if bay.espacio[i][stack][0].end_port not in ya_revisados:
                        aux[0] = bay.espacio[i][stack][0].end_port 
                        ya_revisados.append(aux[0])
                    
                if bay.espacio[i][stack][1] not in [0, 1, 2, None]:
                    if bay.espacio[i][stack][1].end_port not in ya_revisados:   
                        aux[1] = bay.espacio[i][stack][1].end_port
                        ya_revisados.append(aux[1])

                for tier in range(i + 1, 18):
                    slots = bay.espacio[tier][stack]
                    if slots[0] not in [0, 1, 2, None]:
                        if aux[0] != None:
                            if aux[0] < slots[0].end_port:
                                contador += 1                                 
                        if slots[0].largo == 40:
                            continue
                        
                    if slots[1] not in [0, 1, 2, None]:
                        if aux[1] != None:
                            if aux[1] < slots[1].end_port:
                                contador += 1
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