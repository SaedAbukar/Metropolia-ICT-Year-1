import time
from machine import UART, Pin, I2C, Timer, ADC
from ssd1306 import SSD1306_I2C
import framebuf

button0 = Pin(9, Pin.IN, Pin.PULL_UP) # Button up
button1 = Pin(8, Pin.IN, Pin.PULL_UP) # Restart
button2 = Pin(7, Pin.IN, Pin.PULL_UP) # Button down
i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled_width = 128
oled_height = 64
oled = SSD1306_I2C(oled_width, oled_height, i2c)

x = 0
y = int(oled_height / 2)
colour = 1
while True:
    oled.pixel(x, y, colour)
    oled.show()
    x += 1
    # Draw down
    if button0() == 0:
       y += 1
       if y >= oled_height:
           y = oled_height - 1
    # Draw up
    if button2() == 0:
       y -= 1
       if y <= int(oled_height - oled_height):
           y = 1
    if button1() == 0:
        oled.fill(0)
        x = 0
        y = int(oled_height / 2)
    if x >= oled_width-1:
        x = 0
        