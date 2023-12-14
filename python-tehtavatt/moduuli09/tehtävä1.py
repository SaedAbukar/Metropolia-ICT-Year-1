# Write a Car class whose properties are license plate number, top speed, current speed, and distance traveled.
# Write an initializer in the class that sets the first two properties to the values received as parameters.
# The speed and distance traveled of the new car must be automatically set to zero.
# Write the main program to create a new car (registration code ABC-123, top speed 142 km/h).
# In the main program, print all the properties of the car created after that.

class CAR:
    def __init__(self, license_plate, top_speed, current_speed=0, distance_traveled=0):
        self.license_plate = license_plate
        self.top_speed = top_speed


new_car = CAR('ABC-123', 142)
print(f'The new cars license plate is {new_car.license_plate} and top speed is {new_car.top_speed} km/h.')
