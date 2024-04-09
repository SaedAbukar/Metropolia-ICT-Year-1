from machine import Pin, PWM, UART, Pin, I2C, Timer, ADC
from ssd1306 import SSD1306_I2C
from fifo import Fifo
import time
import micropython
micropython.alloc_emergency_exception_buf(200)

class PWMLED:
    def __init__(self, pin, frequency=1000):
        self.led = PWM(Pin(pin, Pin.OUT))
        self.led.freq(frequency)
        self.brightness = 0
        self.set_brightness(self.brightness)
        self.is_on = False

    def set_brightness(self, brightness):
        brightness = max(0, min(10000, brightness))  # Clamp brightness to 0-10000
        self.brightness = brightness
        duty = int((brightness / 10000) * 65535)
        self.led.duty_u16(duty)
       
    def increase_brightness(self, amount=100):
        if self.is_on:
            new_brightness = self.brightness + amount
            self.set_brightness(new_brightness)

    def decrease_brightness(self, amount=100):
        if self.is_on:
            new_brightness = self.brightness - amount
            self.set_brightness(new_brightness)

    def toggle(self):
        if self.is_on:
            self.off()
        else:
            self.on()

    def on(self):
        self.brightness = 50
        self.set_brightness(self.brightness)
        self.is_on = True

    def off(self):
        self.set_brightness(0)
        self.is_on = False

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

pin_numbers = [22, 21, 20]
leds = [PWMLED(pin) for pin in pin_numbers]

led_list = ["LED1", "LED2", "LED3"]


i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled_width = 128
oled_height = 64
oled = SSD1306_I2C(oled_width, oled_height, i2c)


line_height = 10


current_line = 2
current_item = 1
prev_item = current_item - 1
next_item = current_item + 1


def display_menu():
    oled.fill(0)
    for i in range(len(led_list)):
        if leds[i].is_on:
            state = "ON"
        else:
            state = "OFF"
        if i == current_line:
            oled.text("<" + led_list[i] + "-" + state + ">", 0, i * line_height)
        else:
            oled.text(" " + led_list[i] + "-" + state, 0, i * line_height)
            
    
    oled.show()


while True:
    display_menu()
    if rot.fifo.has_data():
        value = rot.fifo.get()

        if value == 1:
            current_line += 1
            if current_line >= len(led_list):
                current_line = 0
        if value == -1:
            current_line -= 1
            if current_line < 0:
                current_line = len(led_list) - 1
        if value == 0:
            leds[current_line].toggle()
            