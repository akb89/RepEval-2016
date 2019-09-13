#!/bin/bash
# $1 = folder that contain all word2vec vector for evaluation

FILES=$(find $1 -type f -name '*.bin')
for file in $FILES
do
	echo $file
	/home/kabbach/venv2/bin/python evaluate.py -i $file #> $file.evaluate.txt
done
