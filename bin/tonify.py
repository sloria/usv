#!/usr/bin/env python
# encoding: utf-8
"""
tonify.py
Uses the usv.usvhear.USVAudible class to "tonify" USV recordings.
Arguments are data outputs from sqk.py (data file must have log metadata).

Usage:
    tonify.py [-m | -f] [datafile]...
"""
import sys
import optparse
import usv.usvhear as uh

def main():
    usage = "usage: tonify.py [-m | -f] [datafile]..."
    parser = optparse.OptionParser(usage=usage)

    parser.add_option('-m', '--male', dest='male', action='store',
        metavar='<DATA_FILE>', help="Specify the male data file.")
    parser.add_option('-f', '--female', dest='female', action='store',
        metavar='<DATA_FILE>', help="Specify the female data file.")
    parser.add_option('-o', '--output', dest='outfile', action='store',
        metavar='<FILENAME>', default="tonifyoutput.wav",
        help="Specify the output filename.")
    (opts, args) = parser.parse_args()

    if not (opts.male or opts.female):
        parser.error("Must include '-m' or '-f' option(s) and data file(s).")

    aud = uh.USVAudible()
    tonegen = uh.ToneGenerator(opts.outfile)
    if opts.male:
        try:
            male_data = uh.DataSheet(opts.male)
        except IOError:
            parser.error("Data file %r not found." % opts.male)
        aud.add_data(male_data, (uh.note('f4'), uh.note('d5'), uh.note('c4')))

    if opts.female:
        try:
            female_data = uh.DataSheet(opts.female)
        except IOError:
            parser.error("Data file %r not found." % opts.male)
        aud.add_data(female_data, (uh.note('f6'), uh.note('d7') , uh.note('c6')))
    aud.tonify(tonegen, verbose=True)

if __name__ == "__main__":
    import datetime
    t1 = datetime.datetime.now()
    main()
    t2 = datetime.datetime.now()
    print "Completed in", t2 - t1