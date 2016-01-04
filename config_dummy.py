from prepare_param_strings import *
from numpy import *
from itertools import izip

#==================================== SIMULATION SPECIFIC DETAILS ============================
#declare parameters
Nsp = 3 #number of species
NWi = 2 #number of Wiener processes
C = zeros([Nsp,NWi])
C[0,0] = 1
C[1,1] = 1
C[2,0] = 1
C[2,1] = 1
corr_matrices = [ C ]
x0 = [ [(1-x0)/2.,(1-x0)/2., x0] for x0 in linspace(0.05,0.95,19,endpoint=True)]
y0 = array([ .1, .2, .4, .8, 1., 1.5, 2., 3. ])
alpha = array([ 0, .1, .2, .4, .8, 1., 1.5, 2., 3. ])
Nmax = 9 * 2**arange(7)
measurements = range(NMEASUREMENTS)

#dict mapping the name of an array above to the option needed in "simulation.py"
name_to_option = { 
                   "corr_matrices": "correlation_matrix",
                   "y0": "y0",
                   "alpha": "alpha",
                   "Nmax": "Nmax",
                   "x0": "x0",
                   "measurements": None,
                 }

#============================== GENERAL CONFIGS =================================

#set memory and seed for RNG
memory = "MEMORY"
seed = "SEED"

#set paths
pythonpath = "PYTHONPATH"
path = "WDPATH"
resultpath = path+"/results"
name = "NAME"

#set parameter settings
#which parameters are taken care of on the cluster
pliststr = "PARAMLISTSTRING"
plist = PARAMLISTSTRING
#which parameters are taken care of internally (per job)
iliststr = "INTERNALLISTSTRING"
ilist = INTERNALLISTSTRING
#which parameters are the same for every job
sliststr = "STANDARDLISTSTRING"
slist = STANDARDLISTSTRING

#prepare for job.py
parameter_names,parameter_list = get_param_lists(pliststr,plist)
internal_names,internal_parameter_list = get_param_lists(iliststr,ilist)

#prepare standard kwargs
standard_names = get_param_lists(sliststr)
std_kwargs = get_kwargs(slist,standard_names,name_to_option)

#get min and max jobnumber
jmin = 0
jmax = len(parameter_list)-1

#Sometimes one prefers to just measure the time of one simulation
only_save_times = ONLYSAVETIME


if __name__=="__main__":
    print "parameter_list =",parameter_list
    print "internal_parameter_list =",internal_parameter_list
    print "std_kwargs =",std_kwargs
