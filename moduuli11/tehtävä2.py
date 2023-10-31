class Car:
    def __init__(self, license_plate, top_speed, current_speed=0):
        self.license_plate = license_plate
        self.top_speed = top_speed
        self.current_speed = current_speed
        self.distance_traveled = 0

    def accelerate(self, change_of_speed):
        self.current_speed += change_of_speed
        if self.current_speed > self.top_speed:
            self.current_speed = self.top_speed
        if self.current_speed < 0:
            self.current_speed = 0

    def move(self, hour):
        self.distance_traveled += (self.current_speed * hour)


class ElectricCar(Car):
    def __init__(self, license_plate, top_speed, battery_capacity, current_speed=0):
        super().__init__(license_plate, top_speed, current_speed)
        self.battery_capacity = battery_capacity


class GasCar(Car):
    def __init__(self, license_plate, top_speed, gas_per_litre, current_speed=0):
        super().__init__(license_plate, top_speed, current_speed)
        self.gas_per_litre = gas_per_litre


electric_car = ElectricCar('ABC-15', 180, 52.5, 50)
gas_car = GasCar('ACD-123', 165, 32.3, 50)

electric_car.move(3)
gas_car.move(3)

print(f'Electric car distance traveled after 3 hours: {electric_car.distance_traveled} km')
print(f'Gas car distance traveled after 3 hours: {gas_car.distance_traveled} km')
