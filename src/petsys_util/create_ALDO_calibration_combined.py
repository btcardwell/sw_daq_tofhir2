list_ASIC = []
list_ASIC.append(0)
#list_ASIC.append(2)

list_ALDO = ['A', 'B']

map_input = {}
for asic in list_ASIC:
    map_input[asic] = {}

list_rang = ['low', 'high']

for rang in list_rang:
    
    map_input[0]['A'] = '../config_2B/T2TB_2B_0009/test_ASIC0_ALDO_A_%s.tsv'%rang
    map_input[0]['B'] = '../config_2B/T2TB_2B_0009/test_ASIC0_ALDO_B_%s.tsv'%rang
    #map_input[2]['A'] = '../config_2B/T2TB_2B_0009/test_ASIC2_ALDO_A_%s.tsv'%rang
    #map_input[2]['B'] = '../config_2B/T2TB_2B_0009/test_ASIC2_ALDO_B_%s.tsv'%rang

  
    for aldo in list_ALDO:
        outFileName = 'aldo_scan_ALDO_%s_%s.tsv' %(aldo,rang)
        out = open(outFileName, 'w')
        
        for asic in list_ASIC:
            with open(map_input[asic][aldo], 'r') as f:
                for line in f:
                    print line
                    readings = line.split()
                    line_out = '0\t0\t%d\t%3d\t%f\n' %(asic,int(readings[0]),float(readings[1]))
                    out.write(line_out)
        out.close()
