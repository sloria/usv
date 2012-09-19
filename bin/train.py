#!/usr/bin/env python
# encoding: utf-8
"""
train.py

Updates the training data using files in EXAMPLE_PATH/HFM, EXAMPLE_PATH/FM,
EXAMPLE_PATH/SV, and EXAMPLE_PATH/BGNOISE as labeled exemplars. Saves the
trainingdata.tab in the current working directory.

Note: Must specify the path where the examples are located and the path where
training data will be written.

Usage:
    train.py
"""
import os
import subprocess
import sys

# Path where the examplars are located
EXAMPLE_PATH = "/Users/sloria1/Dropbox/TRAINING_EXAMPLES/"
TRAIN_DATA = "/Users/sloria1/projects/usv/trainsets/traindata.tab"
COMMAND = "sqk.py"

if not os.path.exists(EXAMPLE_PATH):
    print "Error: Examples folder does not exist"
    print "Current directory: %r" % (os.getcwd())
    sys.exit(1)

train_HFM = COMMAND + " -p " + EXAMPLE_PATH + "HFM -t hfm -d " + TRAIN_DATA
train_FM = COMMAND + " -p " + EXAMPLE_PATH + "FM -t fm -d " + TRAIN_DATA
train_SV = COMMAND + " -p " + EXAMPLE_PATH + "SV -t sv -d " + TRAIN_DATA
train_BG = COMMAND + " -p " + EXAMPLE_PATH + "BGNOISE -t bgnoise -d " + TRAIN_DATA
commands = [train_HFM, train_FM, train_SV, train_BG]

def run_commands(commands):
    for cmd in commands:
        subprocess.call(cmd, shell=True)

def main():
    if os.path.exists(TRAIN_DATA):
        print "Removing old training data. . ."
        subprocess.call('rm ' + TRAIN_DATA, shell=True)
    run_commands(commands)
    print "Finished writing training data."

if __name__ == "__main__":
    main()
