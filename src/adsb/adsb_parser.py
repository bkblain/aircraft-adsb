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
DATA_LENGTH = 112

# The divisional value of a single microsecond .000001, also represented by the
# symbol μs.
MICROSECOND = 1e6

# The preamble is 8 μs and each bit is represented by a 0.5 μs pulse equaling
# 16 total bits. The preamble indicates the start of an ADS-B data message.
PREAMBLE = [1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0]

# signal amplitude threshold difference between 0 and 1 bit
AMPLITUDE_THRESHOLD = 0.8


MESSAGE_LENGTH = len(PREAMBLE) + ((DATA_LENGTH + 1) * 2)


# All Mode S replies start with an 8 μs fixed preamble and continue with 56- or 112 μs data block.

pbits = 8
fbits = 112
message_length = pbits * 2 + (fbits + 1) * 2
preamble = [1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0]


th_amp_diff = 0.8  # signal amplitude threshold difference between 0 and 1 bit


class AdsbParser:
    """Class for streaming samples of ADS-B"""

    @staticmethod
    def calculate_noise_floor(samples):
        """Configure
        sample_rate is samples per second
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
            Fs=adsb_rtlsdr.SAMPLE_RATE/MICROSECOND,
            Fc=adsb_rtlsdr.CENTER_FREQUENCY/MICROSECOND
        )
        matplotlib.pyplot.xlabel('Frequency (MHz)')
        matplotlib.pyplot.ylabel('Relative power (dB)')
        matplotlib.pyplot.show()

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

        print(signal_buffer[0])
        print(len(signal_buffer))

        # To see what the resulting plot looks like, uncomment these lines
        # -----------------------------------------------------------------------------
        self.plot_psd(signal_buffer)
        # -----------------------------------------------------------------------------

        # minimum calculated noise or default to 1 microsecond
        calculated = self.calculate_noise_floor(signal_buffer)
        noise_floor = min(calculated, 1e6)

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

        while i < (buffer_length - message_length):

            # Anything that is below the minimum signal amplitude can be skipped
            if signal_buffer[i] >= min_sig_amp:

                # The pulses are about 0.8 μs wide. P1 and P3 are the two main pulses sent by
                # the directional antenna. They are separated by 8 μs and 21 μs, respectively
                # for Mode A and C. P2 is a pulse emitted through the omnidirectional antenna
                # right after P1. Pulse P2 is introduced for sidelobe suppression
                # [Orlando 1989]. When the power of P2 is higher than P1, the interrogation
                # is likely from the side lobes of the directional antenna and should be
                # ignored by the aircraft. This is can happen when the aircraft is close to
                # the radar.
                # https://mode-s.org/decode/content/introduction.html

                check = True
                pulses = signal_buffer[i: i + pbits * 2]

                # I guess this checks to make sure it's not at the end of the array
                # if len(pulses) != 16:
                #     check = False
                # else:

                for k in range(16):
                    # th_amp_diff = signal amplitude threshold difference between 0 and 1 bit
                    if abs(pulses[k] - preamble[k]) > th_amp_diff:
                        check = False
                        break

                if check:
                    print('current i =' + str(i))

                    frame_start = i + pbits * 2
                    frame_end = i + pbits * 2 + (fbits + 1) * 2
                    frame_length = (fbits + 1) * 2
                    frame_pulses = signal_buffer[frame_start:frame_end]

                    print('frame start = ' + str(frame_start))
                    print('frame end = ' + str(frame_end))
                    print('')

                    self.plot(frame_pulses)

                    threshold = max(frame_pulses) * 0.2

                    msgbin = []
                    for j in range(0, frame_length, 2):
                        p2 = frame_pulses[j: j + 2]
                        if len(p2) < 2:
                            break

                        if p2[0] < threshold and p2[1] < threshold:
                            break
                        elif p2[0] >= p2[1]:
                            c = 1
                        elif p2[0] < p2[1]:
                            c = 0
                        else:
                            msgbin = []
                            break

                        msgbin.append(c)

                    # why is the first data 56 but the second data len 57?
                    # I think there is an off by 1 bug in here (df=4 and df=8).
                    # the df=8 indicates there needs to be another 0 in front of the binary string

                    print('msgbin ' + str(len(msgbin)))
                    print(msgbin)

                    # advance i with a jump
                    i = frame_start + j

                    if len(msgbin) > 0:
                        msg = pyModeS.bin2hex(
                            "".join([str(i) for i in msgbin]))
                        print('msg = ' + msg)

                        # df = downlink format
                        # Mode-S ADS-B technology has two types of squitter, a short, 56 bit, acquisition
                        # squitter which can contain Downlink Formats (DF) 0, 4, 5 and 11 (DF0/4/5/11)
                        # and the 112 bit extended squitter (ES) which can contain DF17.
                        # https://cdn.knmi.nl/knmi/pdf/bibliotheek/knmipubTR/TR336.pdf

                        df = pyModeS.df(msg)
                        print('df = ' + str(df))
                        msglen = len(msg)
                        checkMsg = False

                        if df == 17 and msglen == 28:
                            if pyModeS.crc(msg) == 0:
                                checkMsg = True
                        elif df in [20, 21] and msglen == 28:
                            checkMsg = True
                        elif df in [4, 5, 11] and msglen == 14:
                            checkMsg = True

                        if checkMsg:
                            messages.append([msg, time.time()])

                        # if self.debug:
                        #     self._debug_msg(msghex)

            # elif i > buffer_length - 500:
            #     # save some for next process
            #     break
            # else:
            #     i += 1

            i += 1

        print('i = ' + str(i))

        # reset the buffer
        signal_buffer = signal_buffer[i:]

        print(messages)
        pyModeS.tell(messages[0][0])
