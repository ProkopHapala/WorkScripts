#!/bin/bash

# This script multiply xyz movie file answer.xyz
# It use image script written by prokop so you must have image in your bin directory
# run the script by typing ./image_movie.sh 2 1 1 


# read number of atoms

x=$1
y=$2
z=$3

atoms=`head -1 answer.xyz`
list=$(($atoms+2))
#echo $atoms,$list

# read number of lines and calculate num of steps
#lines=`nl answer.xyz | tail -1 | awk '{print $1}'`
#steps=$((lines / list))
steps=`grep ETOT answer.xyz | nl | tail -1 | awk '{print $1}'`

#echo $lines, $steps

for i in $(eval echo "{1..$steps}"); do
aa=$(($i*$list)) ;
head -$aa answer.xyz | tail -$list | x2b > answer.bas ;
image $x $y $z > aaa ;
cat answer-image.xyz >> answer_.xyz ;

echo $i ;

done

rm aaa