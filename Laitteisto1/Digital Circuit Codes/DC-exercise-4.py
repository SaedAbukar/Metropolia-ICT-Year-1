from picozero import PWMLED
from utime import sleep
from machine import Pin

button = Pin(12, mode=Pin.IN, pull=Pin.PULL_UP)

led1 = PWMLED(22)
led2 = PWMLED(21)
led3 = PWMLED(20)

def update_led(button_pressed):
    led1.value = (button_pressed & 1) * 0.01  
    led2.value = ((button_pressed >> 1) & 1) * 0.01
    led3.value = ((button_pressed >> 2) & 1) * 0.01

button_pressed = 0

while True:
    if button.value() == 0:
        while button.value() == 0:
            pass  
        button_pressed += 1
        if button_pressed > 7:
            button_pressed = 0  
        print("Button pressed: ", button_pressed)
        print("Binary: ", "{:03b}".format(button_pressed))  
        update_led(button_pressed)
        sleep(0.2)  
