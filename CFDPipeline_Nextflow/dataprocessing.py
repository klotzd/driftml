import os
import numpy as np


## param definition

injection_volume = 0.095
steadystate_time = 19


## input output matrix

inputmatrix = 'inputdataset.npy'
outputmatrix = 'outputdataset.npy'

def save_params(params):

    inputs = np.array((5))
    for i in range(4):
        inputs[i] = params[i]

    return inputs

def get_steadystate(df, SS_time, inj_volume):

    outputs = df[:,:, SS_time]
    outputs = outputs / inj_volume * 100

    return outputs

def main():

    if not os.path.exists(inputmatrixt):
        inputmatrix = np.array((5))

    if not os.path.exists(outputmatrix):
        outputmatrix = np.array((30, 20)) 

    subpath = 'resdir/numpys'
    os.chdir(subpath)

    sets = [".".join(f.split(".")[:-1]) for f in os.listdir() if os.path.isfile(f)]

    for dataframe in sets:

        df = np.load( (dataframe + '.npy') )
        run_params = dataframe.split('_')

        inputs = save_params(run_params)
        outputs = get_steadystate(df, steadystate_time, injection_volume)

        np.append(inputmatrix, inputs, axis=1)
        np.append(outputmatrix, outputs, axis = 2)




        

if __name__ == '__main__':
    main()