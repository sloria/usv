#!/usr/bin/env python
# encoding: utf-8
"""
data_chars.py
Prints data characteristics of the training data.
Note: Must be executed in the directory where TRAIN_DATA exists.
"""
import os
import sys
from orange import *

# Name of the training data file
TRAIN_DATA = "/Users/sloria1/projects/usv/trainsets/traindata_with_bark.tab"


def main():
    if not os.path.exists(TRAIN_DATA):
        print "Error: Training data file %r does not exist." % (TRAIN_DATA)
        sys.exit(1)
    print TRAIN_DATA
    data = ExampleTable(TRAIN_DATA)
    class_dist(data)


def class_dist(data):
    # Vector of class counts
    counts = [0] * len(data.domain.classVar.values)
    # Vector of class proportions
    r = [0.] * len(counts)
    for e in data:
        counts[int(e.getclass())] += 1
    for i in range (len(counts)):
        r[i] = counts[i] * 100. / len(data)
    
    print "Instances: ", len(data), "total"
    for i in range(len(data.domain.classVar.values)):
        print "%d(%4.1f%%) with class %s" % (counts[i], r[i], data.domain.classVar.values[i])

if __name__ == '__main__':
    main()
