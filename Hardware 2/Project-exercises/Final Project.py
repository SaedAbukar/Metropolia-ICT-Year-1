from filefifo import Filefifo
from fifo import Fifo
from ssd1306 import SSD1306_I2C
from machine import Pin, I2C, ADC, Signal
from piotimer import Piotimer
import micropython
import time
micropython.alloc_emergency_exception_buf(200)


class isr_adc: 
    def __init__(self, adc_pin_nr):
        self.av = ADC(adc_pin_nr) # sensor AD channel
        self.samples = Fifo(250) # fifo where ISR will put samples
        self.dbg = Pin(0, Pin.OUT) # debug GPIO pin for measuring timing with oscilloscope
        self.measuring = False
        
    def handler(self, tid):
        if self.measuring:
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


class Avg_peaks:
    def __init__(self, size=9):
        self.size = size
        self.data = []

    def add(self, item):
        if len(self.data) >= self.size:
            self.data.pop(0)  # Maintain fixed size
        self.data.append(item)

    def average(self):
        if len(self.data) == 0:
            return 0  # Avoid division by zero
        return sum(self.data) / len(self.data)
    
    def median(self):
        if len(self.data) == 0:
            return 0  # Handle empty list scenario
        sorted_data = sorted(self.data)  # Sort the list
        n = len(sorted_data)
        if n % 2 == 1:
            # If the length is odd, return the middle element
            return sorted_data[n // 2]
        else:
            # If the length is even, return the average of the two middle elements
            return (sorted_data[(n // 2) - 1] + sorted_data[n // 2]) / 2


class PeakDetector:
    def __init__(self, sample_rate=250, sample_threshold=250):
        self.sample_rate = sample_rate
        self.sample_threshold = sample_threshold
        self.sampling_interval = (1 / sample_rate)  # Sampling interval in seconds
        self.sampling_interval_ms = (1 / sample_rate) * 1000
        self.data = isr_adc(26)
        self.tmr = Piotimer(freq=self.sample_rate, callback=self.data.handler)
        self.peaks = []
        self.avg_peaks = Avg_peaks(5)
        self.hr = Avg_peaks(15)
        self.interval_avg = 0
        self.sample_count = 0
        self.count = 0
        self.minimum = 32000
        self.maximum = 32000
        self.threshold_on = self.minimum + (self.maximum - self.minimum) * 0.75
        self.threshold_off = self.minimum + (self.maximum - self.minimum) * 0.70
        self.prev_sample = 0
        self.detecting_peaks = False
        self.filtered = LowPassFilter(63) #Viet 25 and Saed 63
        self.hrv_calculated = False
        
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
                self.reset()
                if len(self.peaks) > 10:
                    #print(self.peaks)
                    ppi = peak_detector.calculate_ppi(self.peaks)
                    if ppi:
                        bpm = peak_detector.calculate_bpm(ppi[-1])
                        print("BPM", bpm)
                        self.show_bpm(bpm, filtered_value, self.maximum, self.minimum)
        
            if self.peaks:
                self.interval_avg = self.peaks_avg(self.peaks)
                
            if not self.detecting_peaks and filtered_value >= self.threshold_on and (self.count - self.prev_sample) > 75:
                if len(self.peaks) >= 10:
                    if -50 < (self.count - self.prev_sample) - self.interval_avg < 50:
                        self.detecting_peaks = True
                        self.peaks.append(self.count)
                else:   
                    self.detecting_peaks = True
                    self.peaks.append(self.count)
                self.prev_sample = self.count
            if self.detecting_peaks and filtered_value <= self.threshold_off:
                self.detecting_peaks = False
                
                
    def HRV_logic(self):                        
        while self.data.samples.has_data():
            raw_value = self.data.samples.get()
            filtered_value = self.filtered.lpf_single(raw_value)  
            self.count += 1
            self.update_minmax(filtered_value)
            samplerate = 5000
            
            
            if self.sample_count % self.sample_threshold == 0:
                # Calculate thresholds after 250 samples
                self.calculate_thresholds()
                self.reset()
        
            if self.peaks:
                self.interval_avg = self.peaks_avg(self.peaks)
                
            if not self.detecting_peaks and filtered_value >= self.threshold_on and (self.count - self.prev_sample) > 75:
                if len(self.peaks) >= 10:
                    if -50 < (self.count - self.prev_sample) - self.interval_avg < 50:
                        self.detecting_peaks = True
                        self.peaks.append(self.count)
                else:   
                    self.detecting_peaks = True
                    self.peaks.append(self.count)
                self.prev_sample = self.count
            if self.detecting_peaks and filtered_value <= self.threshold_off:
                self.detecting_peaks = False
            
            if len(self.peaks) == 15:
                if not self.hrv_calculated:
                    ppi = peak_detector.calculate_ppi(self.peaks)
                    calculate_hrv(ppi)
                    self.hrv_calculated = True
      
      
    def peaks_avg(self, peaks):
        if len(peaks) > 1:
            for i in range(len(peaks)):
                interval = peaks[i] - peaks[i - 1]
                if 75 < interval < 375:
                    self.avg_peaks.add(interval)
        else:
            self.avg_peaks.add(peaks[0])
        #median = self.avg_peaks.median()
        avg = self.avg_peaks.average()
        return avg
                
                
                
    def calculate_ppi(self, peaks, min_ppi=400, max_ppi=1300):
        self.ppi = []
        avg_ppi = 0
        for i in range(1, len(self.peaks)):
            self.interval = (self.peaks[i] - self.peaks[i - 1]) * self.sampling_interval_ms
            if min_ppi < self.interval < max_ppi:
                self.ppi.append(self.interval)
        
        if len(self.ppi) > 1:
            avg_ppi = int(sum(self.ppi) / len(self.ppi))
            
        return self.ppi

    # OLD HR CALCULATOR
    def calculate_bpm1(self, ppi, sample_rate=250, min_hr=30, max_hr=200):
        hr = []
        heart_rate = 60 / (ppi / 1000)  
        if min_hr <= heart_rate <= max_hr:
            hr.append(heart_rate) 
        
        if not hr:  # If 'hr' is empty, there's no valid heart rate to calculate.
            return None  
        
        hr_sorted = sorted(hr)

        n = len(hr_sorted)
        if n % 2 == 1:
            # Odd number of elements: the median is the middle element.
            current_hr = hr_sorted[n // 2]
        else:
            # Even number of elements: the median is the average of the two middle elements.
            current_hr = (hr_sorted[(n // 2) - 1] + hr_sorted[n // 2]) / 2
        
        return int(current_hr)  # Return the median heart rate
    
    # NEW HR CALCULATOR
    def calculate_bpm(self, ppi, sample_rate=250, min_hr=30, max_hr=200):
        heart_rate = 60 / (ppi / 1000)  # Convert milliseconds to seconds, then calculate heart rate
        if min_hr <= heart_rate <= max_hr:
            #print(heart_rate)
            self.hr.add(heart_rate)  # Collect heart rates that meet the range conditions
        
        if not self.hr:  # If 'hr' is empty, there's no valid heart rate to calculate.
            return None  # Return None or an appropriate default value
        
        median_hr = self.hr.median()
        avg_hr = self.hr.average()
        #print(self.hr.data)
        return int(median_hr)  # Return the median heart rate

    
    def show_bpm(self, bpm, val, maximum, minimum):
        last_y = 0
        

        display.vline(0, 0, 64, 0)

        display.scroll(-1, 0)  

        if maximum - minimum > 0:
            y = 64 - int(32 * (val - minimum) / (maximum - minimum))
            display.line(125, last_y, 126, y, 1)
            last_y = y


        display.fill_rect(0, 0, 128, 16, 0)  # Clear the top text area

        if bpm:
            display.text("%d bpm" % bpm, 12, 0)            
        display.show()
        




class Encoder:
    def __init__(self, rot_a, rot_b, rot_c):
        self.a = Pin(rot_a, mode=Pin.IN, pull=Pin.PULL_UP)
        self.b = Pin(rot_b, mode=Pin.IN, pull=Pin.PULL_UP)
        self.c = Pin(rot_c, mode=Pin.IN, pull=Pin.PULL_UP)
        self.fifo = Fifo(30, typecode='i')  # milliseconds
        self.last_pressed_time = 0
        self.button_pressed = False
        self.a.irq(handler=self.handler, trigger=Pin.IRQ_RISING, hard=True)
        self.c.irq(handler=self.button, trigger=Pin.IRQ_FALLING, hard=True)
        
    def handler(self, pin):
        if self.b.value():
            self.fifo.put(-1)  # Counter-clockwise rotation
        else:
            self.fifo.put(1)  # Clockwise rotation
            
    def button(self, pin):
        current_time = time.ticks_ms()
        if current_time - self.last_pressed_time < 200:
            return
        self.last_pressed_time = current_time
        
        self.fifo.put(0)
       
    

class Menu:
    def __init__(self, options, functions):
        self.options = options
        self.functions = functions
        self.selected_index = 0

    def select_next(self):
        self.selected_index = (self.selected_index + 1) % len(self.options)

    def select_prev(self):
        self.selected_index = (self.selected_index - 1) % len(self.options)

    def get_selected_option(self):
        return self.options[self.selected_index]

    def selected_function(self):
        return self.functions[self.selected_index]
    


#--------------------------------------------------#
    # Calculation for HRV analysis

# Mean PPI calculation - (data is the PPI_array)
def mean_ppi_cal(data):
    sumPPI = max(data)
    rounded_PPI = sumPPI/len(data)
    return int(rounded_PPI)

# Mean HR calculation 
def mean_hr_cal(meanPPI):
    rounded_HR = round(60*1000/meanPPI, 0)
    return int(rounded_HR)

# RMSSD calculation
def RMSSD_cal(data):
    i = 0
    summary = 0
    while i < len(data)-1:
        summary += (data[i+1]-data[i])**2
        i += 1
    rounded_RMSSD = round((summary/(len(data)-1))**(1/2), 0)
    return int(rounded_RMSSD)

# SDNN calculation
def SDNN_cal(data, PPI):
    summary = 0
    for i in data:
        summary += (i-PPI)**2
    SDNN = (summary/(len(data)-1))**(1/2)
    rounded_SDNN = round(SDNN, 0)
    return int(rounded_SDNN)


# Function to calculate HRV metrics without statistics module
def calculate_hrv(ppi):
    # Calculate mean PPI
    mean_ppi = sum(ppi) / len(ppi)
    
    # Calculate mean HR
    mean_hr = round(60 * 1000 / mean_ppi, 2)
    
    
    # Calculate RMSSD
    # Calculate sum of squared differences between consecutive elements in ppi
    sum_diff_sq = 0
    for i in range(len(ppi) - 1):
        diff = ppi[i + 1] - ppi[i]  # Calculate difference between consecutive elements
        diff_sq = diff ** 2         # Square the difference
        sum_diff_sq += diff_sq      # Add the squared difference to the sum

    # Calculate Root Mean Square of Successive Differences (RMSSD)
    rmssd = (sum_diff_sq / (len(ppi) - 1)) ** 0.5

    # Calculate Standard Deviation of NN intervals (SDNN)
    sdnn = 0
    for x in ppi:
        diff = x - mean_ppi          # Calculate difference between each element and the mean
        diff_sq = diff ** 2          # Square the difference
        sdnn += diff_sq              # Add the squared difference to the sum
    sdnn /= len(ppi)                # Calculate mean of squared differences
    sdnn = sdnn ** 0.5              # Take square root to get standard deviation
    
    # Print or return the HRV metrics
    print("Mean PPI:", mean_ppi)
    print("Mean HR:", mean_hr)
    print("RMSSD:", rmssd)
    print("SDNN:", sdnn)
    display.fill(0)
    display.text("Mean PPI: %d" % mean_ppi, 0, 10)
    display.text("Mean HR: %d" % mean_hr, 0, 20)
    display.text("RMSSD: %d" % rmssd, 0, 30)
    display.text("SDNN: %d" % sdnn, 0, 40)
    display.show()
    
    
#----------------------------------------------------#


def init_display():
    i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)  # Initialize I2C interface
    oled = SSD1306_I2C(128, 64, i2c)  # Initialize SSD1306 OLED display
    oled.fill(0)  # Clear the display
    return oled

def update_display(oled, menu):
    oled.fill(0)  # Clear the display
    oled.text("Menu:", 0, 0)
    for i, option in enumerate(menu.options):
        if i == menu.selected_index:
            oled.text("<" + option + "> ", 0, 10 + i * 10)
        else:
            oled.text(option, 0, 10 + i * 10)
            
    oled.show()


def start():
    display.fill(0)
    display.text("Welcome", 32, 10)
    display.text("Press SW0", 26, 20)
    display.text("to start", 30, 30)
    display.text("the measurement", 5, 40)
    display.show()
    
def measurement():
    display.text("Place your", 25, 15)
    display.text("finger on to ", 15, 25)
    display.text("the sensor", 25, 35)
    display.text("and wait...", 20, 45)
    display.show()
    



def HR_logic():
    global user_state
    global SW0
    display.fill(0)
    measurement()
    time.sleep_ms(300)
    display.fill(0)
    user_state = "bpm"
    while True:
        peak_detector.data.measuring = True
        peaks = peak_detector.detect_peaks()
        if SW0() == 0:
            peak_detector.data.measuring = False
            print("back")
            user_state == "menu"
            display.fill(0)
            break
        
        
                    

def test_HRV():
    global user_state
    global SW0
    display.fill(0)
    measurement()
    time.sleep_ms(300)
    display.fill(0)
    user_state = "hrv"
    while True:
        peak_detector.data.measuring = True
        peaks = peak_detector.HRV_logic()
        if SW0() == 0:
            peak_detector.data.measuring = False
            print("back")
            user_state == "menu"
            display.fill(0)
            break
   

def kubious_logic():
    global user_state
    global SW0
    while True:
        display.text("Kubious Logic", 0, 0)
        if SW0() == 0:
            peak_detector.data.measuring = False
            print("back")
            user_state == "menu"
            display.fill(0)
            break
    
    
sample_rate = 250 
sampling_interval = 1.0 / sample_rate
peak_detector = PeakDetector(sample_rate=250, sample_threshold=250)
user_state = "start"
led = Signal(Pin("LED", Pin.OUT), invert=True)
i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
display = SSD1306_I2C(128, 64, i2c)
SW0 = Pin(9, Pin.IN, Pin.PULL_UP)
SW1 = Pin(8, Pin.IN, Pin.PULL_UP)
    

def main():
    peak_detector = PeakDetector(sample_rate=250, sample_threshold=250)
    menu_options = ["Measure HR", "HRV", "Kubious"]
    functions = [HR_logic, test_HRV, kubious_logic] 
    menu = Menu(menu_options, functions)
    global user_state
    
    rot = Encoder(10, 11, 12)
    oled = init_display()
    
    while True:
        if user_state == "start":
            start()
            
        if SW0() == 0 and user_state == "start":
            user_state = "menu"
            
        if SW0() == 0 and user_state == "bpm":
            user_state = "menu"
        
        if SW0() == 0 and user_state == "hrv":
            user_state = "menu"
            
        if SW0() == 0 and user_state == "kubios":
            user_state = "menu"
            
            
        if user_state == "menu":
            update_display(oled, menu)  # Update the display to reflect current selection
            time.sleep_ms(100)
            
        if rot.fifo.has_data():
            event = rot.fifo.get()
            if event == 1:
                menu.select_next()
            elif event == -1:
                menu.select_prev()
            elif event == 0:
                selected_function = menu.selected_function()
                selected_function() 
            update_display(oled, menu)  # Update the display regardless of event
        time.sleep_ms(100)

if __name__ == "__main__":
    main()

