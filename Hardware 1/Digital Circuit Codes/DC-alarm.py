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


class AlarmSystem:
    def __init__(self):
        self.lamp = Led(22)
        self.siren = Led(20)
        self.button = Button(7)
        self.alarm_button = Button(9)
        self.alarm = False
        self.state = self.run

    def execute(self):
        self.state()

    def toggle_alarm(self):
        print("Alarm toggled")
        self.alarm = not self.alarm

    def run(self):
        self.lamp.off()
        self.siren.off()
        if self.alarm_button.pressed():
            self.toggle_alarm()
        if self.alarm:
            self.state = self.arm

    def arm(self):
        self.lamp.on()
        self.siren.on()
        if self.alarm_button.pressed():
            self.toggle_alarm()
        if self.button.pressed():
            print("Button pressed")
            if not self.alarm:
                self.state = self.run
            else:
                self.state = self.lamp2
        else:
            if not self.alarm:
                self.state = self.lamp1

    def lamp1(self):
        self.siren.off()
        if self.alarm_button.pressed():
            self.toggle_alarm()
        if self.button.pressed():
            print("Button pressed")
            self.lamp.off()
            self.state = self.run

    def lamp2(self):
        self.siren.off()
        self.lamp.on()
        if self.alarm_button.pressed():
            self.toggle_alarm()
        self.state = self.off

    def off(self):
        self.lamp.off()
        if self.alarm_button.pressed():
            self.toggle_alarm()
        if self.alarm:
            self.state = self.lamp2
        else:
            self.state = self.run


if __name__ == "__main__":
    asys = AlarmSystem()
    while True:
        asys.execute()
        utime.sleep_ms(50)
