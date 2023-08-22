# Käytin apuna tätä tutorialia: https://www.youtube.com/watch?v=rfscVS0vtbw
# Etsin googlesta löytyykö pii:tä pythonista ja ohjasi importaamaan math libraryn
import math

# Käytän try exceptiä, jotta varmistan, että käyttäjä lisää oikean arvon.
# Käytän while looppia, jotta käyttäjä voi vastata kysymkseen uudestaan, mikäli antaa väärän arvon.
# Oikean vastauksen jälkeen break outtaan while loopista.
while True:
    try:
        r = float(input('Mikä on ympyrän säde?: '))
        break
    except ValueError:
        print('Et lisännyt lukua. Yritä uudelleen ja lisää luku!')


# Google myös kertoi, että math.pi löytyy math librarysta
ympyran_pinta_ala = math.pi * r

print(f'Ympyrän pinta-ala on: {ympyran_pinta_ala:.2f} cm^2')
