#!/bin/bash

SCRIPT=$(realpath "$0")
SCRIPT_DIR=$(dirname "$SCRIPT")

for path_to_script in $SCRIPT_DIR; do
  chmod +x $path_to_script;
done
