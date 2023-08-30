# Kirjoita ohjelma, joka kysyy käyttäjältä arpakuutioiden lukumäärän.
# Ohjelma heittää kerran kaikkia arpakuutioita ja tulostaa silmälukujen summan. Käytä for-toistorakennetta.
import random

dice_total = int(input('Lisää arpakuutioiden lukumäärä: '))
dice_sum = 0

for i in range(dice_total):
    dice_throw = random.randint(1, 6)
    print(f'Heitto nro {i+1}: {dice_throw}')
    dice_sum += dice_throw

print(f'Silmälukujen summa on: {dice_sum}')
