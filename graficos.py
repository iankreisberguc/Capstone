import matplotlib.pyplot as plt
from matplotlib import pyplot
import pickle
from funciones import *
from prueba_vcg import *
import time
import pandas as pd
import numpy as np




def grafico_peso_barco():
    with open('peso_output.pickle', 'rb') as handle:
        peso = pickle.load(handle)

    print(peso)

    plt.figure("Peso cargado en el barco")
    plt.bar(x=[a for a in range(len(list(peso.keys())))], height = list(peso.values()), color ="red", edgecolor = "black")
    plt.xlabel("Bay")
    plt.ylabel("Peso cargado")
    plt.xticks(list(range(len(peso))), [i for i in range(len(peso))])
    plt.tight_layout()
    plt.show()

def Calcular_parametros(barco, data_hydrostatic):
    cen_grav = calcular_centro_masa(barco)
    dis_index = calcular_displacemnt_index(data_hydrostatic, barco)
    parametros = {"lcg": cen_grav['lcg'], "tcg": cen_grav['tcg'], "GM": data_hydrostatic.iloc[dis_index]['metacenter (m)'] - cen_grav['vcg']}
    
    return parametros

def grafico_parametros(barco, data_slot, data_hydrostatic, data_loaded,cargados):
    factibilidad = verificar_centro_de_gravedad(barco, data_hydrostatic)
    salir = False
    centro_gravedad = calcular_centro_masa(barco)
    parametros = Calcular_parametros(barco, data_hydrostatic)
    rango_bay, rango_stack = calcular_rangos_desarme(centro_gravedad)
    lcg = ["lcg"]
    tcg = ["tcg"]
    gm = ["GM"]
    lista = [lcg,tcg,gm]
    contenedores_sacados = 0
    inicio_tiempo = time.time()
    lista_tiempos = []
    while salir == False:
        salir = mejorar_vcg(barco, data_hydrostatic, data_slot, data_loaded, rango_stack, rango_bay,cargados,salir=False)
        contenedores_sacados += 50
        
        factibilidad = verificar_centro_de_gravedad(barco, data_hydrostatic)
        centro_gravedad = calcular_centro_masa(barco)
        rango_bay, rango_stack = calcular_rangos_desarme(centro_gravedad)
        fin_tiempo = time.time()
        tiempo_actual = fin_tiempo - inicio_tiempo
        lista_tiempos.append(tiempo_actual)
        parametros = Calcular_parametros(barco, data_hydrostatic)
        lcg.append(parametros["lcg"])
        tcg.append(parametros["tcg"])
        gm.append(parametros["GM"])

    print(f"contenedores sacados:", contenedores_sacados)

    for i in range(0,3): 
        
        N = len(lista[i])-1
        res = lista[i][-N:] 
        if type(res[0]) == str:
            continue

        if i==0:
            dis_index = calcular_displacemnt_index(data_hydrostatic, barco)
            # # Asintotas Min y Max.
            def f_max(x):
                return 0*x + data_hydrostatic.iloc[dis_index]['maxLcg (m)']
            def f_min(x):
                return 0*x + data_hydrostatic.iloc[dis_index]['minLcg (m)']
            # # Valores del eje X que toma el gráfico.
            xp = range(0, 6)
            # # Graficar ambas funciones.
            pyplot.plot(xp, [f_max(i) for i in xp], label = "Máximo",linestyle='--')
            pyplot.plot(xp, [f_min(i) for i in xp], label = "Mínimo" ,linestyle='--')
            
            x = lista_tiempos
            y = res

            plt.plot(x,y,label="LCG")
            plt.xlabel('Tiempo (segundos)')
            plt.ylabel(lista[i][0])
            plt.title(f"Evolucion del {lista[i][0]} al sacar contenedores")
            plt.legend(loc='best')
            plt.show()

        elif i==1:
            dis_index = calcular_displacemnt_index(data_hydrostatic, barco)
            # Asintotas Min y Max.
            def f_max(x):
                return 0*x + data_hydrostatic.iloc[dis_index]['maxTcg (m)']
            def f_min(x):
                return 0*x + data_hydrostatic.iloc[dis_index]['minTcg (m)']
            # # Valores del eje X que toma el gráfico.
            xp = range(0, 6)
            # # Graficar ambas funciones.
            pyplot.plot(xp, [f_max(i) for i in xp], label = "Máximo",linestyle='--')
            pyplot.plot(xp, [f_min(i) for i in xp], label = "Mínimo" ,linestyle='--')
            x = lista_tiempos
            y = res
            plt.plot(x,y,label="TCG")
            plt.xlabel('Tiempo (segundos)')
            plt.ylabel(lista[i][0])
            plt.title(f"Evolucion del {lista[i][0]} al sacar contenedores")
            plt.legend(loc='best')
            plt.show()

        elif i==2:
            # Asintotas Horizontales.
            def f_max(x):
                return 0*x + 2
            def f_min(x):
                return 0*x + 0.5
            # Valores del eje X que toma el gráfico.
            xp = range(0, 6)
            # Graficar ambas funciones.
            pyplot.plot(xp, [f_max(i) for i in xp], label = "Máximo",linestyle='--')
            pyplot.plot(xp, [f_min(i) for i in xp], label = "Mínimo" ,linestyle='--')
            x = lista_tiempos
            y = res
            plt.plot(x,y,label="GM")
            plt.xlabel('Tiempo (segundos)')
            plt.ylabel(lista[i][0])
            plt.title(f"Evolucion del {lista[i][0]} al sacar contenedores")
            plt.legend(loc='best')
            plt.show()
    # x = lista_tiempos
    # y = lcg

    # plt.plot(x,y)
    # plt.xlabel('x')
    # plt.ylabel('y')
    # plt.title('Lab')
    # plt.show()

def grafico_comparativo_peso_barco(barco, data_hydrostatic, data_buoyancy):
    with open('peso_output.pickle', 'rb') as handle:
        peso = pickle.load(handle)
    dis_index = calcular_displacemnt_index(data_hydrostatic, barco)
    list_min =  []
    list_max = []
    for bay in range(21):
        #no estoy seguro si esta al reves
        list_min.append(data_buoyancy.iloc[dis_index][bay] + barco.bays[bay].min_esfuerzo_corte)
        list_max.append(data_buoyancy.iloc[dis_index][bay] + barco.bays[bay].max_esfuerzo_corte)


    lista_pesos = list(peso.values())
  
    data = pd.DataFrame({'Peso' :  lista_pesos,
                     'Minimo': list_min,
                     'Maximo': list_max},
                    index=('0', '1','2','3','4','5','6','7','8',\
                        '9','10','11','12','13','14','15','16','17','18',\
                        '19','20',))
    

    n = len(data.index)
    x = np.arange(n)
    width = 0.3
    plt.bar(x - 2*width, data.Peso, width=width, label='Peso')
    #plt.bar(x - width, data.Minimo , width=width, label='Minimo')
    plt.bar(x - width, data.Maximo, width=width, label='Maximo')
    plt.xticks(x, data.index)
    plt.legend(loc='best')
    plt.xlabel('Bay')
    plt.ylabel('Tonelada')
    plt.title(f"Esfuerzos de corte")
    plt.show()
