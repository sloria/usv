#!/usr/bin/env python
# encoding: utf-8
"""
train.py

Updates the training data using files in EXAMPLE_PATH/HFM, EXAMPLE_PATH/FM,
EXAMPLE_PATH/SV, and EXAMPLE_PATH/BGNOISE as labeled exemplars. Saves the
data in usv/trainsets/traindata.tab

Usage:
    train.py
"""
import os
import subprocess
import sys
from ConfigParser import SafeConfigParser

# check that settings file exists
try:
    file_path = os.path.dirname(os.path.realpath(__file__))
    settings_path = os.path.join(file_path, '..', 'settings.txt')
    with open(settings_path) as f: pass
except IOError as e:
    print "ERROR: No settings file found. Copy 'settings-dist.txt' to 'settings.txt'"\
    " and change the appropriate settings. "
    sys.exit(1)

# Parse settings file
config = SafeConfigParser()
config.read(settings_path)

# Path where the examplars are located
EXAMPLE_PATH = config.get('training', 'train_src')
print EXAMPLE_PATH
# Path where training data will be written to
TRAIN_DATA = os.path.join(config.get('training', 'train_dest'), 'traindata.tab')
COMMAND = "sqk.py"

if not os.path.exists(EXAMPLE_PATH):
    print "Error: Examples folder does not exist. Change the 'train_dest'" \
            "setting in settings.txt."
    print "Current setting: {0}".format(EXAMPLE_PATH)
    sys.exit(1)

train_HFM = COMMAND + " -p " + os.path.join(EXAMPLE_PATH, "HFM") + " -t hfm -d " + TRAIN_DATA
train_FM = COMMAND + " -p " + os.path.join(EXAMPLE_PATH, "FM") + " -t fm -d " + TRAIN_DATA
train_SV = COMMAND + " -p " + os.path.join(EXAMPLE_PATH, "SV") + " -t sv -d " + TRAIN_DATA
train_BG = COMMAND + " -p " + os.path.join(EXAMPLE_PATH, "BGNOISE") + " -t bgnoise -d " + TRAIN_DATA
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
