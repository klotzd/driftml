#!/bin/usr/env python3

def get_run_settings(settings):
    ID = settings["ID"]
    THETA = settings["theta"]
    U0 = settings["U0"]
    UWind = settings["Uwind"]
    xgrid = settings["xgrid"]
    zgrid = settings["zgrid"]
    note = settings["note"]
    interval = settings["write interval"]
    duration = settings["duration"]
    return [ID, THETA, U0, UWind, xgrid, zgrid, note, interval, duration]

def main():
    from Tester import settings
    print(settings)
    run_settings = get_run_settings(settings)

if __name__ == '__main__':
    main()
