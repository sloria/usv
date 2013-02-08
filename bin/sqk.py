#!/usr/bin/env python
# encoding: utf-8
"""
sqk.py

Usage:
    sqk.py [options] [input] [options [classification]]
"""
import optparse
import sys
import os
import datetime
import fnmatch
import subprocess
from glob import glob
import shutil # temporary

import yaafelib as yf
import orange, Orange, orngTree
from Orange.classification.svm import SVMLearner, kernels
import scipy.stats as spstats
import usv.avisoftlog

# Directory where traindata should be written
TRAIN_PATH = '/Users/sloria1/projects/python-projects/usv/trainsets'

def main():
    version = "%prog version 0.1"
    usage = "usage: %prog [options] [input] [options [classification]]"
    desc = "QUICK START: To extract data from a trial, 'cd' to the \
trial's directory and type: 'sqk --classify'. To extract data \
from one channel of the trial (ch 1 in this case), type: \
'sqk --classify --channel=1'."
    # Parse command line options.
    parser = optparse.OptionParser(usage, version=version, description=desc)
    parser.add_option("-C", "--classify",
                    dest="classify",
                    action="store_true",
                    default=False,
                    help="Classify the trial. IMPORTANT: Trial folder must " \
                         "be the current directory.")
    parser.add_option("-m", "--channel", metavar="<CH>",
                    dest="channel",
                    action="store",
                    type="int",
                    default=0,
                    help="Specify which channel to extract data from. " \
                         "Default (%default) extracts data from both " \
                         "channels. Must choose 0 (both channels), 1, or 2.")
    parser.add_option("-l", "--log",
                    dest="log", action="store_true", default=False,
                    help="Parses a log file if it exists and adds time and" \
                         " duration information to the data file.")
    parser.add_option("-T", "--traindata", metavar="<DATA_FILE>",
                    dest="trainData",
                    action="store",
                    default=os.path.join(TRAIN_PATH, 'traindata'),
                    help="Specify training data set. Default is %default")
    parser.add_option("-L", "--learner", metavar="<TYPE>",
                    dest="learner",
                    action="store",
                    default="svm",
                    help="Specify the classifier algorithm. Options include:" \
                         " 'bayes' (Naive Bayes), 'knn' (k-Nearest Neighbor)," \
                         " 'svm' (SVM), 'forest' (random forest). " \
                         "Default is %default.")
    parser.add_option("-f", "--file", metavar="<AUDIO_FILE>",
                    dest="audio",
                    action="store",
                    help="Extract features and classify audio file (wav)")
    parser.add_option("-p", "--path", metavar="<PATH>",
                    dest="path",
                    action="store",
                    help="Extract features and classify all files in a " \
                         "directory. To extract from current directory: " \
                         "'usv.py -p .' ")
    parser.add_option("-r", "--rate", metavar="<SAMPLE_RATE>",
                    dest="sampleRate",
                    action="store",
                    default="11025",
                    help="Specify the sample rate of input files. Default is " \
                         "%default (Hz).")
    parser.add_option("-t", "--train", metavar="<CLASS>",
                    dest="exampleClass",
                    action="store",
                    type='string',
                    help="Label the training example(s).")
    parser.add_option("-d", "--data", metavar="<DATA_FILE>",
                    dest="data",
                    action="store",
                    default="data.tab",
                    help="Write to data file (.tab format). Default is " \
                         "'%default' or 'traindata.tab' for training data.")
    parser.add_option("-S", "--seg-resamp",
                    dest="segment",
                    action="store_true",
                    default=False,
                    help="Resample to 11025 Hz and split into multiple files " \
                         "based on silence. IMPORTANT: Trial folder must " \
                         "be the current directory.")
    (opts, args) = parser.parse_args()
    if opts.channel and not (opts.classify or opts.segment):
        parser.error("'--channel' option requires '--classify' option'")
    if opts.log and not opts.classify:
        parser.error("'--log' option requires '--classify' option'")
        
    # Open data file or create it if it doesn't exist.
    if opts.exampleClass and opts.data == "data.tab":
        opts.data = os.path.join(TRAIN_PATH, 'traindata.tab')

    if opts.audio or opts.path:
        if not opts.segment:
            print 'Opening %r. . .' % (opts.data)
            data = open(opts.data, "a+")
    elif opts.segment:
        print "Resampling and segmenting trial. . ."
    elif opts.classify:
        print "Classifying trial. . ."
    else:
        parser.error('No input file or path specified.')

    # If user specifies an audio file (-f AUDIO_FILE)
    if opts.audio:
        file_name, ext = os.path.splitext(opts.audio)
        # Add MFCC 1-12 to data.
        if not opts.segment:
            write_features(opts.audio, opts.sampleRate, data)
        # If classification is specified, write to data.
        if opts.exampleClass:
            data.write(opts.exampleClass.lower() + "\n")
            print "Classified %r as %r." % (opts.audio, opts.exampleClass.lower())
        # Else if user chooses to segment file (-S)
        elif opts.segment:
            print "Resampling and segmenting %s. . ." % (opts.audio)
            if opts.channel == 0:
                runCommands(seg_resamp(opts.audio, int(opts.sampleRate),
                            outfile=file_name + '_call.wav', directory=file_name + "_ch1_2",
                            ch1=True, ch2=True))
            elif opts.channel == 1:
                runCommands(seg_resamp(opts.audio, int(opts.sampleRate),
                            outfile=file_name + '_ch1_.wav', directory=file_name + "_ch1",
                            ch1=True, ch2=False))
            elif opts.channel == 2:
                runCommands(seg_resamp(opts.audio, int(opts.sampleRate),
                            outfile=file_name + '_ch2_.wav', directory=file_name + "_ch2",
                            ch1=False, ch2=True))
            print "Wrote to './%s'." % (file_name + "_calls")
        else:
            print "Invalid data for %r. Skipping. . ." % opts.audio
            data.write('\n')
    # Else if user specifies path (-p PATH)
    elif opts.path:
        # Read all wav files in specified path
        try:
            for root, dirs, files in os.walk(opts.path):
                for basename in files:
                    if fnmatch.fnmatch(basename, "*.[wW][aA][vV]"):
                        audiofile = os.path.join(root, basename)
                        # Skip small files
                        if os.path.getsize(audiofile) < 100:
                            continue
                        file_name, ext = os.path.splitext(audiofile)
                        # Add MFCC 1-12 to data.
                        if not opts.segment:
                            write_features(audiofile, opts.sampleRate, data)
                        # Write filename
                        data.write(str(os.path.basename(audiofile)) + "\t")
                        # If classification is specified, write to file.
                        if opts.exampleClass:
                            data.write(opts.exampleClass.lower() + "\n")
                            print "Classified %r as %r." % (audiofile,
                                                            opts.exampleClass.lower())
                        # If user specifies resample and segment
                        elif opts.segment:
                            print "Resampling and segmenting %r. . ." % (audiofile)
                            if opts.channel == 0:
                                runCommands(seg_resamp(audiofile,
                                        int(opts.sampleRate),
                                        outfile=os.path.basename(file_name) + '_call.wav',
                                        directory=os.path.basename(file_name) + "_ch1_2",
                                        ch1=True, ch2=True))
                            elif opts.channel == 1:
                                runCommands(seg_resamp(audiofile,
                                        int(opts.sampleRate),
                                        outfile=os.path.basename(file_name) + '_ch1_.wav',
                                        directory=os.path.basename(file_name) + "_ch1",
                                        ch1=True, ch2=False))
                            elif opts.channel == 2:
                                runCommands(seg_resamp(audiofile,
                                        int(opts.sampleRate),
                                        outfile=os.path.basename(file_name) + '_ch2_.wav',
                                        directory=os.path.basename(file_name) + "_ch2",
                                        ch1=False, ch2=True))
                        else:
                            data.write('\n')
        except (FloatingPointError, IOError):
            print "An error occurred. Skipping %. . .r" % audiofile
    # Else if user chooses to segment and resample the trial (current dir)
    elif opts.segment:
        for audiofile in glob(os.path.join('./', "*.[wW][aA][vV]")):
            file_name, ext = os.path.splitext(audiofile)
            print "Resampling and segmenting %r. . ." % (file_name)
            if opts.channel == 0:
                runCommands(seg_resamp(audiofile, int(opts.sampleRate),
                            outfile=file_name + '_call.wav', directory=file_name + "_ch1_2",
                            ch1=True, ch2=True))
            elif opts.channel == 1:
                runCommands(seg_resamp(audiofile, int(opts.sampleRate),
                            outfile=file_name + '_ch1_.wav', directory=file_name + "_ch1",
                            ch1=True, ch2=False))
            elif opts.channel == 2:
                runCommands(seg_resamp(audiofile, int(opts.sampleRate),
                            outfile=file_name + '_ch2_.wav', directory=file_name + "_ch2",
                            ch1=False, ch2=True))
    # Else if user chooses to classify the trial
    elif opts.classify:
        # TODO: Should not be able to classify if no data files in folder
        try:
            traindata = orange.ExampleTable(opts.trainData)
        except SystemError:
            print "Training data not found."
            sys.exit(1)
        # The logger
        if opts.log:
            logs = glob(os.path.join(os.getcwd(), "*.[lL][oO][gG]"))
            if len(logs) > 1:
                print "ERROR: Multiple log files."
                sys.exit(1)
            log = usv.avisoftlog.RecLog(open(logs[0], 'r'))

        # The classifier
        print "Constructing %s classifier \
(may take several minutes). . ." % (opts.learner)
        if opts.learner.lower() == "bayes":
            classifier = orange.BayesLearner(traindata)
            classifier.name = "naive_bayes"
        elif opts.learner.lower() == "knn":
            classifier = Orange.classification.knn.kNNLearner(traindata)
            classifier.name = "kNN"
        elif opts.learner.lower() == "svm":
            svm = SVMLearner(name="SVM", kernel_type=kernels.RBF,
                            C=128, gamma=2, nu=0.1)
            classifier = svm(traindata)
            classifier.name = "SVM"
        elif opts.learner.lower() == "tree":
            classifier = orngTree.TreeLearner(traindata)
            classifier.name = "tree"
        elif opts.learner.lower() == "forest":
            classifier = Orange.ensemble.forest.RandomForestLearner(traindata)
            classifier.name = "random_forest"

        # Create data summary file
        if opts.channel == 0:
            datasummary_name = os.path.splitext(opts.data)[0] + "_ch1_2.tab"
        elif opts.channel == 1:
            datasummary_name = os.path.splitext(opts.data)[0] + "_ch1.tab"
        elif opts.channel == 2:
            datasummary_name = os.path.splitext(opts.data)[0] + "_ch2.tab"
        if os.path.exists(datasummary_name):
            print "Data file %r already exists." % (datasummary_name)
            print "Exiting . . ."
            sys.exit(1)
        else:
            summary = open(datasummary_name, "a+")
        # Write metadata
        summary.write("# data = %s\n" % (datasummary_name))
        summary.write("# channel = %d\n" % (opts.channel))
        summary.write("# sample_rate = %s\n" % (opts.sampleRate))
        summary.write("# classifier = %s\n" % (classifier.name))
        # Write header
        summary.write("FILE\t")
        for i in range(len(traindata.domain.classVar.values)):
            summary.write(traindata.domain.classVar.values[i].upper() + "\t")
        if opts.log:
            summary.write("start: " + str(log.start.time) + "\t")
            summary.write("Duration" + "\t")
        summary.write("\n")

        totals = [0] * len(traindata.domain.classVar.values)
        proportions = [0.0] * len(totals)
        for root, dirs, files in os.walk(os.getcwd()):
            # For each file's directory in this trial
            for dir in dirs:
                data = open(os.path.join(dir, dir + '.tab'), 'w+')
                if opts.channel == 0:
                    calls = glob(os.path.join(dir, "*ch1_2*.[wW][aA][vV]"))
                elif opts.channel == 1:
                    calls = glob(os.path.join(dir, "*ch1*.[wW][aA][vV]"))
                elif opts.channel == 2:
                    calls = glob(os.path.join(dir, "*ch2*.[wW][aA][vV]"))
                # For each call
                for c in calls:
                    # Skip small files
                    if os.path.getsize(c) < 100:
                        print "Skipping %s (not enough data)" % c
                        continue
                    # Write feature data
                    write_features(c, opts.sampleRate, data)
                    data.close() # Ensures that data is saved
                    # Write filenames and classifications
                    data = open(os.path.join(dir, dir + '.tab'), 'a+')
                    datatable = orange.ExampleTable(os.path.join(dir, dir + '.tab'))
                    classification = classifier(datatable[calls.index(c)])
                    data.write(str(os.path.basename(c)) + '\t')
                    data.write(str(classification))
                    data.write('\n')
            data.close()

            # Write class count data to summary table
            for dir in dirs:
                if opts.channel == 0:
                    data_files = glob(os.path.join(dir, "*ch1_2.tab"))
                elif opts.channel == 1:
                    data_files = glob(os.path.join(dir, "*ch1.tab"))
                elif opts.channel == 2:
                    data_files = glob(os.path.join(dir, "*ch2.tab"))
                for c in data_files:
                    if os.path.getsize(c) == 0:
                        continue
                    file_name, ext = os.path.splitext(os.path.basename(c))
                    summary.write(file_name + '\t')
                    callsdata = orange.ExampleTable(os.path.join("./", c))
                    # Vector of class counts
                    counts = [0] * len(callsdata.domain.classVar.values)
                    for e in callsdata:
                        counts[int(e.getclass())] += 1
                    # Write counts
                    for i in range(len(callsdata.domain.classVar.values)):
                        summary.write(str(counts[i]) + "\t")
                        totals[i] += counts[i]
                    # Write log data
                    if opts.log:
                        tmp = str(os.path.basename(dir)).lower()
                        entry = tmp[0:tmp.find("_")] + ".wav"
                        summary.write(str(log.getevent(entry).time) + "\t")
                        summary.write(log.getevent(entry).duration + "\t")
                        log.close()
                    summary.write('\n')
        # Write totals. Exclude BGNOISE.
        summary.write("TOTAL" + "\t\t")
        for i in range(1, len(totals)):
            summary.write(str(totals[i]) + "\t")
        if opts.log:
            summary.write("end: " + str(log.end.time) + "\t")
        summary.write("\n")
        # Write proportions. Exclude BGNOISE.
        summary.write("P" + "\t\t")
        for i in range(1, len(proportions)):
            try:
                proportions[i] = float(totals[i]) / float(sum(totals) - totals[0])
            except ZeroDivisionError:
                proportions[i] = 0.0
            summary.write("%.4f\t" % (proportions[i]))
        summary.write("\n")
        summary.close()
        # Open data file when finished
        subprocess.call('open %s' % (datasummary_name), shell=True)

    else:
        data.write("\n")

    if not opts.segment:
        data.close()
    print "Success!"


def write_features(audiofile, sample_rate, data):
    """Extract features then write means and std devs to data (tab) file.
    Returns True if extraction was successful, False if unsuccessful.
    
    Arguments:
    audioFile -- WAV file to process
    sampleRate -- sample rate of the audio file in Hz
    data -- the data file to write to
    
    """
    N_MFCC = 12 # Number of MFCC coefficients
    N_LLD = 2 # Number of other low-level descriptors
    N_FUNCS = 4 # Number of functionals

    # Add features to extract
    featplan = yf.FeaturePlan(sample_rate=sample_rate, resample=False)
    featplan.addFeature('mfcc: MFCC CepsIgnoreFirstCoeff=0 CepsNbCoeffs=12 \
FFTWindow=Hanning MelMinFreq=1200 MelMaxFreq=5050')
    featplan.addFeature('energy: Energy')
    featplan.addFeature('zcr: ZCR')
    
    # Configure an Engine
    engine = yf.Engine()
    engine.load(featplan.getDataFlow())
    
    # Extract features
    afp = yf.AudioFileProcessor()
    afp.processFile(engine, audiofile)
    # 2D numpy arrays
    mfccs = engine.readOutput('mfcc')
    energy = engine.readOutput('energy')
    zcr = engine.readOutput('zcr')

    # Write header lines if they don't exist
    data.seek(0, 0)
    if not data.readline():
        # Write attribute header line
        for i in range(N_MFCC):
            # MFCC header
            data.write("mfcc" + str(i + 1) + "_mean" + "\t")
            data.write("mfcc" + str(i + 1) + "_std" + "\t")
            data.write("mfcc" + str(i + 1) + "_skew" + "\t")
            data.write("mfcc" + str(i + 1) + "_kurtosis" + "\t")
        
        #Energy header
        data.write("energy_mean" + "\t")
        data.write("energy_std" + "\t")
        data.write("energy_skew" + "\t")
        data.write("energy_kurtosis" + "\t")
        
        # ZCR header
        data.write("zcr_mean" + "\t")
        data.write("zcr_std" + "\t")
        data.write("zcr_skew" + "\t")
        data.write("zcr_kurtosis" + "\t")
        
        # Filename and classification headers
        data.write("filename" + '\t')
        data.write("classification" + "\n")
        
        # Write attribute type line
        for i in range(N_MFCC * N_FUNCS + (N_LLD * N_FUNCS)):
            data.write("continuous" + "\t")
        # filename is a string
        data.write("string" + '\t')
        # Classification is discrete
        data.write("discrete" + "\n")
        
        # Write flags
        for i in range(N_MFCC * N_FUNCS + (N_LLD * N_FUNCS)):
            data.write('\t')
        data.write("meta" + '\t')
        data.write("class" + '\n')
    data.seek(0, 2) # Go to end of file.
    
    # Write feature data    
    if mfccs.size > 0 and energy.size > 0 and zcr.size > 0:
        # Write MFCCs
        for i in range(mfccs[0].size):
            mfcc_mean = mfccs[:, i].mean()
            mfcc_std = mfccs[:, i].std()
            mfcc_skew = spstats.skew(mfccs[:, i])
            mfcc_kurt = spstats.kurtosis(mfccs[:, i])
            data.write(str(mfcc_mean) + '\t' + str(mfcc_std) + '\t' +
                        str(mfcc_skew) + '\t' + str(mfcc_kurt) + '\t')
        # Write energy
        for i in range(energy[0].size):
            energy_mean = energy[:, i].mean()
            energy_std = energy[:, i].std()
            energy_skew = spstats.skew(energy[:, i])
            energy_kurt = spstats.kurtosis(energy[:, i])
            data.write(str(energy_mean) + '\t' + str(energy_std) + '\t' +
                        str(energy_skew) + '\t' + str(energy_kurt) + '\t')
        # Write ZCR
        for i in range(zcr[0].size):
            zcr_mean = zcr[:, i].mean()
            zcr_std = zcr[:, i].std()
            zcr_skew = spstats.skew(zcr[:, i])
            zcr_kurt = spstats.kurtosis(energy[:, i])
            data.write(str(zcr_mean) + '\t' + str(zcr_std) + '\t' +
                        str(zcr_skew) + '\t' + str(zcr_kurt) + '\t')
        return True
    else:
        return False


def seg_resamp(audiofile, resamp_rate, outfile, directory, ch1=True, ch2=True):
    """Return a list of sox commands to resample and split an audio file
    based on silences. Segment files are put into directory that has the 
    same name as the audio file.
    
    Arguments:
    audioFile -- the audio file
    resampleRate -- the resample rate
    outFile -- name of output file
    ch1 -- True if output file includes channel 1 in mixdown.
    ch2 -- True if output file includes channel 2 in mixdown.
    directory -- directory to put split files into
    
    """
    try:
        os.mkdir(directory)
    except OSError:
        print "%s folder already exists." % directory
        print "No files written."
        sys.exit(0)
    # Change the sampling rate and mixes file down to one channel
    if ch1 and ch2:
        resample = "sox -r %s %s -b 16 temp.wav channels 1" % (resamp_rate,
                                                                audiofile)
    elif ch1 and not ch2:
        resample = "sox -r %s %s -b 16 temp.wav remix 1 0 channels 1" % (resamp_rate,
                                                                        audiofile)
    elif ch2 and not ch1:
        resample = "sox -r %s %s -b 16 temp.wav remix 2 0 channels 1" % (resamp_rate,
                                                                        audiofile)
    # Split audio when it detects >= 1 sec of silence (< 0.5% volume)
    # 0.8/0.65 > 0.8/0.6 > 0.9/0.6 = 0.7/0.6 > 1.0/0.7 >(slight) 05/05 > 0.3/0.3 1.0/0.8 >> 1.0/0.5
    segment = 'sox temp.wav %s silence -l 1 \
    0.05 0.5%% 1 0.8 0.65%% : newfile : restart' % (os.path.join(directory, outfile))
    clean = 'rm temp.wav'
    return [resample, segment, clean]


def runCommands(commands):
    """Run all commands in a list of commands."""
    for cmd in commands:
        subprocess.call(cmd, shell=True)

if __name__ == '__main__':
    start = datetime.datetime.now()
    main()
    end = datetime.datetime.now()
    print "Completed in %s." % (end - start)
