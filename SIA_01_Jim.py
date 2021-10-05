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
beta = 1e-8
h_ela = 1000

# Domain
Ltot = 20000  # total length of the domain [m]
dx    =   100 # grid size [m]
T_max = 4000 * 365.2 * 24 * 60 ** 2 # Time [s]
dt = 1 * 365.2 * 24 * 60 **2 # [s]
x_domain = np.linspace(Ltot, dx)


def get_bedrock(xaxis):
    # here you put in your own equation that defines the bedrock
    bedrock = 1900. * np.ones(len(xaxis)) - xaxis*5
    return bedrock

def get_init_height(H0, xaxis):
    H = H0 * np.ones(len(xaxis))
    return H

def accumlation(h):
  return beta * (h - h_ela)

def get_dhdx(h, dx):
    dhdx = np.zeros(len(h))
    dhdx[1:-1] = (h[2:] - h[:-2]) / 2 * dx
    return dhdx


def get_D(H, dhdx):
    D = np.ones(len(H))
    D = (rho * g) ** 3 * H ** 3 * (2 / 5 * fd * H ** 2 * fs) * (dhdx)
    return D
    
    
def execute_code():
    b = get_bedrock(x_domain)
    H = get_init_height(1000, x_domain)
    h = b + H
    H0 = H.copy()
    h0 = h.copy()
    print(h)
    
    
    for t in np.linspace(T_max, dt):
        h = H + b
        dhdx = get_dhdx(h, dx)
        D = get_D(H, dhdx)
        F = D * dhdx 
        F_ph = np.zeros(len(H))
        F_mh = np.zeros(len(H))
        for i in range(0, len(x_domain)-1):
            F_ph[i] = (D[i + 1] - D[i]) / 2  * (h[i+1] - h[i]) / dx
        for i in range(1, len(x_domain)):
            F_mh[i] = (D[i-1] - D[i]) / 2 *  (h[i-1] - h[i]) / dx 
        dHdt = (F_ph - F_mh) / dx
        print(H-H0)
        H += dt * (dHdt) #+ beta * (h - 2000))
        
    plt.figure()
    plt.plot(x_domain, h0)
    plt.plot(x_domain, b)
    plt.plot(x_domain, H + b)
        
        
        
    
    
  