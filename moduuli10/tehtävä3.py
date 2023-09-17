# Continue the program of the previous task so that the House class has a parameterless method fire alarm
# that commands all elevators to the ground floor.
# Continue the main program so that a fire alarm goes off in your house.
class Elevator:

    def __init__(self, lowest_floor, highest_floor, number_of_elevator):
        self.current_floor = lowest_floor
        self.lowest_floor = lowest_floor
        self.highest_floor = highest_floor
        self.number_of_elevator = number_of_elevator

    # Method to move the elevator up one floor
    def floor_up(self):
        if self.current_floor < self.highest_floor:
            self.current_floor += 1
            print(f'The elevator is now in floor {self.current_floor}')

    # Method to move the elevator down one floor
    def floor_down(self):
        if self.current_floor > self.lowest_floor:
            self.current_floor -= 1
            print(f'The elevator is now in floor {self.current_floor}')

    # Method to move the elevator to a specific floor
    def move_to_floor(self, target_floor):
        while self.current_floor < target_floor:
            self.floor_up()
        while self.current_floor > target_floor:
            self.floor_down()


class House:

    def __init__(self, lowest_floor, highest_floor, number_of_elevators):
        self.lowest_floor = lowest_floor
        self.highest_floor = highest_floor
        self.current_floor = lowest_floor
        self.number_of_elevators = number_of_elevators
        self.elevators = []

    def run_elevator(self, elevator_number, target_floor):
        if elevator_number < len(self.elevators):
            elevator = self.elevators[elevator_number]
            elevator.move_to_floor(target_floor)
        else:
            print(f'Elevator {elevator_number} doesnt exist')

    def fire_alarm(self):
        self.current_floor = self.lowest_floor
        print(f'Fire alarm went off. All elevators were commanded to the ground floor.')


elevator1 = Elevator(0, 10, 1)
elevator2 = Elevator(0, 10, 2)
elevator3 = Elevator(0, 10, 3)

house1 = House(0, 10, 3)
house1.elevators.extend([elevator1, elevator2, elevator3])
house1.run_elevator(2, 7)
house1.fire_alarm()
