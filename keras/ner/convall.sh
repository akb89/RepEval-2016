#!/bin/bash

set -e
set -u

for d in data/ner/*; do
    echo "Running" `basename $d`
    /home/kabbach/venv2/bin/python conv.py $d
    echo
done
