#!/usr/bin/env python
"""
This Python script uses RTL-SDR to retrieve radio samples for the ADS-B frequency of 1090 and
publishes those samples to a Kafka topic.
"""

from kafka import KafkaProducer
import pyModeS as pms
import rtlsdr

class RtlSdrProducer:
    """Class for streaming samples of ADS-B (frequency 1090)"""

    def __init__(self):
        self.sdr = rtlsdr.RtlSdr()
        self.sdr.sample_rate = 2e6
        self.sdr.center_freq = 1090e6
        self.sdr.gain = "auto"

        self.topic = ""
        self.producer = None

    def configure(self, config, topic):
        """Configure the Kafka producer and topic"""
        self.topic = topic
        self.producer = KafkaProducer(config)

    async def run(self):
        """Method for publishing samples into kafka topic using Python event loops."""

        async for samples in self.sdr.stream():
            self.producer.send(self.topic, str(len(samples)))

        await self.sdr.stop()
        self.sdr.close()
