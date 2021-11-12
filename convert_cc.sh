#!/bin/bash

outFold="calibration_files/combined_TB03_TB07"
rm -rf "${outFold}"
mkdir "${outFold}"
cp calibration_files/TB07/config.ini "${outFold}/"

for tb in {3,7}
do

    port=0
    slave=2
    if [ "${tb}" == 7 ]
    then
	port=1
	slave=3
    fi

    inFold="calibration_files/TB0${tb}"
    
    for file in {"disc_settings","bias_settings","bias_calibration","qdc_calibration","tdc_calibration","disc_calibration","disc_settings","map_channel"}
    do
	while read lines
	do
	    line=($lines)
	    if [ "${line[0]}" == "#" ]
	    then
		echo "${lines}"
	    else
		line[0]="${port}"
		line[1]="${slave}"
		echo "${line[@]}" | sed 's/ /\t/g'
	    fi
	done < "${inFold}/${file}.tsv" >> "${outFold}/${file}.tsv"
    done

done
