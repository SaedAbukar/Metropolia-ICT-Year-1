# Kirjoita ohjelma, joka kysyy käyttäjältä kuukauden numeron,
# jonka jälkeen ohjelma tulostaa sitä vastaavan vuodenajan (kevät, kesä, syksy, talvi).
# Tallenna ohjelmassasi kuukausia vastaavat vuodenajat merkkijonoina monikkotietorakenteeseen.
# Määritellään kukin vuodenaika kolmen kuukauden mittaiseksi siten, että joulukuu on ensimmäinen talvikuukausi.
vuodenajat = ('talvi', 'talvi', 'kevät', 'kevät', 'kevät', 'kesä', 'kesä', 'kesä', 'syksy', 'syksy', 'syksy', 'talvi')

kuukausi = int(input('Syötä kuukausi numerona (1-12): '))
while kuukausi <= 0 or kuukausi > 12:
    print('Virheellinen syöte. Syötä luku väliltä 1-12!')
    kuukausi = int(input('Syötä kuukausi numerona (1-12): '))
else:
    vuodenaika = vuodenajat[kuukausi - 1]
    print(f'Kuukausi {kuukausi} on {vuodenaika}.')
