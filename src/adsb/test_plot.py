#!/usr/bin/env python
"""
Run this file when a plane is near to capture a single set of samples.
"""

from rtlsdr_util import RtlSdrUtil
import numpy as np

sample_rate = 2e6
center_frequency = 1090e6

samples = np.loadtxt("target/capture.txt", delimiter=',', dtype=np.complex128)
RtlSdrUtil.plot(samples, sample_rate, center_frequency)
