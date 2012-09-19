#!/usr/bin/env python
# encoding: utf-8
"""
tr.py
Command line utility for adding wav files to their correct training folder.

Usage:
    tr.py [wavfile] [class]
"""

import sys
import shutil
script, src, dest = sys.argv

HFM_PATH = "/Users/sloria1/Dropbox/TRAINING_EXAMPLES/HFM/"
FM_PATH = "/Users/sloria1/Dropbox/TRAINING_EXAMPLES/FM/"
SV_PATH = "/Users/sloria1/Dropbox/TRAINING_EXAMPLES/SV/"
BGNOISE_PATH = "/Users/sloria1/Dropbox/TRAINING_EXAMPLES/BGNOISE/"
UNCLEAR_PATH = "/Users/sloria1/Dropbox/TRAINING_EXAMPLES/UNCLEAR/"

def main():
    if dest == 'hfm':
        shutil.move(src, HFM_PATH)
    elif dest == 'fm':
        shutil.move(src, FM_PATH)
    elif dest == 'sv':
        shutil.move(src, SV_PATH)
    elif dest == 'bg':
        shutil.move(src, BGNOISE_PATH)
    elif dest == 'uc':
        shutil.move(src, UNCLEAR_PATH)
    print "Moved %s to %s" % (src, dest)


if __name__ == '__main__':
    main()

