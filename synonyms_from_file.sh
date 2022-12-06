#!/usr/bin/bash

echo "Please enter the name of the file you wish to find the synonyms for. If you want to enter a single word, press enter and wait for next prompt.:"
read filename

python3 synonyms.py $filename

echo "results have been written to output.json"
