# Muokkaa edellistä funktiota siten, että funktio saa parametrinaan nopan tahkojen yhteismäärän.
# Muokatun funktion avulla voit heitellä esimerkiksi 21-tahkoista roolipelinoppaa.
# Edellisestä tehtävästä poiketen nopan heittelyä jatketaan pääohjelmassa kunnes saadaan nopan maksimisilmäluku,
# joka kysytään käyttäjältä ohjelman suorituksen alussa.
import random


def dice_6(face):
    return random.randint(1, face)


dice_max = int(input('Syötä nopan maksimiluku: '))
i = 0
while True:
    dice_throw = dice_6(dice_max)
    print(f'Heitto nro {i+1}: Saatu silmäluku: {dice_throw}')
    i += 1
    if dice_throw == dice_max:
        print('Nopan maksimisilmäluku saavutettu! Ohjelma lopetetaan.')
        break
