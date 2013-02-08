usv
===

A Python library and tools for classifying animal ultrasonic vocalizations using supervised machine learning. Developed for use with recordings from [Avisoft-Recorder](http://www.avisoft.com/recorder.htm) but is compatible with recordings from any software that records to WAV.

Integrates a number of 3rd-party libraries, including Orange for machine learning, Yaafe for feature extraction, and SoX for segmentation.

Requirements
------------
* Python >= 2.7
* [Orange](http://orange.biolab.si/)
* [Yaafe](http://yaafe.sourceforge.net/)
* [SoX](http://sox.sourceforge.net/Main/HomePage) (included in bin/)

Installation
------------
After installing the dependencies, grab and install package:

    git clone https://github.com/sloria/usv.git
    cd usv/
    python setup.py install

Add usv/bin to your path:

    export PATH=$PATH:$PWD/usv/bin

OR add the following to ~/.bash_profile:

    export PATH=$PATH:~/path/to/usv/bin

Adding Training Examples
------------------------
You **must** change the TRAIN_PATH variable in sqk.py to the path where *your* traindata.tab file is located.

    TRAINPATH = '/path/to/training_data_dir'

*Full documentation to come...*

Classification
--------------
First, `cd` to the directory containing the .wav files.
Then, resample and segment all the audio files in the directory using

    sqk.py -S

You can also isolate a specified audio channel. For example,

    sqk.py -Sm 2

isolates channel 2 before reampling and segmenting.

Then, while still in the same directory, classify all the files in the folder using

    sqk.py -C

Again, you can specify an audio channel, e.g.,

    sqk.py -Cm 2

for channel 2.

The output is a .tab file with the classification counts for each file as well as the total classfication counts and proportions. The .tab file can be opened with a plain text editor or a spreadsheet application like Microsoft Excel.

View more options using `sqk --help`.

*Full documentation to come...*
