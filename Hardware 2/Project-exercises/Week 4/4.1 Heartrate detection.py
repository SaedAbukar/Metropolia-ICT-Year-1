from filefifo import Filefifo
from fifo import Fifo

data = Filefifo(10, name='capture02_250Hz.txt')


# Define the sampling interval (ts) in seconds
sample_rate = 250  # Example: Assuming 250 Hz sampling rate
sampling_interval = 1.0 / sample_rate
seconds = 1 / 250
two_seconds = 2 / seconds


def get_samples(data, seconds):
    current = data.get()
    maximum = minimum = current
    ratio = 3/4
    threshold = minimum + (maximum - minimum) * ratio
    sample = 0
    prev = 0
    prev_slope = 0
    slope = 0
    peaks = []
    for i in range(seconds):  # Assuming we've already processed one data point
        prev = current
        current = data.get()  # Get the next data point
        if current > maximum:
            maximum = current
        elif current < minimum:
            minimum = current
        sample += 1
        prev_slope = slope
        slope = current - prev
        threshold = minimum + (maximum - minimum) * ratio
        #print("cur", current)
        #print("prev", prev)
        #print("max", maximum)
        #print("min", minimum)
        #print("prevslope", prev_slope)
        #print("slope", slope)
        #print("threshold", threshold)
        if prev_slope > 0 and slope <= 0 and current > threshold:
            peaks.append(sample)
            
    ppi_samples = []    
    for i in range(1, len(peaks)):
        ppi_samples.append(peaks[i] - peaks[i - 1])
        
    ppi_seconds = [samples * sampling_interval for samples in ppi_samples]
    hr = []
    min_hr = 30
    max_hr = 200
    for ppi in ppi_seconds:
        if min_hr <= (60 / ppi) <= max_hr:
            hr.append(60 / ppi)

    #print("peaks", peaks)
    #print("ppi in seconds", ppi_seconds)
    #print("hr", hr)
    return peaks, ppi_seconds, hr[:20]


        
peaks_list, ppi_list, hr_list = get_samples(data, 5000)
for i in range(len(hr_list)):
    print(hr_list[i])