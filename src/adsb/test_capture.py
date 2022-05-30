#!/usr/bin/env python
"""
Run this file when a plane is near to capture a single set of samples.
"""

from rtlsdr import *
import numpy as np
import os


sdr = RtlSdr()
sdr.sample_rate = 2e6
sdr.center_freq = 1090e6
sdr.gain = "auto"

samples = sdr.read_samples(100*1024)
sdr.close()

os.makedirs("target", exist_ok=True)
np.savetxt("target/capture4.txt", samples, delimiter=",")


