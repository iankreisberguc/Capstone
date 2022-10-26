from operator import itemgetter

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