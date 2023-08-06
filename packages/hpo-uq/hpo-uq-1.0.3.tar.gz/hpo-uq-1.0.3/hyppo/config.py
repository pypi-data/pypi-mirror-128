# System
import os

# External
import yaml

# Local
from .datasets import get_data
from .distribution import get_workers
from .utils import create_logging

def load_config(config_file=None,debug=0,operation=None,**kwargs):
    """
    Load configuration file and embed relevant parameters and data in dictionary.
    """
    # Load configuration file
    with open(config_file) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    # Add paths to dictionary
    config['original'] = str(config)
    config['path'] = os.path.abspath(config_file)
    # Add empty model section if absent and check ML library
    if 'model' not in config.keys():
        config['model'] = {}
    elif config['trainer']=='internal':
        assert 'library' in config['model'].keys(), \
        'ML library must be specified in configuration file for internal trainer. Abort.'
        config['model']['debug'] = debug
    if 'trial' not in config['model'].keys():
        config['model']['trial'] = 1
    # Update dist section
    default = {
        'step':0,
        'nsteps':1,
        'ntasks':1,
        'node_type':'cpu',
        'backend':None,
        'split':'trial',
        'log_dir':'logs',
    }
    if 'dist' in config.keys():
        config['dist'] = {**default,**config['dist']}
    else:
        config['dist'] = default
    # Initialize workers and prepare data
    if operation in ['evaluation','surrogate']:
        config['dist'] = {**config['dist'],**get_workers(**config)}
        config['dist'].pop('operation', None)
        create_logging(operation,**config['dist'])
        # Extract training and test datasets
        if 'data' in config.keys():
            # Merging needed to avoid duplicate (e.g. verbose)
            dicts = {**config['model'],**config['data']}
            data = get_data(**dicts)
            config['data'] = {**config['data'], **data}
    return config
