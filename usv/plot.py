#!/usr/bin/env python
# encoding: utf-8
import os
from glob import glob
import pylab as pl
import numpy as np

class Plotter(object):
    def __init__(self, folder):
        n_fm_list = []
        n_hfm_list = []
        n_sv_list = []
        p_fm_list = []
        p_hfm_list = []
        p_sv_list = []
        datafiles = glob(os.path.join(folder, 'ppd*.[tT][aA][bB]'))
        datafiles.sort()
        for datafile in datafiles:
            with open(datafile, 'r') as data:
                lines = data.readlines()
                counts = lines[len(lines) - 2]
                freqs = lines[len(lines) - 1]
                tokens = counts.split('\t')
                n_fm_list.append(float(tokens[2]))
                n_hfm_list.append(float(tokens[3]))
                n_sv_list.append(float(tokens[4]))
                p_fm_list.append(float(tokens[2]))
                p_hfm_list.append(float(tokens[3]))
                p_sv_list.append(float(tokens[4]))
        self.ppds = [0, 3, 7, 10, 14, 17, 21, 24, 28]
        self.n_fm = np.array(n_fm_list)
        self.n_hfm = np.array(n_hfm_list)
        self.n_sv = np.array(n_sv_list)
        self.p_fm = np.array(p_fm_list)
        self.p_hfm = np.array(p_hfm_list)
        self.p_sv = np.array(p_sv_list)
        
    def plot_counts(self):
        bar_width = 0.65
        x_pos = np.arange(len(self.ppds))
        p1 = pl.bar(x_pos, self.n_fm, width, color='r', label='n FM')
        p2 = pl.bar(x_pos, self.n_hfm, width, color='g', label='n HFM', bottom=self.n_fm)
        p3 = pl.bar(x_pos, self.n_sv, width, color='b', label='n SV', bottom=(self.n_fm + self.n_hfm))
        pl.title('Counts of each call type over time (PPD)')
        pl.ylabel('Count')
        pl.xlabel('PPD')
        pl.xticks(x_pos+width/2., ppds)
        pl.legend()
        print "Opening bar plot..."
        pl.show()

    def plot_freqs(self):
        pl.figure()
        pl.title('Call type frequencies over time (PPD)')
        pl.xlabel('PPD')
        pl.ylabel('p')
        pl.plot(self.ppds, self.p_fm, 'ro-', label='p(FM)')
        pl.plot(self.ppds, self.p_hfm, 'go-', label='p(HFM)')
        pl.plot(self.ppds, self.p_sv, 'bo-', label='p(SV)')
        pl.grid(True)
        pl.legend()
        print "Opening frequency plot..."
        pl.show()