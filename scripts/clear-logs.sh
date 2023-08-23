#!/bin/bash

SCRIPT=$(realpath "$0")
SCRIPT_DIR=$(dirname "$SCRIPT")
REPO_PATH=$(dirname "$SCRIPT_DIR")
LOGS_DIR="$REPO_PATH/logs"

rm -r $LOGS_DIR
mkdir $LOGS_DIR
