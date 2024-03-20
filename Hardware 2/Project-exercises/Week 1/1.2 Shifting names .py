import time
from machine import UART, Pin, I2C, Timer, ADC
from ssd1306 import SSD1306_I2C

button0 = Pin(9, Pin.IN, Pin.PULL_UP)
button1 = Pin(8, Pin.IN, Pin.PULL_UP)
i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled_width = 128
oled_height = 64
oled = SSD1306_I2C(oled_width, oled_height, i2c)

# Global variables
line = 1  # Current line number
shift = 0  # Shift value for displaying menu items
list_length = []  # List to store menu items
max_lines = 8  # Total number of lines to display on the screen
# Menu variables
item = 1  # Counter for menu items
line_height = 8  # Height of each line of text on the screen


while True:
    # Clear the display
    oled.fill(0)

    # Calculate the starting index for displaying items
    start_index = max(0, len(list_length) - max_lines)

    # Get the subset of items to display on the screen
    items_to_display = list_length[start_index:]

    # Display the subset of items on the screen
    for i, item in enumerate(items_to_display):
        oled.text(item, 1, i * line_height)  # Display menu item

    oled.show()

    # Get user input
    user_input = input("Enter something (type 'quit' to exit): ")

    # Process user input
    if user_input.lower() == 'quit':  # Check if user wants to quit
        break
    elif user_input:  # Check if user input is not empty
        list_length.append(user_input)  # Append user input to the list

