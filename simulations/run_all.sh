for i in {0..1}
do
	for j in {0..1}
	do
		for k in {0..1}
		do
			for l in {1..100}
			do
				sbatch run_job.sh Rscript simulation.R $i $j $k $l
			done
		done
	done
done
