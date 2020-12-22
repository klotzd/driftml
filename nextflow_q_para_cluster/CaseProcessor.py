#!/usr/bin/env python3

import numpy as np
import pandas as pd
import subprocess
import os
from common.constants import read_config
from pathlib import Path

class PostProcessor(object):
    """

    """

    def __init__(self, settings):
    
        # RUN ID
        self.run = settings["run"]

        # NOZZLE PARAMS
        self.theta = settings["theta"]
        self.phi = settings["phi"]
        self.u0 = settings["U0"]
        self.nozzle_height = 0.6

        # WIND PARAMS
        self.uwind = settings["Uwind"]
        self.alpha = settings["alpha"]

        # GRID PARAMS
        self.xgrid = settings["xgrid"]
        self.zgrid = settings["zgrid"]

        # FOAM PARAMS
        self.interval = settings["write interval"]
        self.duration = settings["duration"]

        # INFO
        self.note = settings["note"]

        # TARGET AND DOMAIN PARAMs
        self.target_length = 6
        self.target_width  = 2
        self.ylevel = 0.1
        self.domain_x = 7
        self.domain_z = 2

    def savename(self):

        self.savename =   str(self.run) + '_' \
                        + str(self.uwind) + '_' \
                        + str(self.alpha) + '_' \
                        + str(self.u0) + '_' \
                        + str(self.theta) + '_' \
                        + str(self.phi)
      
    def make_numpy(self):

        self.savename()

        subpath = 'casedir/postProcessing/lagrangian/kinematicCloud'
        sets = list(next(os.walk(subpath))[1])

        ba_numpy = np.zeros((self.xgrid, self.zgrid, int(self.duration/self.interval)))

        for ID in sets:
            pth = subpath + '/' + ID + '/0/particleCollector.dat'
            loc_code = ID.split('-')

            if os.path.exists(pth):
                df = pd.read_csv(pth, skiprows=8, delimiter='\t')
                for idx, time in df['#'].items():
                    ba_numpy[int(loc_code[1]), int(loc_code[2]), idx] = df['bin_0'].iloc[idx]

        out = "../../../resdir/numpys/" + self.savename + '.npy'
        np.save(Path(out), ba_numpy)
    
    #def save_foamlog(self):

    #   os.chdir("casedir")
    #	foamlogfile = "../resdir/" + str(self.run) + '/' + "foamlog_" + str(self.run) + ".txt"
    #	os.replace(Path("foamlog.txt"), Path(foamlogfile))

    def process_case(self):
        self.make_numpy()
    #   self.save_log()
        
        

def main():
    content = read_config("params.yml")
    Processor = PostProcessor(content)
    Processor.process_case()

if __name__ == '__main__':
    main()
