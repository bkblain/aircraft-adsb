#!/usr/bin/env python
"""
Run this file when a plane is near to capture a single set of samples.
"""

import adsb_parser
import numpy

samples = numpy.loadtxt(
    "target/capture.txt",
    delimiter=',',
    dtype=numpy.complex128
)

adsb_parser.AdsbRtlSdr.plot_psd(samples)
