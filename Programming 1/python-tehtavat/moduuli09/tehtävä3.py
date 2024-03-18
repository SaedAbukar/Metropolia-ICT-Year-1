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
            self.current_speed += change_of_speed
        if self.current_speed < 0:
            self.current_speed = 0
        else:
            self.current_speed = new_speed
        if self.current_speed > 0:
            print(f'The car accelerates to {self.current_speed} km/h')
        else:
            print(f'The car decelerates to {self.current_speed} km/h')

    def move(self, hour):
        new_distance = self.distance_traveled + (self.current_speed * hour)
        if hour > 1:
            print(f'Current traveled distance is {self.distance_traveled}km. Current speed is {self.current_speed}km/h. Hour elapsed is {hour} hours. The car traveled to {new_distance}km')
        else:
            print(f'Current traveled distance is {self.distance_traveled}km. Current speed is {self.current_speed}km/h. Hour elapsed is {hour} hour. The car traveled to {new_distance}km')

new_car = CAR("ABC-123", 142, 60, 2000)
new_car.move(1.5)
