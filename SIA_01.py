"""
Created on 05/10/2021

@authors: Ben Romero-Wilcock, Jim Regtien and Willem Jan van de Berg
"""

import numpy as np


# Constants
rho = 917
g = 9.81
fd = 1.9e-24
fs = 5.7e-20

# Domain
Ltot = 20000  # total length of the domain [m]
dx    =   100 # grid size [m]


def get_bedrock(xaxis):
    # here you put in your own equation that defines the bedrock
    bedrock = 1900. - xaxis*0.05
    return bedrock


def accumlation(h):
  return beta * (h - h_ela)
