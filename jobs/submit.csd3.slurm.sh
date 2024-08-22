#!/bin/bash
#SBATCH -A UKAEA-AP002-CPU
#SBATCH -p icelake
#SBATCH --job-name=defuse
#SBATCH --output=defuse-%A.out
#SBATCH --time=10:00:00
#SBATCH --mem=250G
#SBATCH --ntasks=32
#SBATCH -N 2

# File containing parameters to extract
parameter_file=./jobs/shots.csv
# Input directory
input_dir=./data/input
# Output directory
output_dir=./data/output

# Load Matlab
module load matlab/r2024a

source ./defuse-env/bin/activate 
mpirun -np $SLURM_NTASKS python3 -m src.run_defuse $parameter_file $input_dir

