#!/bin/bash

SCRIPT=$(realpath "$0")
SCRIPTPATH=$(dirname "$SCRIPT")
REPOPATH=$(dirname "$SCRIPTPATH")

source "$REPOPATH/.env"
python main.py