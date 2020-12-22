# import os

for year in [2017,2018]:
    bril_file_name = "brilcalc_out_%s.csv"%year
    bril_file = open(bril_file_name, 'r')

    lines = bril_file.readlines()

    run_to_lumi_dict = dict()
    l_int = 0.

    run_to_lumi_out = open('run_to_lumi_out_%s.py'%year, 'w')
    run_to_lumi_out.write('run_to_lumi = {\n')

    for l in lines[2:-3]:
        lspl = l.split(',')
        l_int += float(lspl[4])
        run_to_lumi_out.write('\t%s: %s,\n'%(int(lspl[0][0:6]), l_int))
        # run_to_lumi_dict[int(lspl[0][0:6])] = l_int

    run_to_lumi_out.write('}')