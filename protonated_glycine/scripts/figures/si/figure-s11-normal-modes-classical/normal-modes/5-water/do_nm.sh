#!/bin/bash


cd 1-opt
bash do_opt.sh
cat unconverged.xyz optimized.xyz > ../2-hf/config.xyz
cd ../2-hf
bash do_hf.sh

