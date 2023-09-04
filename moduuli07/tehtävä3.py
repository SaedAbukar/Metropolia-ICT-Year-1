# Kirjoita ohjelma lentoasematietojen hakemiseksi ja tallentamiseksi. Ohjelma kysyy käyttäjältä,
# haluaako tämä syöttää uuden lentoaseman, hakea jo syötetyn lentoaseman tiedot vai lopettaa.
# Jos käyttäjä valitsee uuden lentoaseman syöttämisen, ohjelma kysyy käyttäjältä lentoaseman ICAO-koodin ja nimen.
# Jos käyttäjä valitsee haun, ohjelma kysyy ICAO-koodin ja tulostaa sitä vastaavan lentoaseman nimen.
# Jos käyttäjä haluaa lopettaa, ohjelman suoritus päättyy.
# Käyttäjä saa valita uuden toiminnon miten monta kertaa tahansa aina siihen asti, kunnes hän haluaa lopettaa.
# (ICAO-koodi on lentoaseman yksilöivä tunniste.
# Esimerkiksi Helsinki-Vantaan lentoaseman ICAO-koodi on EFHK. Löydät koodeja helposti selaimen avulla.)

lentokentat = {}

while True:
    toiminto = str.upper(input('Jos haluat syöttää uuden lentoaseman, syötä A. '
                               'Jos haluat hakea lentoasemaa, syötä B, '
                               'Jos haluat lopettaa, syötä tyhjä merkkijono: '))
    if toiminto == '':
        break
    if toiminto not in ('a', 'A', 'b', 'B'):
        print('Virheellinen syöte. Syötä A, B tai tyhjä merkkijono!')
    elif toiminto == 'A':
        icao = str.upper(input('Syötä lentoaseman ICAO-koodi: '))
        lentokentta = input('Syötä lentoaseman nimi: ')
        lentokentat[icao] = lentokentta
    else:
        icao2 = str.upper(input('Syötä lentoaseman ICAO-koodi: '))
        if icao2 not in lentokentat:
            print('Lentoasemaa ei löytynyt')
        else:
            print(lentokentat[icao2])

print('Syötit tyhjän merkkijonon. Ohjelma lopetettu.')
print(f'Tässä syöttämäsi lentoasemat:')
for lentokentta in lentokentat:
    print(f'ICAO-koodi: {lentokentta}, Nimi: {lentokentat[lentokentta]}')
