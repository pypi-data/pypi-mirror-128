# System
import os
import glob
import pickle
import logging

# External
import numpy

# Local
from .gp_opt import gp
from .rbf_opt import rbf
from .utility import Optimization
from ..utils import extract_evals, make_tables

def surrogate(config,**kwargs):
    # Print configuration in log file
    logging.info('CONFIGURATION:')
    logging.info('-'*40 + '\n\n%s\n' % config['original'])
    # Create object with relevant information to be used during HPO
    opti = Optimization(config)
    # Extract values from log files
    opti = extract_evals(opti)
    # Initialize array with sample points
    # (first Data.m points are from initial experimental design)
    opti = eval(opti.surrogate)(opti)
    # Makes a table showing the HPO iterations 
    #make_tables('hpo')
    #with open('sampledata_'+opti.surrogate+'.data', 'wb') as dictionary_file:
    #    pickle.dump(opti, dictionary_file)

