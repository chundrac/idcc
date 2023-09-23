for i in {1..10}
do
    for fam in "dravidian" "turkic"
    do
	sbatch run_job_medium.sh Rscript run_model.R $fam $i
    done
done


for i in {1..10}
do
    for fam in "austronesian" "indoeuropean" "sinotibetan" "utoaztecan"
    do
	sbatch run_job_long.sh Rscript run_model.R $fam $i
    done
done
