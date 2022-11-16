from funciones import *

def verificar_centro_de_gravedad(barco, data_hydrostatic):
    cen_grav = calcular_centro_masa(barco)
    lcg = True
    tcg = True
    vcg = True
    dis_index = calcular_displacemnt_index(data_hydrostatic, barco)
    if cen_grav['lcg'] < data_hydrostatic.iloc[dis_index]['minLcg (m)'] or\
        cen_grav['lcg'] > data_hydrostatic.iloc[dis_index]['maxLcg (m)']:
        lcg = False
    
    if cen_grav['tcg'] < data_hydrostatic.iloc[dis_index]['minTcg (m)'] or\
        cen_grav['tcg'] > data_hydrostatic.iloc[dis_index]['maxTcg (m)']:
        tcg = False
    #falta el vcg 
    if data_hydrostatic.iloc[dis_index]['metacenter (m)'] - cen_grav['vcg'] < 0.5 or\
         data_hydrostatic.iloc[dis_index]['metacenter (m)'] - cen_grav['vcg'] > 2:
         vcg = False
    factibilidad = {"lcg": lcg, "tcg": tcg, "altura metacentrica":vcg}
    return factibilidad


def sacar_contenedores_vcg(barco, data_slot, data_hydrostatic, data_loaded):
    factibilidad = verificar_centro_de_gravedad(barco, data_hydrostatic)
    centro_gravedad = calcular_centro_masa(barco)
    rango_bay, rango_stack = calcular_rangos_desarme(centro_gravedad)
    contenedores_sacados = 0

    while factibilidad["altura metacentrica"] == False:
        mejorar_vcg(barco, data_hydrostatic, data_slot, data_loaded, rango_stack, rango_bay)
        contenedores_sacados += 10
        
        factibilidad = verificar_centro_de_gravedad(barco, data_hydrostatic)
        centro_gravedad = calcular_centro_masa(barco)
        rango_bay, rango_stack = calcular_rangos_desarme(centro_gravedad)
    print(f"contenedores sacados:", contenedores_sacados)
    


def mejorar_vcg(barco, data_hydrostatic, data_slot, data_loaded, rango_stack, rango_bay):
    contador = 0
    for bay in rango_bay:
        tier = [8,7,6,5,4,3,2,1,0]
        for a in tier:  
            for stack in rango_stack:
                #print(a, bay, stack)
                for slot in barco.bays[bay].espacio[a][stack]:
                    if slot not in [0, 1, 2, None] :
                        data = data_slot[(data_slot.BAY==bay) & (data_slot.STACK==stack) & (data_slot.TIER== a) & (data_slot.SLOT==1)]
                        refrigerado = data.REEFER.item()
                        carga_peligrosa = data.DA.item()

                        barco.bays[bay].espacio[a][stack][0] = 0 + refrigerado
                        barco.bays[bay].espacio[a][stack][1] = 0 + refrigerado

                        if carga_peligrosa == 0:
                            barco.bays[bay].espacio[a][stack][0] += 2
                            barco.bays[bay].espacio[a][stack][1] += 2

                        
                        contador += 1
                        factibilidad = verificar_centro_de_gravedad(barco, data_hydrostatic)
                        centro_gravedad = calcular_centro_masa(barco)
                        

                        if contador == 10:
                            print(centro_gravedad)
                            print(factibilidad)
                            return
                        if factibilidad["altura metacentrica"] == True:
                            return factibilidad["altura metacentrica"]
            
                           

def calcular_rangos_desarme (centro_gravedad):
    if centro_gravedad["tcg"] > 0 and centro_gravedad["lcg"] > 0:
        rango_stack = range(8, 16)
        rango_bay = range(11)

    elif centro_gravedad["tcg"] < 0 and centro_gravedad["lcg"] > 0:
        rango_stack = range(8)
        rango_bay = range(11)
    
    elif centro_gravedad["tcg"] < 0 and centro_gravedad["lcg"] < 0:
        rango_stack = range(8)
        rango_bay = range(11, 21)
    
    elif centro_gravedad["tcg"] > 0 and centro_gravedad["lcg"] < 0:
        rango_stack = range(8, 16)
        rango_bay = range(11, 21)

    return rango_bay, rango_stack