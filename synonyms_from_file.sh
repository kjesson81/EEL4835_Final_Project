#!/usr/bin/bash

echo "Please enter the name of the file you wish to find the synonyms for:"
read filename

python3 synonyms.py $filename

echo "results have been written to output.json"
