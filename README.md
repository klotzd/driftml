# <p align="center"> Surrogate Modelling of Spray Dispersion using Computational Fluid Dynamics & Machine Learning </p> <p align="center"> *Sam Dale & Dominik Klotz* </p>


Supplementary github repository for our final year research project investigating surrogate modelling of spray dispersion using computational fluid dynamics (CFD) and machine learning (ML). Pushed from our original closed Gitlab repo. Repository contains several minimum working examples (MWE):

* An OpenFOAM (v6 and v8) CFD implementation of a E/L spray dispersion model comparable to wind tunnel studies under ISO22856:2008 
* A Nextflow computational pipeline for the automated generation and processing of hundreds of CFD simulations from a parameter file
* two jupyter notebooks containing the resulting surrogate models for a disinfection application (a classifier) and for agricultural spray drift modelling (a regressor)
* some useful utility scripts
 
___

## **SprayModel_OpenFOAM**

Requires OpenFOAMv6 or OpenFOAMv8. \

Run a single CFD simulation of a spray nozzle (currently based on the ALBUZ ATR80, but easily transferable via `constant/kinematicCloudProperties`) in a 2x2x7 metre wind tunnel with frontal wind.

___

## **CFDPipeline_Nextflow**

Requires OpenFOAMv6, Nextflow and Python 3.8. \
On top of the conda distribution requires the PyFOAM and PyYAML modules. 

Specify a list of CFD Parameters
* nozzle angle via polar angle theta and azimuthal angle phi
* nozzle exit velocity
* wind velocity
* wind angle alpha
* duration, write intervals and further CFD settings 

in `run_list.csv`.  Then call either `make run` to use cx1 settings, or `nextflow run main.nf` to use standard nextflow settings. The process will execute CFD simulations for every single set of parameters, and store collections of deposition density snapshots as numpy matrices in `resdir`. Run settings are encoded into the output matrices' file names like

`<RUN_ID>_<WindVelocity>_<WindAngle>_<NozzleExitVelocity>_<NozzleTheta>_<NozzlePhi>`

___

## **exampleML_notebooks**

Two jupyter notebooks with the suggested surrogate models. Requires a conda distribution with modules sci-kit learn and sci-kit image.

A classifier for disinfection and decontaminationa applications separates the ground downwind into areas of sufficient disinfectant application and areas of insufficient application volume, given by `Disinf_clf`.

The regression model in `localFrameGPR_reg` follows the proposed whole-image regression algorithm outlined in the report. Uses an esemble of local gaussian process regressors to predict the % deposition of total injection volume at some point on the ground solely from input CFD parameters.

___

## **Report**

The submitted report outlining motivation, development and methods, results and conclusions of the project.

___

## **utlitytools**

Collection of useful utlity scripts for performing:

* Latin Hypercube Sampling
* Data extraction from raw `~/Lagrangian/ParticleCollector/` OpenFOAM outputs
* Programmatic generation of `ParticleCollector` grids of specified resolution
* Automated execution of mesh convergence study


