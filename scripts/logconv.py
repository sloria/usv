#!/usr/bin/env python
# encoding: utf-8
"""
logconv.py
Convert the date times in an Avisoft-Recorder playback log file to elapsed
times.

Usage:
    logconv.py [logfile]
"""

from sys import *
from datetime import *
import os

def main():
    USAGE = "USAGE: %s [input.log]" % os.path.basename(argv[0])

    if len(argv) < 2:
        print "ERROR: Must specify an input file."
        print USAGE
        exit(1)
    elif len(argv) > 2:
        print "ERROR: Too many arguments."
        print USAGE
        exit(1)

    script, infile = argv

    try:
        logfile = open(infile, 'r')
        print "Opened " + infile
    except IOError:
        print "ERROR: Log file %r not found." % infile
        print USAGE
        exit(1)

    output = open("output.log", "w+")
    starttime = None
    lines = logfile.readlines()
    for i in range(0, len(lines)):
        line = lines[i]
        tokens = line.split()
        if tokens[0] == "#start":
            trial_name = tokens[1]
            output.write(line)
            print line.strip()
            start = lines[i+1].split()
            start_date = start[0] + " " + start[1]
            starttime = datetime.strptime(start_date, "%m/%d/%y %H:%M:%S")
        elif tokens[0] == "#end":
            output.write(line)
            print line.strip()
            continue
        else:
            date_string = tokens[0] + " " + tokens[1]
            time = datetime.strptime(date_string, "%m/%d/%y %H:%M:%S")
            d = time - starttime
            sound_file = line[18:-1]
            output.write(str(d) + " " + sound_file)
            print str(d) + " " + sound_file
    logfile.close()
    print "Success!"


if __name__ == '__main__':
    main()