import matplotlib.pyplot as plt
import pickle

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