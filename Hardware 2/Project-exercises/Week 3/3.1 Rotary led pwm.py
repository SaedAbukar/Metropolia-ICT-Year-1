from machine import Pin, PWM
from fifo import Fifo
import time

class PWMLED:
    def __init__(self, pin, frequency=1000):
        """
        Initialize the LED on a specific pin with PWM.
        
        :param pin: Pin number where the LED is connected.
        :param frequency: PWM frequency. Default is 1000Hz.
        """
        self.led = PWM(Pin(pin, Pin.OUT))
        self.led.freq(frequency)
        self.brightness = 0
        self.set_brightness(self.brightness)
        self.is_on = False

    def set_brightness(self, brightness):
        """
        Set the brightness of the LED.
        
        :param brightness: Brightness level (0-10000).
        """
        brightness = max(0, min(10000, brightness))  # Clamp brightness to 0-10000
        self.brightness = brightness
        duty = int((brightness / 10000) * 65535)
        self.led.duty_u16(duty)
       
    def increase_brightness(self, amount=100):
        """
        Increase the LED brightness by a specified amount.
        
        :param amount: Amount to increase the brightness by (default is 100).
        """
        new_brightness = self.brightness + amount
        self.set_brightness(new_brightness)

    def decrease_brightness(self, amount=100):
        """
        Decrease the LED brightness by a specified amount.
        
        :param amount: Amount to decrease the brightness by (default is 100).
        """
        new_brightness = self.brightness - amount
        self.set_brightness(new_brightness)

    def toggle(self):
        """
        Toggle the LED on/off.
        """
        if self.is_on:
            self.off()
        else:
            self.on()

    def on(self):
        """
        Turn on the LED.
        """
        self.set_brightness(self.brightness + 10)
        self.is_on = True

    def off(self):
        """
        Turn off the LED.
        """
        self.set_brightness(0)
        self.is_on = False

class Encoder:
    def __init__(self, rot_a, rot_b):
        self.a = Pin(rot_a, mode=Pin.IN, pull=Pin.PULL_UP)
        self.b = Pin(rot_b, mode=Pin.IN, pull=Pin.PULL_UP)
        self.last_pressed_time = 0
        self.fifo = Fifo(30, typecode='i')
        self.a.irq(handler=self.handler, trigger=Pin.IRQ_RISING, hard=True)

    def handler(self, pin):
        if self.b.value():
            self.fifo.put(-1)
        else:
            self.fifo.put(1)

class Button:
    def __init__(self, pin_number):
        """
        Initialize the button on a specific pin.
        
        :param pin_number: Pin number where the button is connected.
        """
        self.button = Pin(pin_number, Pin.IN, Pin.PULL_UP)
        self.last_pressed_time = 0

    def is_pressed(self):
        """
        Check if the button is pressed (with debouncing).
        
        :return: True if the button is pressed, False otherwise.
        """
        current_time = time.ticks_ms()
        if current_time - self.last_pressed_time < 200:  # Debounce time (200ms)
            return False
        if self.button.value() == 0:
            self.last_pressed_time = current_time
            return True
        return False

rot = Encoder(10, 11)
button = Button(12)
led = PWMLED(22)

while True:
    if button.is_pressed():
        led.toggle()

    if rot.fifo.has_data():
        value = rot.fifo.get()
        if value == 1:
            led.increase_brightness()
        elif value == -1:
            led.decrease_brightness()
