#!/usr/bin/env python
# encoding: utf-8
"""
avisoftlog.py

Represents log files from Avisoft-USGH.
"""
from datetime import datetime
import re

class Log(object):
    """An abstract log class.
    """
    def __init__(self, filename):
        self.file = filename
        self.events = {}

    def __parse(self):
        raise NotImplementedError

    def getevent(self, name):
        """Returns the event given a filename.
        """
        return self.events[name.lower()]

    def sorted(self):
        """Returns a sorted list name-event pairs, sorted by event times.
        """
        sorted_list = [x for x in self.events.iteritems()]
        sorted_list.sort(key=lambda x: x[1])
        return sorted_list

    def close(self):
        self.file.close()

class RecLog(Log):
    """Represents a Avisoft-Recorder USGH recording log.
    """
    def __init__(self, filename):
        super(RecLog, self).__init__(filename)
        self.path = None # path to trial folder
        self.start = None # Event object when monitoring started
        self.end = None # Event object when monitoring ended
        self.__parse() # Parse the data file

    def __parse(self):
        """Parses the log file and stores each event in a dictionary.
        """
        lines = self.file.readlines()
        name_idx = 2
        name_idx_found = False
        pathre = re.compile(r"^[A-Z]:[\\/]\w+")
        for i in range(0, len(lines)):
            line = lines[i]
            if line.strip() != "": # check if line isn't empty
                if pathre.match(line):
                    self.path = line.strip()
                    continue
                tokens = line.split()
                time_str = tokens[0] + " " + tokens[1]
                try:
                    time = datetime.strptime(time_str, "%m/%d/%y %H:%M:%S")
                except ValueError:
                    raise LogParseError('Invalid log format. Date must be first \
                                        token for each log event.')    
                if not name_idx_found:
                    name_idx = tokens.index('Monitoring')
                    name_idx_found = True
                name = ""
                if tokens[name_idx].strip() == 'Monitoring':
                    name = tokens[name_idx].lower() + " " + tokens[name_idx + 1].lower()
                    duration = 0.0
                else:
                    name = tokens[name_idx].lower()
                    duration = tokens[name_idx + 1]
                self.events[name] = Event(time, name, duration)
        self.start = self.events['monitoring started']
        self.end = self.events['monitoring stopped']

    def getevent(self, filename):
        """Returns the event given a filename.
        """
        return self.events[filename.lower()]


class PlayLog(Log):
    """Represents a Avisoft-Recorder USGH playback log.
    """
    def __init__(self, filename):
        super(PlayLog, self).__init__(filename)
        self.trials = {} # key is trial name; value is a Trial object
        self.__parse() # Parse the log file

    def __parse(self):
        """Parses and stores information in the playback log.
        """
        lines = self.file.readlines()
        for i in range(0, len(lines)):
            line = lines[i]
            tokens = line.split()
            if tokens[0] == "#start":
                trial_name = tokens[1]
                trial = Trial(trial_name)
                self.trials[trial_name] = trial
            elif tokens[0] == "#end":
                continue
            else:
                date_str = tokens[0] + " " + tokens[1]
                date = datetime.strptime(date_str, "%m/%d/%y %H:%M:%S")
                sound_file = line[18:-1].strip()
                event = Event(date, sound_file, 0)
                trial.addevent(event)

    def getevent(self, trialname, eventname):
        return self.trials[trialname].getevent(eventname)

    def gettrial(self, name):
        try:
            return self.trials[name]
        except KeyError:
            raise TrialNotFoundError

class Event(object):
    """Represents an event in a log.
    """
    def __init__(self, time, name, duration):
        self.time = time # a datetime object
        self.name = name.lower()
        self.duration = duration

    def __lt__(self, other):
        assert isinstance(other, Event)
        return self.time < other.time


class Trial(object):
    """Represents a trial within a log.
    """
    def __init__(self, name):
        self.name = name
        self.events = [] # List of Event objects associated with this trial

    def __lt__(self, other):
        assert isinstance(other, Trial)
        return self.name < other.name

    def addevent(self, event):
        self.events.append(event)

    def getevent(self, name):
        for event in self.events:
            if event.name == name:
                return event
        return False

class TrialNotFoundError(Exception):
    """Used to indicate that a trial cannot be found.
    """

class LogParseError(Exception):
    """Used to indicate that an error occurred while parsing
    a file."""
    
def main():
    reclogfile = open('../tests/reclog2.LOG', 'r')
    log = RecLog(reclogfile)
    sortedlog = log.sorted()
    for event in sortedlog:
        print event[0] + ": " + str(event[1].time)
    log.close()

if __name__ == '__main__':
    main()
