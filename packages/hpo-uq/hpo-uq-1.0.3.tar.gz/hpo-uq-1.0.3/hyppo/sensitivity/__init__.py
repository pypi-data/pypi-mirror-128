# System
import pickle

def sensitivity(config,**kwargs):
    from SALib.analyze import sobol
    sensitivity = sobol.analyze(problem, Y, print_to_console=True)
    with open('sensitivity.pkl', 'wb') as dictionary_file:
        pickle.dump(sensitivity, dictionary_file)

