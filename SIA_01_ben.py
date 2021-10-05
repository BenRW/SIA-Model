"""
Created on 05/10/2021

@authors: Ben Romero-Wilcock, Jim Regtien and Willem Jan van de Berg
"""

import numpy as np

s_yr = 3600*24*365.25   # seconds per year

# Constants
rho = 917
g = 9.81 * s_yr * s_yr
fd = 1.9e-24 * s_yr
fs = 5.7e-20 * s_yr

beta = 0.01
h_ela = 1700

# Spatial domain
Ltot = 20000  # total length of the domain [m]
dx   = 100    # grid size [m]
x = np.arange(0, Ltot+dx, dx)
x_between = (x[1:] + x[:-1])/2

H = np.zeros((x.shape))
F = np.zeros((x_between.shape))

# Temporal domain
dt = 0.1
Ttot = 1e3

times = np.arange(0, Ttot, dt)

def get_between(arr):
    return (arr[1:] + arr[:-1])/2

def get_bedrock(xaxis):
    # here you put in your own equation that defines the bedrock
    bedrock = 1900. - xaxis*0.05
    return bedrock

def accumulation(h):
  return beta * (h - h_ela)

def get_h(x_, H_):
  return get_bedrock(x_) + H_

H_between = get_between(H)
h = get_h(x, H)
h_between = get_h(x_between, H_between)

for n in times:
  F[1:] = (rho*g*H_between[1:])**3*((h_between[1:]-h_between[:-1])/dx)**3*(2./5*fd*H_between[1:]+fs)

  H[1:-1] = H[1:-1] + dt*(accumulation(h[1:-1]) - (F[1:]-F[:-1])/dx)

  H_between = get_between(H)
  h_between = get_h(x_between, H_between)
  h = get_h(x, H)

print(H)

