# Kirjoita ohjelma, joka muuntaa tuumia senttimetreiksi niin kauan kunnes käyttäjä antaa
# negatiivisen tuumamäärän. Sen jälkeen ohjelma lopettaa toimintansa. 1 tuuma = 2,54 cm


while True:
    try:
        tuuma = float(input('Lisää tuuma (negatiivinen luku lopettaa): '))
        break
    except ValueError:
        print('Et lisännyt lukua. Yritä uudelleen ja lisää luku.')

tuuma_to_cm = 2.54
vastaus = tuuma * tuuma_to_cm

while tuuma > 0:
    print(f'{vastaus:.3f}')
    while True:
        try:
            tuuma = float(input('Lisää tuuma (negatiivinen luku lopettaa): '))
            vastaus = tuuma * tuuma_to_cm
            break
        except ValueError:
            print('Et lisännyt lukua. Yritä uudelleen ja lisää luku.')


print('Annoit negatiivisen tuuman. Toiminta lopetettu.')
