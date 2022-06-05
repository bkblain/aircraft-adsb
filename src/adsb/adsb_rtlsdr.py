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

import rtlsdr

# The Secondar Surveillance Radar (SSR) transmits interrogations using the
# 1030 MHz radio frequency and the aircraft transponder transmits replies using
# the 1090 MHz radio frequency.
CENTER_FREQUENCY = 1090e6

SAMPLE_RATE = 2e6


class AdsbRtlSdr:
    """Class for streaming samples of ADS-B"""

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
