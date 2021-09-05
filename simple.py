from rtlsdr import RtlSdr

sdr = RtlSdr()

# configure device
sdr.sample_rate = 1.090e6  # Hz
sdr.center_freq = 70e6     # Hz
sdr.freq_correction = 60   # PPM
sdr.gain = 'auto'

samples = sdr.read_samples(512)

print(samples)
print('length ', len(samples))
