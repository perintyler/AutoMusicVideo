#!/bin/bash

REGION="us-west2";

REPOSITORY_NAME="quickstart-docker-repo";

GCP_PROJECT_ID=`gcloud config get-value project`;

# the image name can be set with a:
# - cli args (e.g. `./scripts/cloud-build.sh "my-image:my-tag"`)
# - by setting the environment variable $DOCKER_IMAGE_TAG
# - using the default value
if [ -n "$1" ]; then
  DOCKER_IMAGE_NAME="$1";
elif [ -n "$DOCKER_IMAGE_NAME" ]; then
  DOCKER_IMAGE_NAME="$GCP_PROJECT_ID:last-build";
fi

IMAGE_URL="$REGION-docker.pkg.dev/$GCP_PROJECT_ID/$REPOSITORY_NAME/$DOCKER_IMAGE_NAME";

clear && printf '\33c\e[3J'; # clear scrollback
echo "building and pushing '$DOCKER_IMAGE_NAME' to GCP for project '$GCP_PROJECT_ID'";
echo "Image URL: $IMAGE_URL";

# build and push
gcloud builds submit --region=$REGION --tag $IMAGE_URL;
