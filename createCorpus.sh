#!/bin/bash

# define $1 (raw text directory)
# change your python directory for the sentence splitter and tokenized text
/home/debian/venv/bin/python sentence_splitter.py $1 senSplit.txt
/home/debian/venv/bin/python tokenize_Text.py senSplit.txt tokenize.txt
