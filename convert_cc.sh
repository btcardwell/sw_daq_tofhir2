#!/bin/bash

tb_list=("06" "07")
extraLabel="_mappedTo_slot_0_3"

outFold="calibration_files/combined_FE${tb_list[0]}_FE${tb_list[1]}${extraLabel}"
rm -rf "${outFold}"
mkdir "${outFold}"
cp calibration_files/TB07/config.ini "${outFold}/"

for tb in "${tb_list[@]}"
do

    port=1
    slave=0
    if [ "${tb}" == "${tb_list[1]}" ]
    then
	port=1
	slave=2
    fi

    inFold="calibration_files/FE${tb}"
    
    for file in {"disc_settings","bias_settings","bias_calibration","qdc_calibration","tdc_calibration","disc_calibration","map_channel"}
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
		########### TMP SWAP ##################3
		if [ "${file}" != "bias_settings" ] && [ "${file}" != "bias_calibration" ] && [ "${file}" != "map_channel" ]
		then
		    if [ "${tb}" == "${tb_list[0]}" ] && [ "${line[2]}" == "6" ]
		    then
			line[2]="0"
		    elif [ "${tb}" == "${tb_list[0]}" ] && [ "${line[2]}" == "7" ]
		    then
			line[2]="1"
		    elif [ "${tb}" == "${tb_list[1]}" ] && [ "${line[2]}" == "6" ]
		    then
			line[2]="4"
		    elif [ "${tb}" == "${tb_list[1]}" ] && [ "${line[2]}" == "7" ]
		    then
			line[2]="5"
	
		    else
			line[2]="1"
		    fi
		fi
		########### END TMP SWAP ##################3
		echo "${line[@]}" | sed 's/ /\t/g'
	    fi
	done < "${inFold}/${file}.tsv" >> "${outFold}/${file}.tsv"
    done

done
