#process austronesian data
cd ACD_processing
./download_data.sh
cd process_data
Rscript process-acd.R
python3 align_forms.py
python3 process_data.py
python3 simulate_sound_change.py
cd ../..

#process semitic data
cd SED_processing
cd SED_data
python3 scrape_SED.py
cd ..
cd process_data
python3 align_forms.py
python3 process_data.py
python3 simulate_sound_change.py
cd ../..

#process uralic data
cd Uralonet_processing
cd Uralonet_data
python3 scrape_Uralonet.py
cd ..
cd process_data
python3 align_forms.py
python3 process_data.py
python3 simulate_sound_change.py
cd ../..

# run cognate traits

cd family_level_distributions
python3 generate_counts.py

cd cognate_models
Rscript process_data.R
./run_models.sh
Rscript get_params.R
Rscript make_histograms.R

git clone https://github.com/chundrac/linguisticCharacterMatrices.git
cp -r linguisticCharacterMatrices/lexibank .
rm -rf linguisticCharacterMatrices

# run cognate-concept models

cd cognate_concept_models
git clone https://github.com/cldf-clts/clts.git
wget https://raw.githubusercontent.com/concepticon/concepticon-data/master/concepticondata/conceptlists/Calude-2011-200.tsv
Rscript generate_lexical_data_sets.R
cd sound_change_simulations
python3 simulate_sound_change.py
cd ..

Rscript process_data.R
./run_models.sh
Rscript get_params.R

Rscript make_histograms.R
Rscript get_CIs.R
Rscript random_effects_HDIs.R
Rscript make_correlations.R

cd SI_graphics
Rscript make_map.R
Rscript make_MCC_trees.R
