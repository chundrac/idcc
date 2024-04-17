#!/bin/bash
#SBATCH --qos=normal
#SBATCH --time=2:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=8GB

echo $@

module load anaconda3
source activate renv
srun $@
