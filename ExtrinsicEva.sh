#!/bin/bash

# $1 = folder for testing word2vec vector.bin

home=$(pwd)/keras
dataPath=$home'/ner/data/ner'
# echo $home

#DIR=$home'/ner/evaluation' #"$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
#echo $DIR
FILES=$(find $1 -type f -name '*.bin' -o -name '*.npy')
DATASETS=($dataPath/CoNLL03 $dataPath/CoNLL00 $dataPath/PTB-pos)
/home/kabbach/venv2/bin/python $home/ner/run_xp.py ${DATASETS[@]} $FILES
# for file in $(echo $FILES | xargs -n1 | sort | xargs)
# do
# 	for f in $dataPath/CoNLL03 $dataPath/CoNLL00 $dataPath/PTB-pos
# 	do
# 	/home/kabbach/venv2/bin/python $home/ner/mlp.py $f $file
# 	done
# done
# /home/kabbach/venv2/bin/python $home/ner/output_results.py
#
# # result located in log and prediction file
# wait
