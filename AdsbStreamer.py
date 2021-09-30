#!/usr/bin/env python
"""
This Python script uses RTL-SDR to retrieve radio samples for the ADS-B frequency of 1090 and
publishes those samples to a Kafka topic.
"""

# Python Standatd Libraries
import asyncio
import traceback

import confluent_kafka as kafka
import rtlsdr

config = {
    "bootstrap.servers":"localhost:9092"
}

KAFKA_TOPIC = "quickstart"

class AdsbStreamer:
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


if __name__ == "__main__":
    try:
        adsb = AdsbStreamer()
        loop = asyncio.get_event_loop()
        loop.run_until_complete(adsb.run())
    except rtlsdr.rtlsdr.LibUSBError:
        print("RTL-SDR Not plugged in.")
        traceback.print_exc()
