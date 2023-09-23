#!/bin/bash
#SBATCH --qos=long
#SBATCH --time=7-0:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=16
#SBATCH --mem=30GB

module load mamba
source activate renv
srun $@

