#!/bin/bash
#SBATCH -A UKAEA-AP002-CPU
#SBATCH -p icelake
#SBATCH --job-name=defuse
#SBATCH --output=defuse-%A.out
#SBATCH --time=0:50:00
#SBATCH --mem=128G
#SBATCH --ntasks=4
#SBATCH -N 1

# File containing parameters to extract
parameter_file=./jobs/test.csv
# Input directory
input_dir=./data/input
# Output directory
output_dir=./data/output

# Load Python
module load python/3.9.12/gcc/pdcqf4o5
# Load Matlab
module load matlab/r2024a

source ~/fair-mast-ingestion/fair-mast-ingestion/bin/activate 
mpirun -np $SLURM_NTASKS python3 -m src.run_defuse $parameter_file $input_dir

