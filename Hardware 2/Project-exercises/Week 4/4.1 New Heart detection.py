from filefifo import Filefifo
from time import sleep

data = Filefifo(10, name='capture01_250Hz.txt')

sample_rate = 250 
sampling_interval = 1.0 / sample_rate

def detect_peaks(data, sample_rate=250):
    curr = lpf1(data.get(), data.get())
    peaks = []
    sample = 0
    maximum = minimum = curr
    counting = False
    sampling_interval_ms = (1 / sample_rate) * 1000
    
    for i in range(1000):  # Assuming we've already processed one data point
        prev = curr
        curr = lpf1(curr, data.get())  # Get the next data point
        if curr > maximum:
            maximum = curr
        elif curr < minimum:
            minimum = curr
        sample += 1
        threshold_on = minimum + (maximum - minimum) * 0.75
        threshold_off = minimum + (maximum - minimum) * 0.5

        if not counting and curr >= threshold_on:
            counting = True
            peaks.append(sample)
        
        if counting and curr <= threshold_off:
            counting = False
            
    return peaks

def lpf1(prev_value, new_value, alpha=0.85):
    return alpha * prev_value + (1 - alpha) * new_value


j = 0
while True:
    while data.has_data():
        result_peaks = detect_peaks(data)
        j += 1
        if len(result_peaks) >= 2:  # Check if there are at least two peaks available
            current_ppi = result_peaks[-1] - result_peaks[-2]  # Get the most recent PP interval in samples
            current_hr = 60 / (current_ppi / sample_rate)  # Calculate heart rate in bpm using sample rate
            print("Current Heart Rate %s:" %j, current_hr)
        
    # Wait for a short duration before checking for data again
    sleep(1)  # Adjust the duration as needed
