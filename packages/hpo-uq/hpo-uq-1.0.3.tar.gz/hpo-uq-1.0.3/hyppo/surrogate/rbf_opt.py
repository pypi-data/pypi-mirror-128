# System
import copy
import time
import logging

# External
import numpy
import numpy as np
import math
import numpy.matlib as npm
from pyDOE import *
import scipy.spatial as scp

# Local
from ..train import train_evaluation
from .phi import phi
from .InitialRBFMatrices import InitialRBFMatrices, UpdateRBFMatrices
from .ComputeRBF import ComputeRBF
from ..utils import extract_evals, check_surrogate_sample

def rbf(opti,**kwargs):

    # tolerance parameters
    opti.tolerance      = 0.001 * np.min([xup-xlow for xup,xlow in zip(opti.xup,opti.xlow)]) * np.linalg.norm(np.ones((1, opti.dim)))
    # algorithm parameters -- delete stuff from here, not necessary for this problem
    sigma_stdev_default = 1#integers
    sigma_stdev         = sigma_stdev_default # current mutation rate
    # maximal number of shrikage of standard deviation
    # for normal distribution when generating the candidate points
    maxshrinkparam      = 5
    failtolerance       = max(5,opti.dim)
    succtolerance       = 3
    # initializations
    shrinkctr           = 0 # number of times sigma_stdev was shrunk
    failctr             = 0 # number of consecutive unsuccessful iterations
    localminflag        = 0 # indicates whether or not xbest is at a local minimum
    succctr             = 0 # number of consecutive successful iterations
    p                   = opti.fvals[0, 0]
    valweight           = 1.25
    maxvalweight        = 1
        
    for iloop in range(opti.loops):
        
        nevals = len(opti.samples)
        
        logging.info('='*40)
        logging.info('SURROGATE ITERATION {:>3} / {:<3}'.format(iloop+1,opti.loops))
        logging.info('-'*40)
        
        if opti.rank == 0:

            if localminflag != 0:
                break
            valweight -= 0.25
            if valweight<0:
                valweight = maxvalweight

            # Initialize array with function values
            fvals = numpy.asmatrix(numpy.zeros(opti.fvals.shape))
            fvals[:,:] = opti.fvals
            opti.fvals = fvals 
            # Build the surrogate
            # determine pairwise distance between points
            PairwiseDistance = scp.distance.cdist(opti.samples, opti.samples, 'euclidean')
            # initial RBF matrices
            PHI, phi0, P, pdim = InitialRBFMatrices(opti, PairwiseDistance)
                
            # number of new samples in an iteration
            #NumberNewSamples = min(data.nns,data.maxeval - data.m)

            # replace large function values by the median of all available function values
            #Ftransform = np.copy(np.asarray(data.Y)[0:data.m])
            #medianF = np.median(np.asarray(data.Y)[0:data.m])
            #Ftransform[Ftransform > medianF] = medianF

            # fit the response surface
            # Compute RBF parameters
            a_part1 = np.concatenate((PHI, P), axis = 1)
            a_part2 = np.concatenate((np.transpose(P), np.zeros((pdim, pdim))), axis = 1)
            a = np.concatenate((a_part1, a_part2), axis = 0)
            eta = math.sqrt((1e-16) * np.linalg.norm(a, 1) * np.linalg.norm(a, np.inf))
            if opti.fvals.shape[1]==1:
                coeff = np.linalg.solve((a + eta * np.eye(nevals + pdim)),
                                        np.concatenate((opti.fvals[:,:1], np.zeros((pdim, 1))), axis = 0))
                # llambda is not a typo, lambda is a python keyword
                opti.llambda = [coeff[0:nevals]]
                opti.ctail = [coeff[nevals: nevals + pdim]]
            else:
                a_inv   = np.linalg.inv(a + eta * np.eye(nevals + pdim))
                llambda = []
                ctail   = []
                for i in range(30): #This generates 30 different response surfaces using the CIs
                    indx  = np.random.choice(range(3),(nevals,1))
                    rhs   = np.asmatrix([opti.fvals[k,indx[k,0]] for k in range(nevals)]).T
                    rhs   = np.concatenate((rhs,np.zeros((pdim,1))),axis=0)
                    coeff = np.matmul(a_inv,rhs)
                    llambda.append(coeff[0:nevals])
                    ctail.append(coeff[nevals: nevals+pdim])
                opti.llambda = llambda
                opti.ctail   = ctail
            #-------------------------------------------------------------------------------------
            # select the next function evaluation point:
            # introduce candidate points  -- update later when number of nodes >1
            #CandPoint = np.asmatrix(data.val_list).T #this needs to be updated when we're 
            #create candidate point:
            #perturb xbest - local perturbations: 1 or 2 for parameters 1 and 2, 1 for parameters 3 and 4
            C1 = npm.repmat(opti.xbest, opti.Ncand, 1)
            R=np.zeros((opti.Ncand, opti.dim))
            for ii in range(opti.dim):
                R[:,ii]=np.ravel(np.random.randint(0,3,(opti.Ncand,1))*np.random.choice(np.array([-1,1]),(opti.Ncand,1)))

            #print(R)

            CP = R + C1
            #reflect outsiders over boundary to inside
            for ii in range(opti.dim):
                vec_ii = CP[:, ii]
                adj_l = np.where(vec_ii < opti.xlow[ii])
                vec_ii[adj_l[0]] = opti.xlow[ii] + (opti.xlow[ii] - vec_ii[adj_l[0]])
                adj_u = np.where(vec_ii > opti.xup[ii])
                vec_ii[adj_u[0]] = opti.xup[ii] - (vec_ii[adj_u[0]]-opti.xup[ii])
                stillout_u = np.where(vec_ii > opti.xup[ii])
                vec_ii[stillout_u[0]] = opti.xlow[ii]
                stillout_l = np.where(vec_ii < opti.xlow[ii])
                vec_ii[stillout_l[0]] = opti.xup[ii]
                CP[:, ii] = copy.copy(vec_ii)
            #generate second set of randomly generated points
            CR = np.zeros((opti.Ncand, opti.dim))
            for ii in range(opti.dim):
                CR[:,ii]=np.ravel(np.random.randint(opti.xlow[ii],opti.xup[ii],(opti.Ncand,1)))

            CandPoint = np.concatenate((CP,CR), axis = 0)#all candidate points
            xselected, normval = Minimize_Merit_Function(opti, CandPoint, valweight)
            xselected = numpy.array(xselected,dtype=int)
            logging.info('Total of sample sets used : %i' % len(opti.samples))
            logging.info('Best loss value so far    : %.5f' % opti.Fbest)
            logging.info('-'*40)
            logging.info('Samples: %s' % xselected)
            
        else:
            
            logging.info('Surrogate modeling in progress...')
            while check_surrogate_sample(opti.log_dir,opti.step,iloop)==[]:
                continue
            xselected = check_surrogate_sample(opti.log_dir,opti.step,iloop)
            logging.info('Samples: %s' % xselected)
        
        # Execute training
        x_sc = [int(xselected[n])*opti.mult[n] for n in range(len(opti.mult))]
        x_sc = {name:value for name,value in zip(opti.names,x_sc)}
        if hasattr(opti,'default'):
            x_sc = {**x_sc,**opti.default}
        output = '_'.join(numpy.array(xselected,dtype=str))
        Fselected = train_evaluation(x_sc, xselected, output='logs/surrogate-%s'%output, **opti.config)
        logging.info('='*40+'\n')
        
        opti = extract_evals(opti)

#         if Fselected < opti.Fbest:
#             if opti.Fbest - Fselected > (1e-3)*math.fabs(opti.Fbest):
#                 # "significant" improvement
#                 failctr = 0
#                 succctr = succctr + 1
#             else:
#                 failctr = failctr + 1
#                 succctr = 0
#             opti.xbest = xselected
#             opti.Fbest = Fselecteds
#             #data.best_Y = best_Y
#             #best_model = model
#         else:
#             failctr = failctr + 1
#             succctr = 0
#         check if algorithm is in a local minimum
#         shrinkflag = 1
#         if failctr >= failtolerance:
#            localminflag = 1
#         if succctr >= succtolerance:
#            sigma_stdev = min(2 * sigma_stdev, sigma_stdev_default)
#            succctr = 0

#         # update PHI matrix only if planning to do another iteration
#         PHI, P = UpdateRBFMatrices(opti, PairwiseDistance, phi0, r=normval[0])
    
    return opti

def Minimize_Merit_Function(opti, CandPoint, valueweight):
    CandValue, NormValue = ComputeRBF(CandPoint, opti)

    if opti.fvals.shape[1]>1:
        #CandValue = CandValue[:,0] #mean value computed for each candiate point of the rbf ensembles
        CandValue = CandValue[:,0]+2*CandValue[:,1] #mean + 2std  

    MinCandValue = np.amin(CandValue)
    MaxCandValue = np.amax(CandValue)
    if MinCandValue == MaxCandValue:
        ScaledCandValue = np.ones((CandValue.shape[0], 1))
    else:
        ScaledCandValue = (CandValue - MinCandValue) / (MaxCandValue - MinCandValue)

    CandMinDist = np.asmatrix(np.amin(NormValue, axis = 0)).T
    MaxCandMinDist = np.amax(CandMinDist)
    MinCandMinDist = np.amin(CandMinDist)
    if MaxCandMinDist == MinCandMinDist:
        ScaledCandMinDist = np.ones((CandMinDist.shape[0], 1))
    else:
        ScaledCandMinDist = (MaxCandMinDist - CandMinDist) / (MaxCandMinDist - MinCandMinDist)

    # compute weighted score for all candidates
    CandTotalValue = valueweight * ScaledCandValue + (1 - valueweight) * ScaledCandMinDist
    # assign bad scores to candidate points that are too close to already sampled points
    CandTotalValue[CandMinDist < opti.tolerance] = np.inf
        
    MinCandTotalValue = np.amin(CandTotalValue)
    selindex = np.argmin(CandTotalValue)
    xselected = np.array(CandPoint[selindex, :])
    #print(xselected)
    normval = {}
    normval[0] = np.asmatrix((NormValue[:, selindex])).T
    
    return xselected, normval
