for i in {1..25}
do
    sbatch run_job_long.sh Rscript run_model.R austronesian $i
    sbatch run_job_medium.sh Rscript run_model.R semitic $i
    sbatch run_job_medium.sh Rscript run_model.R uralic $i
done
