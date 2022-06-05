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

    def configure(self, bootstrap_servers):
        """Configure the Kafka producer and topic"""
        self.producer = kafka.KafkaProducer(
            bootstrap_servers=bootstrap_servers)

    def run(self):
        """Method for publishing samples into kafka topic using Python event loops."""

        for messages in self.sdr.get_messages():
            # Instead of stream, change the method to retrieve adsb messages
            # this will encapsulate the rtlsdr
            self.producer.send(self.topic, str(len(messages)))

        self.sdr.close()

    def set_topic(self, topic):
        self.topic = topic
