#!/bin/bash

for d in */; do
    [[ "$d" == "1-visualization/" ]] && continue
    [[ "$d" == "free-water-oh/" ]] && continue
    cd "$d"
    rm -r *traj do_vvtcf.sh
    cat ../../do_vvtcf.sh | sed '/simulation.vel_0.xyz/d' | sed 's:bash vvtcf.sh:ln -s ../../../${i}_traj/dump.lammpstrj\n\tbash vvtcf.sh:g' | sed '19,21d' > do_vvtcf.sh
    bash do_vvtcf.sh
    echo "$d" done
    cd ..
done


cd 1-visualization/
python plot.py
python plot_high_freq.py
