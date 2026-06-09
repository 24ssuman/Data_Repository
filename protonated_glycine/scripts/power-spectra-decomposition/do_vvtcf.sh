#!/bin/bash

rm -r *traj

for i in {1..10}; do
	mkdir ${i}_traj
	cd ${i}_traj
	cp ../../2-nve/${i}_traj/simulation.vel_0.xyz .
	cp ../files/* .
	bash vvtcf.sh
	echo 'vvtcf done in' ${i}_traj
	cd ../
done


cd average
rm -r *dat *png
bash do_avg.sh
cd ../

cd spectral-decomp
bash do_decomp.sh
cd ../
