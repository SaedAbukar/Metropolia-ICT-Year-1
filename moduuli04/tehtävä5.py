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

while True:
    syotetty_tunnus = str.lower(input('Syötä käyttäjätunnus: '))
    syotetty_salis = str(input('Syötä salasana: '))
    yritykset += 1

    try:
        if yritykset >= 5:
            print('Pääsy evätty')
            break
        elif kayttaja != str.lower(syotetty_tunnus) or salasana != syotetty_salis and yritykset < 5:
            print('Virheeliset tunnukset! Yritä uudestaan.')

        elif kayttaja == syotetty_tunnus and salasana == syotetty_salis:
            print('Tervetuloa!')
            break


    except ValueError:
        print('Virheellinen syöte')
