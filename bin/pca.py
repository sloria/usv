#!/usr/bin/env python
import os
import sys
from glob import glob
import pylab as pl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import yaafelib as yf
import scipy.stats as spstats

def main():
    script, ppd0_pth, ppd7_pth = sys.argv    
    
    ppd0_data = []
    for call1 in glob(os.path.join(ppd0_pth, "*.[wW][aA][vV]")):
        print 'Appending ' + call1
        ppd0_data.append(extract(call1))
    ppd0_array = np.array(ppd0_data)
    ppd0_results = pl.mlab.PCA(ppd0_array)
    
    ppd7_data = []
    for call2 in glob(os.path.join(ppd7_pth, "*.[wW][aA][vV]")):
        print 'Appending ' + call2
        ppd7_data.append(extract(call2))
    ppd7_array = np.array(ppd7_data)   
    ppd7_results = pl.mlab.PCA(ppd7_array)
    
    x1 = []
    y1 = []
    z1 = []
    for item in ppd0_results.Y:
        x1.append(item[0])
        y1.append(item[1])
        z1.append(item[2])

    x2 = []
    y2 = []
    z2 = []
    for item in ppd7_results.Y:
        x2.append(item[0])
        y2.append(item[1])
        z2.append(item[2])
    
    # Create figure and plot data    
    pl.close('all')
    fig1 = pl.figure()
    ax = Axes3D(fig1)
    plot_data1 = [x1,y1,z1]
    ax.scatter(plot_data1[0], plot_data1[1], plot_data1[2], c='b')
    plot_data2 = [x2,y2,z2]
    ax.scatter(plot_data2[0], plot_data2[1], plot_data2[2], c='r')
    
    # make simple, bare axis lines through space:
    xAxisLine = ((min(plot_data1[0] + plot_data2[0]), max(plot_data1[0] + plot_data2[0])), (0, 0), (0,0)) # 2 points make the x-axis line at the data extrema along x-axis 
    ax.plot(xAxisLine[0], xAxisLine[1], xAxisLine[2], 'k') 
    yAxisLine = ((0, 0), (min(plot_data1[1] + plot_data2[1]), max(plot_data1[1] + plot_data2[1])), (0,0)) # 2 points make the y-axis line at the data extrema along y-axis
    ax.plot(yAxisLine[0], yAxisLine[1], yAxisLine[2], 'k') 
    zAxisLine = ((0, 0), (0,0), (min(plot_data1[2] + plot_data2[2]), max(plot_data1[2] + plot_data2[2]))) # 2 points make the z-axis line at the data extrema along z-axis
    ax.plot(zAxisLine[0], zAxisLine[1], zAxisLine[2], 'k') 

    # label the axes 
    ax.set_xlabel("x-axis label") 
    ax.set_ylabel("y-axis label")
    ax.set_zlabel("z-axis label")
    ax.set_title("PCA plot of PPD0 and PPD7 calls")
    print 
    pl.show() 
    
def extract(audiofile, sample_rate=11025):
    """Return a feature vector for an audiofile.
    
    Arguments:
    audioFile -- WAV file to process
    sampleRate -- sample rate of the audio file in Hz
    """
    N_MFCC = 12 # Number of MFCC coefficients
    N_LLD = 2 # Number of other low-level descriptors
    N_FUNCS = 4 # Number of functionals

    # Add features to extract
    featplan = yf.FeaturePlan(sample_rate=sample_rate, resample=False)
#     featplan.addFeature('mfcc: MFCC CepsIgnoreFirstCoeff=0 CepsNbCoeffs=8 \
# FFTWindow=Hanning MelMinFreq=1000 MelMaxFreq=4000')
    featplan.addFeature('energy: Energy')
    featplan.addFeature('zcr: ZCR')
    featplan.addFeature('specstats: SpectralShapeStatistics')
    # featplan.addFeature('tempstats: TemporalShapeStatistics')
    
    # Configure an Engine
    engine = yf.Engine()
    engine.load(featplan.getDataFlow())
    
    # Extract features
    afp = yf.AudioFileProcessor()
    afp.processFile(engine, audiofile)

    # Create feature vector
    features = []
    ##### MFCCs #####
    # mfccs = engine.readOutput('mfcc')
    # for i in range(mfccs[0].size):
    #     features.append(mfccs[:, i].mean())
        # features.append(mfccs[:, i].std())
        # features.append(spstats.skew(mfccs[:, i]))
        # features.append(spstats.kurtosis(mfccs[:, i]))
    ##### Energy #####
    energy = engine.readOutput('energy')
    for i in range(energy[0].size):
        features.append(energy[:, i].mean())
    #     features.append(energy[:, i].std())
    #     features.append(spstats.skew(energy[:, i]))
    #     features.append(spstats.kurtosis(energy[:, i]))
    ##### ZCR #####
    zcr = engine.readOutput('zcr')
    for i in range(zcr[0].size):
        features.append(zcr[:, i].mean())
    #     features.append(zcr[:, i].std())
    #     features.append(spstats.skew(zcr[:, i]))
    #     features.append(spstats.kurtosis(energy[:, i]))
    ##### SPECSTATS #####
    specstats = engine.readOutput('specstats')
    for i in range(specstats[0].size):
        features.append(specstats[:, i].mean())
        # features.append(specstats[:, i].std())
        # features.append(spstats.skew(specstats[:, i]))
        # features.append(spstats.kurtosis(specstats[:, i]))
    ##### TEMP STATS #####
    # tempstats = engine.readOutput('tempstats')
    # for i in range(tempstats[0].size):
    #     features.append(tempstats[:, i].mean())
        # features.append(tempstats[:, i].std())
        # features.append(spstats.skew(tempstats[:, i]))
        # features.append(spstats.kurtosis(tempstats[:, i]))
        
    return np.array(features)
        
if __name__ == '__main__':
    main()