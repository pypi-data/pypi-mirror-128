# System
import time
import array
import random
import logging

# External
import numpy
import scipy.spatial as scp
from scipy.stats import norm
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF
from deap import algorithms
from deap import base
from deap import benchmarks
from deap.benchmarks.tools import diversity, convergence
from deap import creator
from deap import tools

# Local
from ..train import train_evaluation
from ..obj_fct import *
from ..utils import extract_evals, check_surrogate_sample

def gp(opti):
    
    # Print out parameters for generational process
    NGEN, MU, CXPB = 100, 100, 0.75
    logging.info('='*40)
    logging.info('GENERATIONAL PROCESS PARAMETERS')
    logging.info('-'*40)
    logging.info('Number of generations  : {}'.format(NGEN))
    logging.info('Number of individuals  : {}'.format(MU))
    logging.info('Cross-over probability : {}'.format(CXPB))
    logging.info('='*40+'\n')
    
    # Loop through evaluations
    for iloop in range(opti.loops):
        
        logging.info('='*40)
        logging.info('SURROGATE ITERATION {:>3} / {:<3}'.format(iloop+1,opti.loops))
        logging.info('-'*40)
        
        if opti.rank == 0:
            
            # Build Gaussian Process based on input-output pairs
            opti.gpr = GaussianProcessRegressor(kernel=RBF(), random_state=0).fit(opti.samples, opti.fvals)
            if iloop==0:
                toolbox, stats = gp_init(opti)

            pf = tools.ParetoFront()
            logbook = tools.Logbook()
            logbook.header = "gen", "evals", "std", "min", "avg", "max"

            pop = toolbox.population(n=MU)
            hof = tools.HallOfFame(10)
            invalid_ind = [ind for ind in pop if not ind.fitness.valid]
            fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)

            for ind, fit in zip(invalid_ind, fitnesses):
                ind.fitness.values = fit

            pop = toolbox.select(pop, len(pop))
            hof.update(pop)
            record = stats.compile(pop)
            logbook.record(gen=0, evals=len(invalid_ind), **record)

            t0 = time.time()
            # Begin the generational process
            for gen in range(1, NGEN):
                # Vary the population
                offspring = tools.selNSGA2(pop, len(pop))
                offspring = tools.selTournamentDCD(pop, len(pop))
                offspring = [toolbox.clone(ind) for ind in offspring]
                for ind1, ind2 in zip(offspring[::2], offspring[1::2]):
                    if random.random() <= CXPB:
                        toolbox.mate(ind1, ind2)
                    toolbox.mutate(ind1)
                    toolbox.mutate(ind2)
                    del ind1.fitness.values, ind2.fitness.values
                # Evaluate the individuals with an invalid fitness
                invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
                fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
                for ind, fit in zip(invalid_ind, fitnesses):
                    ind.fitness.values = fit
                pop[:] = offspring
                hof.update(offspring)
                record = stats.compile(pop)
                logbook.record(gen=gen, evals=len(invalid_ind), **record)
            logging.info('Total of sample sets used : %i' % len(opti.samples))
            logging.info('Generational process time : %.3f s' % (time.time()-t0))
            logging.info('Best loss value so far    : %.5f' % opti.Fbest)
            logging.info('-'*40)
        
            # Find next set of hyperparameters
            xselected =[]
            for ii in range(10):
                #print(scp.distance.cdist(numpy.asmatrix(hof[ii]), data.S[:data.m], 'euclidean'))
                if numpy.min(scp.distance.cdist(numpy.asmatrix(hof[ii]), opti.samples, 'euclidean'))>=1:
                    xselected=numpy.asarray(hof[ii])
                    break
            while len(xselected)==0: #no new point was selected, use a random one
                x_=numpy.zeros(opti.dim)
                for ii in range(opti.dim):
                    x_[ii] = random.randint(opti.xlow[ii], opti.xup[ii])
                if numpy.min(scp.distance.cdist(numpy.asmatrix(x_), opti.samples[:opti.fevals], 'euclidean'))>=1:
                    xselected=x_
            xselected = numpy.array(xselected,dtype=int)
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
        res = train_evaluation(x_sc,xselected,output='surrogate-%s'%output,**opti.config)
        logging.info('='*40+'\n')

        opti = extract_evals(opti)

    return opti

def gp_init(opti):
    #set up the GP to maximize expected improvement over an integer lattice
    creator.create("FitnessMin", base.Fitness, weights=(-1.0,)) 
    # Individuals in the generation
    creator.create("Individual", array.array, typecode='d', fitness=creator.FitnessMin)
    toolbox = base.Toolbox()
    for ii in range(opti.dim):
        INT_MIN, INT_MAX = opti.xlow[ii], opti.xup[ii]
        toolbox.register("attr_int_"+str(ii), random.randint, INT_MIN, INT_MAX)
    toolbox_list=[]
    for i in range(opti.dim):
        toolbox_list.append(eval("toolbox.attr_int_"+str(i)))
    toolbox.register("individual", tools.initCycle, creator.Individual,tuple(toolbox_list),n=1)  
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("evaluate", Expected_improvement, opti=opti)
    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", tools.mutUniformInt, low=list(opti.xlow), up=list(opti.xup), indpb=.1)
    toolbox.register("select", tools.selNSGA2)
    # Initialize statistical functions
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean, axis=0)
    stats.register("std", numpy.std, axis=0)
    stats.register("min", numpy.min, axis=0)
    stats.register("max", numpy.max, axis=0)
    return toolbox, stats

def Expected_improvement(x, opti):
    #gpr = GaussianProcessRegressor(kernel=RBF(), random_state=0).fit(data.S[0:data.m,:], data.Y[0:data.m])
    #print('score: ',gpr.score(data.S[0:data.m,:], data.Y[0:data.m]) )
    x_to_predict = numpy.array(x).reshape(-1, opti.dim)
    mu, sigma = opti.gpr.predict(x_to_predict, return_std=True)
    greater_is_better = False
    if greater_is_better:
        loss_optimum = numpy.max(opti.fvals[:,0])
    else:
        loss_optimum = numpy.min(opti.fvals[:,0])
    scaling_factor = (-1) ** (not greater_is_better)
    # In case sigma equals zero
    with numpy.errstate(divide='ignore'):
        Z = scaling_factor * (mu - loss_optimum) / sigma
        expected_improvement = scaling_factor * (mu - loss_optimum) * norm.cdf(Z) + sigma * norm.pdf(Z)
        expected_improvement[sigma == 0.0] == 0.0
    answer=-1.*expected_improvement[0,0] #maximize f = minimize -f
    return answer,

