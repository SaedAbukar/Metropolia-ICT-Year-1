import time
from machine import UART, Pin, I2C, Timer, ADC
from ssd1306 import SSD1306_I2C
import framebuf

button0 = Pin(9, Pin.IN, Pin.PULL_UP)
button1 = Pin(8, Pin.IN, Pin.PULL_UP)
i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled_width = 128
oled_height = 64
oled = SSD1306_I2C(oled_width, oled_height, i2c)

# Define the symbol '<=>' as a series of bytes
symbol_bytes = bytearray([0x00, 0x24, 0x42, 0xBD, 0x42, 0x24, 0x00, 0x00])

# Create a framebuffer object
fb = framebuf.FrameBuffer(symbol_bytes, 8, 8, framebuf.MONO_HLSB)

x = int((oled_width - 8) / 2)  # Center the symbol horizontally
y = oled_height - 8  # Position the symbol at the bottom of the screen

while True:
    if button0() == 0:
        print('Going to the right')
        print("%d x" % x)
        x += 5
        if x >= int(oled_width - 8):
            x = int(oled_width - 8)
            print('Hit the right wall')
            print("%d x" % x)
    if button1() == 0:
        print('Going to the left')
        print("%d x" % x)
        x -= 5
        if x <= int(oled_width-oled_width):
            x = int(oled_width-oled_width)
            print('Hit the left wall')
            print("%d x" % x)

    oled.fill(0)  # Clear the display
    oled.blit(fb, x, y)  # Blit the symbol onto the display at the updated position
    oled.show()  # Update the display
