#!/usr/bin/env python

import asyncio
import confluent_kafka as kafka
import rtlsdr
import traceback

config = {
    "bootstrap.servers":"localhost:9092"
}

class AdsbStreamer:

    def __init__(self):
        self.sdr = rtlsdr.RtlSdr()
        self.sdr.sample_rate = 2e6
        self.sdr.center_freq = 1090e6
        self.sdr.gain = "auto"

        self.producer = kafka.Producer(config)

    async def run(self):
        async for samples in self.sdr.stream():
            self.producer.produce("quickstart", str(len(samples)))

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
