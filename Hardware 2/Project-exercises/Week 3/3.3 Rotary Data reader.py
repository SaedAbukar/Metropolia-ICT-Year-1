from machine import Pin, I2C, Timer
from ssd1306 import SSD1306_I2C
from filefifo import Filefifo
from fifo import Fifo
import time
import micropython
micropython.alloc_emergency_exception_buf(200)

class Encoder:
    
    def __init__(self, rot_a, rot_b, rot_c):
        self.a = Pin(rot_a, mode = Pin.IN, pull = Pin.PULL_UP)
        self.b = Pin(rot_b, mode = Pin.IN, pull = Pin.PULL_UP)
        self.c = Pin(rot_c, mode = Pin.IN, pull = Pin.PULL_UP)
        self.pressed = True
        self.last_pressed_time = 0
        self.fifo = Fifo(30, typecode = 'i')
        self.a.irq(handler = self.handler, trigger = Pin.IRQ_RISING, hard = True)
        self.c.irq(handler = self.switch, trigger = Pin.IRQ_FALLING, hard = True)
        
    def handler(self, pin):
        if self.b():
            self.fifo.put(-1)
        else:
            self.fifo.put(1)
    
    def switch(self, pin):
        # Debouncing using time.ticks_ms()
        current_time = time.ticks_ms()
        if current_time - self.last_pressed_time < 200:  # Adjust debounce time as needed (200ms in this case)
            return
        self.last_pressed_time = current_time
        self.fifo.put(0)

rot = Encoder(10, 11, 12)


i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled_width = 128
oled_height = 64
oled = SSD1306_I2C(oled_width, oled_height, i2c)


data = Filefifo(10, name='capture_250Hz_03.txt')
current = data.get()
samples = []



def scale_data(data, min_val, max_val):
    scaled_data = ((data - min_val) / (max_val - min_val)) * (oled_height - 1)
    return scaled_data

# Iterate through the data stream
def get_samples():
    current = data.get()
    maximum = minimum = current
    for i in range(1000):  # Assuming we've already processed one data point
        current = data.get()  # Get the next data point
        if current > maximum:
            maximum = current
        elif current < minimum:
            minimum = current
    return minimum, maximum

minimum, maximum = get_samples()

for i in range(1000):
    current = data.get()
    scaled = int(scale_data(current, minimum, maximum))
    samples.append(scaled)
    

def show(samples, scroll_pos):
    oled.fill(0)
    for i in range(oled_width):
        index = i + scroll_pos
        if index < len(samples):
            oled.pixel(i, samples[index], 1)
        else:
            index = len(samples)
    oled.show()


scroll_pos = 0


while True:
    while rot.fifo.has_data():
        value = rot.fifo.get()
        if value == 1 and scroll_pos <= len(samples) - oled_width:
            scroll_pos += 9

        if value == -1 and scroll_pos > 0:
            scroll_pos -= 9
        
    show(samples, scroll_pos)
