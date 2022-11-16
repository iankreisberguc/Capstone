import pandas as pd 

# data_for_load = pd.read_excel('container_ship_data.xlsx', 'Loading_list_data')

# data_slot = pd.read_excel('container_ship_data.xlsx', 'Slot_data')
# data_prueba_1 = data_slot[(data_slot['BAY'] == 1) & (data_slot['STACK'] == 4) & (data_slot['TIER']==13)]
# data_prueba_2 = data_slot[(data_slot['BAY'] == 3) & (data_slot['STACK'] == 4) & (data_slot['TIER']==13)]
# data_prueba = None
# data_prueba = pd.concat([data_prueba_1, data_prueba_2], axis=0)

# for i in range(3):
#     for index, row in data_prueba.iterrows():
#         data_prueba = data_prueba.drop(index = data_prueba.head(1).index)
#         print(row)
#         print('-'*50)
#         break

# print(data_prueba)

data_barco = pd.read_excel('container_ship_data.xlsx', 'Ship_bays_estr_data', skiprows=4, usecols="C:I", header=1)
data_buoyancy = pd.read_excel('container_ship_data.xlsx', 'Ship_buoyancy_data', skiprows=4, usecols="C:X", header=1)
data_hydrostatic = pd.read_excel('container_ship_data.xlsx', 'Ship_hydrostatic_data', skiprows=6, usecols="B:H", header=1)


# for i in range(len(data_hydrostatic)):
#     if data_hydrostatic.iloc[i]['displacement (ton)'] <= 90000:
#         dis_index = i

# print(dis_index)

# print(data_hydrostatic.iloc[dis_index]['displacement (ton)'])
# print(data_buoyancy.iloc[dis_index][2])
# print(data_buoyancy)

# for bay in range(21):
#     data = data_barco.iloc[bay]['maxBending (ton*m)'] 
#     print(data)

data_cargamento = pd.read_excel("container_ship_data.xlsx","Loading_list_data")
data20 = data_cargamento[data_cargamento["LENGTH (ft)"] == 20].sort_values(by=["WEIGHT (ton)"], ascending=False)
data40 = data_cargamento[data_cargamento["LENGTH (ft)"] == 40].sort_values(by=["WEIGHT (ton)"], ascending=False)

data_ordenada = pd.concat([data20, data40], axis=0).reset_index()
# data_ordenada = data_cargamento.groupby("LENGTH (ft)", \
#               group_keys=False, sort=True).apply(lambda x: x).sort_values(by=["WEIGHT (ton)"], ascending=False)

data_ordenada = data_ordenada.drop(['index'], axis=1)
print(data_ordenada)