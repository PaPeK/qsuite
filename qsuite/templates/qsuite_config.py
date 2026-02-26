import os

#=========== SIMULATION DETAILS ========
projectname = "project"
basename = "experimentname"

seed = -1
N_measurements = 1
save_each_run = False

measurements = range(N_measurements)
params1 = range(3)
params2 = range(3)
params3 = range(3)
params4 = range(3)
params5 = range(3)
params6 = range(3)

# EXTERNAL PARAMETERS: each computation node is assigned a unique combination of external parameters
#  - external parameters should not influence computation time too much
#     - OTHERWISE: 1 node takes forever, all others are done and waiting
external_parameters = [
                        ( 'p1', params1[:2]   ),
                        ( 'p2', params2       ),
                        ( None   , measurements ),
                      ]
# INTERNAL PARAMETERS: all combinations of internal parameters are computed on each node
#  - internal parameters can influence computation time
internal_parameters = [
                        ('p3', params3[:1]),
                        ('p3', params4[:]),
                      ]
standard_parameters = [
                        ( 'p5', params5[1] ),
                        ( 'p6', params6[2] ),
                      ]

only_save_times = False

#============== QUEUE =============================================
#=============== set queing system used at your server          ===
#=============== queue can be one of ['PBS', 'SGE', 'SLURM']    ===
queue = "SLURM"
memory = "1G"
computation_time = "01:00:00"
priority = 0

#============ CLUSTER SETTINGS ============
username = "user"
server = "localhost"
# NOTE: sftp_server only for data-transfer (DELETE if no specific data-transfer server exists)
sftp_server = "localhost"
useratserver = username + u'@' + server
# below the project id of the SynoSys starter project,
# if the computation is part of another project (p_replicatordyn, p_epoch_data), PLEASE specify here
project_id = "p_s_synosys"

shell = "/bin/bash"
pythonpath = "python"
name = basename + "_NMEAS_" + str(N_measurements) + "_ONLYSAVETIME_" + str(only_save_times)
serverpath = "/home/"+username +"/"+ projectname + "/" + name
resultpath = serverpath + "/results"

#============ CLUSTER PREPARATION ==================================================
#======  bash code loading modules to enable python:                      ==========
#======  e.g. "ml purge; ml release/24.10 GCCcore/13.2.0 libffi/3.4.4 bzip2/1.0.8 Python/3.11.5"   ==========
server_cmds = " "


#============== LOCAL SETTINGS ============
localpath = os.path.join(os.getcwd(),"results_"+name)
n_local_cpus = 1

#============= GIT SETTINGS     ============
git_repos = [
                ( "/path/to/repo", server_cmds + "; " + pythonpath + " -m pip install -e . --user" )
            ]
