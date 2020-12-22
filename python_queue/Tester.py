#!/bin/usr/env python3

import subprocess
from pathlib import Path
import os
import CaseMaker
import CaseProcessor
from config.constants import get_run_settings
import config.constants
import pandas as pd

runs = pd.read_csv("run_settings.csv")

print('process starting')

for index, run in runs.iterrows():
    settings = get_run_settings(run)
    
    #CaseMaker.main(settings)
    
    #blockMesh = 'blockMesh'
    #MPPICFoam = 'MPPICFoam'
    #os.chdir("casedir")
    #bm = subprocess.call(blockMesh)
    #logfile = "log_" + str(run["ID"]) + ".txt"
    #fm = open("log.txt", "w+")
    #subprocess.call(MPPICFoam, stdout=fm)

    CaseProcessor.main(settings)

print('process finished')
