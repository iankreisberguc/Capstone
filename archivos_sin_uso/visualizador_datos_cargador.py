from msilib import PID_LASTPRINTED
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

data_cargado = pd.read_excel("container_ship_data.xlsx", sheet_name="Loaded_containers_data")
data_espacio = pd.read_excel("container_ship_data.xlsx", sheet_name="Slot_data")

# print(data_cargado.head())
# print(data_espacio.head())

# data_cargado.shape
# data_cargado.columns

carga = data_cargado[["BAY", "STACK", "TIER", "LENGTH (ft)"]]
# espacio = data_espacio[["BAY","STACK", "TIER"]]


# print(carga.head())

lista = []

for i in range(1,21):
    tabla = carga[carga.BAY == i]
    # print(tabla.head())
    lista.append(tabla)

# print(lista)

numero = 1
for bay in lista:
    if numero != 14:
        tabla_por_bay = bay.groupby(["STACK", "TIER"]).sum()
        # print(tabla_por_bay)
        # tabla_por_bay.shape
        # print(tabla_por_bay)
        tabla_por_bay = tabla_por_bay.reset_index()
        tabla_por_bay = tabla_por_bay.pivot("TIER", "STACK")["LENGTH (ft)"]
        print(tabla_por_bay)
        # print(tabla_por_bay)
        # print(tabla_por_bay.head(20))
        plt.figure(figsize=(8,8))
        plt.xlabel('TIER', size = 15)
        plt.ylabel('STACK', size = 15)
        plt.title('VISUALIZACIÓN DEL BARCO CARGADO EN EL BAY %i' %numero, size = 15)
        visualizacion = sns.heatmap(tabla_por_bay, annot=True, fmt=".0f", linewidths=.5, square = True, cmap = 'YlGnBu', vmin=0, vmax= 40, center= 0)
        visualizacion.invert_yaxis()
    numero += 1
plt.show()
