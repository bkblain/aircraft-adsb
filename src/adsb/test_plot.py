#!/usr/bin/env python
"""
Run this file when a plane is near to capture a single set of samples.
"""

from pylab import *
import numpy as np
import os


sample_rate = 2e6
center_freq = 1090e6

samples = np.loadtxt("target/capture.txt", delimiter=',', dtype=np.complex128)


# use matplotlib to estimate and plot the PSD
psd(samples, NFFT=1024, Fs=sample_rate/1e6, Fc=center_freq/1e6)
xlabel('Frequency (MHz)')
ylabel('Relative power (dB)')

show()
