from clases import Container
from funciones import calcular_displacemnt_index, calcular_centro_masa, maximo_peso

def cargar (data, data_slot, barco, cargados, data_hydrostatic, data_buoyancy):    
    data = data[data["WEIGHT (ton)"] > 9]
    contador_infactible = 0
    contador_iteraciones = 0
    maximo_infactible = 50
    estado = 1

    rango_bay, rango_stack = calcular_rangos (barco, estado) 
    pesos_admitibles_bays = calcular_pesos_bays(barco, data_hydrostatic, data_buoyancy)

    while True:
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

    elif tipo == "DG":
        tipo_espacio = [1, 2]

    else:
        tipo_espacio = [0, 1, 2]

    for bay in rango_bay:
        if peso_admitibles_bay[bay] - peso >= 0:
            peso_restante, tiene_largo20 = maximo_peso(barco.bays[bay])
            for tier in range(18):
                if tier < 9:
                    cubierta = 0
                else:
                    cubierta = 1
                for stack in rango_stack:
                    if peso_restante[cubierta][stack] - peso >= 0:
                        if barco.bays[bay].espacio[tier][stack][0] in tipo_espacio:
                            tcg = float(data_slot[(data_slot.BAY==bay) & (data_slot.STACK==stack) & (data_slot.TIER==tier) & (data_slot.SLOT==1)].TCG)
                            vcg = float(data_slot[(data_slot.BAY==bay) & (data_slot.STACK==stack) & (data_slot.TIER==tier) & (data_slot.SLOT==1)].VCG)
                            container = Container(peso, tipo, valor, end_port, largo, tcg, vcg, es_cargado)
                            barco.bays[bay].espacio[tier][stack][0] = container
                            cargados.append(index)
                            peso_admitibles_bay[bay] -= peso
                            return True

                        elif barco.bays[bay].espacio[tier][stack][0] not in [0, 1, 2, None]:
                            if barco.bays[bay].espacio[tier][stack][0].largo != 40 and barco.bays[bay].espacio[tier][stack][1] in tipo_espacio and largo == 20:
                                tcg = float(data_slot[(data_slot.BAY==bay) & (data_slot.STACK==stack) & (data_slot.TIER==tier) & (data_slot.SLOT==1)].TCG)
                                vcg = float(data_slot[(data_slot.BAY==bay) & (data_slot.STACK==stack) & (data_slot.TIER==tier) & (data_slot.SLOT==1)].VCG)
                                container = Container(peso, tipo, valor, end_port, largo, tcg, vcg, es_cargado)
                                barco.bays[bay].espacio[tier][stack][0] = container 
                                cargados.append(index)
                                peso_admitibles_bay[bay] -= peso
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