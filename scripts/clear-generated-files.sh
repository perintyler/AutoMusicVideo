#!/bin/bash

SCRIPT=$(realpath "$0")
SCRIPT_DIR=$(dirname "$SCRIPT")
REPO_PATH=$(dirname "$SCRIPT_DIR")

rm -r $REPO_PATH/music-videos;
mkdir $REPO_PATH/music-videos;
