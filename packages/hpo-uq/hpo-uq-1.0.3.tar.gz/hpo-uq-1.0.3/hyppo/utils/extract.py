# System
import os
import ast
import glob
import math
import pickle

# External
import yaml
import numpy
from scipy import interpolate

# def extract(path):
#     data = []
#     nevals = 0
#     for fname in sorted(glob.glob(path)):
#         content = numpy.loadtxt(fname,dtype=str,delimiter='\n')
#         for i,line in enumerate(content):
#             if 'Samples:' in line:
#                 samples = line.split('Samples:')[-1].strip()[1:-1]
#                 samples = [int(k) for k in samples.split()]
#             if 'Number of parameters' in line:
#                 params = int(line.split()[-1].replace(',',''))
#             if 'Outer Loss' in line:
#                 loss = float(line.split()[-1])
#             if 'Total of sample sets used' in line:
#                 nevals = int(line.split()[-1])
#             if 'MAD' in line:
#                 mad = float(line.split()[-1])
#                 data.append([params,loss,mad]+samples+[nevals])
#     data = numpy.array(data)
#     print(data.shape)
#     return data

def check_surrogate_sample(log_dir,step,iloop):
    samples = []
    log_file = './%s/surrogate_%03i_01.log' % (log_dir,step+1)
    log_content = numpy.loadtxt(log_file,dtype=str,delimiter='\n').tolist()
    for i,line in enumerate(log_content):
        if 'SURROGATE ITERATION' in line:
            isurrogate = int(line.split()[-3])
        if 'Samples:' in line and isurrogate==iloop+1:
            samples = line.split('Samples:')[-1].strip()[1:-1]
            samples = numpy.array([k for k in samples.split()],dtype=int)
            break
    return samples

def check_evaluation_outer_loss(target,output,log_dir,step,**kwargs):
    outer_loss = False
    log_file = './%s/%s_%03i_01.log' % (log_dir,output.split('-')[0],step+1)
    log_content = numpy.loadtxt(log_file,dtype=str,delimiter='\n').tolist()
    for i,line in enumerate(log_content):
        if 'Samples:' in line:
            samples = line.split('Samples:')[-1].strip()[1:-1]
            samples = [int(k) for k in samples.split()]
        if 'Outer Loss' in line and list(samples)==list(target):
            outer_loss = True
            break
    return outer_loss

def gather_trials(results,target,output,log_dir,ntasks,step,trial,split,**kwargs):
    """
    Collect trial losses for given sample set.
    
    Parameters
    ----------
    results : :class:`dict`
      Results
    """
    models = []
    if split=='trial':
        losses = numpy.zeros((trial,1))
    else:
        losses = numpy.zeros((trial,ntasks))
    n=0
    for rank in range(ntasks):
        log_file = './%s/%s_%03i_%02i.log' % (log_dir,output.split('-')[0],step+1,rank+1)
        log_content = numpy.loadtxt(log_file,dtype=str,delimiter='\n').tolist()
        for i,line in enumerate(log_content):
            if 'Samples:' in line:
                samples = line.split('Samples:')[-1].strip()[1:-1]
                samples = [int(k) for k in samples.split()]
            if 'TESTING' in line and list(samples)==list(target):
                itrial = int(line.split()[-4])-1
                for sub_line in log_content[i:]:
                    if 'Loss' in sub_line and list(samples)==list(target):
                        loss = float(sub_line.split()[-1])
                        checkpoint_dir = os.path.join(log_dir,'checkpoints')
                        path_to_model = os.path.join(checkpoint_dir,'%s.pth.tar' % output)
                        if split=='trial':
                            losses[itrial,0] = loss
                            models.append(path_to_model)
                        else:
                            losses[itrial,rank] = loss
                            if rank==0:
                                models.append(path_to_model)
                        break
    results['loss'] = [] if 0 in losses else numpy.mean(losses,axis=1)
    results['models'] = [] if 0 in losses else models
    return results

def extract_evals(opti):
    opti.samples = []
    opti.fvals = []
    opti.uqvals = []
    for file_name in sorted(glob.glob('%s/*.log' % opti.log_dir)):
        file_content = numpy.loadtxt(file_name,dtype=str,delimiter='\n').tolist()
        for i,line in enumerate(file_content):
            if 'Samples:' in line:
                samples = line.split('Samples:')[-1].strip()[1:-1]
                samples = [int(k) for k in samples.split()]
            if 'Outer Loss' in line:
                loss = float(line.split()[-1])
                if math.isnan(loss)==False:
                    opti.fvals.append(loss)
                    opti.samples.append(samples)
                    if 'Lower Bound of CI' in file_content[i+1]:
                        lower = float(file_content[i+1].split()[-1])
                        upper = float(file_content[i+2].split()[-1])
                        opti.uqvals.append([lower,upper])
    opti.samples = numpy.array(opti.samples,dtype=int)
    assert len(opti.samples)>0, 'No samples found for surrogate modeling. Abort.'
    opti.fvals = numpy.array(opti.fvals).reshape(-1,1)
    if len(opti.uqvals)>0:
        opti.fvals = numpy.hstack((opti.fvals,opti.uqvals))
    # Initialize best point found so far = first evaluated point
    imin = numpy.where(opti.fvals[:,0]==min(opti.fvals[:,0]))[0][0]
    opti.Fbest = opti.fvals[imin,0]
    opti.xbest = opti.samples[imin]
    return opti

def get_samples(log_path,surrogate=False,mult=False):
    all_samples = {}
    evaluations = []
    logs = glob.glob(log_path+'/*.log')
    for file_name in logs:
        file_content = numpy.loadtxt(file_name,delimiter='\n',dtype=str)
        for i,line in enumerate(file_content):
            if 'CONFIGURATION:' in line:
                config = ast.literal_eval(file_content[i+2].strip())
                for key in ['names','mult','xlow','xup']:
                    all_samples[key] = config['prms'][key]
            if 'EVALUATION' in line:
                evaluations.append([int(line.split()[-3])-1])
            if 'Samples:' in line:
                samples = line.split('Samples:')[-1].strip()[1:-1]
                samples = [int(k) for k in samples.split()]
                if mult:
                    evaluations[-1] += [a*b for a,b in zip(samples,all_samples['mult'])]
                else:
                    evaluations[-1] += samples
            if 'Outer Loss' in line:
                evaluations[-1] += [float(line.split()[-1])]
            if 'Lower Bound of CI' in line:
                evaluations[-1] += [float(line.split()[-1])]
            if 'Upper Bound of CI' in line:
                evaluations[-1] += [float(line.split()[-1])]
            if 'Execution Time' in line:
                evaluations[-1] += [float(line.split()[-2])]
    evaluations = numpy.array(evaluations,ndmin=2)
    idxs = numpy.argsort(numpy.array(evaluations)[:,0])
    all_samples['evals'] = numpy.array(evaluations)[idxs,1:]
    if surrogate:
        surrogate = []
        for line in open(log_path+'/surrogate.log'):
            if 'OPTIMIZATION' in line:
                surrogate.append([int(line.split()[-3])-1])
            if 'Samples' in line:
                samples = line.split('Samples:')[-1].strip()[1:-1]
                samples = [float(k) for k in samples.split()]
                if mult:
                    surrogate[-1] += [a*b for a,b in zip(samples,all_samples['mult'])]
                else:
                    surrogate[-1] += samples
            if 'Outer Loss' in line:
                surrogate[-1] += [float(line.split()[-1])]
            if 'Lower Bound of CI' in line:
                surrogate[-1] += [float(line.split()[-1])]
            if 'Upper Bound of CI' in line:
                surrogate[-1] += [float(line.split()[-1])]
            if 'Execution Time' in line:
                surrogate[-1] += [float(line.split()[-2])]
        #surrogate = numpy.array(surrogate[:-1])
        surrogate = numpy.array(surrogate)
        idxs = numpy.argsort(surrogate[:,0])
        all_samples['sgate'] = surrogate[idxs,1:]
    return all_samples

def make_tables(table_type='evaluation'):
    os.makedirs('tables',exist_ok=True)
    if table_type == 'evaluation':
        data = get_samples('logs/')
        f = open('tables/evaluation.txt',"w+")
    else:
        data = get_samples('logs/',surrogate=True)
        f = open('tables/hpo_table.txt',"w+")
    evals = data['evals']
    hps = str([ i for i in data['names']])
    num_prms = len(data['names'])
    for i in range(num_prms):
        evals[:,i] = data['mult'][i]*evals[:,i]
        if 'sgate' in data:
            data['sgate'][:,i] = data['mult'][i]*data['sgate'][:,i]
    f.write('\\begin{table}[h!]\n')
    if numpy.shape(evals)[1] > num_prms+2:
        f.write('\\begin{tabular}{|c|c|c|c|c|c|}\\hline\n')
        f.write('\\textbf{Iterations} & \\textbf{HPs:'+hps+'} & \\textbf{Mean Objective Value} & \\textbf{Lower Bound of C.I.} &\\textbf{Upper Bound of C.I.} &\\textbf{Time (s)} \\\\ \\hline \n')
        for i in range(numpy.shape(evals)[0]):
            f.write('Eval. {}&{}&{}&{}&{}&{}\\\\ \\hline \n'.format(i+1,evals[i,0:num_prms],evals[i,num_prms],evals[i,num_prms+1],evals[i,num_prms+2],evals[i,-1]))
        if 'sgate' in data:
            s_evals = data['sgate']
            for i in range(numpy.shape(s_evals)[0]):
                f.write('HPO. {}&{}&{}&{}&{}&{}\\\\ \\hline \n'.format(i+1,s_evals[i,0:num_prms],s_evals[i,num_prms],s_evals[i,num_prms+1],s_evals[i,num_prms+2],s_evals[i,-1]))
    else:
        f.write('\\begin{tabular}{|c|c|c|c|}\\hline\n')
        f.write('\\textbf{Iterations} & \\textbf{HPs:'+hps+'} & \\textbf{Objective Value} & \\textbf{Time (s)} \\\\ \\hline \n')
        for i in range(numpy.shape(evals)[0]):
            f.write('Eval. {}&{}&{}&{}\\\\ \\hline \n'.format(i+1,evals[i,0:num_prms],evals[i,num_prms],evals[i,-1]))
        if 'sgate' in data:
            s_evals = data['sgate']
            for i in range(numpy.shape(s_evals)[0]):
                f.write('HPO. {}&{}&{}&{}\\\\ \\hline \n'.format(i+1,s_evals[i,0:num_prms],s_evals[i,num_prms],s_evals[i,-1]))
    f.write('\\end{tabular} \n')
    f.write('\\end{table}')
    f.close()

# def get_loss(log_path,weight=False,grid=False,nepochs=50,verbose=False,all_losses=False):
#     if os.path.isfile(log_path):
#         logs = [log_path]
#     else:
#         log_path = os.path.join(log_path,'out_*.log')
#         logs = glob.glob(log_path)
#     trials = []
#     losses = []
#     results = numpy.empty((0,5))
#     for i,file_name in enumerate(logs):
#         for line in open(file_name):
#             if 'Evaluation' in line:
#                 if len(trials)>0 and verbose:
#                     print('Trials not reset, something wrong in file %s'%logs[i-1])
#                 trials = []
#                 neval = int(line.split()[-1])
#             if 'Hyperparameters' in line:
#                 hyperprms = ast.literal_eval(line.split('Hyperparameters:')[-1].strip())
#                 epochs = hyperprms['epochs']
#                 nodes = hyperprms['nodes'][0]#*hyperprms['nodes'][0]
#                 norm = epochs/nodes
#             if 'TRIAL' in line:
#                 ntrials = int(line.split()[-1].split('/')[-1])
#             if 'Epoch ' in line:
#                 nepoch = int(line.split()[4].split('/')[0])
#                 if nepoch==epochs:
#                     loss = float(line.split()[-1])
#                     trials.append(loss)
#             if 'Testing' in line:
#                 losses.extend(trials)
#                 loss = numpy.median(trials)
#                 sdev = numpy.std(trials)
#                 if weight: loss *= norm
#                 results = numpy.vstack((results,[neval,epochs,nodes,loss,sdev]))
#                 trials = []
#     results = results[numpy.argsort(results[:,0])]
#     (x,y,z,e) = results[:,1:].T
#     if grid:
#         # print('Loss: min %.5f | med %.5f max %.2E'%(numpy.nanmin(z),numpy.median(z),numpy.nanmax(z)))
#         xi = numpy.arange(1,nepochs+1)
#         yi = numpy.arange(1,max(y)+1)
#         xi,yi = numpy.meshgrid(xi,yi)
#         z = interpolate.griddata((x,y),z,(xi,yi),method='linear')
#         e = interpolate.griddata((x,y),e,(xi,yi),method='linear')
#     return losses if all_losses else (x,y,z,e)

# def get_sensitivity(samples):
#     from SALib.analyze import morris
#     mult = samples['mult']
#     xlow = samples['xlow']
#     xup = samples['xup']
#     problem = {
#         'num_vars': len(samples['names']),
#         'names': samples['names'],
#         'bounds': numpy.array([[i*j for i,j in zip(xlow,mult)],
#                                [i*j for i,j in zip(xup,mult)]]).T
#     }
#     n_samples = (1+len(samples['names']))*(len(samples['evals'])//(1+len(samples['names'])))
#     X = samples['evals'][:n_samples,:len(samples['names'])]
#     Y = samples['evals'][:n_samples,-1]
#     sensitivity = morris.analyze(problem, X, Y)
#     return sensitivity

# def get_sensitivity_from_tensorboard(log_dir):
#     from SALib.sample import saltelli
#     from SALib.analyze import sobol
#     from SALib.test_functions import Ishigami
#     import tensorflow.compat.v1 as tf
#     from collections import defaultdict
#     logs = glob.glob(log_dir+'/evaluation_*/logs/*/*/events.out.tfevents.*.v2')
#     metrics = defaultdict(list)
#     for file_name in logs:
#         for e in tf.train.summary_iterator(file_name):
#             for v in e.summary.value:
#                 if isinstance(v.simple_value, float):
#                     metrics[v.tag].append(v.simple_value)
#     print(metrics)
    
# def conv2surf(samples,names=[]):
#     assert len(names)==2, 'Exactly two parameters must be selected for 3D plotting. Abort.'
#     # Identify index for each selected parameters
#     xi = samples['names'].index(names[0])
#     yi = samples['names'].index(names[1])
#     # Create data grid
#     xvals = numpy.arange(samples['xlow'][xi],samples['xup'][xi]+1,1) * samples['mult'][xi]
#     yvals = numpy.arange(samples['xlow'][yi],samples['xup'][yi]+1,1) * samples['mult'][yi]
#     # Interpolate model with existed sparse data
# #     f = interpolate.interp2d(samples['evals'][:,xi], samples['evals'][:,yi], samples['evals'][:,-1], kind='linear')
#     x,y,z = samples['evals'][:,xi], samples['evals'][:,yi], samples['evals'][:,-1]
#     # print('Loss: min %.5f | med %.5f max %.2E'%(numpy.nanmin(z),numpy.median(z),numpy.nanmax(z)))
#     xi,yi = numpy.meshgrid(xvals,yvals)
#     z = interpolate.griddata((x,y),z,(xi,yi),method='linear')
#     return xvals, yvals, z
