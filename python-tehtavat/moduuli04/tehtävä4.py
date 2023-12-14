# Kirjoita peli, jossa tietokone arpoo kokonaisluvun väliltä 1..10.
# Kone arvuuttelee lukua pelaajalta siihen asti, kunnes tämä arvaa oikein.
# Kunkin arvauksen jälkeen ohjelma tulostaa tekstin Liian suuri arvaus, Liian pieni arvaus tai Oikein.
# Huomaa, että tietokone ei saa vaihtaa lukuaan arvauskertojen välissä.
import random

arpa_numero = random.randint(1, 10)
vastaus = ''
yritykset = 0

while arpa_numero != vastaus:
    while True:
        try:
            vastaus = int(input('Syötä kokonaisluku väliltä 1-10): '))
            yritykset += 1
            break
        except ValueError:
            print('Et syöttänyt kokonaislukua. Yritä uudelleen ja syötä kokonaisluku.')
    if arpa_numero == vastaus:
        print(f'Onneksi olkoon! Arvasit oikein! Käytit {yritykset} yrityskertaa.')
    elif arpa_numero < vastaus:
        print('Liian suuri arvaus. Yritä uudelleen.')
    else:
        print('Liian pieni arvaus. Yritä uudelleen.')
