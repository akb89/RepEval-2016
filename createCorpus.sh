#!/bin/bash

# define $1 (raw text directory)
# change your python directory for the sentence splitter and tokenized text
/home/kabbach/venv2/bin/python sentence_splitter.py $1 senSplit.txt
/home/kabbach/venv2/bin/python tokenize_Text.py senSplit.txt tokenize.txt
