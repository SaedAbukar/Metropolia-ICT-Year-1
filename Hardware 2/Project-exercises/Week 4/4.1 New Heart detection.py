from filefifo import Filefifo
from time import sleep

data = Filefifo(10, name='capture01_250Hz.txt')

sample_rate = 250 
sampling_interval = 1.0 / sample_rate

def detect_peaks(data, sample_rate=250):
    curr = data.get() #lpf1(data.get(), data.get())
    peaks = []
    sample = 0
    maximum = minimum = curr
    counting = False
    sampling_interval_ms = (1 / sample_rate) * 1000
    
    for i in range(1500):  # Assuming we've already processed one data point
        prev = curr
        curr = lpf1(curr, data.get())  # Get the next data point
        if curr > maximum:
            maximum = curr
        elif curr < minimum:
            minimum = curr
        sample += 1
        threshold_on = minimum + (maximum - minimum) * 0.75
        threshold_off = minimum + (maximum - minimum) * 0.5
#         print("max %s" % sample, maximum)
#         print("thres_on %s" % sample, threshold_on)
#         print("curr %s" % sample, curr)
#         print("peaks %s" % sample, peaks)
#         print("thres_off %s" % sample, threshold_off)
#         print("min %s" % sample, minimum)
        if not counting and curr >= threshold_on:
            counting = True
            peaks.append(sample)
        
        if counting and curr <= threshold_off:
            counting = False
            
    return peaks

def calculate_ppi_ms(peaks, sample_rate=250):
    
    ppi_ms = []
    sampling_interval_ms = (1 / sample_rate) * 1000  # Calculate sampling interval in milliseconds
    
    for i in range(1, len(peaks)):
        ppi_samples = peaks[i] - peaks[i - 1]
        ppi_ms.append(ppi_samples * sampling_interval_ms)  # Calculate PPI in milliseconds
        
    return ppi_ms


def calculate_hr(ppi_ms, sample_rate=250, min_hr=30, max_hr=200):
    
    hr = []
    heart_rate = 60 / (ppi_ms / sample_rate)  # Convert milliseconds back to seconds for heart rate calculation
    if min_hr <= heart_rate <= max_hr:
        hr.append(heart_rate)
    
    if len(hr) > 1:
        hr = sum(hr) / len(hr)
        
    return hr


def lpf1(prev_value, new_value, alpha=0.85):
    return alpha * prev_value + (1 - alpha) * new_value


j = 0
while True:
    while data.has_data():
        result_peaks = detect_peaks(data)
        j += 1
        if len(result_peaks) >= 1:  # Check if there are at least two peaks available
            current_ppi = result_peaks[-1] - result_peaks[-2]  # Get the most recent PP interval in samples
            current_hr = calculate_hr(current_ppi)  # Calculate heart rate in bpm using sample rate
            print("Current Heart Rate %s:" %j, current_hr)
    


