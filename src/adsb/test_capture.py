#!/usr/bin/env python
"""
Run this file when a plane is near to capture a single set of samples.
"""

# Python Standard Libraries
import os

import numpy
import rtlsdr

sdr = rtlsdr.RtlSdr()
sdr.sample_rate = 2e6
sdr.center_freq = 1090e6
sdr.gain = "auto"

samples = sdr.read_samples(100*1024)
sdr.close()

os.makedirs("target", exist_ok=True)
numpy.savetxt("target/capture.txt", samples, delimiter=",")
