#!/bin/bash

sudo apt-get install git-all -y
git clone https://github.com/perintyler/AutoMusicvideo.git
cd AutoMusicvideo

sudo apt-get install python3-pip -y
python3 -m pip install -r requirements.txt
