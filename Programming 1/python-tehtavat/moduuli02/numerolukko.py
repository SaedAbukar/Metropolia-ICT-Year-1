import random

def kolmenarpa():
    print('Arpanumerosi:')
    i = 0
    while i < 3:
        print(random.randint(0, 9))
        i += 1

print(kolmenarpa())

def neljanarpa():
    print('Arpanumerosi:')
    i = 0
    while i < 4:
        print(random.randint(1, 6))
        i += 1

print(neljanarpa())

