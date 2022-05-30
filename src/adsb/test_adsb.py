#!/usr/bin/env python
"""
Run this file when a plane is near to capture a single set of samples.
"""


from pylab import *
import numpy as np
import os
import pyModeS as pms


# example raw message
# 8D4840D6202CC371C32CE0576098
# pms.tell("8D4840D6202CC371C32CE0576098")


sample_rate = 2e6
samples_per_microsec = 2
center_freq = 1090e6
signal_buffer = []

samples = np.loadtxt("target/capture4.txt", delimiter=',', dtype=np.complex128)

print(samples[0])
print(len(samples))


# removing "negative frequencies" (based on numpy, I think this makes it scalar - remember 'j' is imaginary number)
# original complex128 type = (-0.0039215686274509665-0.0039215686274509665j)
# resulting signal_buffer = 0.005545935538718
#
# https://pysdr.org/content/frequency_domain.html
# https://numpy.org/doc/stable/reference/generated/numpy.absolute.html

amp = np.absolute(samples)
signal_buffer.extend(amp.tolist())

print(signal_buffer[0])
print(len(signal_buffer))

# To see what the resulting plot looks like, uncomment these lines
# -----------------------------------------------------------------------------
psd(signal_buffer, NFFT=1024, Fs=sample_rate/1e6, Fc=center_freq/1e6)
xlabel('Frequency (MHz)')
ylabel('Relative power (dB)')
show()
# -----------------------------------------------------------------------------


# Calculate noise floor
window = samples_per_microsec * 100
total_len = len(signal_buffer)

# // = the integer division operator
# no idea what this is doing
means = (
    np.array(signal_buffer[: total_len // window * window])
    .reshape(-1, window)
    .mean(axis=1)
)

# minimum calculated noise or default to 1 microsecond
noise_floor = min(min(means), 1e6)
