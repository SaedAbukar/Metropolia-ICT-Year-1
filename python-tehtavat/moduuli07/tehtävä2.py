# Kirjoita ohjelma, joka kysyy käyttäjältä nimiä siihen saakka, kunnes käyttäjä syöttää tyhjän merkkijonon.
# Kunkin nimen syöttämisen jälkeen ohjelma tulostaa joko tekstin Uusi nimi tai Aiemmin syötetty nimi sen mukaan,
# syötettiinkö nimi ensimmäistä kertaa.
# Lopuksi ohjelma luettelee syötetyt nimet yksi kerrallaan allekkain mielivaltaisessa järjestyksessä.
# Käytä joukkotietorakennetta nimien tallentamiseen.

nimet = set()

while True:
    nimi = input('Syötä nimi tai paina Enter ohjelman lopettamiseksi: ')

    if nimi == '':
        break
    elif nimi in nimet:
        print('Aiemmin syötetty nimi.')
    elif nimi not in nimet:
        print('Uusi nimi.')
        nimet.add(nimi)

print(f'Painoit Enteriä. Ohjelma lopetettu. Tässä syöttämäsi nimet:')
for nimi in nimet:
    print(nimi)
