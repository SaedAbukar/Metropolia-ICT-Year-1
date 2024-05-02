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
        self.minimum = 0
        self.maximum = 0
        self.threshold_on = self.minimum + (self.maximum - self.minimum) * 0.75
        self.threshold_off = self.minimum + (self.maximum - self.minimum) * 0.70
        self.prev_sample = 0
        self.detecting_peaks = False
        self.filtered = LowPassFilter(63) #Viet 25 and Saed 63
        
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
    
    def avg_ppi(self, peaks, min_ppi=400, max_ppi=1300):
        
        # Calculate the intervals between consecutive peaks
        self.ppi = []
        avg_ppi = 0
        for i in range(1, len(self.peaks)):
            self.interval = (self.peaks[i] - self.peaks[i - 1]) * self.sampling_interval_ms
            if min_ppi < self.interval < max_ppi:
                self.ppi.append(self.interval)
        
        if len(self.ppi) > 1:
            avg_ppi = int(sum(self.ppi) / len(self.ppi))
            
        return avg.ppi


    def calculate_bpm(self, ppi, sample_rate=250, min_hr=30, max_hr=200):
        heart_rate = 60 / (ppi / 1000)  # Convert milliseconds to seconds, then calculate heart rate
        if min_hr <= heart_rate <= max_hr:
            #print(heart_rate)
            self.hr.add(heart_rate)  # Collect heart rates that meet the range conditions
        
        if not self.hr:  # If 'hr' is empty, there's no valid heart rate to calculate.
            return None  # Return None or an appropriate default value
        
        median_hr = self.hr.median()
        avg_hr = self.hr.average()
        print(self.hr.data)
        return int(avg_hr)  # Return the median heart rate
    
    
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
        
    
    def calculate_hrv_metrics(PPI_array):
        # Calculate Mean PPI
        sumPPI = sum(PPI_array)
        mean_PPI = round(sumPPI / len(PPI_array), 0)
        mean_PPI = int(mean_PPI)

        # Calculate Mean HR
        mean_HR = round(60 * 1000 / mean_PPI, 0)
        mean_HR = int(mean_HR)

        # Calculate RMSSD
        summary_RMSSD = sum((PPI_array[i + 1] - PPI_array[i])**2 for i in range(len(PPI_array) - 1))
        RMSSD = round((summary_RMSSD / (len(PPI_array) - 1))**(1/2), 0)
        RMSSD = int(RMSSD)

        # Calculate SDNN
        summary_SDNN = sum((ppi - mean_PPI) ** 2 for ppi in PPI_array)
        SDNN = round((summary_SDNN / (len(PPI_array) - 1))**(1/2), 0)
        SDNN = int(SDNN)

        # Return a dictionary with all metrics
        return {
            'mean_PPI': mean_PPI,
            'mean_HR': mean_HR,
            'RMSSD': RMSSD,
            'SDNN': SDNN
        }



class Encoder:
    def __init__(self, rot_a, rot_b, rot_c):
        self.a = Pin(rot_a, mode=Pin.IN, pull=Pin.PULL_UP)
        self.b = Pin(rot_b, mode=Pin.IN, pull=Pin.PULL_UP)
        self.c = Pin(rot_c, mode=Pin.IN, pull=Pin.PULL_UP)
        self.fifo = Fifo(30, typecode='i')  # milliseconds
        self.last_pressed_time = 0
        self.button_pressed = False
        self.turning = True
        self.a.irq(handler=self.handler, trigger=Pin.IRQ_RISING, hard=True)
        self.c.irq(handler=self.button, trigger=Pin.IRQ_FALLING, hard=True)
        
    def handler(self, pin):
        if self.turning:
            if self.b.value():
                self.fifo.put(-1)  # Counter-clockwise rotation
            else:
                self.fifo.put(1)  # Clockwise rotation
            
    def button(self, pin):
        current_time = time.ticks_ms()
        if self.turning:
            if current_time - self.last_pressed_time < 200:
                return
            self.last_pressed_time = current_time
            
            self.fifo.put(0)
       
    

class Menu:
    def __init__(self, options, functions):
        self.options = options
        self.selected_index = 0
        self.functions = functions
    def select_next(self):
        self.selected_index = (self.selected_index + 1) % len(self.options)

    def select_prev(self):
        self.selected_index = (self.selected_index - 1) % len(self.options)

    def get_selected_option(self):
        return self.options[self.selected_index]

    def process_events(self):
        selected_function = self.functions[self.selected_index]
        print(f"Selected function: {selected_function.__name__}")  # Add this line


            
class Logger:
    def info(self):
        print("This is an BPM.")

    def warning(self):
        print("This is HRV.")

    def error(self):
        print("This is KUBIOS.")

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
    display.text("Welcome", 32, 10)
    display.text("Press SW1", 26, 20)
    display.text("to start", 30, 30)
    display.text("the measurement", 5, 40)
    display.show()
    
def measurement():
    display.text("Place your", 25, 15)
    display.text("finger on to ", 15, 25)
    display.text("the sensor", 25, 35)
    display.show()


def main_menu(user_state):
    menu_options = ["MEASURE HR", "HRV ANALYSIS", "KUBIOS"]
    functions = [peak_detector.detect_peaks, logger.warning, logger.error]
    menu = Menu(menu_options, functions)
    rot = Encoder(10, 11, 12)
    oled = init_display()

    while True:
        if user_state == "menu":
            update_display(oled, menu)  # Update the display to reflect current selection
            time.sleep_ms(100)
        
        while rot.fifo.has_data() and rot.turning:
            event = rot.fifo.get()
            if event == 1:  # Clockwise rotation
                menu.select_next()
                print("Selected option:", menu.get_selected_option())  # Add this line
            elif event == -1:  # Counter-clockwise rotation
                menu.select_prev()
                print("Selected option:", menu.get_selected_option())  # Add this line
            elif event == 0:  # Button press
                print("Button pressed. Processing event...")  # Add this line
                selected = menu.get_selected_option()  # Ensure this is running without issues
                if selected == menu_options[0]:
                    rot.turning = False
                    display.fill(0)
                    measurement()
                    time.sleep_ms(300)
                    display.fill(0)
                    peak_detector.data.measuring = True
                    user_state = "measuring"
                    
        peaks = peak_detector.detect_peaks()
        if SW1() == 0:
            peak_detector.data.measuring = False
            rot.turning = True
            user_state = "menu"


logger = Logger()

sample_rate = 250 
sampling_interval = 1.0 / sample_rate
peak_detector = PeakDetector(sample_rate=250, sample_threshold=250)

led = Signal(Pin("LED", Pin.OUT), invert=True)
i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
display = SSD1306_I2C(128, 64, i2c)

SW0 = Pin(9, Pin.IN, Pin.PULL_UP)
SW1 = Pin(8, Pin.IN, Pin.PULL_UP)

user_state = "starting_page"
while True:
    if user_state == "starting_page":
        start()
        if SW1() == 0:
            print("pressed")
            user_state = "menu"
            display.fill(0)
            if user_state == "menu":
                main_menu(user_state)
                    

