#!/usr/bin/env python
"""
This Python script uses RTL-SDR to retrieve radio samples for the ADS-B frequency of 1090 and
publishes those samples to a Kafka topic.
"""

import confluent_kafka as kafka
import rtlsdr

config = {
    "bootstrap.servers":"fractal.local:9092"
}

KAFKA_TOPIC = "quickstart"

class RtlSdrProducer:
    """Class for streaming samples of ADS-B (frequency 1090)"""

    def __init__(self):
        self.sdr = rtlsdr.RtlSdr()
        self.sdr.sample_rate = 2e6
        self.sdr.center_freq = 1090e6
        self.sdr.gain = "auto"

        self.producer = kafka.Producer(config)

    async def run(self):
        """Method for publishing samples into kafka topic using Python event loops."""

        async for samples in self.sdr.stream():
            self.producer.produce(KAFKA_TOPIC, str(len(samples)))

        await self.sdr.stop()
        self.sdr.close()
