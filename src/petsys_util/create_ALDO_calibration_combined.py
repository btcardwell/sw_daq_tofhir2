from collections import OrderedDict

list_link = []
list_link.append(0)
list_link.append(1)

list_port = []
list_port.append(2)
list_port.append(3)

list_ASIC = []
list_ASIC.append(0)
list_ASIC.append(1)

list_ALDO = ['A', 'B']

map_input = OrderedDict()
map_input[(0,2,0,'A')] = '../calibration_files/TB03/A0_ALDO_A_high.tsv'
map_input[(0,2,0,'B')] = '../calibration_files/TB03/A0_ALDO_B_high.tsv'
#map_input[(0,2,1,'A')] = '../calibration_files/TB03/ALDO_ALDO_A_high.tsv'
#map_input[(0,2,1,'B')] = '../calibration_files/TB03/ALDO_ALDO_B_high.tsv'

map_input[(1,3,0,'A')] = '../calibration_files/TB07/A0_ALDO_A_high.tsv'
map_input[(1,3,0,'B')] = '../calibration_files/TB07/A0_ALDO_B_high.tsv'
#map_input[(1,3,1,'A')] = '../calibration_files/TB07/ALDO_ALDO_A_high.tsv'
#map_input[(1,3,1,'B')] = '../calibration_files/TB07/ALDO_ALDO_B_high.tsv'



for aldo in list_ALDO:
    outFileName = 'aldo_scan_ALDO_%s_high.tsv' % aldo
    out = open(outFileName, 'w')
    

    for link, port, asic, aldo1 in map_input.keys():
        if aldo1 != aldo:
            continue

        print link, port, asic, aldo
        with open(map_input[(link,port,asic,aldo)], 'r') as f:
            for line in f:
                print line
                readings = line.split()
                line_out = '%d\t%d\t%d\t%3d\t%f\n' %(link,port,asic,int(readings[0]),float(readings[1]))
                out.write(line_out)
    out.close()
