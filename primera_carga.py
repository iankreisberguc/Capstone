from clases import Container
from funciones import calcular_displacemnt_index, calcular_centro_masa, maximo_peso
import pandas as pd

def cargar (data, data_slot, barco, cargados, data_hydrostatic, data_buoyancy):    
    # data_RC = data_RC[data_RC["WEIGHT (ton)"] > 9]
    # data_noRC = data_noRC[data_noRC["WEIGHT (ton)"] > 9]
    data = data[data["WEIGHT (ton)"] > 9]
    contador_infactible = 0
    contador_iteraciones = 0
    maximo_infactible = 50
    estado = 1

    rango_bay, rango_stack = calcular_rangos (barco, estado) 
    pesos_admitibles_bays = calcular_pesos_bays(barco, data_hydrostatic, data_buoyancy)

    while True:
        # for index, row in data_RC.iterrows():
        #     if index not in cargados:
        #         # contador += 1
        #         agregado = colocar_contenedor (rango_bay, rango_stack, barco, data_slot, row, cargados, index, pesos_admitibles_bays)

        #         if agregado:
        #             contador_iteraciones += 1
        #             contador_infactible = 0

        #         elif agregado == False:
        #             contador_infactible += 1

        #         if estado == 1 and contador_infactible > maximo_infactible:
        #             estado += 1
        #             contador_infactible = 0

        #         if contador_infactible > maximo_infactible and estado == 2:
        #             print('Terminamos')
        #             return
                
        #         if contador_infactible == 20:
        #             rango_bay, rango_stack = calcular_rangos (barco, estado)
        #             print(f"Cambiamos los rangos por infactivilidad {rango_bay}, {rango_stack}, con estado {estado}")
        #             pesos_admitibles_bays = calcular_pesos_bays(barco, data_hydrostatic, data_buoyancy)
        #             print(pesos_admitibles_bays)
        #             if rango_bay == False:
        #                 print('Terminamos rey')
        #                 return

        #         if contador_iteraciones > 50:
        #             estado = 1
        #             rango_bay, rango_stack = calcular_rangos (barco, estado)
        #             print(f"Cambiamos los rangos rudimentariamente {rango_bay}, {rango_stack}")
        #             contador_iteraciones = 0
        #             pesos_admitibles_bays = calcular_pesos_bays(barco, data_hydrostatic, data_buoyancy)
        #             print(pesos_admitibles_bays)

                # if agregado:
                #     contador_iteraciones += 1

                # if contador_iteraciones > 50:
                #     print(f"Cambiamos los rangos")
                #     print(rango_bay, rango_stack)
                #     rango_bay, rango_stack = calcular_rangos (barco, estado)
                #     print(rango_bay, rango_stack)
                #     contador_iteraciones = 0

        for index, row in data.iterrows():
            if index not in cargados:
                agregado = colocar_contenedor (rango_bay, rango_stack, barco, data_slot, row, cargados, index, pesos_admitibles_bays)

                if agregado:
                    contador_iteraciones += 1
                    contador_infactible = 0

                elif agregado == False:
                    contador_infactible += 1

                if estado == 1 and contador_infactible > maximo_infactible:
                    estado += 1
                    contador_infactible = 0

                if contador_infactible > maximo_infactible and estado == 2:
                    print('Terminamos')
                    return
                
                if contador_infactible == 20:
                    rango_bay, rango_stack = calcular_rangos (barco, estado)
                    print(f"Cambiamos los rangos por infactivilidad {rango_bay}, {rango_stack}, con estado {estado}")
                    pesos_admitibles_bays = calcular_pesos_bays(barco, data_hydrostatic, data_buoyancy)
                    print(pesos_admitibles_bays)
                    if rango_bay == False:
                        print('Terminamos rey')
                        return

                if contador_iteraciones > 50:
                    estado = 1
                    rango_bay, rango_stack = calcular_rangos (barco, estado)
                    print(f"Cambiamos los rangos rudimentariamente {rango_bay}, {rango_stack}")
                    contador_iteraciones = 0
                    pesos_admitibles_bays = calcular_pesos_bays(barco, data_hydrostatic, data_buoyancy)
                    print(pesos_admitibles_bays)

def colocar_contenedor (rango_bay, rango_stack, barco, data_slot, row, cargados, index, peso_admitibles_bay):
    peso = row['WEIGHT (ton)']
    tipo = row['TYPE']
    valor = row['VALUE (USD)']
    es_cargado = False
    end_port = row['END_PORT']
    largo = row['LENGTH (ft)']

    if tipo == "RC":
        tipo_espacio = [1]
        # lista_no_tipo = [0, 2, None]

    elif tipo == "DG":
        tipo_espacio = [1, 2]
        # lista_no_tipo = [0, None]

    else:
        tipo_espacio = [0, 1, 2]
        # lista_no_tipo = [None]


    for bay in rango_bay:
        if peso_admitibles_bay[bay] - peso >= 0:
            peso_restante, tiene_largo20 = maximo_peso(barco.bays[bay])
            for tier in range(18):
                if tier < 9:
                    cubierta = 0
                else:
                    cubierta = 1
                for stack in rango_stack:
                    # if (not tiene_largo20[cubierta][stack]) and (largo == 20):
                    #     peso = peso + 100
                    # if peso_admitibles_bay[bay] - peso >= 0:
                    # if peso_restante[cubierta][stack] - peso < 0:
                    #     print(f"Ojo con este peso qlo {peso_restante[cubierta][stack]}, {peso}, {tiene_largo20[cubierta][stack]}")
                    if peso_restante[cubierta][stack] - peso >= 0:
                        # print(f'Peso admitible: {peso_admitibles_bay[bay]} vs peso contenedor: {peso}')
                        if barco.bays[bay].espacio[tier][stack][0] in tipo_espacio:
                            tcg = float(data_slot[(data_slot.BAY==bay) & (data_slot.STACK==stack) & (data_slot.TIER==tier) & (data_slot.SLOT==1)].TCG)
                            vcg = float(data_slot[(data_slot.BAY==bay) & (data_slot.STACK==stack) & (data_slot.TIER==tier) & (data_slot.SLOT==1)].VCG)
                            container = Container(peso, tipo, valor, end_port, largo, tcg, vcg, es_cargado)
                            barco.bays[bay].espacio[tier][stack][0] = container
                            cargados.append(index)
                            peso_admitibles_bay[bay] -= peso
                            # print(f'Peso admitible: {peso_admitibles_bay[bay]} vs peso contenedor: {peso}')
                            return True

                        elif barco.bays[bay].espacio[tier][stack][0] not in [0, 1, 2, None]:
                            # if barco.bays[bay].espacio[tier][stack][0].largo != 40 and (barco.bays[bay].espacio[tier][stack][1] == tipo_espacio or barco.bays[bay].espacio[tier][stack][0] == tipo_espacio + 2) and largo == 20:
                            if barco.bays[bay].espacio[tier][stack][0].largo != 40 and barco.bays[bay].espacio[tier][stack][1] in tipo_espacio and largo == 20:
                                tcg = float(data_slot[(data_slot.BAY==bay) & (data_slot.STACK==stack) & (data_slot.TIER==tier) & (data_slot.SLOT==1)].TCG)
                                vcg = float(data_slot[(data_slot.BAY==bay) & (data_slot.STACK==stack) & (data_slot.TIER==tier) & (data_slot.SLOT==1)].VCG)
                                container = Container(peso, tipo, valor, end_port, largo, tcg, vcg, es_cargado)
                                barco.bays[bay].espacio[tier][stack][0] = container 
                                cargados.append(index)
                                peso_admitibles_bay[bay] -= peso
                                # print(f'Peso admitible: {peso_admitibles_bay[bay]} vs peso contenedor: {peso}')
                                return True
                
    if tipo == "RC": 
        return None
    else:
        return False

def calcular_pesos_bays (barco, data_hydrostatic, data_buoyancy):
    pesos_admitibles = list()
    dis_index = calcular_displacemnt_index(data_hydrostatic, barco)
    for bay in range(21):
        esfuezo = barco.bays[bay].peso - data_buoyancy.iloc[dis_index][bay]
        peso_admitible = barco.bays[bay].max_esfuerzo_corte - esfuezo 
        pesos_admitibles.append(peso_admitible)
    return pesos_admitibles

def calcular_rangos (barco, estado):
    centro_gravedad = calcular_centro_masa(barco)
    print(centro_gravedad)

    if abs(centro_gravedad["tcg"]) > abs(centro_gravedad["lcg"]) and estado == 1:
        tipo = "tcg"

    elif abs(centro_gravedad["tcg"]) < abs(centro_gravedad["lcg"]) and estado == 2:
        if abs(centro_gravedad["lcg"]) < 3:
            tipo = "tcg"
        else: 
            return False, False

    elif abs(centro_gravedad["tcg"]) < abs(centro_gravedad["lcg"]) and estado == 1:
        tipo = "lcg"

    elif abs(centro_gravedad["tcg"]) > abs(centro_gravedad["lcg"]) and estado == 2:
        if abs(centro_gravedad["tcg"]) < 2:
            tipo = "lcg"
        else: 
            return False, False

    if tipo == "tcg":
        rango_bay = [10, 9, 11, 8, 12, 7, 13, 6, 14, 5, 15, 4, 16, 3, 17, 2, 18, 1, 19, 0, 20]
        if  centro_gravedad["tcg"] > 0:
            rango_stack = [7 - x for x in range(0, 8)]
            print('Se carga en el cuadrante 2 y 3')

        else:
            rango_stack = range(8, 15)
            print('Se carga en el cuadrante 1 y 4')

    else:
        rango_stack = [8, 7, 9, 6, 10, 5, 11, 4, 12, 3, 13, 2, 14, 1, 15, 0]
        if  centro_gravedad["lcg"] > 0:
            rango_bay = range(11, 21)
            print('Se carga en el cuadrante 3 y 4')

        else:
            rango_bay = [10 - x for x in range(0, 11)] 
            print('Se carga en el cuadrante 1 y 2')
        
    return rango_bay, rango_stack


# def crear_primera_solucion (data_prueba, data_slot, barco):
    
#     data_RC = data_prueba[data_prueba["TYPE"] == "RC"]
#     data_DG = data_prueba[data_prueba["TYPE"] == "DG"]
#     data_DC = data_prueba[data_prueba["TYPE"] == "DC"]

#     contador_bay = 0
#     contador_carga = 0

#     contador_RC = 0
#     contador_DG = 0
#     contador_DC = 0
#     for bay in barco.bays:
#         contador_tier = 0
#         for tier in bay.espacio:
#             contador_stack = 0
#             for slot in tier:
#                 for contenedor in slot:
#                     if slot[0] in [0,1,2] and slot[1] in [0,1,2]:
#                         #verificar con contenedor in....
#                         if contenedor == 1 and contador_RC < len(data_RC):
#                             peso = data_RC.iloc[contador_RC]['WEIGHT (ton)']
#                             tipo = data_RC.iloc[contador_RC]['TYPE']
#                             valor = data_RC.iloc[contador_RC]['VALUE (USD)']
#                             es_cargado = False
#                             end_port = data_RC.iloc[contador_RC]['END_PORT']
#                             largo = data_RC.iloc[contador_RC]['LENGTH (ft)']
#                             tcg = float(data_slot[(data_slot.BAY==contador_bay) & (data_slot.STACK==contador_stack) & (data_slot.TIER==contador_tier) & (data_slot.SLOT==1)].TCG)
#                             vcg = float(data_slot[(data_slot.BAY==contador_bay) & (data_slot.STACK==contador_stack) & (data_slot.TIER==contador_tier) & (data_slot.SLOT==1)].VCG)
#                             contenedor = Container(peso, tipo, valor, end_port, largo, tcg, vcg, es_cargado)
#                             barco.bays[contador_bay].espacio[contador_tier][contador_stack][0] = contenedor
#                             contador_RC += 1
#                             contador_carga += 1
                    
#                         elif contenedor == 2 and contador_DG < len(data_DG):
#                             peso = data_DG.iloc[contador_DG]['WEIGHT (ton)']
#                             tipo = data_DG.iloc[contador_DG]['TYPE']
#                             valor = data_DG.iloc[contador_DG]['VALUE (USD)']
#                             es_cargado = False
#                             end_port = data_DG.iloc[contador_DG]['END_PORT']
#                             largo = data_DG.iloc[contador_DG]['LENGTH (ft)']
#                             tcg = float(data_slot[(data_slot.BAY==contador_bay) & (data_slot.STACK==contador_stack) & (data_slot.TIER==contador_tier) & (data_slot.SLOT==1)].TCG)
#                             vcg = float(data_slot[(data_slot.BAY==contador_bay) & (data_slot.STACK==contador_stack) & (data_slot.TIER==contador_tier) & (data_slot.SLOT==1)].VCG)
#                             contenedor = Container(peso, tipo, valor, end_port, largo, tcg, vcg, es_cargado)
#                             barco.bays[contador_bay].espacio[contador_tier][contador_stack][0] = contenedor
#                             contador_DG += 1
#                             contador_carga += 1
                    
#                         elif contador_DC < len(data_DC):
#                             peso = data_DC.iloc[contador_DC]['WEIGHT (ton)']
#                             tipo = data_DC.iloc[contador_DC]['TYPE']
#                             valor = data_DC.iloc[contador_DC]['VALUE (USD)']
#                             es_cargado = False
#                             end_port = data_DC.iloc[contador_DC]['END_PORT']
#                             largo = data_DC.iloc[contador_DC]['LENGTH (ft)']
#                             tcg = float(data_slot[(data_slot.BAY==contador_bay) & (data_slot.STACK==contador_stack) & (data_slot.TIER==contador_tier) & (data_slot.SLOT==1)].TCG)
#                             vcg = float(data_slot[(data_slot.BAY==contador_bay) & (data_slot.STACK==contador_stack) & (data_slot.TIER==contador_tier) & (data_slot.SLOT==1)].VCG)
#                             contenedor = Container(peso, tipo, valor, end_port, largo, tcg, vcg, es_cargado)
#                             barco.bays[contador_bay].espacio[contador_tier][contador_stack][0] = contenedor
#                             contador_DC += 1
#                             contador_carga += 1

#                     elif slot[0] in [0,1,2] and slot[1] !=None:
#                         if slot[1].largo != 40:
#                             if contenedor == 1 and contador_RC < len(data_RC):
#                                 peso = data_RC.iloc[contador_RC]['WEIGHT (ton)']
#                                 tipo = data_RC.iloc[contador_RC]['TYPE']
#                                 valor = data_RC.iloc[contador_RC]['VALUE (USD)']
#                                 es_cargado = False
#                                 end_port = data_RC.iloc[contador_RC]['END_PORT']
#                                 largo = data_RC.iloc[contador_RC]['LENGTH (ft)']
#                                 tcg = float(data_slot[(data_slot.BAY==contador_bay) & (data_slot.STACK==contador_stack) & (data_slot.TIER==contador_tier) & (data_slot.SLOT==1)].TCG)
#                                 vcg = float(data_slot[(data_slot.BAY==contador_bay) & (data_slot.STACK==contador_stack) & (data_slot.TIER==contador_tier) & (data_slot.SLOT==1)].VCG)
#                                 contenedor = Container(peso, tipo, valor, end_port, largo, tcg, vcg, es_cargado)
#                                 barco.bays[contador_bay].espacio[contador_tier][contador_stack][0] = contenedor
#                                 contador_RC += 1
#                                 contador_carga += 1
                        
#                             elif contenedor == 2 and contador_DG < len(data_DG):
#                                 peso = data_DG.iloc[contador_DG]['WEIGHT (ton)']
#                                 tipo = data_DG.iloc[contador_DG]['TYPE']
#                                 valor = data_DG.iloc[contador_DG]['VALUE (USD)']
#                                 es_cargado = False
#                                 end_port = data_DG.iloc[contador_DG]['END_PORT']
#                                 largo = data_DG.iloc[contador_RC]['LENGTH (ft)']
#                                 tcg = float(data_slot[(data_slot.BAY==contador_bay) & (data_slot.STACK==contador_stack) & (data_slot.TIER==contador_tier) & (data_slot.SLOT==1)].TCG)
#                                 vcg = float(data_slot[(data_slot.BAY==contador_bay) & (data_slot.STACK==contador_stack) & (data_slot.TIER==contador_tier) & (data_slot.SLOT==1)].VCG)
#                                 contenedor = Container(peso, tipo, valor, end_port, largo, tcg, vcg, es_cargado)
#                                 barco.bays[contador_bay].espacio[contador_tier][contador_stack][0] = contenedor
#                                 contador_DG += 1
#                                 contador_carga += 1
                            
#                             elif contador_DC < len(data_DC):
#                                 peso = data_DC.iloc[contador_DC]['WEIGHT (ton)']
#                                 tipo = data_DC.iloc[contador_DC]['TYPE']
#                                 valor = data_DC.iloc[contador_DC]['VALUE (USD)']
#                                 es_cargado = False
#                                 end_port = data_DC.iloc[contador_DC]['END_PORT']
#                                 largo = data_DC.iloc[contador_DC]['LENGTH (ft)']
#                                 tcg = float(data_slot[(data_slot.BAY==contador_bay) & (data_slot.STACK==contador_stack) & (data_slot.TIER==contador_tier) & (data_slot.SLOT==1)].TCG)
#                                 vcg = float(data_slot[(data_slot.BAY==contador_bay) & (data_slot.STACK==contador_stack) & (data_slot.TIER==contador_tier) & (data_slot.SLOT==1)].VCG)
#                                 contenedor = Container(peso, tipo, valor, end_port, largo, tcg, vcg, es_cargado)
#                                 barco.bays[contador_bay].espacio[contador_tier][contador_stack][0] = contenedor
#                                 contador_DC += 1
#                                 contador_carga += 1

#                     elif slot[1] in [0,1,2] and slot[0] != None:
#                         if slot[0].largo != 40:
#                             if contenedor == 1 and contador_RC < len(data_RC):
#                                 peso = data_RC.iloc[contador_RC]['WEIGHT (ton)']
#                                 tipo = data_RC.iloc[contador_RC]['TYPE']
#                                 valor = data_RC.iloc[contador_RC]['VALUE (USD)']
#                                 es_cargado = False
#                                 end_port = data_RC.iloc[contador_RC]['END_PORT']
#                                 largo = data_RC.iloc[contador_RC]['LENGTH (ft)']
#                                 tcg = float(data_slot[(data_slot.BAY==contador_bay) & (data_slot.STACK==contador_stack) & (data_slot.TIER==contador_tier) & (data_slot.SLOT==1)].TCG)
#                                 vcg = float(data_slot[(data_slot.BAY==contador_bay) & (data_slot.STACK==contador_stack) & (data_slot.TIER==contador_tier) & (data_slot.SLOT==1)].VCG)
#                                 contenedor = Container(peso, tipo, valor, end_port, largo, tcg, vcg, es_cargado)
#                                 barco.bays[contador_bay].espacio[contador_tier][contador_stack][1] = contenedor
#                                 contador_RC += 1
#                                 contador_carga += 1
                        
#                             elif contenedor == 2 and contador_DG < len(data_DG):
#                                 peso = data_DG.iloc[contador_DG]['WEIGHT (ton)']
#                                 tipo = data_DG.iloc[contador_DG]['TYPE']
#                                 valor = data_DG.iloc[contador_DG]['VALUE (USD)']
#                                 es_cargado = False
#                                 end_port = data_DG.iloc[contador_DG]['END_PORT']
#                                 largo = data_DG.iloc[contador_RC]['LENGTH (ft)']
#                                 tcg = float(data_slot[(data_slot.BAY==contador_bay) & (data_slot.STACK==contador_stack) & (data_slot.TIER==contador_tier) & (data_slot.SLOT==1)].TCG)
#                                 vcg = float(data_slot[(data_slot.BAY==contador_bay) & (data_slot.STACK==contador_stack) & (data_slot.TIER==contador_tier) & (data_slot.SLOT==1)].VCG)
#                                 contenedor = Container(peso, tipo, valor, end_port, largo, tcg, vcg, es_cargado)
#                                 barco.bays[contador_bay].espacio[contador_tier][contador_stack][1] = contenedor
#                                 contador_DG += 1
#                                 contador_carga += 1
                            
#                             elif contador_DC < len(data_DC):
#                                 peso = data_DC.iloc[contador_DC]['WEIGHT (ton)']
#                                 tipo = data_DC.iloc[contador_DC]['TYPE']
#                                 valor = data_DC.iloc[contador_DC]['VALUE (USD)']
#                                 es_cargado = False
#                                 end_port = data_DC.iloc[contador_DC]['END_PORT']
#                                 largo = data_DC.iloc[contador_DC]['LENGTH (ft)']
#                                 tcg = float(data_slot[(data_slot.BAY==contador_bay) & (data_slot.STACK==contador_stack) & (data_slot.TIER==contador_tier) & (data_slot.SLOT==1)].TCG)
#                                 vcg = float(data_slot[(data_slot.BAY==contador_bay) & (data_slot.STACK==contador_stack) & (data_slot.TIER==contador_tier) & (data_slot.SLOT==1)].VCG)
#                                 contenedor = Container(peso, tipo, valor, end_port, largo, tcg, vcg, es_cargado)
#                                 barco.bays[contador_bay].espacio[contador_tier][contador_stack][1] = contenedor
#                                 contador_DC += 1
#                                 contador_carga += 1
#                 contador_stack += 1
#             contador_tier += 1
#         contador_bay += 1 

#     print(f"Contador RC", contador_RC)
#     print(f"de un total de:", len(data_RC))
#     print(f"Contador DG", contador_DG)
#     print(f"de un total de:", len(data_DG))
#     print(f"Contador DC", contador_DC)
#     print(f"de un total de:", len(data_DC))
#     return contador_carga
    


