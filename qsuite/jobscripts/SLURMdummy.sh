#!%s

#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=%s
#SBATCH --time=%s
#SBATCH --array=%d-%d
#SBATCH -o %s
#SBATCH -e %s
#SBATCH --priority=%d
#SBATCH --account=%s

# here go "server_cmds": server specific commands necessary to run the job 
%s

INDEX=$((SLURM_ARRAY_TASK_ID-1))
srun %s -u %s/job.py $INDEX
