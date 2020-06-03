#!/bin/bash

set -u
set -e

VEC=${1:-text8.tar.gz}
DIR=${2:-word-classes/}

echo "Evaluating $VEC on classes in $DIR" >&2

for d in $DIR/*; do
    if [ -d $d ]; then
	echo `basename $d`: `/home/debian/venv/bin/python evalclass.py -q $VEC $d/*.txt`
    fi
done
