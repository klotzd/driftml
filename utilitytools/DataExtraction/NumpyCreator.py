#!/bin/python

import pandas as pd
import numpy as np
import os

"""

purpose:

    reads all the lagrangian .dat files in the postProcessing folder and stores them in a numpy array in the form
    
    ( time dimension | cellnumber_x | cellnumber_y )
    
    which is then saved as a .npy file (conveniently small, takes it from ~50mb to 100kb)

definitions:

- loc_code:
    the location code from face generation has the form  'A-XX-ZZ'
    string is split at '-', leaving the cellnumber_x = XX and cellnumber_z = ZZ

- x/z_grid
    the meshing of the grid
    
- write_interval and duration:
    write interval and duration of the simulation
    
"""


######################################################################################################################
####   INITIAL DECLARATIONS
######################################################################################################################


write_interval = 0.1
duration = 2

subpath = 'postProcessing/lagrangian/kinematicCloud'
sets = list(next(os.walk(subpath))[1])
sets = sets[0:1]
fails = []
data = {}

x_grid = 40
z_grid = 20

numpy = np.zeros((x_grid, z_grid, int(duration/write_interval)))

######################################################################################################################
####   EXTRACTION AND PROCESSING
######################################################################################################################


for ID in sets:
    pth = subpath + '/' + ID + '/0/particleCollector.dat'
    loc_code = ID.split('-')
    
    if os.path.exists(pth):
        df = pd.read_csv(pth, skiprows = 8, delimiter = '\t')
        
        for idx, time in df['#'].items():
            numpy[int(loc_code[1]) , int(loc_code[2]), idx] = df['bin_0'].iloc[idx]
    else:
        fails.append(ID)

print('failed cells:')
print(fails)

np.save('BAnumpy.npy', numpy)        
 
