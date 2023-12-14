# Kirjoita ohjelma, joka kysyy käyttäjältä lukuja siihen saakka,
# Kunnes tämä syöttää tyhjän merkkijonon lopetusmerkiksi.
# Lopuksi ohjelma tulostaa saaduista luvuista viisi suurinta suuruusjärjestyksessä suurimmasta alkaen.
# Vihje: listan alkioiden lajittelujärjestyksen voi kääntää antamalla sort-metodille argumentiksi reverse=True.

numbers = []

number = input('Lisää luku tai lopeta painamalla Enter: ')
while number != '':
    numbers.append(number)
    number = input('Lisää luku tai lopeta painamalla Enter: ')

numbers.sort(reverse=True)
print(numbers[:5])
