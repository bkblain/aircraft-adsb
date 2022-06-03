#!/usr/bin/env python
"""
Util class
TODO: better documentation
"""

from pylab import *
import numpy as np
import os


microsecond = 1e6

class RtlSdrUtil:
    """Utility Class for RTL-SDR"""

    def calculateNoiseFloor(samples, sample_rate):
        """Configure
        sample_rate is samples per second
        """

        # Calculate noise floor
        window = int(sample_rate / microsecond) * 100
        length = len(samples)

        # // = the integer division operator
        # no idea what this is doing
        means = (
            np.array(samples[: length // window * window])
            .reshape(-1, window)
            .mean(axis=1)
        )

        return min(means)

    def plot(samples, sample_rate, center_frequency):
        """Use matplotlib to estimate and plot the PSD"""
        psd(samples, NFFT=1024, Fs=sample_rate/microsecond, Fc=center_frequency/microsecond)
        xlabel('Frequency (MHz)')
        ylabel('Relative power (dB)')

        show()