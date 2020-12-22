#!/usr/bin/env python3

import numpy as np
import yaml
import os
from pathlib import Path
from common.collectorfile import *
from common.constants import read_config
from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile


class FoamCase(object):
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


    def calc_injector(self):
        
        precision = 3
        alpha = -np.radians(self.alpha)
        theta = np.radians(self.theta)
        phi = np.radians(self.phi)

        # rotate the injector position to angle alpha        
        inj_pos = np.array((-0.5 * self.target_length, 0))
        c, s = np.cos(alpha), np.sin(alpha)
        Rot = np.array(((c, -s), (s, c)))

        self.inj_pos = np.matmul(inj_pos, Rot)
        self.inj_pos = self.inj_pos + np.array((self.domain_x, self.domain_z)) * 0.5 

        # rotate the injector direction to angle theta, phi
        inj_dir = np.array((0, 1, 0))

        cx, sx = np.cos(theta), np.sin(theta)
        Rot_x  = np.array(((1, 0, 0), (0, cx, -sx), (0, sx, cx)))
        cz, sz = np.cos(phi), np.sin(phi)
        Rot_z  = np.array(((cz, -sz, 0), (sz, cz, 0), (0, 0, 1)))

        self.inj_dir = np.matmul(np.matmul(inj_dir, Rot_x), Rot_z)

        # get keys
        self.inj_poskey  = "(" + str(self.inj_pos[0]) + " " + str(self.nozzle_height) + " " + str(self.inj_pos[1]) + ")"
        self.inj_dirkey  = "(" + str(self.inj_dir[0]) + " " + str(self.inj_dir[1]) + " " + str(self.inj_dir[2]) + ")"

    def make_injector(self):

        self.calc_injector()

        inj_file = ParsedParameterFile(Path("casedir/constant/InjectorModel"))
        inj_file["injector1"]["position"] = self.inj_poskey
        inj_file["injector1"]["direction"] = self.inj_dirkey

        inj_file.writeFile()

    
    def calc_windfield(self):

        self.wind_key = "uniform" + " " + "(" + str(self.uwind) + " " + "0" + " " + "0" + ")"


    def make_windfield(self):

        self.calc_windfield()

        wind_file = ParsedParameterFile(Path("casedir/0/U.air"))
        wind_file["internalField"] = self.wind_key
        for boundary in wind_file["boundaryField"]:
            if "ground" not in boundary:
                wind_file["boundaryField"][boundary]["value"] = self.wind_key
 
        wind_file.writeFile()

    def calc_collectorgrid(self):

        alpha = - np.radians(self.alpha)                      # define the rotation matrix
        c, s = np.cos(alpha), np.sin(alpha)
        Rot = np.array(((c, -s), (s, c)))              

        x_step = np.array((self.target_length / self.xgrid, 0))    # define the step sizes
        z_step = np.array((0, self.target_width / self.zgrid))
        OS = np.array((self.target_length, self.target_width)) * -0.5   # define the starting point in coord system origin = target center

        self.x_step = np.matmul(x_step, Rot)                  # rotate
        self.z_step = np.matmul(z_step, Rot)
        self.OS     = np.matmul(OS, Rot)

        self.OS = self.OS + np.array((self.domain_x, self.domain_z)) * 0.5                        # translate to coord system origin = domain corner
        

    def make_collectorgrid(self):

        self.calc_collectorgrid()

        os.chdir(Path("casedir/constant"))
        filename = "CollectorFaces"
        lines_header = 16

        length = file_length(filename)
        delete_multiple_lines(filename, list(range(lines_header, length)))

        with open(filename, 'r+') as f:

            for _ in range(lines_header):
                next(f)
        
            f.write('\n')
            OS_bckup = self.OS
    
            for zi in range(self.zgrid):   

                if zi != 0:
                    OS = OS_bckup + self.z_step * zi
                else:
                    OS = self.OS
            
                for xi in range(self.xgrid):
            
                    name = cellname(xi, zi, f)         
                    type_declaration(f)         
            
                    p_1 = OS
                    p_2 = p_1 + self.z_step          
                    p_3 = p_2 + self.x_step
                    p_4 = p_3 - self.z_step

                    write_points(p_1, p_2, p_3, p_4, self.ylevel, f)       
                    log_declaration(f)          
            
                    OS = p_4


    def make_case(self):

        os.chdir(os.path.dirname(os.path.abspath(__file__)))

        self.make_injector()
        self.make_windfield()
        self.make_collectorgrid()


def main():

    content = read_config("params.yml")
    Case = FoamCase(content)
    Case.make_case()


if __name__ == '__main__':
    main()
