#!/usr/bin/env python
"""
This Python script uses RTL-SDR to retrieve radio samples for the ADS-B frequency of 1090 and
publishes those samples to a Kafka topic.
"""

# Python Standard Libraries
import asyncio
import sys
import traceback

import rtlsdr_producer

def main() -> int:

    # Parse any arguments

    # TODO: load configuration and pass to the Kafka producer
    # RTL-SDR config
    # Kafka config
    # Kafka topic

    # TODO ADS-B Parser class

    try:
        producer = rtlsdr_producer.RtlSdrProducer()
        loop = asyncio.get_event_loop()
        loop.run_until_complete(producer.run())
    except KeyboardInterrupt:
        print('Aborted manually.', file=sys.stderr)
        return 1
    except Exception as err:
        traceback.print_exc()
        return 1

    return 0


if __name__ == '__main__':
    sys.exit(main())
