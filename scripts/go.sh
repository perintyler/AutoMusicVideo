#!/bin/bash

SCRIPT=$(realpath "$0")
SCRIPTPATH=$(dirname "$SCRIPT")
REPOPATH=$(dirname "$SCRIPTPATH")

cd $REPOPATH;
. env/bin/activate;
clear && printf '\33c\e[3J' && python3 main.py
