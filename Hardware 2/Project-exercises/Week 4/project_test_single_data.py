from filefifo import Filefifo
from time import sleep

class PeakDetector:
    def __init__(self, sample_rate=250, sample_threshold=250):
        self.sample_rate = sample_rate
        self.sample_threshold = sample_threshold
        self.sampling_interval = (1 / sample_rate)  # Sampling interval in seconds
        self.sampling_interval_ms = (1 / sample_rate) * 1000
        self.data = Filefifo(10, name='capture03_250Hz.txt')
        self.peaks = []
        self.count = 0
        
        self.reset()  # Reset state variables at initialization

    def reset(self):
        """Reset all state variables."""
        self.minimum = float('inf')
        self.maximum = float('-inf')
        self.sample_count = 0
        self.count = 0
        self.peaks = []
        self.threshold_on = None
        self.threshold_off = None
        self.detecting_peaks = False

    def update_minmax(self, value):
        """Update minimum and maximum based on the given value."""
        if value > self.maximum:
            self.maximum = value
        if value < self.minimum:
            self.minimum = value
        
        self.sample_count += 1
    
    def calculate_thresholds(self):
        """Calculate on/off thresholds based on minimum and maximum."""
        self.threshold_on = self.minimum + (self.maximum - self.minimum) * 0.75
        self.threshold_off = self.minimum + (self.maximum - self.minimum) * 0.70
    
    def detect_peaks(self):
        while self.data.has_data():
            curr = self.data.get()  # Get the current data point
            self.update_minmax(curr)
            
            if self.sample_count >= self.sample_threshold:
                # Calculate thresholds after 250 samples
                self.calculate_thresholds()
                self.count += 1
                if not self.detecting_peaks and curr >= self.threshold_on:
                    #print(self.detecting_peaks, self.threshold_on, curr, self.threshold_off)
                    self.detecting_peaks = True
                    self.peaks.append(self.count)
                if self.detecting_peaks and curr <= self.threshold_off:
                    self.detecting_peaks = False
                    #print(self.detecting_peaks, self.threshold_on, curr, self.threshold_off) 
                #print(self.peaks)
                
                if len(self.peaks) > 1:
                    return self.peaks
                
                
    def calculate_ppi(self, min_ppi=300, max_ppi=1500):
        """Calculate peak-to-peak intervals (PPI)."""
        peaks = peak_detector.detect_peaks()
        if len(self.peaks) < 1:
            return None  # Cannot calculate intervals with fewer than 2 peaks
        
        # Calculate the intervals between consecutive peaks
        self.ppi = []
        for i in range(1, len(self.peaks)):
            self.interval = (self.peaks[i] - self.peaks[i - 1]) * self.sampling_interval_ms
            if min_ppi < self.interval < max_ppi:
                self.ppi.append(self.interval)
        
        return self.ppi


def calculate_hr(ppi_ms, sample_rate=250, min_hr=30, max_hr=200):
    hr = []
    heart_rate = 60 / (ppi_ms / sample_rate)  # Convert milliseconds to seconds, then calculate heart rate
    if min_hr <= heart_rate <= max_hr:
        hr.append(heart_rate)  # Collect heart rates that meet the range conditions
    
    if not hr:  # If 'hr' is empty, there's no valid heart rate to calculate.
        return None  # Return None or an appropriate default value
    
    # Sort the list of heart rates to get the median
    hr_sorted = sorted(hr)

    n = len(hr_sorted)
    if n % 2 == 1:
        # Odd number of elements: the median is the middle element.
        current_hr = hr_sorted[n // 2]
    else:
        # Even number of elements: the median is the average of the two middle elements.
        current_hr = (hr_sorted[(n // 2) - 1] + hr_sorted[n // 2]) / 2
    
    return current_hr  # Return the median heart rate


peak_detector = PeakDetector(sample_rate=250, sample_threshold=250)

i = 0
while True:
    peaks = peak_detector.detect_peaks()
    ppi = peak_detector.calculate_ppi()
    i += 1
    if i >= 250:
        if len(peaks) >= 1:# Check if there are at least two peaks available
            interval = peaks[-1] - peaks[-2]  # Get the most recent PP interval in samples
            current_ppi = (peaks[-1] - peaks[-2]) * 4
            current_hr = calculate_hr(interval)  # Calculate heart rate in bpm using sample rate
            #print(peaks)
            print("Current PPI:", current_ppi)
            print("Current Heart Rate:", current_hr)
            i = 0


