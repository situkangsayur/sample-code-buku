#!/bin/bash
# Kode 10.15: job hybrid MPI + OpenMP.  sbatch hybrid.sbatch
#SBATCH --job-name=pi-hybrid
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=4
#SBATCH --cpus-per-task=8
#SBATCH --time=00:30:00
#SBATCH --output=hybrid-%j.out

module load openmpi
export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
export OMP_PROC_BIND=close OMP_PLACES=cores
srun --cpu-bind=cores ./hybrid 10000000000
