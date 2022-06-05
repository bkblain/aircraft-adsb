#!/usr/bin/env python
"""
Run this file when a plane is near to capture a single set of samples.
"""

import adsb_rtlsdr
import numpy

samples = numpy.loadtxt("target/capture.txt", delimiter=',', dtype=numpy.complex128)
adsb_rtlsdr.AdsbRtlSdr.plot_psd(samples, adsb_rtlsdr.SAMPLE_RATE, adsb_rtlsdr.CENTER_FREQUENCY)
