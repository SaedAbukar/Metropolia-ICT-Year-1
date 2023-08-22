# Yksi leiviskä on 20 naulaa.
# Yksi naula on 32 luotia.
# Yksi luoti on 13,3 grammaa.

while True:
    try:
        leiviska = float(input('Anna leiviskät:\n'))
        naula = float(input('Anna naulat:\n'))
        luoti = float(input('Anna luoti:\n'))
        break
    except ValueError:
        print('Et lisännyt lukua. Yritä uudelleen ja lisää luku!')

# Muunnokset

leiviska_to_naula = 20
naula_to_luoti = 32
luoti_to_gram = 13.3
gram_to_kg = 0.001

# Käyttäjän input laskelmaan

leiviska_massa = leiviska * leiviska_to_naula * naula_to_luoti * luoti_to_gram * gram_to_kg
naula_massa = naula * naula_to_luoti * luoti_to_gram * gram_to_kg
luoti_massa = luoti * luoti_to_gram * gram_to_kg

kg = leiviska_massa + naula_massa + luoti_massa
g = (kg - int(kg)) * 1000

print(f'Massa nykymittojen mukaan:\n {int(kg)} kilogrammaa ja {g:.2f} grammaa')




