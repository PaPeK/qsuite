from __future__ import print_function
from tabulate import tabulate
import copy
from qsuite import ssh_command




def print_params(cf):

    #for each parameter combination, add job id (j) in the beginning and arrayjob id in the end
    params = [ [j] + list(p) + [j+1] for j,p in enumerate(cf.parameter_list) ]

    #get names from config, besides if the entry is None and the length is equal to the number of measurements, then add MeasID
    names = [ n if not (n is None and len(cf.external_parameters[i][1])==cf.N_measurements) else "Meas.ID" for i,n in enumerate(cf.parameter_names)  ]

    print(tabulate(params, headers=["Job ID"] + names + ["Array ID"]))


def _get_progress(cf,ssh):
    ssh_cmd = ' '.join(['for cat '+cf.serverpath+"/output/progress_%d;" % j for j in range(len(cf.parameter_list)) ])
    N = len(cf.parameter_list)-1
    filepath = cf.serverpath + "/output/progress_"
    cmd = ('for i in `seq 0 %d`; do cat '+filepath+'$i; done;') % N
    progresses = ssh_command(ssh,cmd,noprint=True)
    progresses = progresses.split("\n")[:-1]
    progresses = [ p.split("__") if len(p)>1 else ['waiting...',''] for p in progresses ]

    return progresses


def print_status(cf,ssh):

    #for each parameter combination, add job id (j) in the beginning and arrayjob id in the end
    progresses = _get_progress(cf,ssh)
    prog = [ [j+1]+p for j,p in enumerate(progresses) ]

    names = [ "Array ID", "Progress", "Rem. Time" ]

    print(tabulate(prog, headers=names))


def print_params_and_status(cf,ssh):
    
    #for each parameter combination, add job id (j) in the beginning and arrayjob id in the end
    progresses = _get_progress(cf,ssh)
    table = [ [j] + list(p[0]) + [j+1] + list(p[1]) for j,p in enumerate(zip(cf.parameter_list,progresses)) ]

    #get names from config, besides if the entry is None and the length is equal to the number of measurements, then add MeasID
    names = [ n if not (n is None and len(cf.external_parameters[i][1])==cf.N_measurements) else "Meas.ID" for i,n in enumerate(cf.parameter_names)  ]
    names = ["Job ID"] + names + ["Array ID",  "Progress", "Rem. Time" ]

    print(tabulate(table, headers = names))
