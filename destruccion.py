from operator import itemgetter
from prueba_vcg import calcular_rangos_desarme
def destruccion(barco, numero):
    lista = listar_over_stowage(barco)
    lista_respuesta = []
    for i in range(numero):
        if len(lista) == 0:
            ## Para el segundo criterio de destrucción
            return
        info = lista.pop(0)
        lista_respuesta.append(info)
        bay = info[0]
        cont = bay.espacio[info[2]][info[1]][info[3]]
        tipo = cont.tipo_slot
        bay.espacio[info[2]][info[1]][info[3]] = tipo
        # print(bay.espacio[info[2]][info[1]][info[3]])
    return lista_respuesta

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


def destruir_overstowage(barco, data_slot, cargados, rango_bay,rango_stack):
    contador = 0
    for bay in rango_bay:
        for stack in rango_stack:
            aux = 12
            for tier in range(18):
                for slot in barco.bays[bay].espacio[tier][stack]:
                    if slot not in [0, 1, 2, None]:
                        if aux < slot.end_port:
                            contador += 1 
                            for tier1 in range(tier,18):
                                for slot in barco.bays[bay].espacio[tier1][stack]:
                                    if slot not in [0, 1, 2, None]:
                                        if not slot.es_cargado:
                                            cargados.remove(slot.index)
                                            data = data_slot[(data_slot.BAY==bay) & (data_slot.STACK==stack) & (data_slot.TIER==tier1) & (data_slot.SLOT==1)]
                                            #print(data)
                                            #print(data.REEFER)
                                            refrigerado = data.REEFER.item()
                                            carga_peligrosa = data.DA.item()

                                            barco.bays[bay].espacio[tier1][stack][0] = 0 + refrigerado
                                            barco.bays[bay].espacio[tier1][stack][1] = 0 + refrigerado

                                            if carga_peligrosa == 0:
                                                barco.bays[bay].espacio[tier1][stack][0] += 2
                                                barco.bays[bay].espacio[tier1][stack][1] += 2

                                           
                            
                        elif aux > slot.end_port:
                            aux = slot.end_port  
                            continue                  
    return