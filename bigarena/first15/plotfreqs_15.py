#!/usr/bin/env python
# encoding: utf-8
from glob import glob
import pylab as pl

p_fm = []
p_hfm = []
p_sv = []

ppds = [0, 3, 7, 10, 14, 17, 21, 24, 28]

datafiles = glob('ppd*.[tT][aA][bB]')
datafiles.sort()

for datafile in datafiles:
    with open(datafile, 'r') as data:
        lines = data.readlines()
        freqs = lines[len(lines) -1]
        tokens = freqs.split('\t')
        p_fm.append(float(tokens[2]))
        p_hfm.append(float(tokens[3]))
        p_sv.append(float(tokens[4]))
 
pl.figure()
pl.title('Call type frequencies over time (PPD) in first 15 min')
pl.xlabel('PPD')
pl.ylabel('p')
pl.plot(ppds, p_fm, 'ro-', label='p(FM)')
pl.plot(ppds, p_hfm, 'go-', label='p(HFM)')
pl.plot(ppds, p_sv, 'bo-', label='p(SV)')
pl.grid(True)
pl.legend()

# fm_sv_ratios = []
# for i in range(len(p_fm)):
#     fm_sv_ratios.append(p_fm[i] / p_sv[i])    
# pl.figure()
# pl.title('FM:SV ratio over time (PPD) in first 15 min')
# pl.xlabel('PPD')
# pl.ylabel('FM:SV ratio')
# pl.plot(ppds, fm_sv_ratios, 'bo')
# pl.grid(True)


# d_ratios = []
# pl.figure()
# x = [3, 7, 10, 14, 17, 21, 24, 28]
# y = [(fm_sv_ratios[i + 1] - fm_sv_ratios[i]) for i in range(0, len(fm_sv_ratios) -1)]
# pl.title('Delta FM:SV over time (PPD) in first 15 min')
# pl.xlabel('PPD')
# pl.ylabel('delta FM:SV')
# pl.plot(x, y, 'go')
# pl.grid(True)

pl.show()