from operator import contains


def generar_espacios(data, barco):
    for index_data_slot, row_data_slot in data.iterrows():
        bay = int(row_data_slot['BAY'])
        stack = int(row_data_slot['STACK'])
        tier = int(row_data_slot['TIER'])
        barco.bays[bay].espacio[tier][stack][0] = 0
        barco.bays[bay].espacio[tier][stack][1] = 0

def calcular_centro_masa(barco):
    centro_gravedad = {'lcg': 0, 'tcg': 0, 'vcg': 0}
    peso = 0
    for bay in barco.bays:
        for tier in bay.espacio:
            for slots in tier:
                for container in slots:
                    if container != 0 and container != None:
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

def calcular_esfuerzos_corte(data_hydrostatic, data_buoyancy, bay):
    pass
    
def over_stowage(barco):
    contador = 0
    for bay in barco.bays:
        for stack in range(16):
            ya_revisados = []
            for i in range(18):
                aux = [None, None]
                if bay.espacio[i][stack][0] != None and bay.espacio[i][stack][0] != 0:
                    if bay.espacio[i][stack][0].end_port not in ya_revisados:
                        aux[0] = bay.espacio[i][stack][0].end_port 
                        ya_revisados.append(aux[0])
                    
                if bay.espacio[i][stack][1] != None and bay.espacio[i][stack][1] != 0:
                    if bay.espacio[i][stack][1].end_port not in ya_revisados:   
                        aux[1] = bay.espacio[i][stack][1].end_port
                        ya_revisados.append(aux[1])

                for tier in range(i + 1, 18):
                    slots = bay.espacio[tier][stack]
                    if slots[0] != 0 and slots[0] != None:
                        if aux[0] != None:
                            if aux[0] < slots[0].end_port:
                                contador += 1                                 
                        if slots[0].largo == 40:
                            continue
                        
                    if slots[1] != 0 and slots[1] != None:
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
                    if container != 0 and container != None:
                        valor += container.valor
    return valor

def maximo_peso(bay):
    peso_restante = [[200 for stack in range(16)], [250 for stack in range(16)]]
    contador_tier = 0
    for tier in bay.espacios:
        for stack in range(16):
            for container in tier[stack]:
                if container != 0 and container != None:
                    if contador_tier < 9:
                        peso_restante[0][stack] -= container.peso
                    
                    if contador_tier > 9:
                        peso_restante[1][stack] -= container.peso
        contador_tier += 1
    return peso_restante
                        

