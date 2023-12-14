# Kirjoita ohjelma, joka kysyy vuosiluvun ja ilmoittaa, onko annettu vuosi karkausvuosi.
# Vuosi on karkausvuosi, jos se on jaollinen neljällä.
# Sadalla jaolliset vuodet ovat karkausvuosia vain jos ne ovat jaollisia myös neljälläsadalla.

while True:
    try:
        vuosiluku = int(input('Lisää vuosiluku ja selvitä onko se karkausvuosi!: '))
        break
    except ValueError:
        print('Et lisännyt kokonaislukua. Yritä uudelleen ja lisää kokonaisluku')

if vuosiluku % 4 == 0 or vuosiluku % 100 == 0 and vuosiluku % 400 == 0:
    print('Lisäämäsi vuosiluku on karkausvuosi!')
else:
    print('Lisämääsi vuosiluku ei ole karkausvuosi.')
