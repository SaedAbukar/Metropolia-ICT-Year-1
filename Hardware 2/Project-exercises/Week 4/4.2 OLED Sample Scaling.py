from filefifo import Filefifo
from ssd1306 import SSD1306_I2C
from machine import Pin, I2C
import micropython
micropython.alloc_emergency_exception_buf(200)

# Constants
SAMPLE_RATE = 250  # Sampling rate in Hz
SCREEN_WIDTH = 128
SCREEN_HEIGHT = 64
MAX_SAMPLES_PER_PLOT = 5  # Average of five successive samples per pixel

def scale_value(value, min_val, max_val):
    scaled_value = (value - min_val) / (max_val - min_val) * (SCREEN_HEIGHT - 1)
    return max(0, min(int(scaled_value), SCREEN_HEIGHT - 1))

def show_signal(data):
    oled.fill(0)  # Clear the OLED display
    min_val, max_val = None, None

    for i in range(0, len(data), MAX_SAMPLES_PER_PLOT):
        chunk = data[i:i+MAX_SAMPLES_PER_PLOT]
        if not chunk:
            break

        chunk_min = min(chunk)
        chunk_max = max(chunk)
        
        if min_val is None or chunk_min < min_val:
            min_val = chunk_min
        if max_val is None or chunk_max > max_val:
            max_val = chunk_max

        scaled_chunk = [scale_value(val, min_val, max_val) for val in chunk]

        for j, val in enumerate(scaled_chunk):
            oled.pixel(i // MAX_SAMPLES_PER_PLOT, SCREEN_HEIGHT - 1 - val, 1)

    oled.show()

# Initialize OLED display
i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled = SSD1306_I2C(SCREEN_WIDTH, SCREEN_HEIGHT, i2c)

# Initialize data stream
data = Filefifo(10, name='capture02_250Hz.txt')

# Main loop
while True:
    samples = [data.get() for _ in range(SAMPLE_RATE)]  # Read 1 second of data
    show_signal(samples)
