# Internals
import math

# Externals
import numpy as np

# Locals
from .phi import phi
from .utility import myException

def InitialRBFMatrices(opti, PairwiseDistance):

    PHI = np.zeros((len(opti.samples), len(opti.samples)))
    if opti.phifunction == 'linear':
        PairwiseDistance = PairwiseDistance
    elif opti.phifunction == 'cubic':
        PairwiseDistance = PairwiseDistance ** 3
    elif opti.phifunction == 'thinplate':
        PairwiseDistance = PairwiseDistance ** 2 * math.log(PairwiseDistance + np.finfo(np.double).tiny)

    PHI = PairwiseDistance
    phi0 = phi(0, opti.phifunction) # phi-value where distance of 2 points =0 (diagonal entries)

    if opti.polynomial == 'None':
        pdim = 0
        P = np.array([])
    elif opti.polynomial == 'constant':
        pdim = 1
        P = np.ones((len(opti.samples), 1)), opti.samples
    elif opti.polynomial == 'linear':
        pdim = opti.dim + 1
        P = np.concatenate((np.ones((len(opti.samples), 1)), opti.samples), axis = 1)
    #elif data.polynomial == 'quadratic':
    #    pdim = (data.dim + 1) * (data.dim + 2) / 2
    #    P = np.concatenate((np.concatenate((np.ones((maxeval, 1)), data.S), axis = 1), np.zeros((maxeval, (data.dim*(data.dim+1))/2))), axis = 1)
    #else:
    #    raise myException('Error: Invalid polynomial tail.')
    return np.asmatrix(PHI), np.asmatrix(phi0), np.asmatrix(P), pdim

def UpdateRBFMatrices(opti, PairwiseDistance, phi0, r):

    nevals = len(opti.samples)
    phi0 = phi(0, opti.phifunction) # phi-value where distance of 2 points =0 (diagonal entries)
    PHI = numpy.zeros((nevals, nevals))
    PHI[:PairwiseDistance.shape[0],:PairwiseDistance.shape[0]] = PairwiseDistance
    
    n_old = nevals-1 #because only one point seleced
#     for kk in range(1):
    new_phi = phi(r, opti.phifunction)
    PHI[n_old, 0: n_old] = new_phi
    PHI[0:n_old, n_old] = np.asmatrix(new_phi).T
    PHI[n_old, n_old] = phi0
    P[n_old, 1:opti.dim+1] = np.atleast_2d(xselected)

    if opti.polynomial == 'None':
        P = numpy.array([])
    elif opti.polynomial == 'constant':
        P = numpy.ones((nevals, 1)), opti.samples
    elif opti.polynomial == 'linear':
        P = numpy.concatenate((numpy.ones((nevals, 1)), opti.samples), axis = 1)
    return numpy.asmatrix(PHI), numpy.asmatrix(P)
