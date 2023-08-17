#!/bin/bash

SCRIPT=$(realpath "$0")
SCRIPT_DIR=$(dirname "$SCRIPT")
REPO_PATH=$(dirname "$SCRIPT_DIR")

ARCHIVE_DIRECTORY=$REPO_PATH/ArchivedAutoMusicVideo;

mkdir $ARCHIVE_DIRECTORY
cp $REPO_PATH/*.py $ARCHIVE_DIRECTORY
cp -r $REPO_PATH/deepdaze-data $ARCHIVE_DIRECTORY
cp -r $REPO_PATH/songs $ARCHIVE_DIRECTORY
cp $REPO_PATH/config.json $ARCHIVE_DIRECTORY

zip -r "AutoMusicVideo.zip" $ARCHIVE_DIRECTORY;
rm -r $ARCHIVE_DIRECTORY;