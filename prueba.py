import pandas as pd 

# data_for_load = pd.read_excel('container_ship_data.xlsx', 'Loading_list_data')

data_slot = pd.read_excel('container_ship_data.xlsx', 'Slot_data')
data_prueba_1 = data_slot[(data_slot['BAY'] == 1) & (data_slot['STACK'] == 4) & (data_slot['TIER']==13)]
data_prueba_2 = data_slot[(data_slot['BAY'] == 3) & (data_slot['STACK'] == 4) & (data_slot['TIER']==13)]
data_prueba = None
data_prueba = pd.concat([data_prueba_1, data_prueba_2], axis=0)

for i in range(3):
    for index, row in data_prueba.iterrows():
        data_prueba = data_prueba.drop(index = data_prueba.head(1).index)
        print(row)
        print('-'*50)
        break

print(data_prueba)