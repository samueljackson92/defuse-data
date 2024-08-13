#!/bin/bash
#SBATCH -A UKAEA-AP002-CPU
#SBATCH -p icelake
#SBATCH --job-name=lh-mode-tagger
#SBATCH --output=%A_%a.out
#SBATCH --error=%A_%a.err
#SBATCH --array=1-9527  # Adjust this range based on the number of rows in your CSV (1-based index)
#SBATCH --time=0:15:00
#SBATCH --mem=40G

# File containing parameters to extract
parameter_file=./jobs/shots.csv
# Input directory
input_dir=./data/input
# Output directory
output_dir=./data/output

# Read the parameters from the CSV file
IFS=, read -r index shot_id url  <<< $(sed -n "${SLURM_ARRAY_TASK_ID}p" $parameter_file)

# Use the parameters in your command or script
echo "Processing: job_id = $SLURM_ARRAY_TASK_ID shot = $shot_id, url = $url"

mkdir -p $input_dir
mkdir -p $output_dir

input_file="$input_dir/$shot.h5"

python -m download_data $url $input_file
python -m run_defuse $input_file $output_dir

rm $input_file
