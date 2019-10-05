#!/bin/bash

# $1 = folder for testing word2vec vector.bin

home=$(pwd)/keras
dataPath=$home'/ner/data/ner'
OUT=$2
# echo $home

#DIR=$home'/ner/evaluation' #"$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
#echo $DIR
FILES=$(find $1 -type f -name '*.bin' -o -name '*.npy')
#DATASETS=($dataPath/CoNLL03 $dataPath/CoNLL00 $dataPath/PTB-pos)
DATASETS=($dataPath/CoNLL03 $dataPath/CoNLL00)
#/Users/akb/Desktop/venv2/bin/python $home/ner/run_xp.py ${DATASETS[@]} $FILES
echo -e "MODEL\tCONLL00\tCONLL03\tPTB\tCONLL00-OOV\tCONLL03-OOV\tPTB-OOV" > ${OUT}
for file in $(echo $FILES | xargs -n1 | sort | xargs)
do
  /Users/akb/Desktop/venv2/bin/python $home/ner/run_xp_single.py ${DATASETS[@]} $file 2>> ${OUT}
	# for f in $dataPath/CoNLL03 $dataPath/CoNLL00 $dataPath/PTB-pos
	# do
	# /Users/akb/Desktop/venv2/bin/python $home/ner/mlp.py $f $file
	# done
done
# /Users/akb/Desktop/venv2/bin/python $home/ner/output_results.py

# result located in log and prediction file
# wait
