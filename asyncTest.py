import asyncio
import pyModeS
import rtlsdr
import traceback

async def streaming():
    sdr = rtlsdr.RtlSdr()
    sdr.sample_rate = 256*1024
    sdr.center_freq = 1090e3

    async for samples in sdr.stream():
        print('length ', len(samples))
        # pyModeS.tell

    await sdr.stop()
    sdr.close()

try:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(streaming())
except rtlsdr.rtlsdr.LibUSBError:
    print("RTL-SDR Not plugged in.")
    traceback.print_exc()
