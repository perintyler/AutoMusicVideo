#!/bin/bash

if [ -n $GCP_PROJECT_ID ]; then
    gcloud builds submit --region=us-west2 --tag us-west2-docker.pkg.dev/$GCP_PROJECT_ID/quickstart-docker-repo/quickstart-image:tag1
else
  echo "set the 'GCP_PROJECT_ID' enviroment variable"
fi