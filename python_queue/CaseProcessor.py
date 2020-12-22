#!/usr/bin/env python3

import numpy as np
import pandas as pd
import os
from pathlib import Path
import subprocess

class PostProcessor(object):
    """

    """

    def __init__(self, settings):
    	self.ID    = settings[0]
    	self.xgrid = settings[4]
    	self.zgrid = settings[5]
    	self.note = settings[6]
    	self.intvl = settings[7]
    	self.duration = settings[8]

    def make_numpy(self):
        subpath = 'casedir/postProcessing/lagrangian/kinematicCloud'
        sets = list(next(os.walk(subpath))[1])

        ba_numpy = np.zeros((self.xgrid, self.zgrid, int(self.duration/self.intvl)))

        for ID in sets:
            pth = subpath + '/' + ID + '/0/particleCollector.dat'
            loc_code = ID.split('-')

            if os.path.exists(pth):
                df = pd.read_csv(pth, skiprows=8, delimiter='\t')
                for idx, time in df['#'].items():
                    ba_numpy[int(loc_code[1]), int(loc_code[2]), idx] = df['bin_0'].iloc[idx]

        out = 'resdir/' + str(self.ID) + '.npy'
        np.save(Path(out), ba_numpy)
    
    def save_log(self):
    	os.chdir("casedir")
    	logfile = "../resdir/" + "log_" + str(self.ID) + ".txt"
    	os.replace(Path("log.txt"), Path(logfile))

    def clean_case(self):
        os.walk('casedir')
        #subprocess.run('Allclean')
        
        

def main(run_settings):
    Processor = PostProcessor(run_settings)
    Processor.make_numpy()
    Processor.save_log()
    Processor.clean_case()

if __name__ == '__main__':
    main(run_settings)
