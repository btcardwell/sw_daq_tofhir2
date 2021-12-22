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
    for portID, slaveID, chipID, channelID, vth_t1,  vth_t2,  vth_e in entries:
			
        portIDnew = 1
        slaveIDnew = 6

        if chipID == 6:
		chipIDnew = 0
       		print("something")
        if chipID == 7:
		chipIDnew = 1
        
        index_file.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (portIDnew, slaveIDnew, chipIDnew, channelID, vth_t1, vth_t2, vth_e))
        i=i+1
        print "entry = %d" % i
    
    
    index_file.close()
        


if __name__ == '__main__':
    sys.exit(main(sys.argv))
