#!/bin/python

import pandas as pd
import numpy as np
import os
from tempfile import TemporaryFile

outfile = TemporaryFile()

write_interval = 0.01
duration = 5

dir_path = os.path.dirname(os.path.realpath(__file__))
subpath = "/postProcessing/lagrangian/kinematicCloud"
subpath = subpath + dir_path
sets = list(next(os.walk(subpath))[1])
fails = []
data = {}
print(sets[0])

x_grid = 60
z_grid = 1

big_ass_numpy = np.zeros((x_grid, z_grid, int(duration / write_interval)))

for ID in sets:
    pth = subpath + "/" + ID + "/0/particleCollector.dat"
    loc_code = ID.split("-")

    if os.path.exists(pth):
        df = pd.read_csv(pth, skiprows=8, delimiter="\t")
        for idx, time in df["#"].items():
            big_ass_numpy[int(loc_code[1]), int(loc_code[2]), idx] = df["bin_0"].iloc[
                idx
            ]
    else:
        fails.append(ID)

print("fails")
print(fails)
np.save("BAnumpy.npy", big_ass_numpy)
