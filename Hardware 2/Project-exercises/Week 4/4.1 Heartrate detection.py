from filefifo import Filefifo

data = Filefifo(10, name='capture03_250Hz.txt')

# Define the sampling interval (ts) in seconds
sample_rate = 250  # Example: Assuming 250 Hz sampling rate
sampling_interval = 1.0 / sample_rate


def calculate_ppi_and_hr(data, sample_rate=250, min_hr=30, max_hr=200, max_hr_count=20):
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

    while len(hr) < max_hr_count:
        if data.has_data():# Loop until max_hr_count heart rates are calculated
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
            if not counting and prev_slope > 0 and slope <= 0 and current > threshold:
                peaks.append(sample)
                counting = True  # Start counting samples
            elif counting and current < threshold:
                counting = False  # Stop counting samples
        
        for i in range(1, len(peaks)):
            ppi_samples = peaks[i] - peaks[i - 1]
            ppi_milliseconds.append(ppi_samples * sampling_interval_ms)  # Calculate PPI in milliseconds

        i = 0
        while len(hr) < max_hr_count:
            if i >= len(ppi_milliseconds):
                break
            heart_rate = 60 / (ppi_milliseconds[i] / 1000)  # Convert milliseconds back to seconds for heart rate calculation
            if min_hr <= heart_rate <= max_hr:
                hr.append(heart_rate)
            i += 1
        
    return peaks, ppi_milliseconds, hr


result_peaks, ppi_milliseconds, hr = calculate_ppi_and_hr(data)

for i in range(len(result_peaks)):
    print("peaks", result_peaks[i])

for i in range(len(ppi_milliseconds)):
    print("ppi_millisecond", ppi_milliseconds[i])
    
for i in range(len(hr)):
    print("hr", hr[i])
