#!/bin/bash -l
#SBATCH --partition=gpu-v100s
#SBATCH -w gpu05
#SBATCH --gres=gpu:2
#SBATCH --job-name=TIPS
#SBATCH --output=%x.out
#SBATCH --error=%x.err
#SBATCH --nodes=1
#SBATCH --mem=171G
#SBATCH --ntasks=32
#SBATCH --qos=long

module load miniconda/miniconda3

source activate ~/python_lib

python insertmolecules.py
