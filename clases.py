# import pandas as pd

class Barco:
    def __init__(self):
        self.bays = []
        self.peso = 0
        self.carga = 0
        self.contador_20 = 0
        self.contador_40 = 0


    def generar_bays(self, data):
        for idex, row in data.iterrows():
            bay = Bay(row['lcg (m)'], row['maxShear (ton)'], row['minShear (ton)'], row['maxBending (ton*m)'], row['constWeight (ton)'])
            self.bays.append(bay)

    def actualizar_peso(self):
        peso = 0
        carga = 0
        contador_40 = 0
        contador_20 = 0
        for bay in self.bays:
            peso += bay.peso
            for tier in range(18):
                for stack in range(16):
                    container_0 = bay.espacio[tier][stack][0]
                    container_1 = bay.espacio[tier][stack][1]
                    if container_0 not in [0, 1, 2, None]:
                        peso += container_0.peso
                        if container_0.largo == 40:
                            carga += 2
                            contador_40 += 1
                        else:
                            carga += 1
                            contador_20 += 1
                    if container_1 not in [0, 1, 2, None]:
                        peso += container_1.peso
                        if container_1.largo == 40:
                            carga += 2
                            contador_40 += 1
                        else:
                            carga += 1
                            contador_20 += 1
        self.peso = peso
        self.carga = carga
        self.contador_20 = contador_20
        self.contador_40 = contador_40



        
class Bay:
    def __init__(self, lcg, max_esfuerzo_corte, min_esfuerzo_corte, max_bending, peso):
        self.lcg = lcg
        # self.vcg = 15
        self.max_esfuerzo_corte = max_esfuerzo_corte
        self.min_esfuerzo_corte = min_esfuerzo_corte
        # self.max_bending = max_bending
        self.peso = peso
        self.max_peso = max_bending/lcg
        self.espacio = [[[None, None] for stack in range(16)] for tier in range(18)]

class Container: 
    def __init__(self, peso, tipo, valor, end_port, largo, tcg, vcg, es_cargado):
        self.peso = peso
        self.tipo = tipo
        self.valor = valor
        self.end_port = end_port
        self.largo = largo 
        self.tcg = tcg
        self.vcg = vcg 
        self.es_cargado = es_cargado
