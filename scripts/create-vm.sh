#!/bin/bash

if [ -n "$1" ]; then
  echo "creating instance '$1'";
  gcloud compute instances create $1 \
      --project=lyrics-to-text-dev1 \
      --zone=us-central1-a \
      --machine-type=c2d-highcpu-4 \
      --network-interface=network-tier=PREMIUM,stack-type=IPV4_ONLY,subnet=default \
      --maintenance-policy=MIGRATE \
      --provisioning-model=STANDARD \
      --service-account=324411287970-compute@developer.gserviceaccount.com \
      --scopes=https://www.googleapis.com/auth/devstorage.read_only,https://www.googleapis.com/auth/logging.write,https://www.googleapis.com/auth/monitoring.write,https://www.googleapis.com/auth/servicecontrol,https://www.googleapis.com/auth/service.management.readonly,https://www.googleapis.com/auth/trace.append \
      --enable-display-device \
      --tags=http-server,https-server \
      --create-disk=auto-delete=yes,boot=yes,device-name=instance-15,image=projects/debian-cloud/global/images/debian-11-bullseye-v20230814,mode=rw,size=100,type=projects/lyrics-to-text-dev1/zones/us-central1-a/diskTypes/pd-balanced \
      --no-shielded-secure-boot \
      --shielded-vtpm \
      --shielded-integrity-monitoring \
      --labels=goog-ec-src=vm_add-gcloud \
      --reservation-affinity=any
else
  echo "A CLI argument indicating the name of the instance is required"
fi
