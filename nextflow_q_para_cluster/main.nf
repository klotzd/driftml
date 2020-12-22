#!/bin/usr/env nextflow

params.runs = "run_list.csv"
params.maxForks = 50

Channel  // read the "run" column from file
    .fromPath(params.runs)
    .splitCsv(header:true)
    .map{ row-> tuple(row.run, row.note) }
    .set { run_list }

runs_file = file(params.runs)
res_dir  = file('resdir')

extract_file = file('extractor.py')
common_dir = ('common')
make_file = file('CaseMaker.py')
process_file = file('CaseProcessor.py')



process FoamRun {

    maxForks 1

    input:
    file 'run_list.csv' from runs_file
    file 'extract.py' from extract_file
    file 'constants.py' from common_dir
    file 'CaseMaker.py' from make_file
    file 'CaseProcessor.py' from process_file

    set val(run), val(note) from run_list

    output:
    file "params.yml"

    script:
    """
    module purge
    module load openfoam/7.0
    module load intel-suite
    module load mpi
    module load mpi/intel-2018
    module load anaconda3/personal
    module load gcc/6.2.0

    activate testenv

    python3 extract.py --run=$run run_list.csv > params.yml

    cp -rv $workflow.projectDir/casedir .

    python3 CaseMaker.py

    cd casedir && "./Allrun"

    cd ..

    python3 CaseProcessor.py

    cd casedir && "./Allclean"

    """
}
