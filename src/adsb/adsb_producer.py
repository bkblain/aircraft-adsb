#!/usr/bin/env python
"""
This Python script uses RTL-SDR to retrieve radio samples for the ADS-B frequency of 1090 and
publishes those samples to a Kafka topic.
"""

import adsb_rtlsdr
import kafka

class AdsbProducer:
    """Class for streaming samples of ADS-B (frequency 1090)"""

    def __init__(self):
        self.sdr = adsb_rtlsdr.AdsbRtlSdr()

        self.topic = ""
        self.producer = None

    def configure(self, bootstrap_servers, topic):
        """Configure the Kafka producer and topic"""
        self.topic = topic
        self.producer = kafka.KafkaProducer(bootstrap_servers=bootstrap_servers)

    async def run(self):
        """Method for publishing samples into kafka topic using Python event loops."""

        async for samples in self.sdr.stream():
            # perform parsing on the samples
            # send a json string of the ADS-B data into kafka
            self.producer.send(self.topic, str(len(samples)))

        await self.sdr.stop()
        self.sdr.close()
