# Kirjoita ohjelma, joka kysyy käyttäjältä viiden kaupungin nimet yksi kerrallaan
# (käytä for-toistorakennetta nimien kysymiseen) ja tallentaa ne listarakenteeseen.
# Lopuksi ohjelma tulostaa kaupunkien nimet yksi kerrallaan allekkain samassa järjestyksessä kuin ne syötettiin.
# käytä for-toistorakennetta nimien kysymiseen ja for/in toistorakennetta niiden läpikäymiseen.

cities = []
i = 1
for i in range(5):
    ask_cities = str(input('Lisää viisi kaupunkia: '))
    cities.append(ask_cities)
    i += 1

print('Tässä lisäämäsi kaupungit:')
j = 1
while j <= 5:
    for city in cities:
        print(f'{j}: {city}\n')
        j += 1
