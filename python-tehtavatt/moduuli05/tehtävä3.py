# Kirjoita ohjelma, joka kysyy käyttäjältä kokonaisluvun ja ilmoittaa, onko se alkuluku.
# Tässä tehtävässä alkulukuja ovat luvut, jotka ovat jaollisia vain ykkösellä ja itsellään.
# Esimerkiksi luku 13 on alkuluku, koska se voidaan jakaa vain luvuilla 1 ja 13 siten, että jako menee tasan.
# Toisaalta esimerkiksi luku 21 ei ole alkuluku, koska se voidaan jakaa tasan myös luvulla 3 tai luvulla 7

import math
while True:
    try:
        num = int(input("Syötä kokonaisluku: "))
        break
    except ValueError:
        print("Virheellinen syöte. Syötä kokonaisluku.")

if num <= 1:
    print(f"{num} ei ole alkuluku.")
elif num > 1:
    for i in range(2, int(math.floor(math.sqrt(num)))):
        if num % i == 0:
            print(f'{num} ei ole alkuluku!')
            print(f'{i} kertaa {num// i} on {num}')
            break
    else:
        print(f"{num} on alkuluku.")
