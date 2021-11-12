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
        entry = [str(x) for x in line[0:15]]
        entries.append(entry)
    
    index_file.close()

    new_prefix = prefix + "_cc"
    index_file = open(new_prefix + ".tsv", "w")
    i = 0
# a_file = open("sample.txt","r")
    for portID, slaveID, chipID, channelID, tacID, p0, p1, p2, p3, p4, p5, p6, p7, p8, p9 in entries:
        portIDnew = 1
        slaveIDnew = 3
        # if i < 512:
        #     slaveIDnew = 3
        #     chipIDnew = 23
        # if i >= 512:
        #     slaveIDnew = 1
        #     chipIDnew = 20
        
        index_file.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (portIDnew, slaveIDnew, chipID, channelID, tacID, p0, p1, p2, p3, p4, p5, p6, p7, p8, p9))
        i=i+1
        print "entry = %d" % i
    
    
    index_file.close()
        


if __name__ == '__main__':
    sys.exit(main(sys.argv))
