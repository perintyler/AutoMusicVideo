#!/bin/bash

IMAGE_NAME="automusicvideo"
SCRIPT=$(realpath "$0")
SCRIPT_DIR=$(dirname "$SCRIPT")
REPO_PATH=$(dirname "$SCRIPT_DIR")
SRC_DIR="$REPO_PATH/auto_music_video"
MODAL_MOUNT_DIRECTORY="/tmp/modal-files"


rm -rf $MODAL_MOUNT_DIRECTORY
mkdir $MODAL_MOUNT_DIRECTORY

cp -r $SRC_DIR/ "$MODAL_MOUNT_DIRECTORY"
cp -r $REPO_PATH/storyboards $MODAL_MOUNT_DIRECTORY

cp "$REPO_PATH/pyproject.toml" $MODAL_MOUNT_DIRECTORY

cd $SRC_DIR
modal run run_on_modal.py
