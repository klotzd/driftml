#!/usr/bin/env python3

import numpy as np
from pathlib import Path


class FoamCase(object):
    """

    """

    def __init__(self, settings):
        self.theta = settings[1]
        self.U_nozzle = settings[2]
        self.U_wind = settings[3]

    def make_injector(self):
        # for now:
        precision = 4
        theta = np.radians(self.theta)

        if theta > np.pi / 2:
            inj_zdirection = - np.sin(theta - np.pi / 2) * self.U_nozzle
            inj_xdirection = np.cos(theta - np.pi / 2) * self.U_nozzle

        else:
            inj_zdirection = - np.sin(theta) * self.U_nozzle
            inj_xdirection = - np.cos(theta) * self.U_nozzle

        inj_zdirection = np.round(inj_zdirection, precision)
        inj_xdirection = np.round(inj_xdirection, precision)

        template = Path("templates/InjTemplate.txt")

        with open(template, 'r') as file:
            data = file.readlines()

        data[26] = '\t' + 'U0' + '\t' + '(' + str(inj_xdirection) + ' ' + str(inj_zdirection) + ' ' + '0' + ');' + '\n'
        data[34] = '\t' + 'direction' + '\t' + '(' + str(inj_xdirection) + ' ' + str(inj_zdirection) + ' ' + '0' + ');' + '\n'

        with open(Path('casedir/constant/InjectorModel'), 'w+') as file:
            file.writelines(data)

    def make_windfield(self):

        template = "templates/WindTemplate.txt"

        windfield = 'uniform' + ' ' + '(' + str(self.U_wind) + ' ' + '0' + ' ' + '0);' + '\n'

        with open(template, 'r') as file:
            data = file.readlines()

        data[19] = 'internalField' + '\t' + windfield
        data[32] = '\t' + 'value' + '\t' + windfield
        data[38] = '\t' + 'value' + '\t' + windfield
        data[46] = '\t' + 'value' + '\t' + windfield
        data[54] = '\t' + 'value' + '\t' + windfield

        with open(Path('casedir/0/U.air'), 'w+') as file:
            file.writelines(data)

    def make_case(self):
        import os

        if os.path.exists('casedir/0/U.air.c'):
            os.remove('casedir/0/U.air.c')

        if os.path.exists('casedir/const/InjectionModel.C'):
            os.remove('casedir/const/InjectionModel.C')

        self.make_injector()
        self.make_windfield()


def main(run_settings):
    sim = FoamCase(run_settings)
    sim.make_case()


if __name__ == '__main__':
    main()
