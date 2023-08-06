# System
import os
from urllib.request import urlopen
from shutil import copyfileobj

# External
from pandas import read_csv
from sklearn.preprocessing import MinMaxScaler

# Locals
from .plots import show_acf
from .utils import data_split

def get_data(n_out, n_timestamp, data_path='./', verbose=False, **kwargs):
    if data_path=='temperature': 
        data_path = 'daily-min-temperatures.csv' 
        if os.path.exists(data_path)==False:
            url = 'https://gitlab.com/hpo-uq/hyppo/-/raw/master/data/temperature/'+data_path
            with urlopen(url_path) as in_stream, open(data_path, 'wb') as out_file:
                copyfileobj(in_stream, out_file)
    dataset = read_csv(os.path.expandvars(data_path), header=0, index_col=0)
    if verbose:
        show_acf(dataset)
    # Load and prepare data
    itrain = int(0.6*len(dataset))
    ivalid = int(0.2*len(dataset))
    # Set number of training and testing data
    train_data = dataset[:itrain].reset_index(drop=True)
    valid_data = dataset[itrain: itrain+ivalid].reset_index(drop=True)
    test_data = dataset[itrain+ivalid:].reset_index(drop=True)
    # Preparing training sets
    training_set = train_data.iloc[:].values
    validating_set = valid_data.iloc[:].values
    testing_set = test_data.iloc[:].values
    # Normalize data first
    sc = MinMaxScaler(feature_range = (0, 1))
    training_set_scaled = sc.fit_transform(training_set)
    validating_set_scaled = sc.fit_transform(validating_set)
    testing_set_scaled = sc.fit_transform(testing_set)
    # Split data into n_timestamp
    train_set = data_split(training_set_scaled, n_timestamp, n_out, **kwargs)
    valid_set = data_split(validating_set_scaled, n_timestamp, n_out, **kwargs)
    test_set = data_split(testing_set_scaled, n_timestamp, n_out, step=n_out, **kwargs)
    return {'dataset':'generic',
            'train':train_set, 'valid':valid_set, 'test':test_set,
            'scaler':sc}
