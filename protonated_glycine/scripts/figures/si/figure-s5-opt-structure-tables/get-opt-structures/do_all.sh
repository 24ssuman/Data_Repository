#!/bin/bash

WD=$PWD

for dir in */; do
    cd $dir
    echo $dir
    bash ../do_opt.sh
    echo opt done in ${dir}
    cd $WD
done
