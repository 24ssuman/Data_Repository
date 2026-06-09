#!/bin/bash

export MBX_HOME=/home/zsolomon/software/mbx+ipi/MBX-dev
export MBFIT_HOME=/home/zsolomon/software/MB-Fit_dev
export OMP_NUM_THREADS=4
export PYTHONPATH=$PYTHONPATH:${MBX_HOME}/scripts/remd_analysis/processing_tools

module load cpu/0.15.4 intel/19.1.1.217   intel-mpi/2019.8.254   gsl/2.5  fftw/3.3.8

source ${MBFIT_HOME}/sourceme.sh

NREPLICAS=32
NBEADS=1

# Symmetry of the system after taking out the ingonred atoms
SYMMETRY="A1B3C1D2E1F1G1H1_I1J2"

## Generate initial frames from xyz
#python ${MBX_HOME}/scripts/remd_analysis/pre-processing/s1-generate_initial_frames.py 10 500 $NREPLICAS $NBEADS input.xyz
#
## Generate nrg file from xyz
#python ${MBX_HOME}/scripts/format_conversion/xyz2nrg.py input.xyz
#
## Run MD equilibriation
#mpirun -np $NREPLICAS ${MBX_HOME}/plugins/repimd/bin/repimd -N 200001 -n 200000 -p 2 -t 2 -s 0.0005 -R 10.0 -U 100.0 -i initial -f final -o output -j trajectory -T $NREPLICAS -I input.nrg -J mbx.json
#
#for i in `seq 1 1 $NREPLICAS`; do
#	printf -v j "%02d" $i
#	cp final.${j} newinitial.${j}
#done
#
## Run REMD simulation
#mpirun -np $NREPLICAS ${MBX_HOME}/plugins/repimd/bin/repimd -N 2000 -n 2000000 -p 4000 -t 4000 -s 0.0005 -R 10.0 -U 100.0 -i newinitial -f newfinal -o newoutput -j newtrajectory -T $NREPLICAS -I input.nrg -J mbx.json
#
#
## Unmix trajectories
#python ${MBX_HOME}/scripts/remd_analysis/post-processing/unmix_trajectories.py newtrajectory $NREPLICAS
#
## Convert trajectories to XYZ
#for i in `seq 1 1 $NREPLICAS`; do 
#  printf -v j "%02d" $i
#  python ${MBX_HOME}/scripts/remd_analysis/post-processing/traj_t_centroid_xyz.py unmixed_newtrajectory.$j $NBEADS
#done
#
## Optimize each trajectory 
#for i in `seq 1 1 $NREPLICAS`; do
#  # Optimize trajectory every 20 frames
#  rm optimized.xyz unconverged.xyz
#  printf -v j "%02d" $i
#  mkdir $j
#  cd $j
#     ${MBX_HOME}/bin/optimize ../input.nrg ../mbx.json 10000 0.0005 ../unmixed_newtrajectory.${j}.xyz 20 &
#  cd ../
#done
#
#wait
#
#for i in `seq 1 1 $NREPLICAS`; do
#  printf -v j "%02d" $i
#  mv $j/optimized.xyz optimized_unmixed_trajectory.${j}.xyz
#
#  # Try converging the ones that did not
#  cd $j
#  if [ -s "unconverged.xyz" ]; then
#    ${MBX_HOME}/bin/optimize  ../input.nrg ../mbx.json 10000 0.0005 unconverged.xyz 1 &
#  fi
#  cd ../
#done
#
#wait
#
#for i in `seq 1 1 $NREPLICAS`; do
#  printf -v j "%02d" $i
#  cd $j
#  if [ -s "unconverged.xyz" ]; then
#    cat optimized.xyz >> ../optimized_unmixed_trajectory.${j}.xyz
#  fi
#  cd ../
#done

# Get the permutations
# Note: The permutations should only be for the atoms to consider 
# (i.e. the atoms not in the ignore lis in the rsc.json file.
python ${MBX_HOME}/scripts/remd_analysis/post-processing/generate_permutations.py $SYMMETRY

# Get Unique isomers in a single file
rm unique_isomers.xyz
for i in `seq 1 1 $NREPLICAS`; do
  printf -v j "%02d" $i
  ${MBX_HOME}/scripts/remd_analysis/rmsd_tools/bin/rsc input.nrg optimized_unmixed_trajectory.${j}.xyz rsc.json
  cat configs_rsc.xyz >> unique_isomers.xyz
done

${MBX_HOME}/scripts/remd_analysis/rmsd_tools/bin/rsc input.nrg unique_isomers.xyz rsc.json
mv configs_rsc.xyz unique_isomers.xyz

# Order the isomers
${MBX_HOME}/bin/order_frames input.nrg unique_isomers.xyz mbx.json
#${MBX_HOME}/install/bin/order_frames input.nrg unique_isomers.xyz mbx.json
mv ordered.xyz unique_isomers_ordered.xyz

# Get populations
python ${MBX_HOME}/scripts/remd_analysis/post-processing/generate_population_data.py unmixed_newtrajectory $NREPLICAS sorted_temperatures.dat pops.json

# Plot populations
python ${MBX_HOME}/scripts/remd_analysis/post-processing/plot_populations.py pops.dat
