#!/usr/bin/env python
"""
ADS-B is short for Automatic Dependent Surveillance-Broadcast. It is a
satellite-based surveillance system. Parameters such as position, velocity, and
identification are transmitted through Mode S Extended Squitter (1090 MHz).
Nowadays, the majority of aircraft broadcast ADS-B messages constantly.
Starting from the year 2020, civil aviation aircraft in Europe and United
States are required to be ADS-B compliant. Old aircraft which are not compliant
with ADS-B requirements are required to be retrofitted or phased out within a
number of years.

https://mode-s.org/decode/content/ads-b/1-basics.html
"""

import matplotlib.pyplot
import numpy
import rtlsdr

# The Secondar Surveillance Radar (SSR) transmits interrogations using the
# 1030 MHz radio frequency and the aircraft transponder transmits replies using
# the 1090 MHz radio frequency.
CENTER_FREQUENCY = 1090e6

# Mode-S ADS-B technology has two types of squitter, a short, 56 bit,
# acquisition squitter which can contain Downlink Formats (DF) 0, 4, 5 and 11
# (DF0/4/5/11) and the 112 bit extended squitter (ES) which can contain DF17.
# https://cdn.knmi.nl/knmi/pdf/bibliotheek/knmipubTR/TR336.pdf
DATA_LENGTH = 112

# The divisional value of a single microsecond .000001, also represented by the
# symbol μs.
MICROSECOND = 1e6

# The preamble is 8 μs and each bit is represented by a 0.5 μs pulse equaling
# 16 total bits. The preamble indicates the start of an ADS-B data message.
PREAMBLE = [1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0]

SAMPLE_RATE = 2e6

# signal amplitude threshold difference between 0 and 1 bit
AMPLITUDE_THRESHOLD = 0.8


MESSAGE_LENGTH = len(PREAMBLE) + ((DATA_LENGTH + 1) * 2)


class AdsbRtlSdr:
    """Class for streaming samples of ADS-B"""

    @staticmethod
    def calculate_noise_floor(samples):
        """Configure
        sample_rate is samples per second
        """

        # Calculate noise floor
        window = int(SAMPLE_RATE / MICROSECOND) * 100
        length = len(samples)

        # // = the integer division operator
        # no idea what this is doing
        means = (
            numpy.array(samples[: length // window * window])
            .reshape(-1, window)
            .mean(axis=1)
        )

        return min(means)

    @staticmethod
    def plot(samples):
        """Plot an array of samples"""
        matplotlib.pyplot.plot(samples)
        matplotlib.pyplot.ylabel('some numbers')
        matplotlib.pyplot.show()

    @staticmethod
    def plot_psd(samples):
        """Use matplotlib to estimate and plot the PSD"""

        matplotlib.pyplot.psd(
            samples,
            NFFT=1024,
            Fs=SAMPLE_RATE/MICROSECOND,
            Fc=CENTER_FREQUENCY/MICROSECOND
        )
        matplotlib.pyplot.xlabel('Frequency (MHz)')
        matplotlib.pyplot.ylabel('Relative power (dB)')
        matplotlib.pyplot.show()

    def __init__(self):
        self.sdr = rtlsdr.RtlSdr()
        self.sdr.sample_rate = SAMPLE_RATE
        self.sdr.center_freq = CENTER_FREQUENCY
        self.sdr.gain = "auto"

    def close(self):
        return self.sdr.close()

    async def get_messages(self):
        """
            Parses the current RTL-SDR stream and returns the ADS-B messages
        """

        async for samples in self.sdr.stream():
            # parse the samples
            print(str(len(samples)))

        await self.sdr.stop()
        return []
