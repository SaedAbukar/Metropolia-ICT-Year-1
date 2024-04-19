from filefifo import Filefifo

data = Filefifo(10, name='capture01_250Hz.txt')


sample_rate = 250 
sampling_interval = 1.0 / sample_rate


def calculate_ppi_and_hr(data, sample_rate=250, min_hr=30, max_hr=200):
    current = data.get()
    maximum = minimum = current
    ratio = 3/4
    sample = 0
    prev = 0
    prev_slope = 0
    slope = 0
    peaks = []
    counting = False  # Flag to indicate if counting samples
    ppi_milliseconds = []
    hr = []
    
    sampling_interval_ms = (1 / sample_rate) * 1000  # Calculate sampling interval in milliseconds

     # Loop until max_hr_count heart rates are calculated
    for i in range(1000):
        prev = current
        current = low_pass_filter(prev, data.get())  # Get the next data point
        
        if current > maximum:
            maximum = current
        
        elif current < minimum:
            minimum = current
        
        sample += 1
        prev_slope = slope
        slope = current - prev
        threshold = minimum + (maximum - minimum) * ratio
        
        if not counting and prev_slope > 0 and slope <= 0 and current > threshold:
            peaks.append(sample)
            counting = True  # Start counting samples
        
        elif counting and current < threshold:
            counting = False  # Stop counting samples
        
    for i in range(1, len(peaks)):
        ppi_samples = peaks[i] - peaks[i - 1]
        ppi_milliseconds.append(ppi_samples * sampling_interval_ms)  # Calculate PPI in milliseconds

 
    for i in range(1, len(ppi_milliseconds)):
        
        heart_rate = 60 / (ppi_milliseconds[i] / 1000)  # Convert milliseconds back to seconds for heart rate calculation
        
        if min_hr <= heart_rate <= max_hr:
            hr.append(heart_rate)
    
    return peaks, ppi_milliseconds, hr, threshold

def low_pass_filter(prev_value, new_value, alpha=0.85):
    return alpha * prev_value + (1 - alpha) * new_value



while True:
    while data.has_data():
        peaks, ppi_ms, hr, threshold = calculate_ppi_and_hr(data)
#         for i in range(len(peaks)):
#             print("peak:", peaks[i])
#         for i in range(len(ppi_ms)):
#             print("pps_ms:", ppi_ms[i])
        for i in range(len(hr)):
            print("hr:", hr[i])



