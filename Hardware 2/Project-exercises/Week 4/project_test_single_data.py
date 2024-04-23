from filefifo import Filefifo
from time import sleep

class PeakDetector:
    def __init__(self, sample_rate=250, sample_threshold=250):
        self.sample_rate = sample_rate
        self.sample_threshold = sample_threshold
        self.sampling_interval = (1 / sample_rate)  # Sampling interval in seconds
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
        while True:
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
                    print(self.peaks)
                    
                    if len(self.peaks) > 10:
                        self.reset()
        return self.peaks


peak_detector = PeakDetector(sample_rate=250, sample_threshold=250)
peak_detector.detect_peaks()
