#!/bin/bash

WD=$PWD

for i in {2..6}; do
#for dir in */; do
#    cd $dir
#    echo $dir
    cd ${i}-water
    bash do_nm.sh
    echo nm done in ${i}-water
    cd $WD
done
