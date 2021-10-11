#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 16:49:55 2019

@author: wvdberg
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

totL  = 20000 # total length of the domain [m]
dx    =   100 # grid size [m]
N = int(2000/100)

ntpy  =   200 # number of timesteps per year

ZeroFluxBoundary = True # either no-flux (True) or No-ice boundary (False)
FluxAtPoints     = False # if true, the ice flux is calculated on grid points, 
                        #  otherwise on half points
bump             = False
StopWhenOutOfDomain = True                        
                        
ndyfigure = 5           # number of years between a figure frame                        


rho   =  917.      # kg/m3
g     =    9.80665 # m/s2
fd    =    1.9E-24 # # pa-3 s-1 # this value and dimension is only correct for n=3
fs    =    5.7E-20 # # pa-3 m2 s-1 # this value and dimension is only correct for n=3


elalist = np.array([1800., 1750., 1900., 1800.,])  # m
elayear = np.array([1000., 1000., 1000., 1000.])  # years    
dbdh    =    0.007    # [m/m]/yr
maxb    =    2.      # m/yr

cd    = 2/5 * (rho*g) **3 * fd  # <<< this must be adjused according to your discretisation
cs    = (rho*g) ** 3 *fs  # <<< this must be adjused according to your discretisation

def get_bedrock(xaxis):
    # here you put in your own equation that defines the bedrock
    bedrock = 1900. - xaxis*0.05 
    
    if bump:
        a = 50
        b = 10000
        c = 1000 
        bedrock += a * np.exp(- ((xaxis - b )/c) **2 )
    return bedrock

# Start calculations
# constants that rely on input
nx    = int(totL/dx)
dx    = totL/nx       # redefine, as it     
xaxis = np.linspace(0,totL,nx,False) + dx*0.5
xhaxs = np.linspace(dx,totL,nx-1,False) / 1000.

bedrock = get_bedrock(xaxis)

dt    = 365.*86400./ntpy # in seconds!

h_ice   = np.zeros(nx)    # ice thickness
dhdx   = np.zeros(nx)    # the local gradient of h
fluxd  = np.zeros(nx+2)  # this will be the flux per second!!!!
fluxs  = np.zeros(nx+2)  # this will be the flux per second!!!!
dhdtif = np.zeros(nx)    # change in ice thickness due to the ice flux, per second
smb    = np.zeros(nx)

# preparations for the ela-selection
# elaswch is a list of time steps on which a new ela value should be used.
nyear    = int(np.sum(elayear))
if np.size(elalist) != np.size(elayear):
    print("the arrays of elalist and elayear does not have the same length!")
    exit()
else:
    elaswch = np.zeros(np.size(elalist))
    for i in range(0,np.size(elaswch)-1):
        elaswch[i+1] = elaswch[i] + (elayear[i]*ntpy)
    ela     = elalist[0]
        
# preparations for the animation
nframes  = nyear//ndyfigure + 1
hsurfmem = np.zeros([nx,nframes])
smbmem   = np.zeros([nx,nframes])
ifdmem   = np.zeros([nx,nframes])
fldmem   = np.zeros([nx-1,nframes])
flsmem   = np.zeros([nx-1,nframes])
iframes  = 0
hindexmem = 

print("Run model for {0:3d} years".format(nyear))

for it in range(ntpy*nyear + 1):
    h = h_ice + bedrock
    # if FluxAtPoints:
    #     dhdx[1:-1] = (h[2:]-h[:-2])/(2*dx)
        
    #     # the following equation needs to be adjusted according to your discretisation
    #     # note that flux[1] is at the point 0
    #     fluxd[1:-1] = cd * (dhdx) * (h_ice)  
    #     fluxs[1:-1] = cs * (dhdx) * (h_ice)

    #     # derive flux convergence
    #     dhdtif[:]  = (fluxd[2:]-fluxd[:-2]+fluxs[2:]-fluxs[:-2])/(2*dx)
    dhdx[:-1]  = (h[1:]-h[:-1])/dx # so 0 is at 1/2 actually
    
    # the following equation needs to be adjusted according to your discretisation
    # note that flux[1] is at the point 1/2
    fluxd[1:-2] = cd * dhdx[:-1] ** 3 * ( ((h_ice[1:])+(h_ice[:-1])) * 0.5 ) ** 5
    fluxs[1:-2] = cs * dhdx[:-1] ** 3 * ( ((h_ice[1:])+(h_ice[:-1])) * 0.5 ) ** 3
    
    # derive flux convergence
    dhdtif[:]  = (fluxd[1:-1]-fluxd[:-2] + fluxs[1:-1]-fluxs[:-2])/dx
    
    # calculate smb (per year)
    # first update ela (once a year)
    if it%ntpy == 0:
        # lists the elements of elaswch that are equal or smaller than it
        [ielanow] = np.nonzero(elaswch<=it) 
        # the last one is the current ela
        ela       = elalist[ielanow[-1]]        
    smb[:] = (h-ela)*dbdh
    smb[:] = np.where(smb>maxb, maxb, smb) 
    
    h_ice   += smb/ntpy + dt*dhdtif
    h_ice[:] = np.where(h_ice<0., 0., h_ice) # remove negative ice thicknesses
    
    if ZeroFluxBoundary == False:
        h_ice[0] = h_ice[-1] = 0.
    
    if it%(ndyfigure*ntpy) == 0:
        hsurfmem[:,iframes] = h_ice + bedrock
        smbmem[:,iframes]   = smb
        ifdmem[:,iframes]   = dhdtif[:]*365.*86400.
        fldmem[:,iframes]   = -fluxd[1:-2]*365.*86400.
        flsmem[:,iframes]   = -fluxs[1:-2]*365.*86400.
        iframes            += 1
        if StopWhenOutOfDomain:
            if h_ice[-1]>1.:
                print("Ice at end of domain!")
                break
        
        
# at this point, the simulation is completed.        
# the following is needed to make the animation        
fig  = plt.figure()
ax1  = fig.add_subplot(311, autoscale_on=False, xlim=(0,totL/1000.), \
                      ylim=(np.min(bedrock),np.max(hsurfmem)+10.))
mina2 = min(np.min(smbmem),np.min(ifdmem))
maxa2 = max(np.max(smbmem),np.max(ifdmem))
ax2   = fig.add_subplot(312, autoscale_on=False, xlim=(0,totL/1000.), \
                      ylim=(mina2,maxa2))
mina3 = min(np.min(fldmem),np.min(flsmem))
maxa3 = max(np.max(fldmem),np.max(flsmem))
ax3   = fig.add_subplot(313, autoscale_on=False, xlim=(0,totL/1000.), \
                      ylim=(mina3,maxa3))


# define the line types
bedrline, = ax1.plot([],[],'-', c='saddlebrown', label = 'Bedrock') 
hsrfline, = ax1.plot([],[],'-', c='navy', label = 'total height')
time_template = 'time = %d y'
time_text = ax1.text(0.5, 0.92, '', transform=ax1.transAxes )
smbline,  = ax2.plot([],[],'-', c='navy', label = 'surface mass balance')
ifdline,  = ax2.plot([],[],'-', c='red', label = '$\\frac{dh}{dt}$ due to ice flux')
fxdline,  = ax3.plot([],[],'-', c='navy', label = 'Ice flux due to deformation')
fxsline,  = ax3.plot([],[],'-', c='red', label = 'Ice flux due to sliding')

# initialize the animation
def init_anim():
    bedrline.set_data([], [])
    hsrfline.set_data([], [])
    time_text.set_text('')
    smbline.set_data([], [])
    ifdline.set_data([], [])
    fxdline.set_data([], [])
    fxsline.set_data([], [])

    return bedrline, hsrfline, time_text, smbline, ifdline, fxdline, fxsline

# update the animation with data for saved frame #tf
def animate(tf):
    bedrline.set_data(xaxis/1000., bedrock)
    hsrfline.set_data(xaxis/1000., hsurfmem[:,tf])
    time_text.set_text(time_template % int(tf*ndyfigure))
    smbline.set_data(xaxis/1000.,  smbmem[:,tf])
    ifdline.set_data(xaxis/1000.,  ifdmem[:,tf])
    fxdline.set_data(xhaxs      ,  fldmem[:,tf])
    fxsline.set_data(xhaxs      ,  flsmem[:,tf])
    
    return bedrline, hsrfline, time_text, smbline, ifdline, fxdline, fxsline
    
# call and run animation
ani = animation.FuncAnimation(fig, animate, np.arange(iframes),\
         interval=25, blit=True, init_func=init_anim, )     

ax3.set_xlabel('Distance in Km')
ax3.set_ylabel('Ice flux in m^2 yr-1')
ax2.set_ylabel('accumulation m/yr')
ax1.set_ylabel('Height in m')
ax1.legend()
ax2.legend()
ax3.legend()

ani.save('Bumpless animation.mp4')
plt.show()


        


   

                        

                        
