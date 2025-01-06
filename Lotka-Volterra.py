import matplotlib.pyplot as plt 
import numpy as np
import pandas as pd


time = [0]
lapin = [1]
renard = [2]

alpha = 2/3
beta = 4/3
delta = 1
gamma = 1

step = 0.001



for _ in range(0, 100_000):
    new_value_time = time[-1] + step
    new_value_lapin = (lapin[-1] * (alpha - beta * renard[-1])) * step + lapin[-1]
    new_value_renard = (renard[-1] * (delta * lapin[-1] - gamma)) * step + renard[-1]

    time.append(new_value_time)
    lapin.append(new_value_lapin)
    renard.append(new_value_renard)

lapin = np.array(lapin)
lapin *= 1000
renard = np.array(renard)
renard *= 1000    
plt.figure(figsize=(15, 6))
plt.plot(time, lapin, "b-", label="Lapin")
plt.plot(time, renard, "r-", label="Renard")
plt.xlabel('Temps (Mois)')
plt.ylabel('Population')
plt.legend()
plt.show()
