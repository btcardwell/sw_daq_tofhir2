#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

def main(argv):
    
    prefix = argv[1]
    index_file = open(prefix + ".tsv", "r")
    entries = []

    for line in index_file:
        line = line[:-1]
        if line[0] == "#": continue
        line = line.split("\t")
        entries.append(line)
    
    index_file.close()

    new_prefix = prefix + "_cc"
    index_file = open(new_prefix + ".tsv", "w")
    i = 0
    # a_file = open("sample.txt","r")
    for portID, slaveID, chipID, channelID, baseline_T, baseline_E, zero_T1, zero_T2, zero_E, noise_T1, noise_T2, noise_E in entries:
        portIDnew = 1
        slaveIDnew = 3
        # if i < 512:
        #     slaveIDnew = 3
        #     chipIDnew = 23
        # if i >= 512:
        #     slaveIDnew = 1
        #     chipIDnew = 20
        
        index_file.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (portIDnew, slaveIDnew, chipID, channelID, baseline_T, baseline_E, zero_T1, zero_T2, zero_E, noise_T1, noise_T2, noise_E))
        i=i+1
        print "entry = %d" % i
    
    
    index_file.close()
        


if __name__ == '__main__':
    sys.exit(main(sys.argv))
