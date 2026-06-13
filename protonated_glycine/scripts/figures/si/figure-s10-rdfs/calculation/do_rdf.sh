#!/bin/bash

for i in {2..2}; do
	cd ${i}-water
	python ../rdf_calculation.py
	cd ../
done 
