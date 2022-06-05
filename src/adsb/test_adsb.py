#!/usr/bin/env python
"""
Run this file on the captured data file
"""

import adsb_parser
import numpy as np


# capture1 = 200001122AB752
samples = np.loadtxt("target/capture1.txt", delimiter=',', dtype=np.complex128)
print(len(samples))

parser = adsb_parser.AdsbParser()
parser.parse_samples(samples)
