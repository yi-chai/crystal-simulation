#!/bin/bash -l
   
#SBATCH --partition=cpu-opteron
#SBATCH --job-name=gromacs
#SBATCH --output=%x.out
#SBATCH --error=%x.err
#SBATCH --mem=10G
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --hint=nomultithread
#SBATCH --time=0-00:59:59

module load gromacs/gromacs-2021.2
gmx_mpi editconf -f mTIPS.pdb -o TIPS.gro
