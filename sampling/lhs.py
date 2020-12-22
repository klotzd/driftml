#!/bin/usr/env python3

from pyDOE import *
import pandas as pd


def main():

    # definition of sample variabels as [lower bound, upper bound]
    u_nozzle_bounds = [2.75, 3.25]
    theta_nozzle_bounds = [-45, 45]
    phi_nozzle_bounds = [-45, 45]
    u_wind_bounds = [0, 10]
    alpha_wind_bounds = [0, 10]

    # latin hypercube sampling params
    n = 5
    samples = 50
    crit = "corr"

    latinhypercube = lhs(n, samples)

    u_nozzle = (
        latinhypercube[:, 0] * (u_nozzle_bounds[1] - u_nozzle_bounds[0])
        + u_nozzle_bounds[0]
    )
    theta = (
        latinhypercube[:, 1] * (theta_nozzle_bounds[1] - theta_nozzle_bounds[0])
        + theta_nozzle_bounds[0]
    )
    phi = (
        latinhypercube[:, 2] * (phi_nozzle_bounds[1] - phi_nozzle_bounds[0])
        + theta_nozzle_bounds[0]
    )
    u_wind = (
        latinhypercube[:, 3] * (u_wind_bounds[1] - u_wind_bounds[0]) + u_wind_bounds[0]
    )
    alpha = (
        latinhypercube[:, 4] * (alpha_wind_bounds[1] - alpha_wind_bounds[0])
        + alpha_wind_bounds[0]
    )

    # create samplespace df
    samplespace = pd.DataFrame(
        {
            "U0": u_nozzle,
            "theta": theta,
            "phi": phi,
            "Uwind": u_wind,
            "alpha": alpha,
            "xgrid": 30,
            "zgrid": 20,
            "write interval": 0.25,
            "duration": 5,
            "note": "",
        }
    )

    samplespace.index.name = "run"

    print(samplespace.describe())
    samplespace.to_csv("samplespace.csv")


if __name__ == "__main__":
    main()
