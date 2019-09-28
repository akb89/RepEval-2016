#! /bin/bash
home=$(pwd)/keras
dataPath=$home'/ner/data/ner'
FILES=$(find $1 -type f -name '*.bin' -o -name '*.npy')
DATASETS=($dataPath/CoNLL03 $dataPath/CoNLL00 $dataPath/PTB-pos)
OUT=$2
JOBS=10

runner() {
    echo /home/kabbach/venv2/bin/python $home/ner/run_xp_single.py ${DATASETS[@]} $1
}
export -f runner
parallel -j ${JOBS} runner ::: ${FILES} > ${OUT} 
