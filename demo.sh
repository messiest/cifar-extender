#!/usr/bin/env bash
echo Running CIFAR extender script
pip3 install -r requirements.txt
if ![-e data/images.csv]
then
    python3 cifar_extender/cifar_parser.py
fi
python3 cifar_extender/cifar_download.py 50
echo Done
