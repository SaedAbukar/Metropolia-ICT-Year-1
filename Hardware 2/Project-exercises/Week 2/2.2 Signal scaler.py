from filefifo import Filefifo
from fifo import Fifo

data = Filefifo(10, name='capture_250Hz_01.txt')
current = data.get()
seconds = 1 / 250
two_seconds = 2 / seconds
ten_seconds = 10 / seconds


def scale_data(data, min_val, max_val):
    scaled_data = ((data - min_val) / (max_val - min_val)) * 100
    return scaled_data

# Iterate through the data stream
def get_samples():
    current = data.get()
    maximum = minimum = current
    for _ in range(two_seconds):  # Assuming we've already processed one data point
        current = data.get()  # Get the next data point
        if current > maximum:
            maximum = current
        elif current < minimum:
            minimum = current
    return minimum, maximum

minimum, maximum = get_samples()
    
for i in range(ten_seconds):
    current = data.get()
    scaled = scale_data(current, minimum, maximum)
    print(scaled)
