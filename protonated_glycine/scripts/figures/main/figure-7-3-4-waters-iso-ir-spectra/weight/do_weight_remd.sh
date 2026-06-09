#!/bin/bash



cd 3-water
rm *weighted* 
python ../add.py


cd ../4-water
rm *weighted*
python ../add.py
