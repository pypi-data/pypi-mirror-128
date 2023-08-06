
import numpy as np

def phi(r, type):
    '''determines phi-value of distance r between 2 points (depends on chosen RBF model)

       Input:
            r: distance between 2 points
            type: RBF model type

       Output: 
            output: phi-value according to RBF model
    '''
    if type == 'linear':
        output = r
    elif type == 'cubic':
        output = np.power(r, 3)
    elif type == 'thinplate':
        if r >= 0:
            output = np.multiply(np.power(r, 2), math.log(r + np.finfo(np.double).tiny))
        else:
            output = np.zeros(r.shape)
    #else:
    #    raise myException('Error: Unkonwn type.')

    return output
