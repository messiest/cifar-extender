#!/usr/bin/env bash
echo Running CIFAR extender script
pip3 install -r requirements.txt
python3 cifar_extender/cifar_parser.py
#python3 cifar_extender/cifar_download.py 1000
echo Done
