#!/usr/bin/env python
# encoding: utf-8
import os
from glob import glob
import pylab as pl
import numpy as np

def main():
    plots = all_plots()
    plots['full'].counts()
    pl.title('Counts for each call type over time (full trial)')
    plot_bar(20.5, 889, 259, 332, 1.0)
    plot_bar(22, 25, 14, 97, 1.0)
    pl.savefig('/Users/sloria1/Desktop/count-full.png')
    
    plots['first15'].counts()
    pl.title('Counts folder each call type over time (first 15 min)')
    plot_bar(20.5, 472, 134, 180, 1.0)
    plot_bar(22, 16, 6, 86, 1.0)
    pl.savefig('/Users/sloria1/Desktop/count-15.png')
    
    plots['first5'].counts()
    pl.title('Counts for each call type over time (first 5 min)')
    plot_bar(20.5, 162, 54, 73, 1.0)
    plot_bar(22, 7, 2, 4, 1.0)
    pl.savefig('/Users/sloria1/Desktop/count-5.png')
    
    # plots['full'].freqs()
    # pl.title('Frequencies for each call type over time (full trial)')
    # pl.plot([21], [0.1838], 'rs', label='femA p(FM)')
    # pl.plot([21], [0.1029], 'gs', label='femA p(HFM)')
    # pl.plot([21], [0.7132], 'bs', label='femB p(SV)')
    # draw_arrows2()
    # pl.savefig('/Users/sloria1/Desktop/freq-full.png')
    
    # plots['first15'].freqs()
    # pl.title('Frequencies for each call type over time (first 15 min)')
    # draw_arrows2()
    # pl.plot([21], [0.1838], 'rs', label='femA p(FM)')
    # pl.plot([21], [0.1029], 'gs', label='femA p(HFM)')
    # pl.plot([21], [0.7132], 'bs', label='femB p(SV)')
    # pl.savefig('/Users/sloria1/Desktop/freq-15.png')
    
    # plots['first5'].freqs()
    # pl.title('Frequencies for each call type over time (first 5 min)')
    # pl.plot([21], [0.1838], 'rs', label='femA p(FM)')
    # pl.plot([21], [0.1029], 'gs', label='femA p(HFM)')
    # pl.plot([21], [0.7132], 'bs', label='femB p(SV)')
    # draw_arrows2()
    # pl.savefig('/Users/sloria1/Desktop/freq-5.png')

    pl.ioff()
    pl.show()

def all_plots():
    plots = {}
    plots['full'] = Plotter('bigarena/full')
    plots['first15'] = Plotter('bigarena/first15')
    plots['first5'] = Plotter('bigarena/first5')
    return plots

def draw_arrows1():
    switch1 = (4, 2000)
    switch2 = (6, 2000)
    pl.arrow(switch1[0], switch1[1], 0.0, -100, 
        fc="k", ec="k", head_width=0.7, head_length=0.05)
    pl.arrow(switch2[0], switch2[1], 0.0, -100, 
        fc="k", ec="k", head_width=0.7, head_length=0.05)

def draw_arrows2():
    # pl.arrow( x, y, dx, dy, **kwargs )
    switch1 = (14, 0.9)
    switch2 = (21, 0.9)
    pl.arrow(switch1[0], switch1[1], 0.0, -0.08, 
        fc="k", ec="k", head_width=0.7, head_length=0.05)
    pl.arrow(switch2[0], switch2[1], 0.0, -0.08, 
        fc="k", ec="k", head_width=0.7, head_length=0.05)

def plot_bar(x_pos, n_fm, n_hfm, n_sv, bar_width):
    p1 = pl.bar([x_pos], [n_fm], bar_width, color='r', label='n FM')
    p2 = pl.bar([x_pos], [n_hfm], bar_width, color='g', label='n HFM', bottom=n_fm)
    p3 = pl.bar([x_pos], [n_sv], bar_width, color='b', label='n SV', bottom=(n_fm + n_hfm))

def plot_ppd21_bars():
    plot_bar(20.5, 889, 259, 332, 1.0)
    plot_bar(22, 25, 14, 97, 1.0)

class Plotter(object):
    def __init__(self, folder):
        n_fm_list = []
        n_hfm_list = []
        n_sv_list = []
        
        p_fm_list = []
        p_hfm_list = []
        p_sv_list = []
        datafiles = glob(os.path.join(folder, '*.[tT][aA][bB]'))
        datafiles.sort()
        for datafile in datafiles:
            with open(datafile, 'r') as data:
                lines = data.readlines()
                counts = lines[len(lines) - 2]
                freqs = lines[len(lines) - 1]
                count_tokens = counts.split('\t')
                freq_tokens = freqs.split('\t')
                n_fm_list.append(float(count_tokens[2]))
                n_hfm_list.append(float(count_tokens[3]))
                n_sv_list.append(float(count_tokens[4]))
                p_fm_list.append(float(freq_tokens[2]))
                p_hfm_list.append(float(freq_tokens[3]))
                p_sv_list.append(float(freq_tokens[4]))
        self.x_axis = [0, 3, 7, 10, 14, 17, 24, 28] # PPDs
        self.n_fm = np.array(n_fm_list)
        self.n_hfm = np.array(n_hfm_list)
        self.n_sv = np.array(n_sv_list)
        self.p_fm = np.array(p_fm_list)
        self.p_hfm = np.array(p_hfm_list)
        self.p_sv = np.array(p_sv_list)
        
    def counts(self):
        pl.figure()
        bar_width = 2.0
        x_pos = np.array(self.x_axis)
        p1 = pl.bar(x_pos, self.n_fm, bar_width, color='r', label='n FM')
        p2 = pl.bar(x_pos, self.n_hfm, bar_width, color='g', label='n HFM', bottom=self.n_fm)
        p3 = pl.bar(x_pos, self.n_sv, bar_width, color='b', label='n SV', bottom=(self.n_fm + self.n_hfm))
        pl.title('Counts of each call type over time')
        pl.ylabel('Count')
        pl.xlabel('PPD')
        self.x_axis.append(21)
        self.x_axis.sort()
        x_pos = np.array(self.x_axis)
        pl.xticks(x_pos + bar_width/2., self.x_axis)
        pl.legend()
        print "Opening bar plot..."
        pl.ion()

    def freqs(self):
        pl.figure()
        pl.title('Call type frequencies over time')
        pl.xlabel('PPD')
        pl.ylabel('p')
        pl.plot(self.x_axis, self.p_fm, 'ro-', label='p(FM)')
        pl.plot(self.x_axis, self.p_hfm, 'go-', label='p(HFM)')
        pl.plot(self.x_axis, self.p_sv, 'bo-', label='p(SV)')
        pl.grid(True)
        pl.legend()
        print "Opening frequency plot..."
        pl.ion()

if __name__ == '__main__':
    main()