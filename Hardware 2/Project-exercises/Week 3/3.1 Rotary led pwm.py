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

    def set_brightness(self, brightness):
    
        #:param brightness: Brightness level (0-10000)
        
        brightness = max(0, min(10000, brightness))  # Clamp brightness to 0-10000
        self.brightness = brightness
        duty = int((brightness / 10000) * 65535)
        self.led.duty_u16(duty)
       
    def increase_brightness(self, amount=100):

        #:param amount: Amount to increase the brightness by (default is 10).
        
        new_brightness = self.brightness + amount
        self.set_brightness(new_brightness)

    def decrease_brightness(self, amount=100):

        #:param amount: Amount to decrease the brightness by (default is 10).
        
        new_brightness = self.brightness - amount
        self.set_brightness(new_brightness)

    def on(self):
        self.set_brightness(self.brightness + 10)

    def off(self):
        self.set_brightness(0)

class Encoder:
    
    def __init__(self, rot_a, rot_b, rot_c):
        self.a = Pin(rot_a, mode = Pin.IN, pull = Pin.PULL_UP)
        self.b = Pin(rot_b, mode = Pin.IN, pull = Pin.PULL_UP)
        self.c = Pin(rot_c, mode = Pin.IN, pull = Pin.PULL_UP)
        self.pressed = False
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
        
        if self.pressed:
            self.fifo.put(3)
            self.pressed = False
        else:
            self.fifo.put(2)
            self.pressed = True

rot = Encoder(10, 11, 12)

led = PWMLED(22)

while True:
    if rot.fifo.has_data():
        value = rot.fifo.get()
        print(value)
        print(rot.pressed)
        if rot.pressed:
            led.on()
            if value == 1:
                led.increase_brightness()
            if value == -1:
                led.decrease_brightness()
        else:
            led.off()
