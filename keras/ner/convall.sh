#!/bin/bash

set -e
set -u

for d in data/ner/*; do
    echo "Running" `basename $d`
    /home/debian/venv/bin/python conv.py $d
    echo
done
