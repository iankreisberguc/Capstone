from matplotlib.pyplot import bar
import pandas as pd
from clases import Container
from funciones import maximo_peso, bending

def movimiento_contenedores(barco, contador, data_slot, data_loaded, data_barco, data_hydrostatic, data_buoyancy):
    df_movidos = None
    valor_maximo = 9
    while True:
        for bay in range(11):
            for stack in range(16):
                for tier in range(18):
                    if barco.bays[bay].espacio[tier][stack][0] not in [0, 1, 2, None]:
                        suma_peso = barco.bays[bay].espacio[tier][stack][0].peso
                        if barco.bays[bay].espacio[tier][stack][1] not in [0, 1, 2, None]:
                            suma_peso += barco.bays[bay].espacio[tier][stack][1].peso
                        if suma_peso <= valor_maximo:
                            data_container = data_loaded[(data_loaded.BAY==bay) & (data_loaded.STACK==stack) & (data_loaded.TIER==tier)]
                            df_movidos = pd.concat([df_movidos, data_container], axis=0)

                            data = data_slot[(data_slot.BAY==bay) & (data_slot.STACK==stack) & (data_slot.TIER==tier) & (data_slot.SLOT==1)]
                            refrigerado = data.REEFER.item()
                            carga_peligrosa = data.DA.item()

                            barco.bays[bay].espacio[tier][stack][0] = 0 + refrigerado
                            barco.bays[bay].espacio[tier][stack][1] = 0 + refrigerado

                            if carga_peligrosa == 0:
                                barco.bays[bay].espacio[tier][stack][0] += 2
                                barco.bays[bay].espacio[tier][stack][1] += 2
        break
    
    for bay in range(11):
        primera, segunda = maximo_peso(barco.bays[bay])
        for stack in range(16):
            if primera[0][stack] < 0:
                for tier in [8 - x for x in range(9)]:
                    if barco.bays[bay].espacio[tier][stack][0] not in [0, 1, 2, None]:
                        data_container = data_loaded[(data_loaded.BAY==bay) & (data_loaded.STACK==stack) & (data_loaded.TIER==tier)]
                        df_movidos = pd.concat([df_movidos, data_container], axis=0)
                        
                        data = data_slot[(data_slot.BAY==bay) & (data_slot.STACK==stack) & (data_slot.TIER==tier) & (data_slot.SLOT==1)]
                        refrigerado = data.REEFER.item()
                        carga_peligrosa = data.DA.item()

                        barco.bays[bay].espacio[tier][stack][0] = 0 + refrigerado
                        barco.bays[bay].espacio[tier][stack][1] = 0 + refrigerado

                        if carga_peligrosa == 0:
                            barco.bays[bay].espacio[tier][stack][0] += 2
                            barco.bays[bay].espacio[tier][stack][1] += 2

                        primera[0][stack] += data_container.head(1)['WEIGHT (ton)'].item()

                    if primera[0][stack] >= 0: break
                             
            if primera[1][stack] < 0:
                for tier in [17 - x for x in range(8)]:
                    if barco.bays[bay].espacio[tier][stack][0] not in [0, 1, 2, None]:
                        data_container = data_loaded[(data_loaded.BAY==bay) & (data_loaded.STACK==stack) & (data_loaded.TIER==tier)]
                        df_movidos = pd.concat([df_movidos, data_container], axis=0)
                        
                        data = data_slot[(data_slot.BAY==bay) & (data_slot.STACK==stack) & (data_slot.TIER==tier) & (data_slot.SLOT==1)]
                        refrigerado = data.REEFER.item()
                        carga_peligrosa = data.DA.item()

                        barco.bays[bay].espacio[tier][stack][0] = 0 + refrigerado
                        barco.bays[bay].espacio[tier][stack][1] = 0 + refrigerado

                        if carga_peligrosa == 0:
                            barco.bays[bay].espacio[tier][stack][0] += 2
                            barco.bays[bay].espacio[tier][stack][1] += 2
                        
                        primera[1][stack] += data_container.head(1)['WEIGHT (ton)'].item()

                    if primera[1][stack] >= 0: break

    contador_movidos = len(df_movidos)

    df_movidos = df_movidos.groupby("END_PORT", \
    group_keys=False).apply(lambda x: x).sort_values(by=["END_PORT", "WEIGHT (ton)"], ascending=False)

    df_movidos20 = df_movidos[df_movidos['LENGTH (ft)'] == 20]
    df_movidos40 = df_movidos[df_movidos['LENGTH (ft)'] == 40]
    
    for bay in [20 - x for x in range(0, 10)]:
        #max_bending = bending(barco, bay, data_barco, data_hydrostatic, data_buoyancy)
        for stack in range(16):
            for tier in [x for x in range(8)]+[x for x in range(10, 17)]:
                if barco.bays[bay].espacio[tier][stack][0] != None:
                    slot = 0
                    for index, row in df_movidos20.iterrows():
                        tipo = row['TYPE']
                        peso = row['WEIGHT (ton)']
                        # if max_bending - peso*barco.bays[bay].lcg < 0:
                        #     break
                        if (tipo == 'RC' and barco.bays[bay].espacio[tier][stack][slot] == 1) or tipo == 'DC':
                            valor = 0
                            es_cargado = True
                            end_port = row['END_PORT']
                            largo = row['LENGTH (ft)']
                            tcg = float(data_slot[(data_slot.BAY==bay) & (data_slot.STACK==stack) & (data_slot.TIER==tier) & (data_slot.SLOT==1)].TCG)
                            vcg = float(data_slot[(data_slot.BAY==bay) & (data_slot.STACK==stack) & (data_slot.TIER==tier) & (data_slot.SLOT==1)].VCG)
                            container = Container(peso, tipo, valor, end_port, largo, tcg, vcg, es_cargado)
                            
                            aux = barco.bays[bay].espacio[tier][stack][slot]
                            barco.bays[bay].espacio[tier][stack][slot] = container
                            container.tipo_slot = aux   

                            df_movidos20 =  df_movidos20.drop(index = index)
                            #max_bending -= peso*barco.bays[bay].lcg
                            slot += 1
                            if slot == 2:
                                break
    
    for bay in [20 - x for x in range(0, 10)]:
        #max_bending = bending(barco, bay, data_barco, data_hydrostatic, data_buoyancy)
        for stack in range(16):
            for tier in range(18):
                if barco.bays[bay].espacio[tier][stack][0] != None:
                    for index, row in df_movidos40.iterrows():
                        tipo = row['TYPE']
                        peso = row['WEIGHT (ton)']
                        # if max_bending - (peso + barco.bays[bay].peso)*abs(barco.bays[bay].lcg) < 0:
                        #     break
                        if (tipo == 'RC' and barco.bays[bay].espacio[tier][stack][slot] == 1) or tipo == 'DC':
                            valor = 0
                            es_cargado = True
                            end_port = row['END_PORT']
                            largo = row['LENGTH (ft)']
                            tcg = float(data_slot[(data_slot.BAY==bay) & (data_slot.STACK==stack) & (data_slot.TIER==tier) & (data_slot.SLOT==1)].TCG)
                            vcg = float(data_slot[(data_slot.BAY==bay) & (data_slot.STACK==stack) & (data_slot.TIER==tier) & (data_slot.SLOT==1)].VCG)
                            container = Container(peso, tipo, valor, end_port, largo, tcg, vcg, es_cargado)
                            
                            aux = barco.bays[bay].espacio[tier][stack][0]
                            barco.bays[bay].espacio[tier][stack][0] = container
                            container.tipo_slot = aux   

                            #max_bending -= abs(peso*barco.bays[bay].lcg)
                            df_movidos40 =  df_movidos40.drop(index = index)
                            break
    
    return contador_movidos