#!/bin/bash

echo starting
N=3 #number of graphs to generate
L=10 #size of side of square
M=100 #nb of bonds to remove

for i in $(seq 1 $N)
do
    ./make_graph $L $M $i percolate_L_${L}_$i
done
echo done
