#!/usr/bin/env python
"""
This Python script uses RTL-SDR to retrieve radio samples for the ADS-B frequency of 1090 and
publishes those samples to a Kafka topic.
"""

# Python Standard Libraries
import asyncio
import os
import sys

import adsb_producer

BOOTSTRAP_SERVERS = os.environ.get("ADSB_KAFKA_SERVERS")
KAFKA_TOPIC = os.environ.get("ADSB_KAFKA_TOPIC")


def main() -> int:
    """
        The main method to initiate application execution
    """

    producer = adsb_producer.AdsbProducer()
    producer.configure(BOOTSTRAP_SERVERS)
    producer.set_topic(KAFKA_TOPIC)

    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(producer.run())
    except KeyboardInterrupt:
        print('Aborted manually.', file=sys.stderr)
        return 1

    return 0


if __name__ == '__main__':
    sys.exit(main())
