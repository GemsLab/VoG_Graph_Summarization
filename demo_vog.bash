#!/bin/bash

echo ''
echo -e "\e[34m======== Steps 1 & 2: Subgraph Generation and Labeling  ==========\e[0m"
matlab -r run_structureDiscovery
echo ''
echo 'Structure discovery finished.'

unweighted_graph='DATA/cliqueStarClique.out'
model='DATA/cliqueStarClique_orderedALL.model'
modelFile='cliqueStarClique_orderedALL.model'
modelTop10='DATA/cliqueStarClique_top10ordered.model'

echo ''
echo -e "\e[34m=============== Step 3: Summary Assembly ===============\e[0m"
echo ''
echo -e "\e[31m=============== TOP 10 structures ===============\e[0m"
head -n 10 $model > $modelTop10
echo 'Computing the encoding cost...'
echo ''
python MDL/score.py $unweighted_graph $modelTop10 > DATA/encoding_top10.out 
echo '>> Output DATA/encoding_top10.out saved.'
echo ': M_0 is the zero-model where the graph is encoded as noise (no structure is assumed).'
echo ': M_x is the model of the graph as represented by the top-10 structures.'
echo ''
cat DATA/encoding_top10.out
echo ''
echo ''

echo -e "\e[31m========= Greedy selection of structures =========\e[0m"
echo 'Computing the encoding cost...'
echo ''
python2.7 MDL/greedySearch_nStop.py $unweighted_graph $model > DATA/encoding_greedyScan.out 
echo '>> Outputs saved in DATA/.'
echo ": DATA/greedyScan_structures_$modelFile has the lines of the $model structures included in the summary."
echo ": DATA/greedyScan_costs_$modelFile has the encoding cost of the considered model at each time step."
echo ''
echo ''
