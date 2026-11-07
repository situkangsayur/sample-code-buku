#!/bin/bash
# Kode 10.13: job Slurm untuk program MPI.  sbatch pi.sbatch
#SBATCH --job-name=pi-mpi
#SBATCH --partition=compute
#SBATCH --nodes=4
#SBATCH --ntasks-per-node=32
#SBATCH --time=00:10:00
#SBATCH --output=pi-%j.out

module load openmpi             # nama module bergantung pada klaster Anda
srun ./pi 10000000000
