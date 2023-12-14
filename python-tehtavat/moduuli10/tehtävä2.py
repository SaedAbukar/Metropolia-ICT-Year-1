# Continue the program of the previous task by making the House class.
# The number of the lowest and highest floors and the number of elevators are given as initialization parameters
# of the house. When creating a house, the house creates the required number of elevators.
# The list of elevators is saved as a property of the house.
# Enter the method run_elevator in the house, which receives the elevator number and target floor as parameters.
# In the main program, write the sentences to create the house and ride the elevators in the house.
class Elevator:
    def __init__(self, lowest_floor, highest_floor):
        self.lowest_floor = lowest_floor
        self.highest_floor = highest_floor
        self.current_floor = lowest_floor

    def move_to_floor(self, floor):
        while floor > self.current_floor:
            self.move_up()
        while floor < self.current_floor:
            self.move_down()

    def move_up(self):
        if self.current_floor < self.highest_floor:
            self.current_floor += 1
            print(f'The elevator is now in floor {self.current_floor}')

    def move_down(self):
        if self.current_floor > self.lowest_floor:
            self.current_floor -= 1
            print(f'The elevator is now in floor {self.current_floor}')


class House:
    def __init__(self, lowest_floor, highest_floor, elevator_numbers):
        self.lowest_floor = lowest_floor
        self.highest_floor = highest_floor
        self.elevator_numbers = elevator_numbers
        self.elevators = [Elevator(lowest_floor, highest_floor) for i in range(elevator_numbers)]

    def move_elevator(self, elevator_number, target_floor):
        if 0 <= elevator_number < len(self.elevators):
            elevator = self.elevators[elevator_number]
            elevator.move_to_floor(target_floor)
        else:
            print(f"Elevator number doesn't exist")

house = House(0, 20, 3)

house.move_elevator(0, 10)
house.move_elevator(1, 15)
house.move_elevator(2, 5)