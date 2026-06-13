#!/bin/bash

MBX_HOME=/home/zsolomon/codes/mbx-tests/ACTUAL/MBX+IPI

python ${MBX_HOME}/scripts/format_conversion/xyz2nrg.py config.xyz

${MBX_HOME}/bin/optimize config.nrg ../mbx.json 100000 0.00005 > out 
