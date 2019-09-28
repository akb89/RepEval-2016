#! /bin/bash

FILES=$(find $1 -type f -name '*.bin' -o -name '*.npy')
OUT=$2
JOBS=10

runner() {
	home=$(pwd)/keras
	dataPath=$home'/ner/data/ner'
	DATASETS=($dataPath/CoNLL03 $dataPath/CoNLL00 $dataPath/PTB-pos)
    echo /home/kabbach/venv2/bin/python $home/ner/run_xp_single.py ${DATASETS[@]} $1
}
export -f runner
parallel --citation -j ${JOBS} runner ::: ${FILES} > ${OUT} 
