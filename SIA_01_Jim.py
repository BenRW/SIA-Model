"""
Created on 05/10/2021

@authors: Ben Romero-Wilcock and Jim Regtien
"""

import matplotlib.pyplot as plt
import numpy as np


# Constants
rho = 917
g = 9.81
fd = 1.9e-24
fs = 5.7e-20
beta = 1e-4
h_ela = 1000

# Domain
Ltot = 20000  # total length of the domain [m]
dx    =   10 # grid size [m]
T_max = 4000 * 365.2 * 24 * 60 ** 2 # Time [s]
dt = 1 * 365.2 * 24 * 60 **2 # [s]
x_domain = np.arange(0, Ltot, dx)

time = np.arange(0, T_max, dt)


def get_bedrock(xaxis):
    # here you put in your own equation that defines the bedrock
    bedrock = 1900. * np.ones(len(xaxis)) - xaxis*0.05
    return bedrock

def get_init_height(H0, xaxis):
    H = H0 * np.ones(len(xaxis))
    H[:50] = np.ones(50)*900
    H[-50:] = np.ones(50)*900
    return H

def accumlation(h):
  return beta * (h - h_ela)

def get_dhdx(h, dx):
    dhdx = np.zeros(len(h))
    dhdx[1:-1] = (h[2:] - h[:-2]) / 2 * dx
    return dhdx


def get_D(H, dhdx):
    D = np.zeros(len(H))
    D[1:-1] = (rho * g) ** 3 * H[1:-1] ** 3 * (2 / 5 * fd * H[1:-1] ** 2 * fs) * (dhdx[1:-1]) ** 2
    return D
    
    
def execute_code():
    b = get_bedrock(x_domain)
    # H = get_init_height(1000, x_domain)
    H = get_init_height(1000, x_domain)
    h = b + H
    H0 = H.copy()
    h0 = h.copy()
    
    for i in range(len(time)):
        t = time[i]
        h = H + b
        dhdx = get_dhdx(h, dx)
        D = get_D(H, dhdx)
        F = D * dhdx
        F_ph = np.zeros(len(H)-1)
        F_mh = np.zeros(len(H)-1)
        for j in range(0, len(x_domain)-1):
            #i+1/2 indexes
            F_ph[j] = (D[j + 1] - D[j]) / 2  * (h[j+1] - h[j]) / dx
        # for i in range(1, len(x_domain)):
        #     F_mh[i] = (D[i-1] - D[i]) / 2 *  (h[i-1] - h[i]) / dx 
        # dHdt = (F_ph - F_mh) / dx
        
        F_mh = np.roll(F_ph, 1)
        F_mh[0] = 0

        # H += dt * (dHdt) #+ beta * (h - 2000))

        # NB!!! This doesn't include accumulation
        H[:-1] += - dt * (F_ph - F_mh)/dx
        if i>0:
            H[-1] = - dt * (F_end_temp - F_ph[-1])/dx
        else:
            H[-1] = - dt * (- F_ph[-1])/dx


        F_end_temp = F_ph[-1]
        
    plt.figure()
    plt.plot(x_domain, h0)
    plt.plot(x_domain, b)
    plt.plot(x_domain, H + b)

    # plt.plot(x_domain, H-H0)

    plt.show()


execute_code()
        

    
    
  