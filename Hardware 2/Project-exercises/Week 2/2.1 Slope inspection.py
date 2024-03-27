from filefifo import Filefifo
from fifo import Fifo

data = Filefifo(10, name='capture_250Hz_01.txt')
current = data.get()
prev = 0
slope = 0
prev_slope = 0
peaks = []
peaks2 = []

# Define the sampling interval (ts) in seconds
sample_rate = 250  # Example: Assuming 250 Hz sampling rate
sampling_interval = 1.0 / sample_rate

# Store peak-to-peak intervals and their corresponding number of samples
peak_to_peak_intervals_samples = []
peak_to_peak_intervals_seconds = []

for _ in range(3000):
    prev = current
    current = data.get()
    prev_slope = slope
    slope = current - prev
    
    if prev_slope > 0 and slope <= 0:
        peaks.append(_)

        
for _ in range(1, len(peaks)):
    peak_to_peak_samples = peaks[_] - peaks[_ - 1]
    peak_to_peak_seconds = peak_to_peak_samples * sampling_interval  # Calculate peak-to-peak interval in seconds
    peak_to_peak_intervals_samples.append(peak_to_peak_samples)
    peak_to_peak_intervals_seconds.append(peak_to_peak_seconds)



# Calculate the frequency of the signal
average_ppi = sum(peak_to_peak_intervals_seconds) / (len(peak_to_peak_intervals_seconds))
frequency = 1 / average_ppi

# Print at least three peak-to-peak intervals
print("Peak-to-Peak Intervals (in number of samples):", peak_to_peak_intervals_samples[1:4])
print("Peak-to-Peak Intervals (in seconds):", peak_to_peak_seconds, "seconds")
print("Average Frequency of the Signal:", frequency, "Hz")

