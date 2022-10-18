from clases import Container
from funciones import verificar_factibilidad_fisica
import pandas as pd

def crear_primera_solucion (data_prueba, data_slot, barco):
    
    data_RC = data_prueba[data_prueba["TYPE"] == "RC"]
    data_DG = data_prueba[data_prueba["TYPE"] == "DG"]
    data_DC = data_prueba[data_prueba["TYPE"] == "DC"]

    contador_bay = 0
    contador_carga = 0

    contador_RC = 0
    contador_DG = 0
    contador_DC = 0
    for bay in barco.bays:
        contador_tier = 0
        for tier in bay.espacio:
            contador_stack = 0
            for slot in tier:
                for contenedor in slot:
                    if slot[0] in [0,1,2] and slot[1] in [0,1,2]:
                        #verificar con contenedor in....
                        if contenedor == 1 and contador_RC < len(data_RC):
                            peso = data_RC.iloc[contador_RC]['WEIGHT (ton)']
                            tipo = data_RC.iloc[contador_RC]['TYPE']
                            valor = data_RC.iloc[contador_RC]['VALUE (USD)']
                            es_cargado = False
                            end_port = data_RC.iloc[contador_RC]['END_PORT']
                            largo = data_RC.iloc[contador_RC]['LENGTH (ft)']
                            tcg = float(data_slot[(data_slot.BAY==contador_bay) & (data_slot.STACK==contador_stack) & (data_slot.TIER==contador_tier) & (data_slot.SLOT==1)].TCG)
                            vcg = float(data_slot[(data_slot.BAY==contador_bay) & (data_slot.STACK==contador_stack) & (data_slot.TIER==contador_tier) & (data_slot.SLOT==1)].VCG)
                            contenedor = Container(peso, tipo, valor, end_port, largo, tcg, vcg, es_cargado)
                            aux = barco.bays[contador_bay].espacio[contador_tier][contador_stack][0]
                            barco.bays[contador_bay].espacio[contador_tier][contador_stack][0] = contenedor
                            contenedor.tipo_slot = aux
                            contador_RC += 1
                            contador_carga += 1
                    
                        elif contenedor == 2 and contador_DG < len(data_DG):
                            peso = data_DG.iloc[contador_DG]['WEIGHT (ton)']
                            tipo = data_DG.iloc[contador_DG]['TYPE']
                            valor = data_DG.iloc[contador_DG]['VALUE (USD)']
                            es_cargado = False
                            end_port = data_DG.iloc[contador_DG]['END_PORT']
                            largo = data_DG.iloc[contador_DG]['LENGTH (ft)']
                            tcg = float(data_slot[(data_slot.BAY==contador_bay) & (data_slot.STACK==contador_stack) & (data_slot.TIER==contador_tier) & (data_slot.SLOT==1)].TCG)
                            vcg = float(data_slot[(data_slot.BAY==contador_bay) & (data_slot.STACK==contador_stack) & (data_slot.TIER==contador_tier) & (data_slot.SLOT==1)].VCG)
                            contenedor = Container(peso, tipo, valor, end_port, largo, tcg, vcg, es_cargado)
                            aux = barco.bays[contador_bay].espacio[contador_tier][contador_stack][0]
                            barco.bays[contador_bay].espacio[contador_tier][contador_stack][0] = contenedor
                            contenedor.tipo_slot = aux
                            contador_DG += 1
                            contador_carga += 1
                    
                        elif contador_DC < len(data_DC):
                            peso = data_DC.iloc[contador_DC]['WEIGHT (ton)']
                            tipo = data_DC.iloc[contador_DC]['TYPE']
                            valor = data_DC.iloc[contador_DC]['VALUE (USD)']
                            es_cargado = False
                            end_port = data_DC.iloc[contador_DC]['END_PORT']
                            largo = data_DC.iloc[contador_DC]['LENGTH (ft)']
                            tcg = float(data_slot[(data_slot.BAY==contador_bay) & (data_slot.STACK==contador_stack) & (data_slot.TIER==contador_tier) & (data_slot.SLOT==1)].TCG)
                            vcg = float(data_slot[(data_slot.BAY==contador_bay) & (data_slot.STACK==contador_stack) & (data_slot.TIER==contador_tier) & (data_slot.SLOT==1)].VCG)
                            contenedor = Container(peso, tipo, valor, end_port, largo, tcg, vcg, es_cargado)
                            aux = barco.bays[contador_bay].espacio[contador_tier][contador_stack][0]
                            barco.bays[contador_bay].espacio[contador_tier][contador_stack][0] = contenedor
                            contenedor.tipo_slot = aux
                            contador_DC += 1
                            contador_carga += 1

                    elif slot[0] in [0,1,2] and slot[1] !=None:
                        if slot[1].largo != 40:
                            if contenedor == 1 and contador_RC < len(data_RC):
                                peso = data_RC.iloc[contador_RC]['WEIGHT (ton)']
                                tipo = data_RC.iloc[contador_RC]['TYPE']
                                valor = data_RC.iloc[contador_RC]['VALUE (USD)']
                                es_cargado = False
                                end_port = data_RC.iloc[contador_RC]['END_PORT']
                                largo = data_RC.iloc[contador_RC]['LENGTH (ft)']
                                tcg = float(data_slot[(data_slot.BAY==contador_bay) & (data_slot.STACK==contador_stack) & (data_slot.TIER==contador_tier) & (data_slot.SLOT==1)].TCG)
                                vcg = float(data_slot[(data_slot.BAY==contador_bay) & (data_slot.STACK==contador_stack) & (data_slot.TIER==contador_tier) & (data_slot.SLOT==1)].VCG)
                                contenedor = Container(peso, tipo, valor, end_port, largo, tcg, vcg, es_cargado)
                                aux = barco.bays[contador_bay].espacio[contador_tier][contador_stack][0]
                                barco.bays[contador_bay].espacio[contador_tier][contador_stack][0] = contenedor
                                contenedor.tipo_slot = aux
                                contador_RC += 1
                                contador_carga += 1
                        
                            elif contenedor == 2 and contador_DG < len(data_DG):
                                peso = data_DG.iloc[contador_DG]['WEIGHT (ton)']
                                tipo = data_DG.iloc[contador_DG]['TYPE']
                                valor = data_DG.iloc[contador_DG]['VALUE (USD)']
                                es_cargado = False
                                end_port = data_DG.iloc[contador_DG]['END_PORT']
                                largo = data_DG.iloc[contador_RC]['LENGTH (ft)']
                                tcg = float(data_slot[(data_slot.BAY==contador_bay) & (data_slot.STACK==contador_stack) & (data_slot.TIER==contador_tier) & (data_slot.SLOT==1)].TCG)
                                vcg = float(data_slot[(data_slot.BAY==contador_bay) & (data_slot.STACK==contador_stack) & (data_slot.TIER==contador_tier) & (data_slot.SLOT==1)].VCG)
                                contenedor = Container(peso, tipo, valor, end_port, largo, tcg, vcg, es_cargado)
                                aux = barco.bays[contador_bay].espacio[contador_tier][contador_stack][0]
                                barco.bays[contador_bay].espacio[contador_tier][contador_stack][0] = contenedor
                                contenedor.tipo_slot = aux
                                contador_DG += 1
                                contador_carga += 1
                            
                            elif contador_DC < len(data_DC):
                                peso = data_DC.iloc[contador_DC]['WEIGHT (ton)']
                                tipo = data_DC.iloc[contador_DC]['TYPE']
                                valor = data_DC.iloc[contador_DC]['VALUE (USD)']
                                es_cargado = False
                                end_port = data_DC.iloc[contador_DC]['END_PORT']
                                largo = data_DC.iloc[contador_DC]['LENGTH (ft)']
                                tcg = float(data_slot[(data_slot.BAY==contador_bay) & (data_slot.STACK==contador_stack) & (data_slot.TIER==contador_tier) & (data_slot.SLOT==1)].TCG)
                                vcg = float(data_slot[(data_slot.BAY==contador_bay) & (data_slot.STACK==contador_stack) & (data_slot.TIER==contador_tier) & (data_slot.SLOT==1)].VCG)
                                contenedor = Container(peso, tipo, valor, end_port, largo, tcg, vcg, es_cargado)
                                aux = barco.bays[contador_bay].espacio[contador_tier][contador_stack][0]
                                barco.bays[contador_bay].espacio[contador_tier][contador_stack][0] = contenedor
                                contenedor.tipo_slot = aux
                                contador_DC += 1
                                contador_carga += 1

                    elif slot[1] in [0,1,2] and slot[0] != None:
                        if slot[0].largo != 40:
                            if contenedor == 1 and contador_RC < len(data_RC):
                                peso = data_RC.iloc[contador_RC]['WEIGHT (ton)']
                                tipo = data_RC.iloc[contador_RC]['TYPE']
                                valor = data_RC.iloc[contador_RC]['VALUE (USD)']
                                es_cargado = False
                                end_port = data_RC.iloc[contador_RC]['END_PORT']
                                largo = data_RC.iloc[contador_RC]['LENGTH (ft)']
                                tcg = float(data_slot[(data_slot.BAY==contador_bay) & (data_slot.STACK==contador_stack) & (data_slot.TIER==contador_tier) & (data_slot.SLOT==1)].TCG)
                                vcg = float(data_slot[(data_slot.BAY==contador_bay) & (data_slot.STACK==contador_stack) & (data_slot.TIER==contador_tier) & (data_slot.SLOT==1)].VCG)
                                contenedor = Container(peso, tipo, valor, end_port, largo, tcg, vcg, es_cargado)
                                aux = barco.bays[contador_bay].espacio[contador_tier][contador_stack][1]
                                barco.bays[contador_bay].espacio[contador_tier][contador_stack][1] = contenedor
                                contenedor.tipo_slot = aux
                                contador_RC += 1
                                contador_carga += 1
                        
                            elif contenedor == 2 and contador_DG < len(data_DG):
                                peso = data_DG.iloc[contador_DG]['WEIGHT (ton)']
                                tipo = data_DG.iloc[contador_DG]['TYPE']
                                valor = data_DG.iloc[contador_DG]['VALUE (USD)']
                                es_cargado = False
                                end_port = data_DG.iloc[contador_DG]['END_PORT']
                                largo = data_DG.iloc[contador_RC]['LENGTH (ft)']
                                tcg = float(data_slot[(data_slot.BAY==contador_bay) & (data_slot.STACK==contador_stack) & (data_slot.TIER==contador_tier) & (data_slot.SLOT==1)].TCG)
                                vcg = float(data_slot[(data_slot.BAY==contador_bay) & (data_slot.STACK==contador_stack) & (data_slot.TIER==contador_tier) & (data_slot.SLOT==1)].VCG)
                                contenedor = Container(peso, tipo, valor, end_port, largo, tcg, vcg, es_cargado)
                                aux = barco.bays[contador_bay].espacio[contador_tier][contador_stack][1]
                                barco.bays[contador_bay].espacio[contador_tier][contador_stack][1] = contenedor
                                contenedor.tipo_slot = aux
                                contador_DG += 1
                                contador_carga += 1
                            
                            elif contador_DC < len(data_DC):
                                peso = data_DC.iloc[contador_DC]['WEIGHT (ton)']
                                tipo = data_DC.iloc[contador_DC]['TYPE']
                                valor = data_DC.iloc[contador_DC]['VALUE (USD)']
                                es_cargado = False
                                end_port = data_DC.iloc[contador_DC]['END_PORT']
                                largo = data_DC.iloc[contador_DC]['LENGTH (ft)']
                                tcg = float(data_slot[(data_slot.BAY==contador_bay) & (data_slot.STACK==contador_stack) & (data_slot.TIER==contador_tier) & (data_slot.SLOT==1)].TCG)
                                vcg = float(data_slot[(data_slot.BAY==contador_bay) & (data_slot.STACK==contador_stack) & (data_slot.TIER==contador_tier) & (data_slot.SLOT==1)].VCG)
                                contenedor = Container(peso, tipo, valor, end_port, largo, tcg, vcg, es_cargado)
                                aux = barco.bays[contador_bay].espacio[contador_tier][contador_stack][1]
                                barco.bays[contador_bay].espacio[contador_tier][contador_stack][1] = contenedor
                                contenedor.tipo_slot = aux
                                contador_DC += 1
                                contador_carga += 1
                contador_stack += 1
            contador_tier += 1
        contador_bay += 1 

    print(f"Contador RC", contador_RC)
    print(f"de un total de:", len(data_RC))
    print(f"Contador DG", contador_DG)
    print(f"de un total de:", len(data_DG))
    print(f"Contador DC", contador_DC)
    print(f"de un total de:", len(data_DC))
    return contador_carga
    



