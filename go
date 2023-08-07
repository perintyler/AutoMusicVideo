#!/bin/bash

cd $( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
clear && printf '\33c\e[3J' && python3 main.py