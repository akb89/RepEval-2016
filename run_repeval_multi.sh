#! /bin/bash
. /usr/bin/env_parallel.bash
FILES=$(find $1 -type f -name '*.bin' -o -name '*.npy')
OUT=$2
JOBS=1

runner() {
        home=$(pwd)/keras
        dataPath=$home'/ner/data/ner'
        DATASETS=($dataPath/CoNLL03 $dataPath/CoNLL00 $dataPath/PTB-pos)
        /home/debian/venv/bin/python $home/ner/run_xp_single.py ${DATASETS[@]} $1
}
export -f runner
echo -e "MODEL\tCONLL00\tCONLL03\tPTB\tCONLL00-OOV\tCONLL03-OOV\tPTB-OOV" > ${OUT}
env_parallel -j ${JOBS} runner ::: ${FILES} >> ${OUT}
