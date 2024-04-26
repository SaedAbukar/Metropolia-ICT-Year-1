from filefifo import Filefifo
from fifo import Fifo
from ssd1306 import SSD1306_I2C
from machine import Pin, I2C, ADC, Signal
from piotimer import Piotimer
import micropython
import time
micropython.alloc_emergency_exception_buf(200)

led = Signal(Pin("LED", Pin.OUT), invert=True)
i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
display = SSD1306_I2C(128, 64, i2c)

class isr_adc: 
    def __init__(self, adc_pin_nr):
        self.av = ADC(adc_pin_nr) # sensor AD channel
        self.samples = Fifo(250) # fifo where ISR will put samples
        self.dbg = Pin(0, Pin.OUT) # debug GPIO pin for measuring timing with oscilloscope
        
    def handler(self, tid):
        self.samples.put(self.av.read_u16())
        self.dbg.toggle()
     
     
class LowPassFilter:
    def __init__(self, filtering_amount=63):
        # Initialize with the filtering amount and an empty list for previous values
        self.filtering_amount = filtering_amount
        self.lastvals = []

    def lpf_single(self, value):
        """Apply low-pass filter to a single value and maintain state."""
        if len(self.lastvals) < self.filtering_amount:
            # If the list is not full yet, just add the value and return the raw value
            self.lastvals.append(value)
            # Initial condition: return the current value when the window isn't full
            filtered_value = int((value + sum(self.lastvals)) / (len(self.lastvals)))
        else:
            # If the list is full, calculate the filtered value and update the list
            filtered_value = int((value + sum(self.lastvals)) / self.filtering_amount)
            # Remove the oldest value and add the new one
            self.lastvals.pop(0)
            self.lastvals.append(value)

        return filtered_value  # Return the filtered result


class PeakDetector:
    def __init__(self, sample_rate=250, sample_threshold=250):
        self.sample_rate = sample_rate
        self.sample_threshold = sample_threshold
        self.sampling_interval = (1 / sample_rate)  # Sampling interval in seconds
        self.sampling_interval_ms = (1 / sample_rate) * 1000
        self.data = isr_adc(26)
        self.tmr = Piotimer(freq=self.sample_rate, callback=self.data.handler)
        self.peaks = []
        self.sample_count = 0
        self.count = 0
        self.minimum = 0
        self.maximum = 0
        self.threshold_on = self.minimum + (self.maximum - self.minimum) * 0.75
        self.threshold_off = self.minimum + (self.maximum - self.minimum) * 0.70
        self.detecting_peaks = False
        self.filtered = LowPassFilter(63)
        
        self.reset()  # Reset state variables at initialization

    def reset(self):
        """Reset variables."""
        self.minimum = float('inf')
        self.maximum = float('-inf')

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
        while self.data.samples.has_data():
            raw_value = self.data.samples.get()  # Get the current data point from ADC
            
            # Apply the low-pass filter to smooth the data
            filtered_value = self.filtered.lpf_single(raw_value)  # Filter the raw ADC data
            self.count += 1
            self.update_minmax(filtered_value)
            
            if self.sample_count % self.sample_threshold == 0:
                # Calculate thresholds after 250 samples
                self.calculate_thresholds()
                if len(self.peaks) >= 10:
                    #print(peaks)
                    ppi = peak_detector.calculate_ppi(self.peaks)
                    if ppi:
                        bpm = peak_detector.calculate_bpm(ppi[-1])
                        print("PPI:", ppi[-1], "BPM", bpm)
                        self.show_bpm(bpm, filtered_value, self.maximum, self.minimum)
                #print(self.threshold_on)
            #print(self.detecting_peaks, self.threshold_on, curr, self.threshold_off, self.minimum, self.maximum)
                self.reset()
                #print(self.detecting_peaks, self.threshold_on, curr, self.threshold_off)

            if not self.detecting_peaks and filtered_value >= self.threshold_on:
                #print(self.detecting_peaks, self.threshold_on, curr, self.threshold_off, self.minimum, self.maximum)
                #print(self.detecting_peaks, self.threshold_on, curr, self.threshold_off)
                #print(self.count)
                self.detecting_peaks = True
                self.peaks.append(self.count)
            if self.detecting_peaks and filtered_value <= self.threshold_off:
                self.detecting_peaks = False
                #print(self.detecting_peaks, self.threshold_on, curr, self.threshold_off) 
            #print(self.peaks)
            #print(self.detecting_peaks, self.threshold_on, curr, self.threshold_off, self.minimum, self.maximum)
#         if self.peaks:
#             #print(peaks)
#             ppi = peak_detector.calculate_ppi(self.peaks)
#             if ppi:
#                 bpm = peak_detector.calculate_bpm(ppi[-1])
#                 print("PPI:", ppi[-1], "BPM", bpm)
#                 self.show_bpm(bpm, filtered_value, self.maximum, self.minimum)
                
                
    def calculate_ppi(self, peaks, min_ppi=400, max_ppi=1300):
#         """Calculate peak-to-peak intervals (PPI)."""
#         peaks = peak_detector.detect_peaks()
#         if len(self.peaks) < 1:
#             return None  # Cannot calculate intervals with fewer than 2 peaks
        
        # Calculate the intervals between consecutive peaks
        self.ppi = []
        avg_ppi = 0
        for i in range(1, len(self.peaks)):
            self.interval = (self.peaks[i] - self.peaks[i - 1]) * self.sampling_interval_ms
            if min_ppi < self.interval < max_ppi:
                self.ppi.append(self.interval)
        
        if len(self.ppi) > 1:
            avg_ppi = int(sum(self.ppi) / len(self.ppi))
            
        return self.ppi


    def calculate_bpm(self, ppi, sample_rate=250, min_hr=30, max_hr=200):
        hr = []
        heart_rate = 60 / (ppi / 1000)  # Convert milliseconds to seconds, then calculate heart rate
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
        
        return int(current_hr)  # Return the median heart rate
    
    
    def show_bpm(self, bpm, val, maximum, minimum):
        last_y = 0

        display.vline(0, 0, 64, 0)
        display.scroll(-1, 0)  # Scroll left 1 pixel

        if maximum - minimum > 0:
            # Draw beat line.
            y = 64 - int(32 * (val - minimum) / (maximum - minimum))
            display.line(125, last_y, 126, y, 1)
            last_y = y

        # Clear top text area.
        display.fill_rect(0, 0, 128, 16, 0)  # Clear the top text area

        if bpm:
            display.text("%d bpm" % bpm, 12, 0)
            #print("%d bpm" % bpm)
            
        display.show()



sample_rate = 250 
sampling_interval = 1.0 / sample_rate
peak_detector = PeakDetector(sample_rate=250, sample_threshold=250)


while True:
    peaks = peak_detector.detect_peaks()





