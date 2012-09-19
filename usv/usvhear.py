#!/usr/bin/env python
# encoding: utf-8
"""
usvhear.py

Classes for converting Sqk data files (with log metadata) into a series of tones
written to a WAV file.
"""
import wave
import math
from datetime import datetime
import os

def main():
    tg = ToneGenerator('testnew.wav')
    tg.writetone((0, 6, 0), 3)
    tg.close()

class DataSheet(object):
    """Represents a Sqk data sheet (with log metadata).
    """
    def __init__(self, filename):
        self.data = open(filename, 'r')
        self.timecol = 5 # date/time column in data file (0-indexed)
        self.durationcol = 6 # duration column in data file  (0-indexed)
        self.times = []
        self.calls = [] # list of 3-tuples (fms, hfms, svs)
        self.durations = []
        self.length = 0.0 # duration of recording
        self.__parse() # parse the data file
        self.data.close()

    def __parse(self):
        """
        Parses the Sqk data file and stores the information that is to be
        converted into tones.
        """
        lines = self.data.readlines()
        for i in range(0, len(lines)):
            line = lines[i]
            if line[0] == '#':
                continue
            tokens = line.split("\t")
            time_str = tokens[self.timecol]
            if time_str.find('start:') != -1:
                time_str = time_str.split()[1] + " " + time_str.split()[2]
                self.calls.append((0, 0, 0))
                self.durations.append(0.0)
            elif time_str.find('end:') != -1:
                time_str = time_str.split()[1] + " " + time_str.split()[2]
                time = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
                self.times.append(time)
                self.calls.append((0, 0, 0))
                self.durations.append(0.0)
                break
            else:
                duration = float(tokens[6])
                fms = int(tokens[2])
                hfms = int(tokens[3])
                svs = int(tokens[4])
                self.calls.append((fms, hfms, svs))
                self.durations.append(duration)
            time = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
            self.times.append(time)
        self.length = (self.times[len(self.times) - 1] -\
                             self.times[0]).seconds
    def __len__(self):
        return self.length


class USVAudible(object):
    """An object that can convert Sqk data files into a sequence of tones.
    """
    def __init__(self):
        self.sheets = [] # list of DataSheets
        self.freqs = [] # list of tone frequencies (tuples) associated with the
                        # data sheets

    def add_data(self, datasheet, freqs):
        """Add a data sheet and associate it with tone frequencies.

        Arguments;
        datasheet -- A DataSheet.
        freqs -- A tuple of call tone frequencies: (fmfreq, hfmfreq, svfreq)
        """
        self.sheets.append(datasheet)
        self.freqs.append(freqs)

    def tonify(self, tone_generator=None, verbose=False):
        """Makes a wav file from the parsed data file.

        Arguments:
        tone_generator -- A custom ToneGenerator. If not specified, a new
            ToneGenerator will be created with the default parameters, with the
             output filename the same as the data filename.
        """
        if tone_generator is None:
            tone_generator = ToneGenerator('tonifyoutput.wav')
        tone_generator.file.setnchannels(len(self.sheets))
        # Find the max length (in seconds) of the data sheets
        max_length = 0.0
        for sheet in self.sheets:
            if len(sheet) > max_length:
                max_length = len(sheet)
        nframes = int(max_length * tone_generator.sample_rate)
        tone_generator.file.setnframes(nframes)

        tone_strs = []
        for d in self.sheets:
            if verbose:
                print "File:", d.data.name
                print "Frequencies:", self.freqs[self.sheets.index(d)]
            values = []
            tone_generator.setfreqs(self.freqs[self.sheets.index(d)])
            for i in range(0, len(d.times)):
                duration = d.durations[i]
                calls = d.calls[i]
                if verbose:
                    print "\ttone: (%d, %d, %d) for %f seconds" % (calls[0], calls[1],
                                                                calls[2], duration)
                tone = tone_generator.get_tone((calls[0], calls[1], calls[2]), duration)
                values.append(str(tone))
                try:
                    delta = float((d.times[i + 1] - d.times[i]).seconds)
                    if float(delta) - duration < 0.0:
                        silence_duration = 0.0
                    else:
                        silence_duration = float(delta) - duration
                except IndexError:
                    break
                if verbose:
                    print "\tsilence for", silence_duration,"seconds"
                silence = tone_generator.get_silence(silence_duration)
                values.append(str(silence))
            if len(d) < max_length:
                end_silence = tone_generator.get_silence(max_length - len(d))
                values.append(str(end_silence))
            value_str = ''.join(values)
            tone_strs.append(value_str)
            
        if verbose:
            print "Writing to file... (may take several minutes)"
        combined = interleave_binarystr(tone_strs)
        tone_generator.file.writeframes(combined)
        if verbose:
            print "Finished writing."
        tone_generator.close()

class ToneGenerator(object):
    """Writes tones to a WAV file or gets the binary string representation
    of a tone.
    """
    def __init__(self, output):
        # Output file name
        self.output = output
        # Wav file
        self.file = wave.open(self.output, 'w')
        # Maximum amplitude (32767 for 16-bit audio)
        self.max_amplitude = 32767
        # Maximum number of calls of a given type
        self.max_calls = 20
        # Sampling rate in Hz
        self.sample_rate = 44100
        # Number of channels
        self.channels = 2
        # Bit depth
        self.bit_depth = 16
        # Frequencies at which to play call types
        self.fm_freq = 440.000
        self.hfm_freq = 659.255 # hfm tones either monotonal or ditonal
        self.sv_freq = 293.665
        # Set wave write parameters
        self.file.setparams((self.channels, self.bit_depth / 8,
                             self.sample_rate, 0, 'NONE', 'uncompressed'))

    def writetone(self, call_vector, duration):
        """Generates a tone given the counts of the call types and
        a given duration, then writes the tone to the WAV file.
        """
        if duration == 0:
            return
        samples = int(self.sample_rate * duration)
        values = []
        fvector = (self.fm_freq, self.hfm_freq, self.sv_freq)
        for i in range(0, samples):
            try:
                if type(fvector[1]) == tuple:
                    tone = self.__get_waveval2(i, call_vector, fvector)
                else:
                    tone = self.__get_waveval(i, call_vector, fvector)
            except ValueError:
                print "ERROR: Sum of calls cannot exceed max calls"
                print "Cleaning up..."
                print "No files written."
                os.remove(self.output)
                exit(1)
            signal = wave.struct.pack('h', tone) # convert to binary
            values.append(signal)
            # Buffer values every 5 seconds (22050 samples)
            if len(values) >= 220500:
                value_string = "".join(values)
                self.file.writeframes(value_string)
                # Clear values array
                del values[0:len(values)]
        value_string = "".join(values)
        self.file.writeframes(value_string)

    def get_tone(self, call_vector, duration):
        """Returns a binary string representing a call tone.
        """
        if duration == 0:
            return
        nsamples = int(self.sample_rate * duration)
        values = []
        fvector = (self.fm_freq, self.hfm_freq, self.sv_freq)
        for i in range(0, nsamples):
            try:
                if type(fvector[1]) == tuple:
                    tone = self.__get_waveval2(i, call_vector, fvector)
                else:
                    tone = self.__get_waveval(i, call_vector, fvector)
            except ValueError:
                print "ERROR: Sum of calls cannot exceed max calls"
                print "Cleaning up..."
                print "No files written."
                os.remove(self.output)
                exit(1)
            signal = wave.struct.pack('h', tone) # convert to binary
            values.append(signal)
        value_string = "".join(values)
        return value_string


    def writesilence(self, duration):
        """Write silence of a given duration to the wav file.
        """
        samples = int(self.sample_rate * duration)
        values = []
        for i in range(0, samples):
            signal = wave.struct.pack('h', 0)
            values.append(signal)
            # Buffer values every 5 seconds (22050 samples)
            if len(values) >= 220500:
                value_string = "".join(values)
                self.file.writeframes(value_string)
                # Clear values array
                del values[0:len(values)]
        value_string = "".join(values)
        self.file.writeframes(value_string)

    def get_silence(self, duration):
        """Returns a binary string representing silence of a given duration.
        """
        nsamples = int(self.sample_rate * duration)
        return "".join([wave.struct.pack('h', 0) for i in range(0, nsamples)])

    def setfreqs(self, freqs):
        """Set the tone frequencies for the call types.

        Arguments:
        freqs -- A tuple of frequencies in the form (fmfreq, hfmfreq, svfreq)
        """
        self.fm_freq, self.hfm_freq, self.sv_freq = freqs[0], freqs[1], freqs[2]

    def __get_waveval2(self, t, nvector=(0, 0, 0), fvector=None):
        """Returns the value of a wave function generated from a vector of
        counts and a vector of frequencies. Use this version if hfms are 
        represented by two tones.
        
        Arguments:
        t -- Sample at which to write to
        nvector -- Tuple of call type counts: (fms, hfms, svs)
        fvector -- Tuple of call type frequencies: (fmfreq, hfmfreq, svfreq)
        """
        if sum(nvector) > self.max_calls:
            raise ValueError("sum(nvector) cannot exceed max_calls")
        if fvector == None:
            fvector = (self.fm_freq, self.hfm_freq, self.sv_freq)
        val = 0.0
        c = self.max_amplitude / self.max_calls
        fm = c * nvector[0] * math.sin((t * fvector[0] * 2 * math.pi) / self.sample_rate)
        hfm1 = c/2 * nvector[1] * math.sin((t * fvector[1][0] * 2 * math.pi) / self.sample_rate)
        hfm2 = c/2 * nvector[1] * math.sin((t * fvector[1][1] * 2 * math.pi) / self.sample_rate)
        sv = c * nvector[2] * math.sin((t * fvector[2] * 2 * math.pi) / self.sample_rate)
        return fm + hfm1 + hfm2 + sv
    
    def __get_waveval(self, t, nvector=(0, 0, 0), fvector=None):
        """Returns the value of a wave function generated from a vector of
        counts and a vector of frequencies. 

        Arguments:
        t -- Sample at which to write to
        nvector -- Tuple of call type counts: (fms, hfms, svs)
        fvector -- Tuple of call type frequencies: (fmfreq, hfmfreq, svfreq)
        """
        if sum(nvector) > self.max_calls:
            raise ValueError("sum(nvector) cannot exceed max_calls")
        if fvector == None:
            fvector = (self.fm_freq, self.hfm_freq, self.sv_freq)
        val = 0.0
        c = self.max_amplitude / self.max_calls
        for i in range(0, 3):
               amp = c * nvector[i]
               x = (t * fvector[i] * 2 * math.pi) / self.sample_rate
               y = amp * math.sin(x)
               val += y
        return val
    

    def close(self):
        """Closes the wave file.
        """
        self.file.close()

pitchhz = {}
keys_s = ('a', 'a#', 'b', 'c', 'c#', 'd', 'd#', 'e', 'f', 'f#', 'g', 'g#')
keys_f = ('a', 'bb', 'b', 'c', 'db', 'd', 'eb', 'e', 'f', 'gb', 'g', 'ab')
for k in range(88):
    freq = 27.5 * 2.**(k/12.)
    oct = (k+9) // 12
    note = '%s%u' % (keys_s[k%12], oct)
    pitchhz[note] = freq
    note = '%s%u' % (keys_f[k%12], oct)
    pitchhz[note] = freq

def note(note_str):
    """Returns the frequency of a piano key.
    """
    return pitchhz[note_str.lower()]
    

def interleave_binarystr(str_list):
    """Interleaves a list of binary strings.
    """
    ret = ""
    for i in range(0, len(min(str_list)), 2):
        for j in range(len(str_list)):
            ret += str_list[j][i:(i + 2)]
    return ret

if __name__ == "__main__":
    main()