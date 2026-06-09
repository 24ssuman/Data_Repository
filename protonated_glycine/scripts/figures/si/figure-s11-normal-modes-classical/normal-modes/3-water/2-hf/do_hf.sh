#!/bin/bash

MBX_HOME=/home/zsolomon/codes/mbx-tests/ACTUAL/MBX+IPI

python ${MBX_HOME}/scripts/format_conversion/xyz2nrg.py config.xyz

${MBX_HOME}/bin/normal_modes config.nrg mbx.json 1 > out 
