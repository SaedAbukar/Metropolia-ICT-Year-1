# Kirjoita parametriton funktio, joka palauttaa paluuarvonaan satunnaisen nopan silmäluvun väliltä 1..6.
# Kirjoita pääohjelma, joka heittää noppaa niin kauan kunnes tulee kuutonen.
# Pääohjelma tulostaa kunkin heiton jälkeen saadun silmäluvun.
import random


def dice_6():
    return random.randint(1, 6)


i = 0
while True:
    dice_throw = dice_6()
    print(f'Heitto nro {i+1}, saatu silmäluku: {dice_throw}')
    i += 1
    if dice_throw == 6:
        break
