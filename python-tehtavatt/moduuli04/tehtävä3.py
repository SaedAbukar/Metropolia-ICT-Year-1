# Kirjoita ohjelma, joka kysyy käyttäjältä lukuja siihen saakka,
# Kunnes tämä syöttää tyhjän merkkijonon lopetusmerkiksi.
# Lopuksi ohjelma tulostaa saaduista luvuista pienimmän ja suurimman.
lista = []

# Ei try exceptia alkuun, jotta käyttäjä voi syöttää luvun tai ''.
while True:
    vastaus = (input('Lisää luku (tyhjä merkkijono lopettaa ohjelman): '))
    if vastaus == '':
        break
    try:
        luku = float(vastaus)
        lista.append(luku)
    except ValueError:
        print('Epäkelvollinen vastaus. Yritä uudelleen ja lisää luku tai '' ')

# Jos käyttäjä ei lisää yhtään lukua, ohjelma ei crashaa, koska varmistetan if else statementilla.
if len(lista) > 0:
    pienin = min(lista)
    suurin = max(lista)
    print(f'Tässä syöttämäsi lukujen pienin luku: {pienin} ja suurin luku: {suurin}')
else:
    print('Syötit tyhjän merkkijonon lopetusmerkiksi. Ohjelma lopetettu.')
