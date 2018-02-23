#!/usr/bin/env bash
echo Running CIFAR extender script
pip3 install -r requirements.txt
if [ ! -f data/images.csv ]; then
    echo "Gathering image urls"
    python3 cifar_extender/cifar_parser.py
fi
python3 cifar_extender/cifar_download.py 250
echo Done
