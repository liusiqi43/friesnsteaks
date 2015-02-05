#!/bin/bash
IFS=" "
for dir in */; do
    i=0
    class=${dir%?}
    sed 1d ${dir}bb_info.txt | while read id x1 y1 x2 y2 ; do 
        echo "processing img: ${class}/${id}"
        convert -extract $(($x2-$x1))x$(($y2-$y1))+$x1+$y1 "${class}/${id}.jpg" "output/img_${class}_${i}.jpg"
        ((i++))
    done 
done
