# Write an Elevator class that receives the lowest and highest floor number as its initializer parameters.
# The elevator has the methods move_to_floor, floor_up and floor_down. The new elevator is always on the lowest floor.
# For example, if you make a method call to the created elevator h to h.move_floor(5),
# the method calls either the floor_up or floor_down method as many times as the elevator ends up on the fifth floor.
# The last-mentioned methods drive the elevator up or down one floor
# and indicate which floor the elevator is on afterward.
# Test the class by creating an elevator in the main program
# and telling it to go to the floor you want and then back to the lowest floor.
# noinspection PyMethodMayBeStatic
class Elevator:
    def __init__(self, lowest_floor, highest_floor):
        self.current_floor = lowest_floor
        self.lowest_floor = lowest_floor
        self.highest_floor = highest_floor

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


# Testing the Elevator class
elevator1 = Elevator(0, 20)
elevator1.move_to_floor(5)

# Moving back to the lowest floor
elevator1.move_to_floor(elevator1.lowest_floor)
