# Kysy käyttäjältä biologinen sukupuoli ja hemoglobiiniarvo(g/l)
# while not in varmistaa sen, että käyttäjä laittaa 'mies' tai 'nainen'

sukupuoli = str.lower(input('Mikä on sinun biologinen sukupuoli? '))
while sukupuoli not in ['mies', 'nainen']:
    sukupuoli = str.lower(input('Valitse mies tai nainen? '))

while True:
    try:
        hb_arvo = float(input('Mikä on sinun hemoglobiiniarvo(g/l)? '))
        break
    except ValueError:
        print('Syötä arvo lukuina.')


# Miehen normaali hemoglobiiniarvo on välillä 134-195 g/l
# Naisen normaali hemoglobiiniarvo on välillä 117-175 g/l

if sukupuoli == 'mies' and hb_arvo < 134:
    print('Hemoglobiiniarvo on liian alhainen.')
elif sukupuoli == 'mies' and 134 < hb_arvo < 195:
    print('Hemoglobiiniarvo on normaali.')
elif sukupuoli == 'mies' and hb_arvo > 195:
    print('Hemoglobiiniarvo on liian korkea.')
elif sukupuoli == 'nainen' and hb_arvo < 117:
    print('Hemoglobiiniarvo on liian alhainen.')
elif sukupuoli == 'nainen' and 117 < hb_arvo < 175:
    print('Hemoglobiiniarvo on normaali.')
else:
    print('Hemoglobiiniarvo on liian korkea.')
