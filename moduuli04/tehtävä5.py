# Kirjoita ohjelma, joka kysyy käyttäjältä käyttäjätunnuksen ja salasanan.
# Jos jompikumpi tai molemmat ovat väärin, tunnus ja salasana kysytään uudelleen.
# Tätä jatketaan kunnes kirjautumistiedot ovat oikein tai väärät tiedot on syötetty viisi kertaa.
# Edellisessä tapauksessa tulostetaan Tervetuloa ja jälkimmäisessä Pääsy evätty.
# (Oikea käyttäjätunnus on python ja salasana rules).

kayttaja = 'python'
salasana = 'rules'
syotetty_tunnus = ''
syotetty_salis = ''
yritykset = 0
yritys_maara = 5
paasy_evatty = False

while (kayttaja != str.lower(syotetty_tunnus) or salasana != syotetty_salis) and not paasy_evatty:
    if yritykset < yritys_maara:
        syotetty_tunnus = str.lower(input('Syötä käyttäjätunnus: '))
        syotetty_salis = str(input('Syötä salasana: '))
        yritykset += 1
        print('Virheelliset tunnukset! Yritä uudelleen.')
    else:
        paasy_evatty = True
if paasy_evatty:
    print('Pääsy evätty.')
else:
    print('Tervetuloa!')
