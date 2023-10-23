# Continue the program by writing the accelerate method in the Auto class,
# which receives the speed change (km/h) as a parameter.
# If the change in speed is negative, the car slows down.
# The method must change the value of the car object's speed property.
# The car's speed must not increase above the top speed or decrease below zero.
# Continue the main program so that the car's speed is first increased to +30 km/h, then +70 km/h and finally +50 km/h.
# After that, print the speed of the car.
# Then perform emergency braking by specifying a speed change of -200 km/h and print the new speed.
# The traveled distance does not need to be updated yet.

class CAR:
    def __init__(self, license_plate, top_speed, current_speed, distance_traveled=0):
        self.license_plate = license_plate
        self.top_speed = top_speed
        self.current_speed = current_speed

    def accelerate(self, change_of_speed):
        new_speed = self.current_speed + change_of_speed
        if self.current_speed > self.top_speed:
            self.current_speed = self.top_speed
        if change_of_speed < 0:
            self.current_speed += change_of_speed
        if self.current_speed < 0:
            self.current_speed = 0
        else:
            self.current_speed = new_speed
        if self.current_speed > 0:
            print(f'The car accelerates to {self.current_speed} km/h')
        else:
            print(f'The car decelerates to {self.current_speed} km/h')


new_car = CAR('ABC-123', 142, 0)
new_car.accelerate(30)
new_car.accelerate(70)
new_car.accelerate(50)
print(f'The new cars current speed is {new_car.current_speed}.')

new_car.accelerate(-200)
print(f'The new car performed an emergency break. The new cars current speed is {new_car.current_speed}.')
