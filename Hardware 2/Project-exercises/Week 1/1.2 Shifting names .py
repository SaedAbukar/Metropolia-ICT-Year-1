import time
from machine import UART, Pin, I2C, Timer, ADC
from ssd1306 import SSD1306_I2C

button0 = Pin(9, Pin.IN, Pin.PULL_UP)
button1 = Pin(8, Pin.IN, Pin.PULL_UP)
i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled_width = 128
oled_height = 64
oled = SSD1306_I2C(oled_width, oled_height, i2c)

# Menu variables
item_line_y = 0
line_height = 8  # Height of each line of text on the screen
rect_height_y = oled_height - 1 - line_height
scroll_height = 0 - line_height
rect_height_x = 0
black_colour = 0
white_colour = 1


while True:
    # Get user input
    user_input = input("Enter something (type 'quit' to exit): ")
    # Display the subset of items on the screen
    if user_input != '':
        oled.text('%s' % user_input, rect_height_x, item_line_y, white_colour)
    
    item_line_y += 8
    if item_line_y > oled_height and user_input != '':
        oled.scroll(0, scroll_height)
        oled.fill_rect(0, rect_height_y, oled_width, oled_height - 1, black_colour)
        oled.text('%s' % user_input, rect_height_x, rect_height_y, white_colour)
    oled.show()

    # Process user input
    if user_input.lower() == 'quit':  # Check if user wants to quit
        break
