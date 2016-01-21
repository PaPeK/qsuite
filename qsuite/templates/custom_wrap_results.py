import cPickle as pickle
from numpy import *
import os
from qconfig import qconfig

cf = qconfig()

#=============================================================================

def mean_and_err(arr,axis=None):

    if isinstance(axis,basestring) or axis is None:
        axis = (cf.parameter_names+cf.internal_names).index(axis)
    else:
        axis = axis

    N = len((cf.external_parameters+cf.internal_parameters)[axis][1])

    return arr.mean(axis=axis), arr.std(axis=axis)/sqrt(N)

#====== definition for the treatment of the results goes here ================= 

def prepare_results(res):
    return mean_and_err(res)

#==============================================================================

times = pickle.load(open(cf.resultpath+"/times.p",'r'))
time,err = mean_and_err(array(times))
savez(cf.resultpath+"/mean_err_times.npz",time,err)

if not cf.only_save_times:
    results = pickle.load(open(cf.resultpath+"/results.p",'r'))
    results = prepare_results(array(results))
    if isinstance(results,(list,tuple)):
        savez(cf.resultpath+"/mean_err_result_list.npz",*results)
    else:
        save(cf.resultpath+"/mean_err_results.npy",results)


