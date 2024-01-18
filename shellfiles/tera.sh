#!/bin/bash -l
#SBATCH --partition=gpu-titan
#SBATCH -w gpu02
#SBATCH --gres=gpu:3
#SBATCH --job-name=automation
#SBATCH --output=%x.out
#SBATCH --error=%x.err
#SBATCH --nodes=1
#SBATCH --mem=100G
#SBATCH --ntasks=16
#SBATCH --time=5-23:59:00
#SBATCH --qos=long

module load miniconda/miniconda3

source activate ~/python_lib

python w-single.py
