list_ASIC = []
#list_ASIC.append(0)
list_ASIC.append(2)

list_ALDO = ['A', 'B']

map_input = {}
for asic in list_ASIC:
    map_input[asic] = {}

#map_input[0]['A'] = '../config/ALDO_T2TB04/aldo_scan_ALDO_A_high.tsv'
#map_input[0]['B'] = '../config/ALDO_T2TB04/aldo_scan_ALDO_B_high.tsv'
#map_input[2]['A'] = '../config/ALDO_T2TB03_v0/aldo_scan_ALDO_A.tsv'
#map_input[2]['B'] = '../config/ALDO_T2TB03_v0/aldo_scan_ALDO_B.tsv'
map_input[2]['A'] = 'ALDO_T2TB03_v0/aldo_scan_ALDO_A_low_RECALIB.tsv'
map_input[2]['B'] = 'ALDO_T2TB03_v0/aldo_scan_ALDO_B_low_RECALIB.tsv'

for aldo in list_ALDO:
    outFileName = 'aldo_scan_ALDO_%s_low_RECALIB.tsv' % aldo
    out = open(outFileName, 'w')
    
    for asic in list_ASIC:
        with open(map_input[asic][aldo], 'r') as f:
            print "ASIC:",asic 
            for line in f:
                readings = line.split()
                line_out = '0\t0\t%d\t%3d\t%f\n' %(asic,int(readings[3]),float(readings[4]))
                print line_out 
                out.write(line_out)
    out.close()
                
