#!/bin/usr/env nextflow

params.runs = "run_list.csv"
params.maxForks = 1	                           # overriden by nextflow.config

Channel  // read the "run" column from file       # create nextflow channel from run_list
    .fromPath(params.runs)
    .splitCsv(header:true)
    .map{ row-> tuple(row.run, row.note) }
    .set { run_list }

runs_file = file(params.runs)   	           # load scripts and directories
res_dir  = file('resdir')
extract_file = file('extractor.py')
common_dir = ('common')
make_file = file('CaseMaker.py')
process_file = file('CaseProcessor.py')



process FoamRun {


    maxForks params.maxForks                      # set max no of submitted jobs

    input:
    file 'run_list.csv' from runs_file
    file 'extract.py' from extract_file
    file 'constants.py' from common_dir
    file 'CaseMaker.py' from make_file
    file 'CaseProcessor.py' from process_file

    set val(run), val(note) from run_list         # set current run id from run_list

    output:
    file "params.yml"				    # create current CFD param file

    script:                                       # bash script executing:
    """
    module purge				    # clean module import
    module load openfoam/7.0
    module load intel-suite
    module load mpi
    module load anaconda3/personal
    module load gcc/6.2.0

    activate testenv    		           # actiate py environment
    python3 extract.py --run=$run run_list.csv > params.yml     # extract and dump CFD params

    cp -rv $workflow.projectDir/casedir .	   # create copy of casedir

    python3 CaseMaker.py 			   # create CFD case from current params

    cd casedir && "blockMesh" 		   # generate mesh
    "MPPICFoam" > log.txt			   # solve CFD
    cd ..

    python3 CaseProcessor.py			   # postprocess results
    rm -r casedir				   # clean up workdir

    """
}
