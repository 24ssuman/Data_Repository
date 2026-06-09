#!/bin/bash



cd 1-water
rm *weighted* 
python ../add.py


cd ../2-water
rm *weighted*
python ../add.py
