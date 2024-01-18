#!/bin/bash -l
#SBATCH --partition=gpu-k40c
#SBATCH -w gpu04
#SBATCH --gres=gpu:2
#SBATCH --job-name=XRD
#SBATCH --output=%x.out
#SBATCH --error=%x.err
#SBATCH --nodes=1
#SBATCH --mem=56G
#SBATCH --ntasks=16
#SBATCH --qos=long

module load miniconda/miniconda3
source activate ~/python_lib
source activate ~/MD-Structure-Factor-master
python main_gromacs.py -i em30
python main_gromacs.py -top em30.gro -traj em30.trr
