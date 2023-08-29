#!/bin/bash

SCRIPT=$(realpath "$0")
SCRIPT_DIR=$(dirname "$SCRIPT")
REPO_PATH=$(dirname "$SCRIPT_DIR")
STORYBOARD_DIRECTORY=$REPO_PATH/storyboard

rm -r $STORYBOARD_DIRECTORY/storyboard.egg-info
rm -r $STORYBOARD_DIRECTORY/build

python -m pip uninstall storyboard -y

pushd $STORYBOARD_DIRECTORY
python -m pip install .
popd

