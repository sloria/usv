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

    git clone ___
    python setup.py install

Add usv/bin to your path:

    export PATH=$PATH:$PWD/usv/bin

OR add the following to ~/.bash_profile:

    export PATH=$PATH:~/projects/usv/bin
