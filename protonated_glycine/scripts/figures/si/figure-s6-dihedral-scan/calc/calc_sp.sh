#!/bin/bash

MBX_HOME_OLD=/home/zsolomon/codes/old-mbx-for-test/MBX-dev
MBX_HOME_NEW=/home/zsolomon/codes/mbx-tests/ACTUAL/MBX+IPI


rm energies-plus-old.dat mb_temp*

python ${MBX_HOME_NEW}/scripts/format_conversion/xyz2nrg.py configs.xyz
${MBX_HOME_NEW}/bin/single_point configs.nrg mbx.json i| awk '{print $2}' > mb_temp
${MBX_HOME_OLD}/bin/single_point configs.nrg mbx.json i| awk '{print $2}' > mb_temp2
paste ref_temp mb_temp mb_temp2 >> energies-plus-old.dat
