## Photon pulse analysis

### Preparation

* Install python (preferred 2.7 version)
* Install special packages: numpy, matplotlib, scipy, pylandau
   * usually works: pip install numpy matplotlib scipy pylandau
* Clone github repository: git clone https://github.com/JLabMit/JLabExperiments
* Download data (http://t3serv001.mit.edu/~paus/tmp/data.tgz) and untar in the JLabExperiments/Pulses directory: tar fzx data.tgz

### Running the code

#### Look at the first plot

Go to the JLabExperiments/Pulses directory and run analysis command

* cd JLabExperiments/Pulses
* ./python/analysis.py ./data/15181.CSV

Make sure to ‘delete the displayed windows’ to continue. Inspect the code and see how this works
* emacs ./python/analyze.py

Analyze a full dataset (like data in ./data-a folder):

* cd JLabExperiments/Pulses
* ./python/analysis.py ./data-a/*

you might *not* want to fit for each dataset or even show the raw data or the cleaned up data, which can be changed easily using the included switches in the code (ex. plotting = False, fitting = False).
