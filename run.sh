#!/bin/bash

source ~/.pyenv/versions/amazonoffers/bin/activate
cd "$(dirname "$0")"
python main.py $1
