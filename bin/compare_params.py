#!/usr/bin/env python

import sys
import os
import yaafelib as yf
from glob import glob
import pylab as pl
import numpy as np


def test():
    script, audiofile, feature_definition = sys.argv
    print extract(audiofile, feature_definition)

def main():
    script, folder1, folder2 = sys.argv
    FEATURE1 = 'ps: PerceptualSharpness'
    FEATURE2 = 'zcr: ZCR'

    audiofiles1 = glob(os.path.join(folder1, '*.[wW][aA][vV]'))
    audiofiles2 = glob(os.path.join(folder2, '*.[wW][aA][vV]'))
    pl.figure()
    # pl.title('Barks vs. Croons')
    font = {'family' : 'normal',
        'weight' : 'normal',
        'size'   : 25}

    pl.rc('font', **font)
    pl.xlabel('Perceptual Sharpness (acum)')
    pl.ylabel('ZCR (Hz)')
    
    # Plot folder1 data
    x_list1 = []
    y_list1= []
    for audiofile in audiofiles1:
        a = extract(audiofile, FEATURE1)
        b = extract(audiofile, FEATURE2)
        meana = a[:, 0].mean()
        x_list1.append(meana)
        meanb = b[:,0].mean()
        y_list1.append(meanb)
    x_axis1 = np.array(x_list1)
    y_axis1 = np.array(y_list1)
    pl.plot(x_axis1, y_axis1, 'ro', label='Bark')

    # Plot folder2 data
    x_list2 = []
    y_list2 = []
    for audiofile in audiofiles2:
        a = extract(audiofile, FEATURE1)
        b = extract(audiofile, FEATURE2)
        meana = a[:, 0].mean()
        x_list2.append(meana)
        meanb = b[:,0].mean()
        y_list2.append(meanb)
    x_axis2 = np.array(x_list2)
    y_axis2 = np.array(y_list2)
    pl.plot(x_axis2, y_axis2, 'bo', label='SV')

    pl.legend(loc='lower right')
    pl.savefig('/Users/sloria1/Desktop/bark-sv-2-feature-comparison.pdf', bbox_inches='tight')
    # pl.show()


def extract(audiofile, feature_definition, sample_rate=11025):
    # Add features to extract
    featplan = yf.FeaturePlan(sample_rate=sample_rate, resample=False)
    featplan.addFeature(feature_definition)

    # Configure engine
    engine = yf.Engine()
    engine.load(featplan.getDataFlow())

    # Extract features
    afp = yf.AudioFileProcessor()
    afp.processFile(engine, audiofile)
    feature_name = feature_definition.split(':')[0]
    feature = engine.readOutput(feature_name) # 2D array
    return feature

if __name__ == '__main__':
    main()