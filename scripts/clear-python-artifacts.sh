#!/bin/bash

SCRIPT=$(realpath "$0")
SCRIPT_DIR=$(dirname "$SCRIPT")
REPO_PATH=$(dirname "$SCRIPT_DIR")

rm -r $REPO_PATH/__pycach__
rm -r $REPO_PATH/storyboard/__pycach__
rm -r $REPO_PATH/*.egg-info
rm -r $REPO_PATH/storyboard/*.egg-info
rm -r $REPO_PATH/storyboard/build
rm -r $REPO_PATH/storyboard/.pytest_cache
rm -r $REPO_PATH/storyboard/__pycach__
rm -r $REPO_PATH/storyboard/storyboard/.pytest_cache
rm -r $REPO_PATH/storyboard/storyboard/__pycach__


