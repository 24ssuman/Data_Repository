#!/bin/bash

for i in {1..10}; do
	ln -s ../${i}_traj/dos_quantum_smooth.res spectrum_${i}.dat
done

python add.py
