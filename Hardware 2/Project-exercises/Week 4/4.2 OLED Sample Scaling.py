from filefifo import Filefifo
from ssd1306 import SSD1306_I2C
from machine import Pin, I2C
import micropython
micropython.alloc_emergency_exception_buf(200)

def scale_data(data, min_val, max_val):
    scaled_data = ((data - min_val) / (max_val - min_val)) * 63
    return max(0, min(int(scaled_data), 63))


def plot_scaled_data_to_oled(data, sample_rate=250, max_samples_per_plot=5, screen_height=64):
    oled.fill(0)
    current = data.get()
    maximum = minimum = current
    sample = 0
    window = []
    scaled_window = []
    

    for i in range(sample_rate):
        current = data.get()  # Get the next data point
        
        if current > maximum:
            maximum = current
        elif current < minimum:
            minimum = current
        
        window.append(current)
        sample += 1
        
        if len(window) == max_samples_per_plot:
            scaled_window = [scale_data(val, minimum, maximum) for val in window]
            for i, val in enumerate(scaled_window):
                oled.pixel((sample + i) // max_samples_per_plot, int(screen_height - 1 - val), 1)
            
            
            window.clear()
            
    oled.show()
        

i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled_width = 128
oled_height = 64
oled = SSD1306_I2C(oled_width, oled_height, i2c)

# Initialize data stream
data = Filefifo(10, name='capture03_250Hz.txt')     

while True:
    plot_scaled_data_to_oled(data)

