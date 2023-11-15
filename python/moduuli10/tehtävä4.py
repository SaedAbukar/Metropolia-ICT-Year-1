# The mission is a continuation of the previous car racing mission. Enter the Race class,
# which has the name of the race, the length in kilometers and the list of participating cars as properties.
# The class has an initializer that receives the name, mileage and car list as parameters
# and sets them as values for the properties. The class has the following methods:
# hour_elapses, which implements the hourly actions mentioned in the previous car racing task,
# i.e. draws a random number of changes in the speed of each car and calls the go method for each car.
# print_situation, which prints the current information of all cars in a clear table format.
# race_over, which returns True if one of the cars is at the finish line,
# i.e. it has driven at least the total number of kilometers of the race. Otherwise, False is returned.
# Write a main program that creates an 8000 km race called "The Great Scrap Rally".
# The race to be created is given a list of ten cars in the same way as in the previous task.
# The main program simulates the progress of the competition
# by calling the hour_elapses method in the repetition structure,
# after which it is always checked with the competition_over method whether the competition is over.
# The up-to-date situation is printed using the situation method every ten hours
# and once after the competition has ended.
import random


class Car:
    def __init__(self, license_plate, top_speed):
        self.license_plate = license_plate
        self.top_speed = top_speed
        self.current_speed = 0
        self.distance_traveled = 0

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

    def move(self, hour):
        new_distance = (self.current_speed * hour)
        self.distance_traveled += new_distance


class Race:
    def __init__(self, name, distance_km, car_list):
        self.name = name
        self.distance_km = distance_km
        self.cars = car_list

    def hour_elapses(self):
        for car in self.cars:
            car.accelerate(random.randint(-10, 15))
            car.move(1)

    def print_situation(self):
        print(f"{'Car':<15}{'Distance (km)':<15}{'Speed (km/h)':<15}")
        for car in self.cars:
            print(f'{car.license_plate:<15}{car.distance_traveled:<15.2f}{car.current_speed * 3.6:<15.2f}')

    def race_over(self):
        for car in self.cars:
            if car.distance_traveled >= self.distance_km:
                return True
        return False


cars = [Car(f'ABC{i}', random.randint(100, 200)) for i in range(1, 11)]

# for i in range(1, 11):
#     car = Car(f'ABC-{i}', random.randint(100,200))
#     cars.append(car)
#

race = Race(f'The Great Scrap Rally', 10000, cars)

hours = 0
while not race.race_over():
    race.hour_elapses()
    hours += 1
    if hours % 10 == 0:
        print(f'Situation after {hours} hours.')
        race.print_situation()

print('Race over! The result of the race is: ')
race.print_situation()
