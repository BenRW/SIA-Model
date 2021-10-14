import numpy as np
import matplotlib.pyplot as plt

n_bumps = 9

labels = ["1850m to 1800m", "1800m to 1750m", "1750m to 1700m", "1700m to 1750m", "1750m to 1800m", "1800m to 1850m"]

t_r = np.zeros((len(labels), n_bumps)) # response times
b_h = np.zeros((len(labels), n_bumps)) # bump heights

for i in range(n_bumps):
    for j in range(len(labels)):
        t_r[j, i] = np.loadtxt("glacier_bump"+str(i)+".csv", delimiter=",", skiprows=1, usecols=2)[j]
        b_h[j, i] = np.loadtxt("glacier_bump"+str(i)+".csv", delimiter=",", skiprows=1, usecols=5)[j]

for k in range(len(labels)):
    plt.plot(b_h[k,:], t_r[k,:], ".--", label=labels[k])

plt.xlabel("Bump height [m]")
plt.ylabel("Response time [y]")
plt.legend(loc=0)
plt.show()




