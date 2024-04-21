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
        self.samples = Fifo(1000) # fifo where ISR will put samples
        self.dbg = Pin(0, Pin.OUT) # debug GPIO pin for measuring timing with oscilloscope
        
    def handler(self, tid):
        self.samples.put(self.av.read_u16())
        self.dbg.toggle()


def min_and_max(data):
    
    maximum = minimum = data[0]
    
    for i in range(1, len(data)):
        if data[i] > maximum:
            maximum = data[i]
        if data[i] < minimum:
            minimum = data[i]
            
    return minimum, maximum
    

def detect_peaks(data, sample_rate=250):
    curr = data[0] #lpf1(data.get(), data.get())
    peaks = []
    minimum, maximum = min_and_max(data)
    sample = 0
    counting = False
    sampling_interval_ms = (1 / sample_rate) * 1000
    
    for i in range(1, len(data)):  # Assuming we've already processed one data point
        prev = curr
        curr = data[i]#lpf1(curr, data[i])  # Get the next data point
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
            
    return peaks, minimum, maximum

def lpf1(prev_value, new_value, alpha=0.85):
    return alpha * prev_value + (1 - alpha) * new_value

def lpf2(data, filtering_amount=4):
    lastvals = []
    filtered_range = []
    for value in data:
        if len(lastvals) < filtering_amount:
            lastvals.append(value)
        else:
            filtered_range.append(int((value + sum(lastvals)) / (filtering_amount)))
            lastvals.pop(0)
            lastvals.append(value)
    return filtered_range



def calculate_ppi_ms(peaks, sample_rate=250):
    
    ppi_ms = []
    sampling_interval_ms = (1 / sample_rate) * 1000  # Calculate sampling interval in milliseconds
    
    for i in range(1, len(peaks)):
        ppi_samples = peaks[i] - peaks[i - 1]
        ppi_ms.append(ppi_samples * sampling_interval_ms)  # Calculate PPI in milliseconds
        
    return ppi_ms


def calculate_hr(ppi_ms, min_hr=30, max_hr=200):
    
    hr = []
    
    for i in range(len(ppi_ms)):
        heart_rate = 60 / (ppi_ms[i] / 1000)  # Convert milliseconds back to seconds for heart rate calculation
        if min_hr <= heart_rate <= max_hr:
            return heart_rate
    
    current_hr = sum(hr) / len(hr)
    
    return current_hr

def show_hr(bpm, data, minimum, maximum):
    global last_y

    display.vline(0, 0, 64, 0)
    display.scroll(-1, 0)  # Scroll left 1 pixel

    if maximum - minimum > 0:
        # Draw beat line.
        y = 64 - int(32 * (data[-1] - minimum) / (maximum - minimum))
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


sensor = isr_adc(26)
tmr = Piotimer(freq = sample_rate, callback = sensor.handler)
count = 0
last_y = 0

while True:
    while sensor.samples.has_data():
        value = sensor.samples.get()
        count += 1
        
        if count % 1000 == 0:
            count = 0
            data = lpf2(sensor.samples.data)
#             print("raw_data", sensor.samples.data)
#             print("filtered_data", data)
            peaks, minimum, maximum = detect_peaks(data)
            print(peaks)
            if len(peaks) > 1:
                current_ppi = peaks[-1] - peaks[-2]  # Get the most recent PP interval in samples
                ppi_ms = calculate_ppi_ms(peaks)
                current_hr = calculate_hr(ppi_ms)  # Calculate heart rate in bpm using sample rate
                print("Current ppi:", ppi_ms[-1])
                print("Current Heart Rate:", current_hr)
                show_hr(current_hr, data, minimum, maximum)
        


