#!/bin/bash

clear

REGION="us-west2";

ARTIFACTS_REGISTRY_REPO_NAME="quickstart-docker-repo";

GCP_PROJECT_ID=`gcloud config get-value project`

if [ -n $IMAGE_NAME ]; then
  IMAGE_NAME="auto-music-video"
fi

if [ -n $IMAGE_NAME ]; then
  IMAGE_TAG="tag1"
fi

IMAGE_URI="$REGION-docker.pkg.dev"

BUILD_ID="$IMAGE_NAME:$IMAGE_TAG"

IMAGE_PATH=$IMAGE_URI/$GCP_PROJECT_ID/$ARTIFACTS_REGISTRY_REPO_NAME/$BUILD_ID

gcloud builds submit --region=$REGION --tag $IMAGE_PATH
