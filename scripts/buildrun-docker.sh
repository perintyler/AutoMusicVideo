#!/bin/bash

IMAGE_NAME="automusicvideo"
SCRIPT=$(realpath "$0")
SCRIPT_DIR=$(dirname "$SCRIPT")
REPO_PATH=$(dirname "$SCRIPT_DIR")
ENV_FILE_PATH="$REPO_PATH/.env"

docker build -t $IMAGE_NAME $REPO_PATH
docker run --env-file $ENV_FILE_PATH automusicvideo
