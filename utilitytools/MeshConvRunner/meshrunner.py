#!/bin/python3

import os
import subprocess

runs = range(1,5)

blockMesh = 'blockMesh'
MPPICCFoam = 'MPPICFoam'

bspth = '/' +  str(1)
os.chdir(bspth)

for r in runs:
    
    if r != 1:
        bspth = '/' + str(r)
        os.chdir(bspth)
        
    bm = subprocess.getstatusoutput(blockMesh)
    fm = open("log.txt", "w")
    subprocess.call(MPPICFoam, stdout=fm)
    
    print('complete')
    
    subprocess.call('python3 BANumpyCreator.py')

print('overall complete')