import network
from time import sleep
from umqtt.simple import MQTTClient
from filefifo import Filefifo
from fifo import Fifo
from ssd1306 import SSD1306_I2C
from machine import Pin, I2C, ADC, Signal
from piotimer import Piotimer
import micropython
from time import sleep
import time
import utime
import mip
import urequests as requests
import ujson
import network
from umqtt.simple import MQTTClient

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
        self.ppi = []
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
        global user_state
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
                if len(self.peaks) > 10 and user_state == "bpm":
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
                
            if len(self.peaks) == 20 and user_state == "hrv":
                if not self.hrv_calculated:
                    print("working")
                    ppi = peak_detector.calculate_ppi(self.peaks)
                    self.calculate_hrv(ppi)
                    self.hrv_calculated = True
            if len(self.peaks) == 30 and user_state == "kubios":
                if not self.hrv_calculated:
                    ppi = peak_detector.calculate_ppi(self.peaks)
                    self.kubios_data(ppi)
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
        avg_ppi = 0
        for i in range(1, len(self.peaks)):
            self.interval = (self.peaks[i] - self.peaks[i - 1]) * self.sampling_interval_ms
            if min_ppi < self.interval < max_ppi:
                self.ppi.append(self.interval)
        
        if len(self.ppi) > 1:
            avg_ppi = int(sum(self.ppi) / len(self.ppi))
            
        return self.ppi

    
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
    
    
    def ppg_signal(self, val, maximum, minimum):
        last_y = 0
        

        display.vline(0, 0, 64, 0)

        display.scroll(-1, 0)  

        if maximum - minimum > 0:
            y = 64 - int(32 * (val - minimum) / (maximum - minimum))
            display.line(125, last_y, 126, y, 1)
            last_y = y
        display.show()

    
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
        
            
    # Function to calculate HRV metrics with Kubios for SNS & PNS
    def calculate_hrv(self, ppi):
        # Timestamp
        timestamp = utime.time()
        time_tuple = utime.localtime(timestamp)
        iso_format = "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(*time_tuple)


        # Mean PPI
        mean_ppi = sum(ppi) / len(ppi)
        # Mean HR
        mean_hr = round(60 * 1000 / mean_ppi, 2)
            
        # RMSSD calculation
        sum_diff_sq = 0
        for i in range(len(ppi) - 1):
            diff = ppi[i + 1] - ppi[i]
            diff_sq = diff ** 2         
            sum_diff_sq += diff_sq      

        rmssd = (sum_diff_sq / (len(ppi) - 1)) ** 0.5

        # SDNN calculation
        sdnn = 0
        for x in ppi:
            diff = x - mean_ppi          
            diff_sq = diff ** 2          
            sdnn += diff_sq              
        sdnn /= len(ppi)                
        sdnn = sdnn ** 0.5
        
        
        # Print or return the HRV metrics
        print("Mean PPI:", mean_ppi)
        print("Mean HR:", mean_hr)
        print("RMSSD:", rmssd)
        print("SDNN:", sdnn)
        display.fill(0)
        display.text("Mean PPI: %d" % mean_ppi, 0, 0)
        display.text("Mean HR: %d" % mean_hr, 0, 10)
        display.text("RMSSD: %d" % rmssd, 0, 20)
        display.text("SDNN: %d" % sdnn, 0, 30)
        display.text("Timestamp: %s" % iso_format, 0, 40)
        display.show()
        self.data.measuring = False

        
        try:
            
            mqtt_client=connect_mqtt()
        
        except Exception as e:
            print(f"Failed to connect to MQTT: {e}")

        # Send MQTT message
        try:

            # Sending a message every 5 seconds.
            topic = "pico/test"
            measurement = {
                "mean_hr": mean_hr,
                "mean_ppi": mean_ppi,
                "rmssd": rmssd,
                "sdnn": sdnn,
                "timestamp": iso_format
                }
            json_message = ujson.dumps(measurement)
            store_measurement(json_message)
            print("The data has been stored to the measurements.txt file.")
            
            mqtt_client.publish(topic, json_message)
            print(f"Sending to MQTT: {topic} -> {json_message}")
            
            
        
                
        except Exception as e:
            print(f"Failed to send MQTT message: {e}")
            
        
        
        
    # Function to calculate HRV metrics with Kubios for SNS & PNS
    def kubios_data(self, ppi):
        self.data.measuring = False
        try:
            response = requests.post(
                url = TOKEN_URL,
                data = 'grant_type=client_credentials&client_id={}'.format(CLIENT_ID),
                headers = {'Content-Type':'application/x-www-form-urlencoded'},
                auth = (CLIENT_ID, CLIENT_SECRET))

            response = response.json() #Parse JSON response into a python dictionary
            access_token = response["access_token"] #Parse access token

            intervals = ppi
            print(intervals)
            
            # Dictionary to be sent to Kubios
            dataset = {
                "type": "RRI",
                "data": intervals,
                "analysis": {"type": "readiness"}
                }

            
            response = requests.post(
                url = "https://analysis.kubioscloud.com/v2/analytics/analyze",
                headers = { "Authorization": "Bearer {}".format(access_token), 
                "X-Api-Key": APIKEY},
                json = dataset)

            response = response.json()
            print("API Response:", response)
            
            if 'error' in response:
                print("Error in API response:", response['error'])
                # Put this on OLED if it works
                print("ERROR SENDING DATA")
                print("PRESS THE SW0 BUTTON TO RETRY")
                print("OR WAIT 3 SECONDS TO RETURN TO MAIN MENU")
                if SW0() == 0:
                    rot.active = False
                    peak_detector.data.measuring = False
                    peaks = peak_detector.detect_peaks()
                else:
                    time.sleep(3)
            
            sns = round(response['analysis']['sns_index'], 2)
            pns = round(response['analysis']['pns_index'], 2)
            timestamp_str = response['analysis']['create_timestamp']
            # Directly extract components from the timestamp string
            year = int(timestamp_str[0:4])
            month = int(timestamp_str[5:7])
            day = int(timestamp_str[8:10])
            hour = int(timestamp_str[11:13])
            minute = int(timestamp_str[14:16])
            second = int(timestamp_str[17:19])

            # Create the time tuple
            time_tuple = (year, month, day, hour, minute, second, 0, 0, 0)

            # Get epoch time from the time tuple
            epoch_time = utime.mktime(time_tuple)

            print("Epoch time:", epoch_time)

            # Recreate ISO 8601 format if needed
            iso_format = "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(year, month, day, hour, minute, second)
            print("Reformatted ISO 8601 date:", iso_format)
            
            
        except KeyboardInterrupt:
                    machine.reset()

        # Mean PPI
        mean_ppi = sum(ppi) / len(ppi)
        # Mean HR
        mean_hr = round(60 * 1000 / mean_ppi, 2)
            
        # RMSSD calculation
        sum_diff_sq = 0
        for i in range(len(ppi) - 1):
            diff = ppi[i + 1] - ppi[i]
            diff_sq = diff ** 2         
            sum_diff_sq += diff_sq      

        rmssd = (sum_diff_sq / (len(ppi) - 1)) ** 0.5

        # SDNN calculation
        sdnn = 0
        for x in ppi:
            diff = x - mean_ppi          
            diff_sq = diff ** 2          
            sdnn += diff_sq              
        sdnn /= len(ppi)                
        sdnn = sdnn ** 0.5              
        
        # Print or return the HRV metrics
        print("Mean PPI:", mean_ppi)
        print("Mean HR:", mean_hr)
        print("RMSSD:", rmssd)
        print("SDNN:", sdnn)
        print("SNS:", sns)
        print("PNs:", pns)
        display.fill(0)
        display.text("Mean PPI: %d" % mean_ppi, 0, 0)
        display.text("Mean HR: %d" % mean_hr, 0, 8)
        display.text("RMSSD: %d" % rmssd, 0, 18)
        display.text("SDNN: %d" % sdnn, 0, 28)
        display.text("SNS: %d" % sns, 0, 38)
        display.text("PNS: %d" % pns, 0, 48)
        display.text("Timestamp: %s" % iso_format, 0, 58)
        display.show()
        
        measurement = {
                "mean_hr": mean_hr,
                "mean_ppi": mean_ppi,
                "rmssd": rmssd,
                "sdnn": sdnn,
                "sns": sns,
                "pns": pns,
                "timestamp": iso_format
                }
        
        json_message = ujson.dumps(measurement)
        store_measurement(json_message)
        print("The data has been stored to the measurements.txt file.")



            
        
class Encoder:
    def __init__(self, rot_a, rot_b, rot_c):
        self.a = Pin(rot_a, mode=Pin.IN, pull=Pin.PULL_UP)
        self.b = Pin(rot_b, mode=Pin.IN, pull=Pin.PULL_UP)
        self.c = Pin(rot_c, mode=Pin.IN, pull=Pin.PULL_UP)
        self.fifo = Fifo(30, typecode='i')  # milliseconds
        self.last_pressed_time = 0
        self.button_pressed = False
        self.active = False
        self.a.irq(handler=self.handler, trigger=Pin.IRQ_RISING, hard=True)
        self.c.irq(handler=self.button, trigger=Pin.IRQ_FALLING, hard=True)
        
    def handler(self, pin):
        if self.active:
            if self.b.value():
                self.fifo.put(-1)  # Counter-clockwise rotation
            else:
                self.fifo.put(1)  # Clockwise rotation
            
    def button(self, pin):
        if self.active:
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
    
    def update_options(self, new_options):
        self.options = new_options
    
    def update_functions(self, new_functions):
        self.functions = new_functions

    
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
    
def history_empty():
    display.text("No history", 25, 5)
    display.text("available ", 30, 15)
    display.text("Select Kubios", 15, 25)
    display.text("and follow", 25, 35)
    display.text("the instructions", 0, 45)
    display.show()
    
def kubios_waiting():
    display.text("Sending", 30, 15)
    display.text("data to ", 30, 25)
    display.text("the Kubios", 20, 35)
    display.text("please wait...", 10, 45)
    display.show()
    
#------------------------------------------------------------------------------------------------------------#
                                # History - reading the data from text file

# Append the measures to the measurements.txt file on pico board
def store_measurement(measurement):
    with open("measurements.txt", "a") as file:
        file.write(measurement + "\n")
        
        
# Store the measurements from the text file to the measurements list
def read_measurements():
    measurements = []
    file_path = "measurements.txt"
    
    try:
        with open(file_path, "r") as file:
            for line in file:
                try:
                    measurement = ujson.loads(line.strip())
                    measurements.append(measurement)
                except Exception as e:
                    # Log the error or raise an exception
                    print(f"Error parsing line: {line.strip()}. Skipping.")
    except Exception as e:
        # Log the error or raise an exception
        print(f"Error reading file: {e}")
    
    return measurements



# Displaying the data after selected the specific measurement option from history
def display_measurement_data(oled, measurement, options, functions):
    global user_state
    global SW0
    global rot
    oled.fill(0)
    user_state = "history_data"
    
    while True:
        # Dictionary mapping field names to display names
        field_display_names = {
            'timestamp': 'timestamp',
            'mean_hr': 'Mean HR',
            'mean_ppi': 'Mean PPI',
            'rmssd': 'RMSSD',
            'sdnn': 'SDNN',
            'sns': 'SNS',
            'pns': 'PNS',
            
        }
        
        # Iterate over each field and display its value if available
        for i, (field, display_name) in enumerate(field_display_names.items()):
            field_value = measurement.get(field, 'N/A')  # Get the field value or 'N/A' if not available
            if isinstance(field_value, (int, float)):
                field_value = round(field_value, 2)  # Round numerical values for display
            oled.text(f"{display_name}: {field_value}", 0, 0 + i * 9)
        
        oled.show()
        
        
        # Check wether the code goes back or not when pressing sw0
        if SW0() == 0 and user_state == "history_data":
            print("aaaa")
            rot.active = True
            user_state == "history"
            updated_options = menu.update_options(options)
            update_functions = menu.update_functions(functions)
            print("back")
            display.fill(0)
            break
        
    
    
    
def create_display_function(oled, measurement, options, functions):
    return lambda: display_measurement_data(oled, measurement, options, functions)
 

#------------------------------------------------------------------------------------------------------------#

                                    # Functions logic

def HR_logic():
    global user_state
    global SW0
    global rot
    display.fill(0)
    measurement()
    time.sleep_ms(300)
    display.fill(0)
    user_state = "bpm"
    while True:
        rot.active = False
        peak_detector.data.measuring = True
        peaks = peak_detector.detect_peaks()
        if SW0() == 0:
            rot.active = True
            peak_detector.data.measuring = False
            peak_detector.peaks.clear()
            peak_detector.ppi.clear()
            print("back")
            user_state == "menu"
            display.fill(0)
            break
        
        
                    

def test_HRV():
    global user_state
    global SW0
    global rot
    display.fill(0)
    measurement()
    time.sleep_ms(300)
    display.fill(0)
    user_state = "hrv"
    while True:
        rot.active = False
        peak_detector.data.measuring = True
        peaks = peak_detector.detect_peaks()
        if SW0() == 0:
            rot.active = True
            peak_detector.hrv_calculated = False
            peak_detector.data.measuring = False
            peak_detector.peaks.clear()
            peak_detector.ppi.clear()
            print("back")
            user_state == "menu"
            display.fill(0)
            break
        
        
def history_logic():
    global user_state
    global SW0
    global rot
    global oled
    user_state = "history"
    
    
    if SW0 == 0 and user_state == "history_data":
        rot.active = True
        user_state == "history"
        updated_options = menu.update_options(measurement_options)
        update_functions = menu.update_functions(measurement_data)
        print("back")
        display.fill(0)
    
    if SW0 == 0:
        rot.active = True
        user_state == "menu"
        updated_options = menu.update_options(menu_options)
        update_functions = menu.update_functions(functions)
        print("back")
        display.fill(0)
    
    measurements = read_measurements()
    
    measurement_options = []
    for i in range(len(measurements)):
        option = f"Measurement {i+1}"
        measurement_options.append(option)
     

    measurement_data = []
    for i in range(len(measurements)): 
        data = create_display_function(oled, measurements[i], measurement_options, measurement_data)
        measurement_data.append(data)
         
    updated_options = menu.update_options(measurement_options)
    update_functions = menu.update_functions(measurement_data)

        

def kubious_logic():
    global user_state
    global SW0
    global rot
    display.fill(0)
    kubios_waiting()
    time.sleep_ms(300)
    display.fill(0)
    user_state = "kubios"
    while True:
        rot.active = False
        peak_detector.data.measuring = True
        peaks = peak_detector.detect_peaks()
        if SW0() == 0:
            rot.active = True
            peak_detector.hrv_calculated = False
            peak_detector.data.measuring = False
            peak_detector.peaks.clear()
            peak_detector.ppi.clear()
            print("back")
            user_state == "menu"
            display.fill(0)
            break
        
#------------------------------------------------------------------------------------------------------------#
                                # MQTT functions
                                
def connect_wlan():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)

    # Attempt to connect once per second
    while wlan.isconnected() == False:
        print("Connecting... ")
        sleep(1)

    print("Connection successful. Pico IP:", wlan.ifconfig()[0])
    
def connect_mqtt():
    mqtt_client = MQTTClient("", MQTT_IP)
    mqtt_client.connect(clean_session=True)
    return mqtt_client

    
    
sample_rate = 250 
sampling_interval = 1.0 / sample_rate
peak_detector = PeakDetector(sample_rate=250, sample_threshold=250)
user_state = "start"
led = Signal(Pin("LED", Pin.OUT), invert=True)
i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
display = SSD1306_I2C(128, 64, i2c)
SW0 = Pin(9, Pin.IN, Pin.PULL_UP)
SW1 = Pin(8, Pin.IN, Pin.PULL_UP)
rot = Encoder(10, 11, 12)
menu_options = ["Measure HR", "HRV", "History", "Kubious"]
functions = [HR_logic, test_HRV, history_logic, kubious_logic] 
menu = Menu(menu_options, functions)
oled = init_display()

# SSID credentials (wifi)
SSID = 'KMD_757_Group_6'
PASSWORD = 'KoSaVi_Ankkalinna'
MQTT_IP = '192.168.6.253'
MQTT_TOPIC = 'pico/test'

# Kubios credentials
APIKEY = "pbZRUi49X48I56oL1Lq8y8NDjq6rPfzX3AQeNo3a"
CLIENT_ID = "3pjgjdmamlj759te85icf0lucv"
CLIENT_SECRET = "111fqsli1eo7mejcrlffbklvftcnfl4keoadrdv1o45vt9pndlef"

LOGIN_URL = "https://kubioscloud.auth.eu-west-1.amazoncognito.com/login"
TOKEN_URL = "https://kubioscloud.auth.eu-west-1.amazoncognito.com/oauth2/token"
REDIRECT_URI = "https://analysis.kubioscloud.com/v1/portal/login"




def main():
    global peak_detector
    global menu_options
    global functions
    global menu
    global user_state
    global rot
    
    oled = init_display()
    
    connect_wlan()
    
    while True:
        if user_state == "start":
            start()
            
        if SW0() == 0 and user_state == "start":
            rot.active = True
            user_state = "menu"
            
        if SW0() == 0 and user_state == "bpm":
            user_state = "menu"
        
        if SW0() == 0 and user_state == "hrv":
            user_state = "menu"
            
        if SW0() == 0 and user_state == "history":
            rot.active = True
            menu.update_options(menu_options)
            menu.update_functions(functions)
            user_state = "menu"
            
            
        if SW0() == 0 and user_state == "kubios":
            user_state = "menu"
        
        if SW0() == 0 and user_state == "history_data":
            rot.active = True
            menu.update_options(menu_options)
            menu.update_functions(functions)
            user_state = "history"
            
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


