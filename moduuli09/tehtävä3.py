# Expand the program so that there is a go method that takes the number of hours as a parameter.The method increases
# the traveled distance as much as the car has moved at a constant speed in the given number of hours.
# Example: the current traveled distance of the car is 2000 km.
# The speed is 60 km/h. The method call car.go(1.5) increases the traveled distance to 2090 km.

class CAR:
    def __init__(self, license_plate, top_speed, current_speed, distance_traveled):
        self.license_plate = license_plate
        self.top_speed = top_speed
        self.current_speed = current_speed
        self.distance_traveled = distance_traveled

    def accelerate(self, change_of_speed):
        new_speed = self.current_speed + change_of_speed
        if self.current_speed > self.top_speed:
            self.current_speed = self.top_speed
        if change_of_speed < 0:
            self.current_speed = 0
        else:
            self.current_speed = new_speed

    def go(self, hours):
        new_distance = self.current_speed * hours
        self.distance_traveled += new_distance

new_car = CAR('ABC-123', 142, 60, 2000)
new_car.go(1.5)
print(f'The car traveled {new_car.distance_traveled:.0f} kilometers')
