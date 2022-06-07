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

import time

import adsb_rtlsdr
import matplotlib.pyplot
import numpy
import pyModeS

# Mode-S ADS-B technology has two types of squitter, a short, 56 bit,
# acquisition squitter which can contain Downlink Formats (DF) 0, 4, 5 and 11
# (DF0/4/5/11) and the 112 bit extended squitter (ES) which can contain DF17.
# https://cdn.knmi.nl/knmi/pdf/bibliotheek/knmipubTR/TR336.pdf
DATA_LENGTH = 224

# The divisional value of a single microsecond .000001, also represented by the
# symbol μs.
MICROSECOND = 1e6

# The preamble is 8 μs and each bit is represented by a 0.5 μs pulse equaling
# 16 total bits. The preamble indicates the start of an ADS-B data message.
PREAMBLE = [1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0]

PREAMBLE_LENGTH = len(PREAMBLE)

# signal amplitude threshold difference between 0 and 1 bit
AMPLITUDE_THRESHOLD = 0.8

MESSAGE_LENGTH = PREAMBLE_LENGTH + DATA_LENGTH + 1


class AdsbParser:
    """Class for streaming samples of ADS-B"""

    @staticmethod
    def calculate_noise_floor(samples):
        """Configure
        sample_rate is samples per second
        Returns minimum calculated noise or default to 1 microsecond

        """

        # Calculate noise floor
        window = int(adsb_rtlsdr.SAMPLE_RATE / MICROSECOND) * 100
        length = len(samples)

        # // = the integer division operator
        # no idea what this is doing
        means = (
            numpy.array(samples[: length // window * window])
            .reshape(-1, window)
            .mean(axis=1)
        )

        calculated = min(means)
        return min(calculated, MICROSECOND)

    @staticmethod
    def is_adsb_squitter(samples):
        """
        Returns if the given message is of type ADS-B.

        Mode-S ADS-B technology has two types of squitter, a short, 56 bit,
        acquisition squitter which can contain Downlink Formats (DF) 0, 4, 5
        and 11 (DF0/4/5/11) and the 112 bit extended squitter (ES) which can
        contain DF17.

        https://cdn.knmi.nl/knmi/pdf/bibliotheek/knmipubTR/TR336.pdf
        """

        downlink_format = pyModeS.df(samples)
        length = len(samples)

        if downlink_format == 17 and length == 28:
            if pyModeS.crc(samples) == 0:
                return True
        elif downlink_format in [20, 21] and length == 28:
            return True
        elif downlink_format in [4, 5, 11] and length == 14:
            return True

        return False

    @staticmethod
    def is_preamble(samples):
        """
        Determines if the given samples match the ADS-B preamble. The samples
        size must be 16 bits in length.
        """

        if(len(samples) != PREAMBLE_LENGTH):
            return False

        for i in range(PREAMBLE_LENGTH):
            if abs(samples[i] - PREAMBLE[i]) > AMPLITUDE_THRESHOLD:
                return False

        return True

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
            Fs=adsb_rtlsdr.SAMPLE_RATE/MICROSECOND,
            Fc=adsb_rtlsdr.CENTER_FREQUENCY/MICROSECOND
        )
        matplotlib.pyplot.xlabel('Frequency (MHz)')
        matplotlib.pyplot.ylabel('Relative power (dB)')
        matplotlib.pyplot.show()

    @staticmethod
    def signal_to_binary(samples):

        # TODO not sure why they set a noise floor and then still had to set this
        # threshold value to avoid noise from becoming bits.
        threshold = max(samples) * 0.25

        # The information contained in the data block is modulated using
        #  the Pulse Position Modulation (PPM), which is a type of
        # amplitude modulation. In PPM, the 1 bit is represented by a 0.5 μs
        # of pulse followed by a 0.5 μs flat signal. The 0 bit is reversed
        # compared to the 1 bit, which is represented by a 0.5 μs flat
        # signal and followed by a 0.5 μs pulse.

        message = []
        for i in range(0, len(samples), 2):
            pulse = samples[i: i + 2]

            if pulse[0] < threshold and pulse[1] < threshold:
                break

            if pulse[0] >= pulse[1]:
                message.append("1")
            else:
                message.append("0")

        return message

    def parse_samples(self, samples):

        signal_buffer = []
        messages = []

        # removing "negative frequencies" (based on numpy, I think this makes it scalar
        # - remember 'j' is imaginary number)
        # original complex128 type = (-0.0039215686274509665-0.0039215686274509665j)
        # resulting signal_buffer = 0.005545935538718
        #
        # https://pysdr.org/content/frequency_domain.html
        # https://numpy.org/doc/stable/reference/generated/numpy.absolute.html
        amp = numpy.absolute(samples)
        signal_buffer.extend(amp.tolist())

        # To see what the resulting plot looks like, uncomment these lines
        # -----------------------------------------------------------------------------
        self.plot_psd(signal_buffer)
        # -----------------------------------------------------------------------------

        noise_floor = self.calculate_noise_floor(signal_buffer)

        # set minimum signal amplitude
        # 10 dB SNR
        # SNR = Signal to Noise Ratio = 3.162
        #
        # I don't understand why they are using a constant instead of calculating the value
        #
        # https://www.electronics-tutorials.ws/filter/decibels.html
        # https://dsp.stackexchange.com/questions/70779/how-is-signal-to-noise-ratio-actually-measured-by-receiver-equipment
        # https://documentation.meraki.com/MR/WiFi_Basics_and_Best_Practices/Signal-to-Noise_Ratio_(SNR)_and_Wireless_Signal_Strength
        min_sig_amp = 3.162 * noise_floor

        buffer_length = len(signal_buffer)

        i = 0
        while i <= (buffer_length - MESSAGE_LENGTH):

            # Anything that is below the minimum signal amplitude can be skipped
            if signal_buffer[i] >= min_sig_amp:

                pulses = signal_buffer[i: i + PREAMBLE_LENGTH]

                if self.is_preamble(pulses):
                    data_start = i + PREAMBLE_LENGTH
                    data_end = i + MESSAGE_LENGTH
                    data = signal_buffer[data_start:data_end]

                    self.plot(data)

                    message_binary = self.signal_to_binary(data)
                    message = pyModeS.bin2hex(
                        "".join([str(i) for i in message_binary]))

                    if self.is_adsb_squitter(message):
                        messages.append([message, time.time()])

                    # advance i past the data it just read
                    i += len(data)

            i += 1

        print(messages)
        pyModeS.tell(messages[0][0])

        return messages
