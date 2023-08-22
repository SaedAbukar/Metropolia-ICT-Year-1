# Käytin apuna tätä tutorialia: https://www.youtube.com/watch?v=rfscVS0vtbw
# Käytän try exceptiä, jotta varmistan, että käyttäjä lisää oikean arvon.
# Käytän while looppia, jotta käyttäjä voi vastata kysymkseen uudestaan, mikäli antaa väärän arvon.
# Oikean vastauksen jälkeen break outtaan while loopista.
while True:
      try:
            suorakulmion_kanta = int(input('Mikä on suorakulmion kanta?: '))
            suorakulmion_korkeus = int(input('Mikä on suorakulmion korkeus?: '))
            break
      except ValueError:
            print('Et lisännyt lukua. Yritä uudelleen ja lisää jokaiseen kohtaan luku!')

suorakulmion_piiri = suorakulmion_kanta * 2 + suorakulmion_korkeus * 2
suorakulmion_pinta_ala = suorakulmion_kanta * suorakulmion_korkeus

print(f'Suorakulmion piiri on: {suorakulmion_piiri} cm ja Suorakulmion pinta-ala on: {suorakulmion_pinta_ala} cm^2')
