from nose.tools import *
from usv.usvhear import *
from datetime import datetime
from usv.avisoftlog import *

def setup():
	print "SETUP!"
	
def teardown():
	print "TEAR DOWN!"
	
def test_datasheet():
    datasheet = DataSheet('./tests/datasheet.tab')
    assert_equal(datasheet.times[0], datetime.strptime('2011-06-12 15:24:00',
                                                        "%Y-%m-%d %H:%M:%S"))
    assert_equal(datasheet.durations[0], 0)
    assert_equal(datasheet.durations[1], 0.6)
    assert_equal(datasheet.calls[10], (6,6,6))
    assert_equal(datasheet.calls[12], (1,1,1))
    assert_equal(datasheet.times[13], datetime.strptime('2011-06-12 15:24:25',
                                                        "%Y-%m-%d %H:%M:%S"))
    assert_equal(len(datasheet.times), 14)

def test_audible():
    data2 = DataSheet('./tests/datasheet2.tab')
    assert_equal(data2.length, 25)
    aud = USVAudible()
    aud.add_data(data2, (440.0, 522.0, 633.0))
    str_list = ['123456', 'abcdef', 'ABCDEF']
    assert_equal(interleave_binarystr(str_list), '12abAB34cdCD56efEF')
      
    
def test_reclog():
    reclogfile = open('./tests/reclog.LOG', 'r')
    log = RecLog(reclogfile)
    sortedlog = log.sorted()
    assert_equal(sortedlog[0][0], 'monitoring started')
    assert_equal(sortedlog[0][1].time, datetime(year=2011, 
                month=6, day=12, hour=15, minute=24, second=38))
    assert_equal(sortedlog[1][0], 't0000000.wav')
    assert_equal(sortedlog[1][1].time, datetime(year=2011, 
                month=6, day=12, hour=15, minute=24, second=47))
    assert_equal(sortedlog[len(sortedlog)-1][1].time, datetime(year=2011, 
                month=6, day=12, hour=15, minute=55, second=59))
    assert_equal(log.path, "E:\Experiment Data\c2988vc3065\ch1")
    
    for event in sortedlog:
        print event[0] + ": " + str(event[1].time)
    log.close()
 
def test_playlog():
    playlogfile = open('./tests/playback.log', 'r')
    log = PlayLog(playlogfile)
    sv = log.gettrial('sv_pilot')
    assert_equal(list(enumerate(sv.events))[0][1].time, datetime(year=2012, 
                month=7, day=24, hour=14, minute=38, second=13))
    fm = log.gettrial('fm_pilot')
    assert_equal(list(enumerate(fm.events))[0][1].time, datetime(year=2012, 
                month=7, day=24, hour=14, minute=00, second=02))
    hfm = log.gettrial('hfm_pilot')
    assert_equal(list(enumerate(hfm.events))[0][1].time, datetime(year=2012, 
                month=7, day=24, hour=14, minute=27, second=01))
    for trial in log.trials:
        print trial
        for event in log.gettrial(trial).events:
          print "%r: %s" % (event.name, event.time)
          log.close()