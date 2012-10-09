#!/usr/bin/env python
# encoding: utf-8
from glob import glob
import pylab as pl
import numpy as np

n_fm = []
n_hfm = []
n_sv = []

ppds = [0, 3, 7, 10, 14, 17, 21, 24, 28]

datafiles = glob('ppd*.[tT][aA][bB]')
datafiles.sort()

for datafile in datafiles:
    with open(datafile, 'r') as data:
        lines = data.readlines()
        counts = lines[len(lines) - 2]
        tokens = counts.split('\t')
        n_fm.append(float(tokens[2]))
        n_hfm.append(float(tokens[3]))
        n_sv.append(float(tokens[4]))
n_fm_array = np.array(n_fm)
n_hfm_array = np.array(n_hfm)
n_sv_array = np.array(n_sv)
x_pos = np.arange(len(ppds))
width = 0.65


p1 = pl.bar(x_pos, n_fm_array, width, color='r', label='n FM')
p2 = pl.bar(x_pos, n_hfm_array, width, color='g', label='n HFM', bottom=n_fm_array)
p3 = pl.bar(x_pos, n_sv_array, width, color='b', label='n SV', bottom=(n_fm_array + n_hfm_array))
pl.title('Counts of each call type over time (PPD) in full trial')
pl.ylabel('Count')
pl.xlabel('PPD')
pl.xticks(x_pos+width/2., ppds)
pl.legend()

print "Opening plot..."
pl.show()
print "Closed plot."