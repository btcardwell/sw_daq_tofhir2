list_ASIC = []
list_ASIC.append(0)
list_ASIC.append(2)

list_ALDO = ['A', 'B']

map_input = {}
for asic in list_ASIC:
    map_input[asic] = {}

map_input[0]['A'] = '../config/ALDO_T2TB06_2021_07_15/aldo_scan_ALDO_A_low.tsv'
map_input[0]['B'] = '../config/ALDO_T2TB06_2021_07_15/aldo_scan_ALDO_B_low.tsv'
map_input[2]['A'] = '../config/ALDO_T2TB03_v0_2021_07_15/aldo_scan_ALDO_A_low.tsv'
map_input[2]['B'] = '../config/ALDO_T2TB03_v0_2021_07_15/aldo_scan_ALDO_B_low.tsv'

for aldo in list_ALDO:
    outFileName = 'aldo_scan_ALDO_%s_low.tsv' % aldo
    out = open(outFileName, 'w')
    
    for asic in list_ASIC:
        with open(map_input[asic][aldo], 'r') as f:
            for line in f:
                print line
                readings = line.split()
                line_out = '0\t0\t%d\t%3d\t%f\n' %(asic,int(readings[0]),float(readings[1]))
                out.write(line_out)
    out.close()
