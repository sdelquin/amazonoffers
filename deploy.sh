#!/bin/bash

source ~/.pyenv/versions/amazonoffers/bin/activate
cd "$(dirname "$0")"
git pull
pip install -r requirements.txt
