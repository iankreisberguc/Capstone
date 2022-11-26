from gurobipy import GRB, Model, math, quicksum, abs_
import pandas as pd 
import time

data_barco = pd.read_excel('container_ship_data.xlsx', 'Ship_bays_estr_data', skiprows=4, usecols="C:I", header=1)
data_loaded = pd.read_excel('container_ship_data.xlsx', 'Loaded_containers_data')
data_hydrostatic = pd.read_excel('container_ship_data.xlsx', 'Ship_hydrostatic_data', skiprows=6, usecols="B:I", header=1)
data_buoyancy = pd.read_excel('container_ship_data.xlsx', 'Ship_buoyancy_data', skiprows=4, usecols="C:X", header=1)

data = data_loaded.groupby(["BAY"])["WEIGHT (ton)"].sum()

data.loc[14]= 0
data.loc[0]= 0

data = data.sort_index()

merged_left = pd.merge(left=data_barco[['Bay index', "constWeight (ton)"]], right=data, how='left', left_on='Bay index', right_on='BAY')

modelo = Model()

weight_bays = [modelo.addVar(vtype = GRB.CONTINUOUS, 
            lb = merged_left.iloc[bay]["WEIGHT (ton)"] + merged_left.iloc[bay]["constWeight (ton)"],
            name = f"weight_bay{bay}") for bay in range(len(merged_left))]

displacement = modelo.addVars(15, vtype = GRB.BINARY, name="displacement index")


modelo.update()   

modelo.setObjective(quicksum(weight_bays), GRB.MINIMIZE)

####### RESTRICCIONES #######
### No se puede cargar ni en el bay 0 o 14
modelo.addConstr(weight_bays[0] == 1080, name="Restriccion peso bay 0")
modelo.addConstr(weight_bays[14] == 6732, name="Restriccion peso bay 0")

### Seleccionar un displacement index
modelo.addConstr(quicksum(displacement) == 1, name="Restricción 1")

cota_inferior = quicksum(list(map(lambda ci, xi: displacement[ci]*xi, list(displacement)[1:], data_hydrostatic["displacement (ton)"][:14])))
modelo.addConstr(cota_inferior <= quicksum(weight_bays), name="Restriccion 2")

cota_superior = quicksum(list(map(lambda ci, xi: displacement[ci]*xi, list(displacement)[1:], data_hydrostatic["displacement (ton)"][1:])))
modelo.addConstr(quicksum(weight_bays) <= cota_superior, name="Restriccion 3")

### Valores de lcg
lcg = quicksum(list(map(lambda ci, xi: ci*xi, weight_bays, data_barco["lcg (m)"])))

lcg_min = quicksum(list(map(lambda ci, xi: displacement[ci]*xi, list(displacement), data_hydrostatic["minLcg (m)"])))
modelo.addConstr(lcg_min <= lcg, name="Restriccion 4")

lcg_max = quicksum(list(map(lambda ci, xi: displacement[ci]*xi, list(displacement), data_hydrostatic["maxLcg (m)"])))
modelo.addConstr(lcg <= lcg_max, name="Restriccion 5")

### Esfuerzos de corte 
for bay in range(21):
    bouyancy = quicksum(list(map(lambda ci, xi: displacement[ci]*xi, list(displacement), data_buoyancy[bay])))
    weight = weight_bays[bay] - bouyancy
    modelo.addConstr(int(data_barco["minShear (ton)"][bay]) <= weight, name=f"Restriccion 6 min shear bay {bay}")
    modelo.addConstr(weight <= int(data_barco["maxShear (ton)"][bay]), name=f"Restriccion 6 max shear bay {bay}")

### Bending 
bending_particular = list()
for bay in range(21):
    bouyancy = quicksum(list(map(lambda ci, xi: displacement[ci]*xi, list(displacement), data_buoyancy[bay])))
    weight = weight_bays[bay] - bouyancy
    bending = (148 - float(data_barco["lcg (m)"][bay]))*weight
    bending_particular.append(bending)

for bay in range(21):
    # modelo.addConstr(-int(data_barco["maxBending (ton*m)"][bay]) <= quicksum(bending_particular[:bay + 1]), name=f"Restriccion 7 min bending bay {bay}")
    modelo.addConstr(quicksum(bending_particular[:bay + 1]) <= int(data_barco["maxBending (ton*m)"][bay]), name=f"Restriccion 7 max bending bay {bay}")

modelo.optimize()

modelo.printAttr("X")
