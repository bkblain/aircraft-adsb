import asyncio
import rtlsdr

async def streaming():
    sdr = rtlsdr.RtlSdr()
    sdr.sample_rate = 1090000
    
    async for samples in sdr.stream():
        print('length ', len(samples))

    await sdr.stop()
    sdr.close()

try:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(streaming())
except rtlsdr.rtlsdr.LibUSBError:
    print("RTL-SDR Not plugged in.")
