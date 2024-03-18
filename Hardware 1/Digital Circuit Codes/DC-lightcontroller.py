from machine import Pin, PWM
import utime


class Led:
    def __init__(self, pin_id):
        self.pwm = PWM(Pin(pin_id, Pin.OUT))
        self.pwm.freq(1000)

    def on(self):
        self.pwm.duty_u16(1000)

    def off(self):
        self.pwm.duty_u16(0)


class Button:
    def __init__(self, pin_id):
        self.button = Pin(pin_id, Pin.IN, Pin.PULL_UP)

    def pressed(self):
        if self.button.value() == 0:
            utime.sleep(0.05)
            if self.button.value() == 0:
                utime.sleep(0.05)
                return True


class LightController:
    def __init__(self):
        self.led = Led(20)
        self.button = Button(7)
        self.state = self.off

    def execute(self):
        self.state()

    def off(self):
        self.led.off()
        if self.button.pressed():
            print("Transitioning from OFF to ONW")
            self.state = self.onw

    def onw(self):
        self.led.on()
        if not self.button.pressed():
            print("Transitioning from ONW to ON")
            self.state = self.on

    def on(self):
        if self.button.pressed():
            print("Transitioning from ON to OFFW")
            self.led.off()
            self.state = self.offw

    def offw(self):
        if not self.button.pressed():
            print("Transitioning from OFFW to OFF")
            self.state = self.off


if __name__ == "__main__":
    l = LightController()
    while True:
        l.execute()
        utime.sleep_ms(50)
